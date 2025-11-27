import streamlit as st
import time
import requests

# === YOUR FIREBASE URL ===
DATABASE_URL = "https://surgisight-25e86-default-rtdb.firebaseio.com/or1.json"

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
    try:
        response = requests.get(DATABASE_URL, timeout=10)  # Longer timeout
        response.raise_for_status()  # Raise error if 403 or other
        data = response.json() or {}
        current = [v for v in data.values() if v.get("present", False)]
        st.success("Connected!")  # Success message (remove later)
    except Exception as e:
        current = []
        st.warning(f"Connection retrying... (Error: {str(e)[:50]}...)")  # Show partial error for debugging

    with placeholder.container():
        if current:
            for p in current:
                info = people.get(p.get("userId", ""), {"name":"Unknown", "title":"", "photo":"https://i.imgur.com/5pHsTRk.png"})
                c1, c2 = st.columns([1,4])
                with c1: st.image(info["photo"], width=110)
                with c2:
                    st.markdown(f"**{info['name']}**")
                    st.write(f"{info['title']}")
                    ts = p.get("timestamp", "")
                    if ts: st.caption(f"Entered {ts[-8:]}")
                st.markdown("---")
        else:
            st.info("Room empty – waiting for first person")

    time.sleep(5)  # Slower refresh to avoid rate limits
