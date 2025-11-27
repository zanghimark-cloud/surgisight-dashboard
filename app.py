import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# === Load Firebase credentials from Streamlit secrets (TOML format) ===
cred = credentials.Certificate(st.secrets["firebase"])

# === Your Firebase URL ===
DATABASE_URL = "https://surgisight-25e86-default-rtdb.firebaseio.com/"

# Initialize Firebase (only once)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})

# Point to the OR room
ref = db.reference("/or1")

# === SurgiSight Dashboard ===
st.set_page_config(page_title="SurgiSight", layout="centered")
st.markdown('<h1 style="text-align:center;font-size:4.5rem;color:#005566;font-weight:900;">SurgiSight</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;font-size:1.5rem;color:#555;">Automatic OR presence • One beacon • Zero friction</p>', unsafe_allow_html=True)

people = {
    "alex":   {"name": "Alex Rivera",     "title": "Sales Rep",       "photo": "https://i.imgur.com/5pHsTRk.png"},
    "marcus": {"name": "Dr. Marcus Chen", "title": "Lead Surgeon",    "photo": "https://i.imgur.com/3f6j0kM.png"},
    "sarah":  {"name": "Sarah Kim",       "title": "Circulating Nurse","photo": "https://i.imgur.com/8zJ0K8s.png"},
}

placeholder = st.empty()

while True:
    data = ref.get() or {}
    current = [v for v in data.values() if v.get("present", False)]
    
    with placeholder.container():
        if current:
            for p in current:
                info = people.get(p["userId"], {"name":"Unknown", "title":"", "photo":"https://i.imgur.com/5pHsTRk.png"})
                c1, c2 = st.columns([1,4])
                with c1: st.image(info["photo"], width=110)
                with c2:
                    st.markdown(f"**{info['name']}**")
                    st.write(f"{info['title']}")
                    st.caption(f"Entered {p['timestamp'][-8:]}")
                st.markdown("---")
        else:
            st.info("Room empty – waiting for first person")
    
    time.sleep(3)
