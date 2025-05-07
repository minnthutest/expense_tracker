# expense_manager.py
from database import insert_expense, fetch_all_expenses, filter_by_category, fetch_by_month, fetch_by_year, fetch_category_summary, fetch_monthly_summary

def add_expense(date, category, amount, description):
    insert_expense(date, category, amount, description)

def get_expenses():
    return fetch_all_expenses()

def filter_expenses_by_category(category):
    return filter_by_category(category)

def get_total_by_month(month):
    return fetch_by_month(month)

def get_total_by_year(year):
    return fetch_by_year(year)

def get_category_summary():
    return fetch_category_summary()

def get_monthly_summary():
    return fetch_monthly_summary()
