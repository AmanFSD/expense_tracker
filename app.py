from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        category TEXT,
                        amount REAL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])

        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)", (date, category, amount))
        conn.commit()
        conn.close()
        return redirect(url_for('summary'))
    return render_template('add_expense.html')

@app.route('/summary')
def summary():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()
    conn.close()

    categories = {}
    for row in data:
        category = row[2]
        amount = row[3]
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    return render_template('summary.html', expenses=data, categories=categories)

@app.route('/data')
def data():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    return jsonify({'categories': categories, 'amounts': amounts})

if __name__ == '__main__':
    app.run(debug=True)