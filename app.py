from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = "secret_key"  # For flash messages and sessions

# Mock user data (replace with a database in production)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

# Data storage (JSON file)
DATA_FILE = "inventory_data.json"

# Helper functions
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Routes
from flask import jsonify

@app.route('/get_inventory', methods=['GET'])
def get_inventory():
    inventory = load_data()  # Use your existing load_data() function
    return jsonify(inventory)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = USERS.get(username)
        if user and user["password"] == password:
            session["username"] = username
            session["role"] = user["role"]
            flash("Login successful!")
            return redirect(url_for("admin_console" if user["role"] == "admin" else "user_console"))
        else:
            flash("Invalid username or password.")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("index"))

@app.route("/admin")
def admin_console():
    if session.get("role") != "admin":
        flash("Unauthorized access!")
        return redirect(url_for("login"))
    inventory = load_data()
    return render_template("admin_console.html", inventory=inventory)

@app.route("/user")
def user_console():
    if session.get("role") != "user":
        flash("Unauthorized access!")
        return redirect(url_for("login"))
    inventory = load_data()
    return render_template("user_console.html", inventory=inventory)

@app.route("/add", methods=["GET", "POST"])
def add_item():
    if session.get("role") != "admin":
        flash("Unauthorized access!")
        return redirect(url_for("login"))
    
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
        return redirect(url_for("admin_console"))

    return render_template("add_item.html")

@app.route("/update/<item_name>", methods=["GET", "POST"])
def update_item(item_name):
    if session.get("role") != "admin":
        flash("Unauthorized access!")
        return redirect(url_for("login"))

    inventory = load_data()
    if request.method == "POST":
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])
        inventory[item_name] = {"quantity": quantity, "price": price}
        save_data(inventory)
        flash(f"{item_name} updated successfully!")
        return redirect(url_for("admin_console"))

    return render_template("update_item.html", item_name=item_name, details=inventory[item_name])

@app.route("/delete/<item_name>")
def delete_item(item_name):
    if session.get("role") != "admin":
        flash("Unauthorized access!")
        return redirect(url_for("login"))

    inventory = load_data()
    if item_name in inventory:
        del inventory[item_name]
        save_data(inventory)
        flash(f"{item_name} deleted successfully!")
    return redirect(url_for("admin_console"))

if __name__ == "__main__":
    app.run(debug=True)
