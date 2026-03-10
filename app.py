from flask import Flask, render_template, request, redirect # pyright: ignore[reportMissingImports]
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    return conn


# Create table if not exists
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            address TEXT,
            email TEXT UNIQUE,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()


# READ
@app.route('/')
def index():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)


# CREATE
@app.route('/add', methods=['POST'])
def add():
    first = request.form['first_name']
    last = request.form['last_name']
    address = request.form['address']
    email = request.form['email']
    phone = request.form['phone']

    conn = get_db_connection()
    conn.execute('INSERT INTO contacts (first_name,last_name,address,email,phone) VALUES (?,?,?,?,?)',
                 (first, last, address, email, phone))
    conn.commit()
    conn.close()

    return redirect('/')


# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')


# UPDATE PAGE
@app.route('/edit/<int:id>')
def edit(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', contact=contact)


# UPDATE FUNCTION
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    first = request.form['first_name']
    last = request.form['last_name']
    address = request.form['address']
    email = request.form['email']
    phone = request.form['phone']

    conn = get_db_connection()
    conn.execute('''
        UPDATE contacts
        SET first_name=?, last_name=?, address=?, email=?, phone=?
        WHERE id=?
    ''', (first, last, address, email, phone, id))
    conn.commit()
    conn.close()

    return redirect('/')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)