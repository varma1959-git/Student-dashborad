# main.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from services.operations import add_entry, get_summary
from db.storage import load_data
from utils.validators import valid_name, valid_age, valid_score
from config.constants import HISTORY_FILE

st.set_page_config(page_title="Student Dashboard", layout="wide")
st.title("Student Dashboard 🚀")

df = load_data()

# ---- Sidebar Form (NO user field) ----
st.sidebar.header("Add new entry")
with st.sidebar.form("entry", clear_on_submit=True):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120, value=18, step=1)
    score = st.number_input("Score", min_value=0, max_value=100, value=0, step=1)
    submitted = st.form_submit_button("Add")   # << submit button INSIDE the form

if submitted:
    if not valid_name(name):
        st.sidebar.error("Enter a valid name.")
    elif not valid_age(age):
        st.sidebar.error("Enter a valid age (> 0).")
    elif not valid_score(score):
        st.sidebar.error("Enter a valid score (0–100).")
    else:
        df = add_entry(name.strip(), int(age), float(score))  # << no user arg
        st.sidebar.success(f"Added {name}!")

# ---- Data table ----
st.subheader("Current Data")
st.dataframe(df, use_container_width=True)

# ---- KPIs ----
st.subheader("Summary")
summary = get_summary(df)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total entries", summary["count"])
c2.metric("Average score", "—" if summary["avg_score"] is None else f"{summary['avg_score']:.2f}")
c3.metric("Max score", "—" if summary["max_score"] is None else summary["max_score"])
c4.metric("Min score", "—" if summary["min_score"] is None else summary["min_score"])

# ---- Chart ----
st.subheader("Scores Chart")
if not df.empty:
    # Ensure Name is string, Score is numeric
    df["Name"] = df["Name"].astype(str)
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce").fillna(0)

    fig, ax = plt.subplots()
    ax.bar(df["Name"], df["Score"])
    ax.set_xlabel("Name")
    ax.set_ylabel("Score")
    ax.set_title("Scores by Student")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)
else:
    st.info("No data yet. Add some entries from the sidebar to see the chart.")
