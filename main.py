# main.py
import streamlit as st
import pandas as pd
import datetime
from expense_manager import add_expense, get_expenses, filter_expenses_by_category, get_total_by_month, get_total_by_year, get_category_summary, get_monthly_summary
from database import create_table
import plotly.express as px

# --- Load Custom CSS ---
def load_css():
    with open("css/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- App Setup ---
st.set_page_config("💸 Personal Expense Tracker", layout="centered")
create_table()
load_css()
st.title("💸 Personal Expense Tracker")

menu = ["Add Expense", "View Expenses", "Charts"]
choice = st.sidebar.radio("Menu", menu)

# --- Add Expense ---
if choice == "Add Expense":
    st.subheader("➕ Add New Expense")
    with st.form("expense_form"):
        date = st.date_input("Date", value=datetime.date.today())
        category = st.selectbox("Category", ["Food", "Transport", "Bills", "Others"])
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        description = st.text_input("Description")
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            add_expense(date, category, amount, description)
            st.success("✅ Expense added successfully!")

# --- View Expenses ---
elif choice == "View Expenses":
    st.subheader("📋 All Expenses")
    category_filter = st.selectbox("Filter by Category", ["All", "Food", "Transport", "Bills", "Others"])
    if category_filter == "All":
        data = get_expenses()
    else:
        data = filter_expenses_by_category(category_filter)

    df = pd.DataFrame(data, columns=["Date", "Category", "Amount", "Description"])
    st.dataframe(df)

    st.markdown("### 📆 Total Overview")
    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox("Select Month", range(1, 13), format_func=lambda x: datetime.date(1900, x, 1).strftime('%B'))
        total_month = get_total_by_month(selected_month)
        st.metric(label="Monthly Total", value=f"{total_month:,.0f} MMK")

    with col2:
        selected_year = st.selectbox("Select Year", range(2022, 2031))
        total_year = get_total_by_year(selected_year)
        st.metric(label="Yearly Total",value=f"{total_year:,.0f} MMK")

# --- Charts ---
elif choice == "Charts":
    st.subheader("📊 Expense Charts")

    category_summary = get_category_summary()
    monthly_summary = get_monthly_summary()

    if not category_summary.empty:
        pie_chart = px.pie(category_summary, names="Category", values="Total", title="Expenses by Category")
        st.plotly_chart(pie_chart, use_container_width=True)

        monthly_summary["Month"] = monthly_summary["Month"].apply(lambda x: datetime.date(1900, int(x), 1).strftime('%B'))
        bar_chart = px.bar(monthly_summary, x="Month", y="Total", title="Monthly Expenses")
        st.plotly_chart(bar_chart, use_container_width=True)
    else:
        st.info("No data to display charts.")
