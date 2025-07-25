from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
import sqlite3, os

app = Flask(__name__)
app.secret_key = os.environ.get("MY_SECRET_KEY", "supersecret")

def get_db_connection():
    conn = sqlite3.connect('vikkie.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------- ROUTES ----------------------

@app.route('/')
def index():
    return redirect('/login') if 'user_id' not in session else redirect('/home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password)).fetchone()
        if user:
            session['user_id'] = user['id']
            conn.execute("UPDATE users SET last_login=? WHERE id=?", (datetime.now(), user['id']))
            conn.commit()
            conn.close()
            return redirect('/home')
        conn.close()
        return render_template("homepage.html", error="Invalid login")
    return render_template("homepage.html")

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    conn.execute("INSERT INTO users (name, email, password, points) VALUES (?, ?, ?, 0)", (name, email, password))
    conn.commit()
    conn.close()
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id=?", (session['user_id'],)).fetchone()

    # Example placeholders
    filtered_products = {}
    wishlist = conn.execute("SELECT * FROM wishlist WHERE user_id=?", (user['id'],)).fetchall()
    cart_items = conn.execute("SELECT * FROM cart WHERE user_id=?", (user['id'],)).fetchall()
    orders = conn.execute("SELECT * FROM orders WHERE user_id=?", (user['id'],)).fetchall()
    reviews = conn.execute("SELECT * FROM reviews").fetchall()
    all_products = conn.execute("SELECT * FROM products").fetchall()
    flash_sales = conn.execute("SELECT * FROM products WHERE flash_end IS NOT NULL").fetchall()
    stock_alerts = conn.execute("SELECT * FROM products WHERE stock <= 5").fetchall()
    addresses = conn.execute("SELECT * FROM users WHERE id=?", (user['id'],)).fetchall()
    notifications = []
    recent_products = []
    recommendations = []
    referral_link = f"http://127.0.0.1:5000/signup?ref={user['id']}"
    grand_total = sum([item['quantity'] * item['price'] for item in cart_items])
    
    conn.close()

    return render_template("homepage.html", 
        user=user,
        filtered_products=filtered_products,
        wishlist=wishlist,
        cart_items=cart_items,
        orders=orders,
        reviews=reviews,
        all_products=all_products,
        flash_sales=flash_sales,
        stock_alerts=stock_alerts,
        addresses=addresses,
        notifications=notifications,
        recent_products=recent_products,
        recommendations=recommendations,
        referral_link=referral_link,
        grand_total=grand_total,
        user_points=user['points'],
        conversion_rate=1,
        discount_applied=None
    )

# ---------------------- POST ROUTES ----------------------

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    pid = request.form['product_id']
    conn = get_db_connection()
    conn.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1)", (session['user_id'], pid))
    conn.commit()
    conn.close()
    return redirect('/home#cart')

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    pid = request.form['product_id']
    conn = get_db_connection()
    conn.execute("DELETE FROM cart WHERE user_id=? AND product_id=?", (session['user_id'], pid))
    conn.commit()
    conn.close()
    return redirect('/home#cart')

@app.route('/wishlist', methods=['POST'])
def wishlist():
    pid = request.form['product_id']
    conn = get_db_connection()
    conn.execute("INSERT INTO wishlist (user_id, product_id) VALUES (?, ?)", (session['user_id'], pid))
    conn.commit()
    conn.close()
    return redirect('/home#wishlist')

@app.route('/remove-wishlist', methods=['POST'])
def remove_wishlist():
    pid = request.form['product_id']
    conn = get_db_connection()
    conn.execute("DELETE FROM wishlist WHERE user_id=? AND product_id=?", (session['user_id'], pid))
    conn.commit()
    conn.close()
    return redirect('/home#wishlist')

@app.route('/convert-points', methods=['POST'])
def convert_points():
    points = int(request.form['points_to_convert'])
    conn = get_db_connection()
    conn.execute("UPDATE users SET points = points - ? WHERE id=?", (points, session['user_id']))
    conn.commit()
    conn.close()
    return redirect('/home#convert-points')

@app.route('/checkout', methods=['POST'])
def checkout():
    address = request.form['address']
    phone = request.form['phone']
    conn = get_db_connection()
    conn.execute("INSERT INTO orders (user_id, date, status, total) VALUES (?, ?, ?, ?)", 
                 (session['user_id'], datetime.now(), "Pending", 0))  # Replace 0 with real total
    conn.commit()
    conn.close()
    return redirect('/home#order-history')

@app.route('/submit-review', methods=['POST'])
def submit_review():
    product_id = request.form['product_id']
    rating = request.form['rating']
    comment = request.form['comment']
    conn = get_db_connection()
    conn.execute("INSERT INTO reviews (user, product, rating, comment) VALUES (?, ?, ?, ?)",
                 (session['user_id'], product_id, rating, comment))
    conn.commit()
    conn.close()
    return redirect('/home#reviews')

@app.route('/admin-message', methods=['POST'])
def admin_message():
    subject = request.form['subject']
    message = request.form['message']
    conn = get_db_connection()
    conn.execute("INSERT INTO messages (user_id, subject, message) VALUES (?, ?, ?)", (session['user_id'], subject, message))
    conn.commit()
    conn.close()
    return redirect('/home#admin-contact')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    conn = get_db_connection()
    conn.execute("INSERT INTO newsletter (email) VALUES (?)", (email,))
    conn.commit()
    conn.close()
    return redirect('/home#newsletter')

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.form['email']
    conn = get_db_connection()
    conn.execute("DELETE FROM newsletter WHERE email=?", (email,))
    conn.commit()
    conn.close()
    return redirect('/home#newsletter')

@app.route('/track-order', methods=['GET'])
def track_order():
    order_id = request.args.get('order_id')
    conn = get_db_connection()
    order = conn.execute("SELECT status FROM orders WHERE id=?", (order_id,)).fetchone()
    conn.close()
    return redirect(f"/home#track-order?status={order['status']}" if order else "/home#track-order")

@app.route('/update-profile', methods=['POST'])
def update_profile():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form.get('password')
    conn = get_db_connection()
    if password:
        conn.execute("UPDATE users SET name=?, email=?, phone=?, password=? WHERE id=?",
                     (name, email, phone, password, session['user_id']))
    else:
        conn.execute("UPDATE users SET name=?, email=?, phone=? WHERE id=?",
                     (name, email, phone, session['user_id']))
    conn.commit()
    conn.close()
    return redirect('/home#settings')

@app.route('/set-preferences', methods=['POST'])
def set_preferences():
    language = request.form['language']
    currency = request.form['currency']
    # You could store these preferences in a table
    return redirect('/home#preferences')

@app.route('/delete-address', methods=['POST'])
def delete_address():
    addr_id = request.form['address_id']
    conn = get_db_connection()
    conn.execute("DELETE FROM addresses WHERE id=? AND user_id=?", (addr_id, session['user_id']))
    conn.commit()
    conn.close()
    return redirect('/home#saved-addresses')

@app.route('/feedback', methods=['POST'])
def feedback():
    message = request.form['message']
    # Save feedback if you have a table for it
    return redirect('/home#feedback')

@app.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    # Implement search
    return redirect('/home#shop')

# ------------------- ADMIN ROUTES SKIPPED FOR BREVITY ------------------

if __name__ == "__main__":
    app.run(debug=True)
