import streamlit as st
import os
import base64
from dotenv import load_dotenv
from groq import Groq
from ddgs import DDGS
import requests
import streamlit.components.v1 as components

load_dotenv()
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="SAFARMATE 2.0", page_icon="🇮🇳", layout="wide")

# ===== BACKGROUND =====
def get_bg():
    if os.path.exists("background.jpg"):
        with open("background.jpg", "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

bg_data = get_bg()
if bg_data:
    st.markdown(f"""
    <style>
 .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.65)), url("data:image/jpeg;base64,{bg_data}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# ===== ULTRA PATLA + TIRANGA TITLE =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&display=swap');

.sky,.track,.road {
    background: rgba(0,0,0,0.25)!important;
    backdrop-filter: blur(2px);
    height: 32px!important;
    position: relative; overflow: hidden;
    border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.2)!important;
    box-shadow: none!important;
    width: 100%;
    margin-top: 6px!important;
}
.sky { margin-top: 0px!important; }
.plane { position: absolute; font-size: 18px!important; animation: fly 6s linear infinite; top: 4px; }
.train { position: absolute; font-size: 18px!important; animation: run 8s linear infinite; top: 3px; white-space: nowrap; }
.bus { position: absolute; font-size: 18px!important; animation: run 5s linear infinite; top: 3px; white-space: nowrap; }
@keyframes fly { 0% { left: -10%; } 100% { left: 110%; } }
@keyframes run { 0% { left: -50%; } 100% { left: 110%; } }

.tiranga-title {
    text-align:center; font-family:'Orbitron';
    font-size:50px!important; font-weight:900;
    letter-spacing:3px; margin-top:12px;
    line-height:1.1;
    filter: drop-shadow(2px 2px 6px rgba(0,0,0,0.8));
}
.saffron { color: #FF9933; text-shadow: 0 0 10px rgba(255,153,51,0.6); }
.white { color: #FFFFFF; text-shadow: 0 0 10px rgba(255,255,255,0.6); }
.green { color: #138808; text-shadow: 0 0 10px rgba(19,136,8,0.6); }
.chakra {
    display:inline-block;
    font-size:38px;
    color:#000080;
    animation: spin 3s linear infinite;
    vertical-align: middle;
    margin: 0 4px;
    text-shadow: 0 0 8px white;
}
@keyframes spin { 100% { transform: rotate(360deg); } }

.sub-title {
    text-align:center; color:#e0f7fa;
    font-family:monospace; font-size:13px;
    letter-spacing:1.5px; margin-bottom:10px;
    text-shadow: 1px 1px 4px black;
}
.glass {
    background: rgba(0,0,0,0.45); backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.15); border-radius: 10px;
    padding: 16px;
}
</style>

<div class="sky"><div class="plane">✈️</div></div>
<div class="track"><div class="train">🚃🚃🚃🚃🚃🚃🚃🚃🚂</div></div>
<div class="road"><div class="bus">🚌</div></div>

<div class="tiranga-title">
    <span class="saffron">SAFAR</span><span class="chakra">☸️</span><span class="green">MATE 2.0</span>
</div>
<div class="sub-title">SYSTEM ONLINE • GPS + VENDOR INTELLIGENCE • LIVE SEARCH</div>
""", unsafe_allow_html=True)

# ===== SESSION STATE =====
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "trip_context" not in st.session_state:
    st.session_state.trip_context = ""
if "latlon" not in st.session_state:
    st.session_state.latlon = None

tab1, tab2 = st.tabs(["🧪 MISSION PLANNER", "🤖 VENDOR & STREET FOOD CHATBOT + GPS"])

with tab1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: source = st.text_input("Source", "Lucknow")
    with c2: destination = st.text_input("Destination", "Goa")
    with c3: days = st.number_input("Days", 1, 30, 3)
    with c4: budget = st.selectbox("Budget", ["Cheap", "Medium", "Luxury"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### 📍 GPS MODULE")
    components.html("""
    <button onclick="getLoc()" style="background:#FF9933;color:black;padding:10px 20px;border-radius:8px;border:none;font-weight:bold;cursor:pointer;">📡 DETECT MY LOCATION</button>
    <p id="loc" style="color:#00ff88;font-family:monospace;margin-top:10px;font-size:13px;background:rgba(0,0,0,0.6);padding:6px;border-radius:6px;"></p>
    <script>
    function getLoc(){
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition((p)=>{
                document.getElementById('loc').innerText = `LAT: ${p.coords.latitude}, LON: ${p.coords.longitude}`;
            });
        }
    }
    </script>
    """, height=90)

    lat_input = st.text_input("Paste LAT,LON here (e.g. 26.8467,80.9462) for vendor scan", "")
    if st.button("🚀 Search Live Plan + Scan Vendors", use_container_width=True, type="primary"):
        with st.spinner("Fetching LIVE data..."):
            live_info = ""
            try:
                with DDGS() as ddgs:
                    q = f"{source} to {destination} flight train bus price hotels {budget}"
                    results = list(ddgs.text(q, max_results=5))
                    live_info = "\\n".join([r['body'] for r in results])
            except:
                live_info = "Live search unavailable"

            vendor_info = ""
            if lat_input and "," in lat_input:
                try:
                    lat, lon = map(float, lat_input.split(","))
                    overpass_query = f"[out:json];node(around:500,{lat},{lon})[amenity~'fast_food|street_vendor|food_court|restaurant|cafe'];out 10;"
                    r = requests.post("https://overpass-api.de/api/interpreter", data=overpass_query, timeout=10)
                    data = r.json()
                    vendor_info = "\\nNearby Vendors:\\n" + "\\n".join([f"- {e.get('tags',{}).get('name','Unnamed')} ({e.get('tags',{}).get('amenity')})" for e in data.get('elements',[])[:10]])
                except:
                    vendor_info = "Vendor scan failed"

            client = Groq(api_key=GROQ_KEY)
            prompt = f"Create detailed travel plan from {source} to {destination} for {days} days, budget {budget}. Use live info: {live_info}. {vendor_info}. Give transport, hotels, itinerary, cost, and also list street food & cheap vendors."

            models = ["openai/gpt-oss-20b","llama-3.3-70b-versatile","llama-3.1-8b-instant"]
            for model_name in models:
                try:
                    res = client.chat.completions.create(model=model_name, messages=[{"role":"user","content":prompt}], max_tokens=3000)
                    st.balloons()
                    st.success(f"PLAN DECODED | Model: {model_name}")
                    st.session_state.trip_context = res.choices[0].message.content
                    st.markdown(f'<div class="glass">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
                    break
                except:
                    continue

with tab2:
    st.markdown("### 🤖 SAFARMATE AI - Vendor Guide")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if q := st.chat_input("Pucho: Goa me best cheap fish thali kahan milegi?"):
        st.session_state.chat_history.append({"role":"user","content":q})
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            client = Groq(api_key=GROQ_KEY)
            context_prompt = f"You are SAFARMATE vendor guide. Trip context: {st.session_state.trip_context}. Location: {lat_input}. User asks: {q}. Answer in Hinglish."
            try:
                res = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"user","content":context_prompt}], max_tokens=800)
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.chat_history.append({"role":"assistant","content":ans})
            except Exception as e:
                st.error(f"Bot error: {e}")
