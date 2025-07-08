import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_by_month_tab():
    st.title("Monthly Expense Breakdown")

    # --- 1. Call the API ----------------------------------------------------
    resp = requests.get(f"{API_URL}/analytics/monthly")
    if resp.status_code != 200:
        st.error("Could not load monthly analytics.")
        return

    monthly_summary = resp.json()              # e.g. [{'month_name':'August','total':5315}, …]
    if not monthly_summary:
        st.info("No expense data found.")
        return

    # --- 2. Convert the list→DataFrame --------------------------------------
    df = pd.DataFrame(monthly_summary)         # columns: month_name, total
    df = df.sort_values("month_name")          # keeps Jan→Dec order, just in case

    # --- 3. Bar chart --------------------------------------------------------
    st.bar_chart(
        data=df.set_index("month_name")["total"],   # x = month_name, y = total
        use_container_width=True
    )

    # --- 4. Pretty table -----------------------------------------------------
    df_display = df.rename(columns={"month_name": "Month", "total": "Total"})
    df_display["Total"] = df_display["Total"].map("{:.2f}".format)

    st.table(df_display)
