import streamlit as st
import pandas as pd
from datetime import datetime
from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history

# Initialize tracker flag
if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

if not st.session_state.tracker_started:
    st.title("Welcome to AI Water Tracker")
    st.markdown("""
        Track your daily hydration with the help of an AI Assistant.  
        Log your intake, get smart feedback, and stay healthy.
    """)

    if st.button("Start Tracking"):
        st.session_state.tracker_started = True
        st.experimental_rerun()

else:
    st.title("AI Water Tracker Dashboard")

    st.sidebar.header("Log Your Water Intake")
    user_id = st.sidebar.text_input("User ID", value="user_123")

    intake_ml = st.sidebar.number_input(
        "Water Intake (ml)", min_value=0, max_value=5000, step=50
    )

    if st.sidebar.button("Submit"):
        if user_id.strip() and intake_ml > 0:
            log_intake(user_id.strip(), intake_ml)
            st.success(f"Logged {intake_ml} ml for {user_id}")

            agent = WaterIntakeAgent()
            feedback = agent.analyse_intake(intake_ml)
            st.info(f"AI Feedback: {feedback}")
        else:
            st.error("Please enter a valid User ID and intake amount greater than 0.")

    st.markdown("---")
    st.header("Water Intake History")

    if user_id.strip():
        history = get_intake_history(user_id.strip())

        if history:
            try:
                dates = [datetime.strptime(row[1], "%Y-%m-%d") for row in history]
                values = [row[0] for row in history]

                df = pd.DataFrame({
                    "Date": dates,
                    "Water Intake (ml)": values
                })

                st.dataframe(df)
                st.line_chart(df.set_index("Date"))
            except Exception as e:
                st.error(f"Error processing history data: {e}")
        else:
            st.warning("No water intake data found. Please log your intake first.")
