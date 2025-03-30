import streamlit as st
from ai_itinerary import AItineraryGenerator
from ai_assistant import AIAssistant
import base64

# Constants
INR_RATE = 83.38  # 1 USD = ₹83.38

# Initialize session state
if "generator" not in st.session_state:
    st.session_state.generator = AItineraryGenerator()
    st.session_state.assistant = AIAssistant()
    st.session_state.itinerary = None
    st.session_state.chat_history = []

# --- UI Config ---
st.set_page_config(layout="wide", page_title="✨ AI Travel Planner")
st.markdown("""
    <style>
    .stTextInput input, .stTextArea textarea { border-radius: 20px; }
    .stDownloadButton button { width: 100%; justify-content: center; }
    .css-1v0mbdj { border-radius: 20px !important; }
    [data-testid="stChatMessage"] { padding: 12px; margin: 5px 0; border-radius: 15px; }
    .assistant-message { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# --- Main Columns ---
col1, col2 = st.columns([3, 2])

# --- Left Column: Itinerary Generator ---
with col1:
    st.title("✈️ Personalized Travel Planner")
    
    # Currency Toggle
    currency = st.radio("Currency", ["₹ INR", "$ USD"], horizontal=True, key="currency")
    
    with st.expander("🔍 Trip Details", expanded=True):
        with st.form("preferences"):
            destination = st.text_input("Destination*", placeholder="e.g., Goa, Paris")
            days = st.number_input("Number of Days*", min_value=1, max_value=30, value=5)
            
            if currency == "₹ INR":
                budget = st.number_input("Total Budget* (₹)", min_value=5000, value=50000, step=5000)
            else:
                budget = st.number_input("Total Budget* ($)", min_value=100, value=2000, step=100)
                budget = int(budget * INR_RATE)
            
            travel_style = st.text_area("Travel Style*", placeholder="e.g., 'Beach resorts, local street food'")
            special_requests = st.text_area("Special Requests", placeholder="e.g., 'Pet-friendly hotels'", height=100)
            companions = st.text_input("Who's joining?*", placeholder="e.g., 'Family of 4'")
            
            if st.form_submit_button("✨ Generate Itinerary"):
                if not destination or not travel_style:
                    st.error("Please fill required fields (*)")
                else:
                    with st.spinner("Creating your perfect itinerary..."):
                        st.session_state.itinerary = st.session_state.generator.generate(
                            destination=destination,
                            days=days,
                            budget=budget,
                            currency=currency,
                            style=travel_style,
                            companions=companions,
                            requests=special_requests
                        )
                    st.session_state.chat_history = [("assistant", f"I've created a {days}-day itinerary for {destination}! How can I improve it?")]

    # Display Itinerary
    if st.session_state.itinerary:
        st.subheader(f"🗓️ {destination} Itinerary")
        st.markdown("---")
        st.markdown(st.session_state.itinerary)
        
        # Download Button (Text only)
        st.download_button(
            label="📥 Download Itinerary (TXT)",
            data=st.session_state.itinerary,
            file_name=f"{destination}_itinerary.txt",
            mime="text/plain"
        )

# --- Right Column: Chat Assistant ---
with col2:
    st.title("🤖 Travel Assistant")
    
    # Chat History Container
    chat_container = st.container(height=500)
    
    # Display all chat messages
    for sender, message in st.session_state.chat_history:
        with chat_container:
            if sender == "user":
                with st.chat_message("user"):
                    st.write(message)
            else:
                with st.chat_message("assistant"):
                    st.write(message)
    
    # Chat Input at Bottom
    if st.session_state.itinerary:
        user_input = st.chat_input("Ask to modify your itinerary...", key="chat_input")
        
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append(("user", user_input))
            
            # Get AI response
            with st.spinner("Thinking..."):
                response = st.session_state.assistant.chat(
                    message=user_input,
                    itinerary=st.session_state.itinerary
                )
                
                # Add assistant response to chat history
                st.session_state.chat_history.append(("assistant", response))
                
                # Check if response contains an updated itinerary
                if "Day 1" in response and "Morning" in response:
                    st.session_state.itinerary = response
                    st.rerun()
    else:
        st.info("Generate an itinerary first to chat with the assistant")