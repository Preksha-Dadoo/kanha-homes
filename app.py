from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

def get_db_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    return psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.secret_key = "kanha-secret-key"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            name TEXT,
            phone TEXT,
            email TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


init_db()

def save_booking(name, phone, email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO bookings (name, phone, email) VALUES (%s, %s, %s)",
        (name, phone, email)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_all_bookings():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, phone, email FROM bookings ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        save_booking(name, phone, email)
        return "<h2>Thank you! Your booking request has been submitted.</h2><a href='/'>Go Home</a>"
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")
        else:
            error = "Invalid login!"

    return render_template("login.html", error=error)

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    bookings = get_all_bookings()
    return render_template("admin.html", bookings=bookings)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
