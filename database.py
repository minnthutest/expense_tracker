# database.py
import sqlite3
import pandas as pd
from datetime import datetime
import os

# Setup
if 'streamlit' in os.environ.get('HOME', ''):
    DB_PATH = os.path.join('/tmp', 'expenses.db')
else:
    DB_PATH = 'expenses.db'

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()  # ← Initialize the cursor here


def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            "date" TEXT,  # Using double quotes to avoid SQL keyword conflict
            category TEXT,
            amount REAL,
            description TEXT
        )
    ''')
    conn.commit()

def insert_expense(date, category, amount, description):
    # Ensure date is in the correct format (YYYY-MM-DD)
    date = datetime.now().strftime('%Y-%m-%d') if not date else date

    c.execute('''
        INSERT INTO expenses ("date", category, amount, description)
        VALUES (?, ?, ?, ?)
    ''', (date, category, amount, description))
    conn.commit()

def fetch_all_expenses():
    c.execute('SELECT "date", category, amount, description FROM expenses ORDER BY "date" DESC')
    return c.fetchall()

def filter_by_category(category):
    c.execute('SELECT "date", category, amount, description FROM expenses WHERE category = ? ORDER BY "date" DESC', (category,))
    return c.fetchall()

def fetch_by_month(month):
    c.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%m', \"date\") = ?", (f"{int(month):02}",))
    res = c.fetchone()[0]
    return res if res else 0.0

def fetch_by_year(year):
    c.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y', \"date\") = ?", (str(year),))
    res = c.fetchone()[0]
    return res if res else 0.0

def fetch_category_summary():
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = c.fetchall()
    return pd.DataFrame(data, columns=["Category", "Total"])

def fetch_monthly_summary():
    c.execute("SELECT strftime('%m', \"date\") as month, SUM(amount) FROM expenses GROUP BY month ORDER BY month")
    data = c.fetchall()
    return pd.DataFrame(data, columns=["Month", "Total"])
