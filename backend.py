from fastapi import FastAPI
from fastapi import HTTPException
import models

app = FastAPI()

coffeeDescriptions = [
    "A latte is a coffee drink made with espresso and steamed milk. It is a single shot of espresso served in a tall glass, with a layer of steamed milk on top, and a layer of microfoam on top of that.",
    "A cappuccino is an espresso-based coffee drink that originated in Italy, and is traditionally prepared with steamed milk foam.",
    "An espresso is a coffee drink that is prepared by forcing a small amount of boiling water under pressure through finely ground coffee beans. Espresso is generally thicker than coffee brewed by other methods, and has cream on top.",
    "Your average cup of joe made by putting boiled water through some freshly ground coffee beans, nothing special."
]
coffeePrices = [2.5, 3.5, 4.5, 1.5]
orders = []


@app.get("/")
async def root():
    """
    Returns the menu for the coffee shop
    """
    return {"menu": {1: "latte", 2: "cappuccino", 3: "espresso", 4:"normal"}}


@app.get("/coffee/{coffee_id}")
async def describeCoffee(coffee_id: int):
    """

    Args:
        coffee_id (int): The id of the coffee you want to know more about

    Raises:
        HTTPException: If the coffee_id is not between 1 and 4

    Returns:
        The description of the coffee
    """
    if coffee_id > 4 or coffee_id < 1:
        raise HTTPException(status_code=404, detail="Item not found, please choose a number between 1 and 4")
    return {"description": coffeeDescriptions[coffee_id-1]}

@app.get("/coffee/{coffee_id}/price")
async def priceCoffee(coffee_id: int):
    """
    gets the price of the coffee including tax in USD

    Args:
        coffee_id (int): The id of the coffee

    Raises:
        HTTPException: If the coffee_id is not between 1 and 4

    Returns:
        The price of the coffee including tax in USD
    """
    if coffee_id > 4 or coffee_id < 1:
        raise HTTPException(status_code=404, detail="Item not found, please choose a number between 1 and 4")
    return {"price": coffeePrices[coffee_id-1], "currency": "USD", "tax": 0.1, "total": coffeePrices[coffee_id-1]*1.1,}

@app.post("/coffee/{coffee_id}/order")
async def orderCoffee(coffee_id: int, quantity: int = 1, payed: bool = True):
    """
    Orders the coffee

    Args:
        coffee_id (int): The id of the coffee
        quantity (int, optional): The quantity of the coffee. Defaults to 1.
        payed (bool, optional): If the coffee has been payed for. Defaults to True.

    Raises:
        HTTPException: If the coffee_id is not between 1 and 4

    Returns:
        A message saying that the coffee was ordered
    """
    if coffee_id > 4 or coffee_id < 1:
        raise HTTPException(status_code=404, detail="Item not found, please choose a number between 1 and 4")
    if not payed:
        raise HTTPException(status_code=402, detail="You have not payed for your coffee")
    orders.append(coffee_id)
    return {"message": "Your coffee has been ordered"}

@app.get("/orders")
async def getOrders():
    """
    Gets all the orders

    Returns:
        A list of all the orders
    """
    return {"orders": orders}

@app.delete("/orders/{order_number}")
async def deleteOrders(order_number: int, token: models.Token):
    """
    Deletes an order

    Args:
        order_number (int): The order number

    Raises:
        HTTPException: If the order_id is not in the list of orders

    Returns:
        A message saying that the order was deleted
    """
    if token.id != "secret":
        raise HTTPException(status_code=403, detail="You do not have permission to delete orders")
    if order_number > len(orders) or order_number < 1:
        raise HTTPException(status_code=404, detail="Order not found")
    orders.pop(order_number-1)
    return {"message": "Your order has been deleted"}

if __name__ == "__main__":
    import uvicorn
    # launch the server on port 8000
    uvicorn.run(app, host="localhost", port=8000)