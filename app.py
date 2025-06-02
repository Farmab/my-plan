import streamlit as st
import sqlite3
from datetime import date, datetime

# Connect to SQLite database
conn = sqlite3.connect("plans.db", check_same_thread=False)
c = conn.cursor()

# Create table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        plan TEXT
    )
''')
conn.commit()

# Streamlit App
st.set_page_config(page_title="Daily Planner", layout="centered")
st.title("📅 Daily Planner")

# Add new plan
st.subheader("➕ Add Your Plan")
selected_date = st.date_input("Select the date", date.today())
plan_text = st.text_area("Write your plan or daily details")

if st.button("Add Plan"):
    if plan_text.strip() != "":
        c.execute("INSERT INTO plans (date, plan) VALUES (?, ?)", (selected_date.isoformat(), plan_text.strip()))
        conn.commit()
        st.success("Plan added successfully!")
    else:
        st.warning("Please enter a plan before saving.")

# View plans by date
st.subheader("📖 View Your Plans")
view_date = st.date_input("Choose a date to view plans", date.today(), key="view")
c.execute("SELECT plan FROM plans WHERE date = ?", (view_date.isoformat(),))
rows = c.fetchall()

if rows:
    for row in rows:
        st.info(f"📝 {row[0]}")
else:
    st.write("No plans for this date.")

# Monthly report
st.subheader("📊 Monthly Report")
current_month = st.date_input("Choose a month for report", date.today(), key="month")
start_month = current_month.replace(day=1)
end_month = (current_month.replace(day=28) + timedelta(days=4)).replace(day=1)

c.execute("SELECT date, plan FROM plans WHERE date >= ? AND date < ? ORDER BY date", (start_month.isoformat(), end_month.isoformat()))
monthly_plans = c.fetchall()

if monthly_plans:
    for d, p in monthly_plans:
        d_fmt = datetime.strptime(d, "%Y-%m-%d").strftime("%b %d")
        st.markdown(f"**{d_fmt}:** {p}")
else:
    st.write("No plans found for this month.")
