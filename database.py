import sqlite3
import pandas as pd
from datetime import datetime
import os

# Determine database path depending on environment
if 'streamlit' in os.environ.get('HOME', ''):
    DB_PATH = os.path.join('/tmp', 'expenses.db')  # Streamlit Cloud
else:
    DB_PATH = 'expenses.db'  # Local

# Establish connection and cursor
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()  # Must be declared for executing queries

# Test DB connection
def test_connection():
    try:
        c.execute('SELECT 1')
        print("✅ Database connection is working.")
    except sqlite3.OperationalError as e:
        print(f"❌ Database connection test failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error testing DB connection: {e}")

# Create table if not exists
def create_table():
    try:
        query = '''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "date" TEXT,
                category TEXT,
                amount REAL,
                description TEXT
            )
        '''
        print("🛠 Executing SQL to create table...")
        c.execute(query)
        conn.commit()
        print("✅ Table created successfully or already exists.")
    except sqlite3.OperationalError as e:
        print(f"❌ SQLite OperationalError: {e}")
        raise
    except sqlite3.DatabaseError as e:
        print(f"❌ SQLite DatabaseError: {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise

# Insert expense into the database
def insert_expense(date, category, amount, description):
    try:
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        c.execute('''
            INSERT INTO expenses ("date", category, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (date, category, amount, description))
        conn.commit()
        print("✅ Expense added.")
    except Exception as e:
        print(f"❌ Failed to insert expense: {e}")
        raise

# Fetch all expenses
def fetch_all_expenses():
    c.execute('SELECT "date", category, amount, description FROM expenses ORDER BY "date" DESC')
    return c.fetchall()

# Filter by category
def filter_by_category(category):
    c.execute('SELECT "date", category, amount, description FROM expenses WHERE category = ? ORDER BY "date" DESC', (category,))
    return c.fetchall()

# Get total expenses by month
def fetch_by_month(month):
    c.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%m', \"date\") = ?", (f"{int(month):02}",))
    res = c.fetchone()[0]
    return res if res else 0.0

# Get total expenses by year
def fetch_by_year(year):
    c.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y', \"date\") = ?", (str(year),))
    res = c.fetchone()[0]
    return res if res else 0.0

# Get total expenses per category
def fetch_category_summary():
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = c.fetchall()
    return pd.DataFrame(data, columns=["Category", "Total"])

# Get total expenses per month
def fetch_monthly_summary():
    c.execute("SELECT strftime('%m', \"date\") as month, SUM(amount) FROM expenses GROUP BY month ORDER BY month")
    data = c.fetchall()
    return pd.DataFrame(data, columns=["Month", "Total"])
