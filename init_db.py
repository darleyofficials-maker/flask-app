import sqlite3

conn = sqlite3.connect('vikkie.db')
c = conn.cursor()

# USERS
c.execute('''
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  password TEXT NOT NULL,
  points INTEGER DEFAULT 0
)
''')

# PRODUCTS
c.execute('''
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  price INTEGER NOT NULL,
  category TEXT,
  flash_end TEXT
)
''')

# ORDERS
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  total INTEGER,
  address TEXT,
  phone TEXT,
  status TEXT DEFAULT 'pending'
)
''')

# REVIEWS
c.execute('''
CREATE TABLE IF NOT EXISTS reviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user TEXT,
  product TEXT,
  rating INTEGER,
  comment TEXT
)
''')

# WISHLIST
c.execute('''
CREATE TABLE IF NOT EXISTS wishlist (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  product_id INTEGER
)
''')

# CART
c.execute('''
CREATE TABLE IF NOT EXISTS cart (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  product_id INTEGER,
  quantity INTEGER
)
''')

# MESSAGES
c.execute('''
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content TEXT
)
''')

# NEWSLETTER
c.execute('''
CREATE TABLE IF NOT EXISTS newsletter (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT
)
''')

conn.commit()
conn.close()

print("✅ Database initialized successfully.")
