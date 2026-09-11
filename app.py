from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/admin/orders")
def admin_orders():
    if os.path.exists("orders.json"):
        try:
            with open("orders.json", "r") as file:
                orders = json.load(file)
        except:
            orders = []
    else:
        orders = []

    return jsonify(orders)


@app.route("/place-order", methods=["POST"])
def place_order():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No order data received"
        })


    table_number = data.get("tableNumber")
    customer_name = data.get("customerName")
    cart = data.get("cart", [])


    if not table_number:
        return jsonify({
            "success": False,
            "message": "Table number is required"
        })


    if not customer_name:
        return jsonify({
            "success": False,
            "message": "Customer name is required"
        })


    if not cart:
        return jsonify({
            "success": False,
            "message": "Cart is empty"
        })


    total = 0

    for item in cart:
        price = float(item.get("price", 0))
        quantity = int(item.get("quantity", 1))
        total = total + (price * quantity)


    if os.path.exists("orders.json"):
        try:
            with open("orders.json", "r") as file:
                orders = json.load(file)
        except:
            orders = []
    else:
        orders = []


    order = {
        "orderNumber": len(orders) + 1,
        "tableNumber": table_number,
        "customerName": customer_name,
        "items": cart,
        "total": total,
        "status": "Pending",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


    orders.append(order)


    with open("orders.json", "w") as file:
        json.dump(orders, file, indent=4)


    return jsonify({
        "success": True,
        "message": "Order placed successfully!",
        "orderNumber": order["orderNumber"]
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )