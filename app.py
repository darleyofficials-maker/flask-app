from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv("MY_SECRET_KEY", "dev_key")  # Replace in production

def get_db_connection():
    conn = sqlite3.connect("vikkie.db")
    conn.row_factory = sqlite3.Row
    return conn

# Redirect root to login
@app.route('/')
def index():
    return redirect('/login')

# SIGNUP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (name, email, password, points, last_login) VALUES (?, ?, ?, 0, ?)",
                         (name, email, password, datetime.now()))
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template("login.html", error="Email already exists.")
        conn.close()
        return redirect('/login')
    return render_template('login.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cur.fetchone()

        if user:
            session['user_id'] = user['id']
            cur.execute("UPDATE users SET last_login = ? WHERE id = ?", (datetime.now(), user['id']))
            conn.commit()
            conn.close()
            return redirect('/homepage')
        else:
            conn.close()
            return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# HOMEPAGE (Protected)
@app.route('/homepage')
def homepage():
    if "user_id" not in session:
        return redirect('/login')

    conn = get_db_connection()
    user = conn.execute("SELECT name, email, phone, points, last_login FROM users WHERE id = ?",
                        (session["user_id"],)).fetchone()

    # Fetch dynamic data or mock placeholders
    filtered_products = {}
    wishlist = []
    cart_items = []
    orders = []
    flash_sales = []
    stock_alerts = []
    referral_link = f"http://127.0.0.1:5000/signup?ref={user['email']}"
    notifications = []
    addresses = []
    recent_products = []
    recommendations = []
    all_products = []
    reviews = []
    user_points = user['points']
    discount_applied = 0
    conversion_rate = 1

    conn.close()

    return render_template("homepage.html",
                           user=user,
                           filtered_products=filtered_products,
                           wishlist=wishlist,
                           cart_items=cart_items,
                           grand_total=0,
                           orders=orders,
                           flash_sales=flash_sales,
                           stock_alerts=stock_alerts,
                           referral_link=referral_link,
                           notifications=notifications,
                           addresses=addresses,
                           recent_products=recent_products,
                           recommendations=recommendations,
                           all_products=all_products,
                           reviews=reviews,
                           user_points=user_points,
                           discount_applied=discount_applied,
                           conversion_rate=conversion_rate)

if __name__ == "__main__":
    app.run(debug=True)
