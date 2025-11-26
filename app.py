import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import db
import time

# === YOUR EXACT FIREBASE URL (already correct) ===
DATABASE_URL = "https://surgisight-25e86-default-rtdb.firebaseio.com/"

# Connect to your Firebase (temporary shortcut for test mode – no full credentials needed yet)
if not firebase_admin._apps:
    firebase_admin.initialize_app(options={'databaseURL': DATABASE_URL})

# Point to the exact room node
ref = db.reference('/or1')

# === SURGISIGHT BRANDING ===
st.set_page_config(page_title="SurgiSight OR Screen", layout="centered")
st.markdown('<h1 style="text-align:center;font-size:4.5rem;color:#005566;font-weight:900;">SurgiSight</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;font-size:1.5rem;color:#555;">Automatic OR presence • One beacon • Zero friction</p>', unsafe_allow_html=True)

# People database
people = {
    "alex":   {"name": "Alex Rivera",     "title": "Sales Rep",       "photo": "https://i.imgur.com/5pHsTRk.png"},
    "marcus": {"name": "Dr. Marcus Chen", "title": "Lead Surgeon",    "photo": "https://i.imgur.com/3f6j0kM.png"},
    "sarah":  {"name": "Sarah Kim",       "title": "Circulating Nurse","photo": "https://i.imgur.com/8zJ0K8s.png"},
}

# Live refresh loop
placeholder = st.empty()
log_placeholder = st.empty()

while True:
    data = ref.get() or {}
    current = [v for v in data.values() if v.get("present", False)]
    
    with placeholder.container():
        if current:
            for person in current:
                info = people.get(person["userId"], {"name":"Unknown", "title":"", "photo": "https://i.imgur.com/5pHsTRk.png"})
                c1, c2 = st.columns([1, 4])
                with c1:
                    st.image(info["photo"], width=110)
                with c2:
                    st.markdown(f"**{info['name']}**")
                    st.write(f"{info['title']}")
                    st.caption(f"Entered {person['timestamp'][-8:]}")
                st.markdown("---")
        else:
            st.info("Room empty – waiting for first person")

    # Log (using session state for persistence)
    if 'log' not in st.session_state:
        st.session_state.log = []
    # Update log from data (simple example – expand as needed)
    with log_placeholder.container():
        st.markdown("### Legal Event Log")
        for key, value in data.items():
            if 'action' in value:
                st.session_state.log.append(f"[{value['timestamp']}] {value['action']} → {people.get(value['userId'], {'name': 'Unknown'})['name']}")
        for entry in reversed(st.session_state.log[-20:]):  # Show last 20
            st.write(entry)

    time.sleep(3)
