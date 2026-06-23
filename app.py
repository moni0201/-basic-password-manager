import sqlite3
import random
import string
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "super_secret_session_encryption_key"

def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT website, username, password FROM vault")
    credentials = cursor.fetchall()
    conn.close()
    return render_template("index.html", credentials=credentials)

@app.route('/add', methods=['POST'])
def add_password():
    website = request.form.get('website')
    username = request.form.get('username')
    password = request.form.get('password')
    
    if website and username and password:
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vault (website, username, password) VALUES (?, ?, ?)", 
                       (website, username, password))
        conn.commit()
        conn.close()
        flash("Credentials saved successfully!")
    return redirect(url_for('index'))

# --- NEW ROUTES FOR THE GENERATOR PAGE ---

@app.route('/generator')
def generator_page():
    return render_template("generator.html", password=None)

@app.route('/generate', methods=['POST'])
def generate_password():
    length = int(request.form.get('length', 12))
    include_upper = request.form.get('uppercase')
    include_numbers = request.form.get('numbers')
    include_symbols = request.form.get('symbols')

    # Base characters pool (always contains lowercase)
    char_pool = string.ascii_lowercase
    if include_upper:
        char_pool += string.ascii_uppercase
    if include_numbers:
        char_pool += string.digits
    if include_symbols:
        char_pool += "!@#$%^&*()-_=+"

    # Generate random string choice pool
    generated_password = "".join(random.choice(char_pool) for _ in range(length))
    
    return render_template("generator.html", password=generated_password, length=length)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
