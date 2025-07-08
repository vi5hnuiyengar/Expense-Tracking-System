import streamlit as st
from add_update import add_update_tab
from analytics_by_category import analytics_by_category_tab
from analytics_by_month import analytics_by_month_tab
from savings_plan import savings_plan_tab

st.title("Expense Tracking System")
# st.markdown(
#     """
#     <style>
#         /* ========== GLOBAL ================================================= */
#         html, body, [class*="st-"] {
#             font-family: "Garamond", serif;
#             background-color: #000;
#             color: #f5f5f5;
#         }
#
#         /* ========== HEADINGS ============================================== */
#         h1, h2, h3, h4, h5, h6 {
#             color: #ffd700;                      /* gold                           */
#         }
#
#         /* ========== GOLD BUTTONS ========================================== */
#         /* normal state */
#         .stButton > button {
#             background: #d4af37;                 /* royal gold                     */
#             color: #000;
#             border: none;
#             border-radius: 8px;                  /* ✨ rounded corners              */
#             padding: 0.5rem 1.25rem;
#             font-weight: 600;
#             cursor: pointer;
#             transition: all 120ms ease-in-out;
#         }
#         /* hover / focus */
#         .stButton > button:hover,
#         .stButton > button:focus-visible {
#             background: #e0bd4c;
#             box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.35);
#             outline: none;
#         }
#         /* disabled */
#         .stButton > button:disabled {
#             opacity: 0.4 !important;
#             cursor: default !important;
#             box-shadow: none !important;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
tab1, tab2, tab3, tab4 = st.tabs(
    ["Add/Update", "Analytics by Category", "Analytics by Month", "Savings Plan"]
)

with tab1:
    add_update_tab()
with tab2:
    analytics_by_category_tab()
with tab3:
    analytics_by_month_tab()
with tab4:
    savings_plan_tab()
























# # Text Elements
# st.header("Streamlit Core Features")
# st.subheader("Text Elements")
# st.text("This is a simple text element.")
#
# st.title("Expense Management System")
#
# # Data display
# st.subheader("Data Display")
# st.write("Here is a simple table:")
#
#
# df = pd.DataFrame({
#     "Date":["2024-08-01", "2024-08-02", "2024-08-03"],
#     "Amount": [250, 134, 340]
# })
#
# st.table({"Column 1": [1, 2, 3], "Column 2": [4, 5, 6]})
# st.table(df)
#
# # Charts
# st.subheader("Charts")
# st.line_chart([1, 2, 3, 4])
#
# # User Input
# st.subheader("User Input")
# value = st.slider("Select a value", min_value=0, max_value=100)
# st.write(f"Selected value: {value}")
#
# expense_dt = st.date_input("Expense Date:")
# if expense_dt:
#     st.write(f"Fetching expenses for {expense_dt}")
#
#
#
# st.title("Interactive Widgets Example")
#
# # Checkbox
# if st.checkbox("Show/Hide"):
#     st.write("Checkbox is checked!")
#
# # Selectbox
# option = st.selectbox("Category", ["Rent", "Food"], label_visibility="collapsed")
# st.write(f"You selected: {option}")
#
# # Multiselect
# options = st.multiselect("Select multiple numbers", [1, 2, 3, 4])
# st.write(f"You selected: {options}")