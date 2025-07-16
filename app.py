from flask import Flask, render_template, request, redirect, session, url_for, jsonify, send_from_directory
import firebase_admin
from firebase_admin import credentials, auth, db
import json
import os

app = Flask(__name__)
app.secret_key = "AIzaSyCYRdTIbpui9cN0R8vWwRhvpBV4cW2-3o8"  # Required for managing sessions

# Load Firebase Admin SDK credentials and initialize with Realtime Database URL
cred = credentials.Certificate("sev.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://login-8d7bc-default-rtdb.firebaseio.com/'
})

DATABASE_FILE = "database.json"

# Load products from JSON
def load_products():
    products = []
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                products = json.load(f)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in database.json")
    return products

# Format price for display (adds the rupee symbol)
def format_price(price):
    try:
        price = price.replace("\u20b9", "").replace(",", "")
        return f"₹{float(price):,.0f}"
    except (ValueError, TypeError):
        return "₹0"

# Helper function to extract numeric value from a price string.
def parse_price_value(price):
    try:
        return float(str(price).replace("\u20b9", "").replace("₹", "").replace(",", "").strip())
    except (ValueError, TypeError):
        return 0.0

# Home Page
@app.route("/")
def home():
    return render_template("index.html", user=session.get("user"))

# Explore Products Page
@app.route("/explore")
def explore():
    PRODUCTS = load_products()
    for product in PRODUCTS:
        product["price"] = format_price(product["price"])
    return render_template("explore.html", products=PRODUCTS, user=session.get("user"))

# Individual Product Page
@app.route("/product/<int:product_id>")
def product_page(product_id):
    PRODUCTS = load_products()
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        product["price"] = format_price(product["price"])
        return render_template("product.html", product=product, user=session.get("user"))
    return "Product not found", 404

# About Page
@app.route("/about")
def about():
    return render_template("about.html", user=session.get("user"))

# Contact Page
@app.route("/contact")
def contact():
    return render_template("contact.html", user=session.get("user"))

# Search Functionality with Price Filtering and Sorting
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").lower()
    sort_order = request.args.get("sort", "").lower()  # expecting 'asc' or 'desc'
    min_price_str = request.args.get("minPrice", "")
    max_price_str = request.args.get("maxPrice", "")
    
    try:
        min_price = float(min_price_str) if min_price_str else None
    except ValueError:
        min_price = None
    try:
        max_price = float(max_price_str) if max_price_str else None
    except ValueError:
        max_price = None

    PRODUCTS = load_products()
    results = [p for p in PRODUCTS if query in p["name"].lower()]
    
    # Apply price filtering.
    if min_price is not None:
        results = [p for p in results if parse_price_value(p["price"]) >= min_price]
    if max_price is not None:
        results = [p for p in results if parse_price_value(p["price"]) <= max_price]
    
    # Apply sorting.
    if sort_order == "asc":
        results.sort(key=lambda x: parse_price_value(x["price"]))
    elif sort_order == "desc":
        results.sort(key=lambda x: parse_price_value(x["price"]), reverse=True)
    
    # Format prices for display.
    for product in results:
        product["price"] = format_price(product["price"])
    
    return jsonify(results)

# Cart: Add Product to Cart (if logged in) using Firebase Realtime Database
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if "user" not in session:
        return redirect(url_for("login"))
    
    uid = session["user"]["uid"]
    PRODUCTS = load_products()
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        cart_ref = db.reference('carts').child(uid)
        current_cart = cart_ref.get() or []
        current_cart.append(product)
        cart_ref.set(current_cart)
    return redirect(url_for("cart"))

# Remove Product from Cart (if logged in) using Firebase Realtime Database
@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    if "user" not in session:
        return redirect(url_for("login"))
    
    uid = session["user"]["uid"]
    cart_ref = db.reference('carts').child(uid)
    current_cart = cart_ref.get() or []
    updated_cart = [item for item in current_cart if item["id"] != product_id]
    cart_ref.set(updated_cart)
    return redirect(url_for("cart"))

# Checkout Page: Retrieve Cart Items from Firebase Realtime Database
@app.route("/checkout")
def checkout():
    if "user" not in session:
        return redirect(url_for("login"))
    
    uid = session["user"]["uid"]
    cart_ref = db.reference('carts').child(uid)
    current_cart = cart_ref.get() or []
    return render_template("checkout.html", user=session.get("user"), cart=current_cart)

# Cart Page: View Cart (if logged in) using Firebase Realtime Database
@app.route("/cart")
def cart():
    if "user" not in session:
        return redirect(url_for("login"))
    
    uid = session["user"]["uid"]
    cart_ref = db.reference('carts').child(uid)
    current_cart = cart_ref.get() or []
    for product in current_cart:
        product["price"] = format_price(product["price"])
    return render_template("cart.html", products=current_cart, user=session.get("user"))

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.get_user_by_email(email)
            session["user"] = {"uid": user.uid, "email": user.email}
            return redirect(url_for("home"))
        except Exception as e:
            print(e)
            return "Login Failed: Invalid Credentials", 401
    return render_template("login.html", user=session.get("user"))

# Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        try:
            # Create user using Firebase Authentication
            user = auth.create_user(email=email, password=password)
            # Save additional user data (name and phone) to Realtime Database under /users/<uid>
            db.reference('users').child(user.uid).set({
                'name': name,
                'phone': phone,
                'email': email
            })
            session["user"] = {"uid": user.uid, "email": user.email}
            return redirect(url_for("home"))
        except Exception as e:
            print(e)
            return "Signup Failed", 400
    return render_template("signup.html", user=session.get("user"))

# Logout Route
@app.route("/logout")
def logout():
    session.pop("user", None)
    # Optionally, you might want to clear the local session cart,
    # but since we now use Firebase, the cart is persisted.
    return redirect(url_for("home"))

# Profile Page
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    
    uid = session["user"]["uid"]
    user_ref = db.reference(f'users/{uid}')
    user_data = user_ref.get()
    
    if user_data:
        session["user"].update(user_data)  # Store name, phone in session
    
    return render_template("profile.html", user=session.get("user"))

# Serve Static Images
@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/images'), filename)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
