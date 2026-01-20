import sqlite3

conn = sqlite3.connect("bookings.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    phone TEXT, 
    email TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully")