from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "secret_key"  # For flash messages

# Data storage (JSON file)
DATA_FILE = "inventory_data.json"

# Helper function to load and save data
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/view")
def view_inventory():
    inventory = load_data()
    return render_template("view_inventory.html", inventory=inventory)

@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        item_name = request.form["item_name"]
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])

        inventory = load_data()
        if item_name in inventory:
            flash(f"{item_name} already exists. Use the update option.")
        else:
            inventory[item_name] = {"quantity": quantity, "price": price}
            save_data(inventory)
            flash(f"{item_name} added successfully!")
        return redirect(url_for("view_inventory"))

    return render_template("add_item.html")

@app.route("/update/<item_name>", methods=["GET", "POST"])
def update_item(item_name):
    inventory = load_data()
    if request.method == "POST":
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])
        inventory[item_name] = {"quantity": quantity, "price": price}
        save_data(inventory)
        flash(f"{item_name} updated successfully!")
        return redirect(url_for("view_inventory"))

    return render_template("update_item.html", item_name=item_name, details=inventory[item_name])

@app.route("/delete/<item_name>")
def delete_item(item_name):
    inventory = load_data()
    if item_name in inventory:
        del inventory[item_name]
        save_data(inventory)
        flash(f"{item_name} deleted successfully!")
    return redirect(url_for("view_inventory"))

if __name__ == "__main__":
    app.run(debug=True)
