import streamlit as st
import os
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

st.set_page_config(page_title="CHARIOT 2.0", page_icon="🏹", layout="wide")

# ===== SCIENTIST FUTURISTIC UI =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=JetBrains+Mono&display=swap');
.stApp { background: radial-gradient(circle at top, #0f2027, #000000); }
.sky { background: linear-gradient(90deg, #00111a, #00334d); height: 65px; position: relative; overflow: hidden; border-radius: 12px; border: 1px solid #00f7ff; box-shadow: 0 0 15px #00f7ff; }
.plane { position: absolute; font-size: 35px; animation: fly 6s linear infinite; top: 10px; }
.track { background: #0a0a0a; height: 55px; position: relative; overflow: hidden; border-radius: 12px; border: 1px solid #ff00ff; box-shadow: 0 0 10px #ff00ff; margin-top: 8px; }
.road { background: #111; height: 55px; position: relative; overflow: hidden; border-radius: 12px; border: 1px solid #00ff88; box-shadow: 0 0 10px #00ff88; margin-top: 8px; }
@keyframes fly { 0% { left: -10%; } 100% { left: 110%; } }
@keyframes run { 0% { left: -40%; } 100% { left: 110%; } }
.train { position: absolute; font-size: 30px; animation: run 8s linear infinite; top: 6px; }
.bus { position: absolute; font-size: 30px; animation: run 5s linear infinite; top: 6px; }
.title { text-align:center; font-family:'Orbitron'; font-size:50px; font-weight:900; color:#00f7ff; text-shadow: 0 0 20px #00f7ff; margin-top:15px; letter-spacing:3px;}
.glass { background: rgba(255,255,255,0.05); backdrop-filter: blur(12px); border: 1px solid rgba(0,247,255,0.2); border-radius: 15px; padding: 15px; box-shadow: 0 0 25px rgba(0,247,255,0.1); }
.stChatMessage { font-family: 'JetBrains Mono'!important; }
</style>
<div class="sky"><div class="plane">✈️</div></div>
<div class="track"><div class="train">🚃🚃🚃🚃🚃🚃🚃🚃🚂</div></div>
<div class="road"><div class="bus">🚌💨</div></div>
<div class="title">CHARIOT 2.0</div>
<p style="text-align:center; color:#00f7ff; font-family:'JetBrains Mono';">SYSTEM ONLINE • GPS + VENDOR INTELLIGENCE • LIVE SEARCH</p>
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

    # GPS COMPONENT
    st.markdown("#### 📍 GPS MODULE")
    components.html("""
    <button onclick="getLoc()" style="background:#00f7ff;color:black;padding:10px 20px;border-radius:8px;border:none;font-weight:bold;cursor:pointer;box-shadow:0 0 10px #00f7ff;">📡 DETECT MY LOCATION</button>
    <p id="loc" style="color:#00ff88;font-family:monospace;margin-top:10px;"></p>
    <script>
    function getLoc(){
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition((p)=>{
                document.getElementById('loc').innerText = `LAT: ${p.coords.latitude}, LON: ${p.coords.longitude} | Copy this & paste in chatbot`;
                // Send to Streamlit via parent
            });
        } else {
            document.getElementById('loc').innerText = "Geolocation not supported";
        }
    }
    </script>
    """, height=100)

    lat_input = st.text_input("Paste LAT,LON here (e.g. 26.8467,80.9462) for vendor scan", "")
    if st.button("🚀 Search Live Plan + Scan Vendors", use_container_width=True, type="primary"):
        with st.spinner("Fetching LIVE data + scanning street vendors..."):
            live_info = ""
            try:
                with DDGS() as ddgs:
                    q = f"{source} to {destination} flight train bus price hotels {budget}"
                    results = list(ddgs.text(q, max_results=5))
                    live_info = "\\n".join([r['body'] for r in results])
            except:
                live_info = "Live search unavailable"

            # Vendor scan via Overpass API if latlon given
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
            prompt = f"Create detailed travel plan from {source} to {destination} for {days} days, budget {budget}. Use live info: {live_info}. {vendor_info}. Give transport, hotels, itinerary, cost, and also list street food & cheap vendors. Make it futuristic scientist style."

            models = ["openai/gpt-oss-20b","llama-3.3-70b-versatile","llama-3.1-8b-instant","meta-llama/llama-4-maverick-17b-128e-instruct"]
            for model_name in models:
                try:
                    res = client.chat.completions.create(model=model_name, messages=[{"role":"user","content":prompt}], max_tokens=3000)
                    st.balloons()
                    st.success(f"PLAN DECODED | Model: {model_name}")
                    st.session_state.trip_context = res.choices[0].message.content
                    st.markdown(f'<div class="glass">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
                    with st.expander("🛰️ RAW TELEMETRY (Live Search + Vendors)"):
                        st.write(live_info)
                        st.write(vendor_info)
                    break
                except Exception as e:
                    continue

with tab2:
    st.markdown("### 🤖 CHARIOT AI - Street Food & Vendor Intelligence")
    st.caption("Ye chatbot tere trip context + GPS location se batayega - 'Yahan 100m pe best chai kahan milegi?'")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if q := st.chat_input("Pucho: Goa me best cheap fish thali kahan milegi?"):
        st.session_state.chat_history.append({"role":"user","content":q})
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            client = Groq(api_key=GROQ_KEY)
            context_prompt = f"You are CHARIOT vendor guide. Trip context: {st.session_state.trip_context}. User location query: {lat_input}. User asks: {q}. Answer in Hinglish, short, with exact street food names, price range, and GPS tip. Be friendly scientist assistant."
            try:
                res = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"user","content":context_prompt}], max_tokens=800)
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.chat_history.append({"role":"assistant","content":ans})
            except Exception as e:
                st.error(f"Bot error: {e}")