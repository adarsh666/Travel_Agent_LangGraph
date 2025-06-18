from agent import TravelAgent
from langchain_core.messages import HumanMessage
import streamlit as st

# Streamlit App Title
st.title("🌍 AI-Powered Trip Planner")

st.markdown("""
💡 **Plan your next trip with AI!**  
Enter your travel details below, and our AI-powered travel assistant will create a personalized itinerary including:
 Best places to visit 🎡   Accommodation & budget planning 💰
 Local food recommendations 🍕   Transportation & visa details 🚆
""")

# User Inputs
from_city = st.text_input("🏡 From City", "Delhi")
destination_city = st.text_input("✈️ Destination City", "Tokyo")
date_from = st.date_input("📅 Departure Date")
date_to = st.date_input("📅 Return Date")
num_travellers = st.number_input("Total Passengers")
budget = st.number_input("🎯 Max Budget")

# Button to run Trip Agent
if st.button("🚀 Generate Travel Plan"):
    if not from_city or not destination_city or not date_from or not date_to or not num_travellers\
         or not budget:
        st.error("⚠️ Please fill in all fields before generating your travel plan.")
    else:
        st.write("⏳ AI is preparing your personalized travel itinerary... Please wait.")

        agent = TravelAgent()
        app_graph = agent.workflow()
        message=[HumanMessage(content=f"I am planning to travel from {from_city} to {destination_city}.\
                              Start date is {date_from}, end date is {date_to} number of travelers is {num_travellers}.\
                              and Budget in currency in {from_city} and max budget is {budget}")]
        
        messages = app_graph.invoke({"messages": message})

        result = messages['messages'][-1].content

        st.subheader("✅ Your AI-Powered Travel Plan")
        st.markdown(result)

        travel_plan_text = str(result)

        st.download_button(
            label="📥 Download Travel Plan",
            data=travel_plan_text,
            file_name=f"Travel_Plan_{destination_city}.txt",
            mime="text/plain"
        )