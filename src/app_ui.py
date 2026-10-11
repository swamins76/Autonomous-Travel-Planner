import streamlit as st
import requests

# 1. Page Configuration Setup
st.set_page_config(page_title="Autonomous Travel Planner", page_icon="🏕️", layout="wide")

st.title("🏕️ Autonomous Travel & Camping Planner Agent")
st.write("Plan your next regional trip with real-time weather alerts and localized park rules.")

# 2. Input Sidebar Layout
st.sidebar.header("Trip Specifications")
destination = st.sidebar.text_input("Where are you heading?", placeholder="e.g., Lake Anna State Park")
duration_days = st.sidebar.slider("Trip Duration (Days)", min_value=1, max_value=7, value=3)
additional_notes = st.sidebar.text_area(
    "Special requirements / Gear notes:", 
    placeholder="e.g., I have a family tent and a 2-burner propane camp stove. Making vegetable skewers."
)

submit_button = st.sidebar.button("Generate Smart Itinerary", type="primary")

# 3. Main Dashboard Interaction Area
if submit_button:
    if not destination.strip():
        st.error("Please enter a valid destination folder name or park location before running.")
    else:
        with st.spinner(f"Agent is analyzing paths, weather networks, and rules for {destination}..."):
            try:
                # Target the active FastAPI backend endpoint we just tested
                backend_url = "http://127.0.0.1:8000/api/plan-trip"
                payload = {
                    "destination": destination,
                    "duration_days": duration_days,
                    "additional_notes": additional_notes
                }
                
                response = requests.post(backend_url, json=payload)
                
                if response.status_code == 200:
                    result_data = response.json()
                    st.success("✨ Itinerary Generated Successfully!")
                    
                    # Output the LangChain Agent response text layout natively 
                    st.markdown("### 📋 Your Tailored Agent Itinerary")
                    st.info(result_data["itinerary"])
                else:
                    st.error(f"Backend Server error returned code: {response.status_code}")
                    st.json(response.json())
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not link to the backend engine. Ensure Uvicorn is actively listening on port 8000.")
