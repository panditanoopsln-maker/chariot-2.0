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
        background: linear-gradient(rgba(0,0,0,0.60), rgba(0,0,0,0.75)), url("data:image/jpeg;base64,{bg_data}");
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
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@700&display=swap');

.sky,.track,.road {
    background: rgba(0,0,0,0.55)!important;
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
.train { position: absolute; font-size: 22px!important; animation: run 8s linear infinite; top: 2px; white-space: nowrap; }
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
    letter-spacing:1.5px; margin-bottom:6px;
    text-shadow: 1px 1px 4px black;
}

.hindi-tagline {
    text-align:center;
    font-family:'Noto Sans Devanagari', sans-serif;
    font-size:20px!important;
    font-weight:700;
    color:#FFD700;
    letter-spacing:0.5px;
    margin-bottom:14px;
    text-shadow: 0 0 8px rgba(255,215,0,0.7), 2px 2px 6px black;
}

.glass {
    background: rgba(0,0,0,0.68)!important;
    backdrop-filter: blur(12px)!important;
    border: 1px solid rgba(255,255,255,0.22)!important;
    border-radius: 12px!important;
    padding: 16px!important;
}
.glass p,.glass li,.glass h1,.glass h2,.glass h3,.glass h4 {
    color: #FFFFFF!important;
}
.glass table {
    background: rgba(255,255,255,0.95)!important;
    border-radius: 8px!important;
    width: 100%!important;
    margin: 10px 0!important;
}
.glass th {
    background: #FF9933!important;
    color: #000000!important;
    font-weight: 800!important;
    padding: 10px!important;
}
.glass td {
    background: rgba(255,255,255,0.95)!important;
    color: #000000!important;
    -webkit-text-fill-color: #000000!important;
    font-weight: 700!important;
    border: 1px solid #ddd!important;
    padding: 8px!important;
}

/* ===== CHAT KA FINAL FIX - USER KA QUESTION + BOT KA ANSWER DONO BLACK ===== */
div[data-testid="stChatMessage"] {
    background: #ffffff!important;
    border: 1px solid #FF9933!important;
    border-radius: 12px!important;
}
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] div,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] b {
    color: #000000!important;
    -webkit-text-fill-color: #000000!important;
    opacity: 1!important;
}

@media only screen and (max-width: 768px) {
 .hindi-tagline { font-size:17px!important; }
  input { background: white!important; color: black!important; -webkit-text-fill-color: black!important; }
}
</style>

<div class="sky"><div class="plane">✈️</div></div>
<div class="track"><div class="train">🚃🚃🚃🚃🚃🚃🚃🚃🚂</div></div>
<div class="road"><div class="bus">🚌</div></div>

<div class="tiranga-title">
    <span class="saffron">SAFAR</span><span class="chakra">☸️</span><span class="green">MATE 2.0</span>
</div>
<div class="sub-title">SYSTEM ONLINE • GPS + VENDOR INTELLIGENCE • LIVE SEARCH + WEATHER</div>
<div class="hindi-tagline">SAFARMATE-2.0 आपके सफ़र का साथी</div>
""".replace("BGDATA", bg_data), unsafe_allow_html=True)

# ===== NEW: WEATHER AGENT (Added Only This) =====
def get_weather_agent(place):
    try:
        url = f"https://wttr.in/{place}?format=j1"
        r = requests.get(url, timeout=8).json()
        curr = r['current_condition'][0]
        weather_data = {
            "temp": curr['temp_C'],
            "feels": curr['FeelsLikeC'],
            "desc": curr['weatherDesc'][0]['value'],
            "humidity": curr['humidity'],
            "wind": curr['windspeedKmph']
        }
        return weather_data
    except Exception as e:
        return None

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
        with st.spinner("Fetching LIVE data + WEATHER..."):
            live_info = ""
            try:
                with DDGS() as ddgs:
                    q = f"{source} to {destination} flight train bus price hotels {budget}"
                    results = list(ddgs.text(q, max_results=5))
                    live_info = "\n".join([r['body'] for r in results])
            except:
                live_info = "Live search unavailable"

            dest_weather = get_weather_agent(destination)
            source_weather = get_weather_agent(source)

            weather_text = ""
            if dest_weather:
                st.markdown(f'<div class="glass" style="border-left: 4px solid #FF9933;">🌦️ <b>{destination} Weather:</b> {dest_weather["temp"]}°C, {dest_weather["desc"]}, Humidity: {dest_weather["humidity"]}% | <b>{source} Weather:</b> {source_weather["temp"] if source_weather else "N/A"}°C</div>', unsafe_allow_html=True)
                weather_text = f"Destination {destination} weather is {dest_weather['temp']}C {dest_weather['desc']}. Source {source} weather {source_weather['temp'] if source_weather else ''}C."

            vendor_info = ""
            if lat_input and "," in lat_input:
                try:
                    lat, lon = map(float, lat_input.split(","))
                    overpass_query = f"[out:json];node(around:500,{lat},{lon})[amenity~'fast_food|street_vendor|food_court|restaurant|cafe'];out 10;"
                    r = requests.post("https://overpass-api.de/api/interpreter", data=overpass_query, timeout=10)
                    data = r.json()
                    vendor_info = "\nNearby Vendors:\n" + "\n".join([f"- {e.get('tags',{}).get('name','Unnamed')} ({e.get('tags',{}).get('amenity')})" for e in data.get('elements',[])[:10]])
                except:
                    vendor_info = "Vendor scan failed"

            client = Groq(api_key=GROQ_KEY)
            prompt = f"Create detailed travel plan from {source} to {destination} for {days} days, budget {budget}. Use live info: {live_info}. {vendor_info}. Weather info: {weather_text}. Give transport, hotels, itinerary, cost, and also list street food & cheap vendors. If weather is rainy suggest indoor alternatives."

            models = ["openai/gpt-oss-20b","llama-3.3-70b-versatile","llama-3.1-8b-instant"]
            for model_name in models:
                try:
                    res = client.chat.completions.create(model=model_name, messages=[{"role":"user","content":prompt}], max_tokens=3000)
                    st.balloons()
                    st.success(f"PLAN DECODED | Model: {model_name} | Weather Integrated")
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
            context_prompt = f"You are SAFARMATE vendor guide. Trip context: {st.session_state.trip_context}. Location: {lat_input}. User asks: {q}. Answer in Hinglish. If user asks about weather, use your knowledge."
            try:
                res = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"user","content":context_prompt}], max_tokens=800)
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.chat_history.append({"role":"assistant","content":ans})
            except Exception as e:
                st.error(f"Bot error: {e}")
