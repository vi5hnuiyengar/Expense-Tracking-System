import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

def savings_plan_tab():
    st.header("Savings Plan")

    # ----- inputs -----------------------------------------------------------
    col1, col2 = st.columns(2)
    with col1:
        target = st.number_input("Target amount ($)", min_value=1.0, step=50.0)
    with col2:
        period = st.selectbox("Save every …", ("week", "month"))

    col3, col4 = st.columns(2)
    with col3:
        start_date = st.date_input(
            "Analyse spending from",
            value=datetime.today().replace(day=1)
        )
    with col4:
        end_date = st.date_input("… to", value=datetime.today())

    # ----- submit -----------------------------------------------------------
    if st.button("Generate Plan"):
        req_payload = {
            "target": target,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "period": period
        }

        try:
            resp = requests.post(f"{API_URL}/savings_plan", json=req_payload, timeout=5)
        except requests.exceptions.RequestException as e:
            st.error(f"Cannot reach API: {e}")
            return

        if resp.status_code != 200:
            st.error(resp.json().get("detail", "Unknown error"))
            return

        plan = resp.json()
        # ----- plain-text result -------------------------------------------
        # ----- plain-text result inside a custom div -------------------------------
        msg = (
            f"Save ${plan['save_per_period']:.2f} each {plan['period']} on "
            f"{plan['category']} for {plan['num_periods']} {plan['period']}"
            f"{'s' if plan['num_periods'] != 1 else ''} to reach your "
            f"${target:.2f} goal."
        )

        st.markdown(
            f"""
            <div style="background:#0d3b66;padding:0.6rem 1rem;border-radius:6px;
                        color:#fff;font-size:0.9rem;white-space:pre;">
                {msg}
            </div>
            """,
            unsafe_allow_html=True,
        )