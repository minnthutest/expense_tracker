# database.py
import sqlite3
import pandas as pd

# Setup
conn = sqlite3.connect('expenses.db', check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    ''')
    conn.commit()

def insert_expense(date, category, amount, description):
    c.execute('''
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    ''', (date, category, amount, description))
    conn.commit()

def fetch_all_expenses():
    c.execute('SELECT date, category, amount, description FROM expenses ORDER BY date DESC')
    return c.fetchall()

def filter_by_category(category):
    c.execute('SELECT date, category, amount, description FROM expenses WHERE category = ? ORDER BY date DESC', (category,))
    return c.fetchall()

def fetch_by_month(month):
    c.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%m', date) = ?", (f"{int(month):02}",))
    res = c.fetchone()[0]
    return res if res else 0.0

def fetch_by_year(year):
    c.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y', date) = ?", (str(year),))
    res = c.fetchone()[0]
    return res if res else 0.0

def fetch_category_summary():
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = c.fetchall()
    return pd.DataFrame(data, columns=["Category", "Total"])

def fetch_monthly_summary():
    c.execute("SELECT strftime('%m', date) as month, SUM(amount) FROM expenses GROUP BY month ORDER BY month")
    data = c.fetchall()
    return pd.DataFrame(data, columns=["Month", "Total"])
