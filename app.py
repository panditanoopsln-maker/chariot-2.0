import streamlit as st
import os
from groq import Groq
from ddgs import DDGS

# Secret loading - 100% fixed
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    GROQ_KEY = GROQ_KEY.strip() # space hatane ke liye
except:
    GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    st.error("GROQ_API_KEY not found! Go to Manage app -> Settings -> Secrets me key daalo.")
    st.stop()

st.set_page_config(page_title="CHARIOT 2.0", page_icon="🏹", layout="wide")

st.markdown("""
<style>
@keyframes fly { 0% { left: -10%; } 100% { left: 110%; } }
@keyframes run { 0% { left: -40%; } 100% { left: 110%; } }
.sky { background: linear-gradient(to right, #87CEEB, #E0F6FF); height: 65px; position: relative; overflow: hidden; border-radius: 12px; }
.plane { position: absolute; font-size: 35px; animation: fly 6s linear infinite; top: 10px; }
.track { background: #f5f5f5; height: 55px; position: relative; overflow: hidden; border-radius: 12px; border-bottom: 5px solid #444; margin-top: 8px; }
.road { background: #34495e; height: 55px; position: relative; overflow: hidden; border-radius: 12px; border-bottom: 5px dashed white; margin-top: 8px; }
.train { position: absolute; font-size: 30px; animation: run 8s linear infinite; top: 6px; }
.bus { position: absolute; font-size: 30px; animation: run 5s linear infinite; top: 6px; }
.title { text-align:center; font-size:50px; font-weight:900; color:#FF5500; margin-top:10px; }
</style>
<div class="sky"><div class="plane">✈️</div></div>
<div class="track"><div class="train">🚃🚃🚃🚃🚂</div></div>
<div class="road"><div class="bus">🚌💨</div></div>
<div class="title">CHARIOT 2.0</div>
<p style="text-align:center; color:grey;">Your Rath for Every Journey - LIVE Search Enabled</p>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
with c1: source = st.text_input("Source", "Lucknow")
with c2: destination = st.text_input("Destination", "Goa")
with c3: days = st.number_input("Days", 1, 30, 3)
with c4: budget = st.selectbox("Budget", ["Cheap", "Medium", "Luxury"])

if st.button("🚀 Search Live Plan", use_container_width=True, type="primary"):
    client = Groq(api_key=GROQ_KEY)
    with st.spinner("Fetching LIVE data from internet..."):
        live_info = ""
        try:
            with DDGS() as ddgs:
                q = f"{source} to {destination} flight train bus price hotels {budget}"
                results = list(ddgs.text(q, max_results=5))
                live_info = "\n".join([r['body'] for r in results])
        except:
            live_info = "Live search temporarily unavailable, use general knowledge"

        prompt = f"Create detailed travel plan from {source} to {destination} for {days} days, budget {budget}. Use live info: {live_info}. Give transport, hotels, itinerary, cost."

        models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]

        success = False
        for model_name in models:
            try:
                res = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role":"user","content":prompt}],
                    max_tokens=2500
                )
                st.balloons()
                st.success(f"Plan Ready! (Model: {model_name}) | {source} -> {destination}")
                st.markdown(res.choices[0].message.content)
                with st.expander("View Live Search Data"):
                    st.write(live_info)
                success = True
                break
            except Exception as e:
                st.write(f"Trying next model... {e}")
                continue

        if not success:
            st.error("All models failed. Check GROQ_API_KEY in Secrets")