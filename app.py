from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "kanha-secret-key"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"

def save_booking(name, phone, email):
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    conn.close()

def get_all_bookings():
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
    data = cursor.fetchall()
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
