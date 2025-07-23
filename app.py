from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'vikkies-super-secret'

# DB connection
def get_db_connection():
    conn = sqlite3.connect('vikkie.db')
    conn.row_factory = sqlite3.Row
    return conn

# 🔐 Admin Login
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'NALUUMA360':
            session['admin'] = 'NALUUMA360'
            return redirect('/admin')
        else:
            return render_template('admin-login.html', error='Wrong password')
    return render_template('admin-login.html')

# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# 📋 Admin Dashboard
@app.route('/admin')
def admin_dashboard():
    if session.get('admin') != 'NALUUMA360':
        return redirect('/admin-login')

    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch everything
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    cur.execute("SELECT * FROM reviews")
    reviews = cur.fetchall()

    # Totals
    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM messages")
    total_messages = cur.fetchone()[0]

    conn.close()

    return render_template(
        'admin.html',
        orders=orders,
        users=users,
        products=products,
        reviews=reviews,
        total_products=total_products,
        total_orders=total_orders,
        total_messages=total_messages
    )

# 🗑️ Delete User
@app.route('/delete-user', methods=['POST'])
def delete_user():
    if session.get('admin') != 'NALUUMA360':
        return redirect('/admin-login')

    user_id = request.form['user_id']
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# ➕ Add Product
@app.route('/add-product', methods=['POST'])
def add_product():
    if session.get('admin') != 'NALUUMA360':
        return redirect('/admin-login')

    name = request.form['name']
    price = request.form['price']
    category = request.form['category']
    flash_end = request.form['flash_end']

    conn = get_db_connection()
    conn.execute("INSERT INTO products (name, price, category, flash_end) VALUES (?, ?, ?, ?)",
                 (name, price, category, flash_end))
    conn.commit()
    conn.close()
    return redirect('/admin')

# ✏️ Edit Product
@app.route('/edit-product', methods=['POST'])
def edit_product():
    if session.get('admin') != 'NALUUMA360':
        return redirect('/admin-login')

    product_id = request.form['product_id']
    name = request.form['name']
    price = request.form['price']
    category = request.form['category']
    flash_end = request.form['flash_end']

    conn = get_db_connection()
    conn.execute("""
        UPDATE products SET name=?, price=?, category=?, flash_end=?
        WHERE id=?
    """, (name, price, category, flash_end, product_id))
    conn.commit()
    conn.close()
    return redirect('/admin')

# ❌ Delete Product
@app.route('/delete-product', methods=['POST'])
def delete_product():
    if session.get('admin') != 'NALUUMA360':
        return redirect('/admin-login')

    product_id = request.form['product_id']
    conn = get_db_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# 🏁 Main
if __name__ == '__main__':
    app.run(debug=True)
