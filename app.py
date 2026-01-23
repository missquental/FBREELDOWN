import streamlit as st
import requests
import json
import os

# =========================
# KONFIG FILE API KEY
# =========================
API_KEY_FILE = "api_key.json"

def load_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            return json.load(f).get("api_key", "")
    return ""

def save_api_key(key):
    with open(API_KEY_FILE, "w") as f:
        json.dump({"api_key": key}, f)

# =========================
# STREAMLIT CONFIG
# =========================
st.set_page_config(
    page_title="Text → Video Generator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Text → Video Generator")

# =========================
# API KEY INPUT (SAVED)
# =========================
saved_api_key = load_api_key()

api_key = st.text_input(
    "API Key",
    type="password",
    value=saved_api_key,
    placeholder="Masukkan API Key sekali saja"
)

if st.button("💾 Simpan API Key"):
    if api_key:
        save_api_key(api_key)
        st.success("✅ API Key berhasil disimpan")
    else:
        st.warning("⚠️ API Key kosong")

st.divider()

# =========================
# INPUT PROMPT
# =========================
prompt = st.text_area(
    "Prompt Video",
    height=150,
    placeholder="Describe your video scene..."
)

aspect_ratio = st.selectbox(
    "Aspect Ratio",
    ["2:3", "16:9", "1:1"]
)

mode = st.selectbox(
    "Mode",
    ["normal", "fast"]
)

callback_url = st.text_input(
    "Callback URL",
    value="https://fbreeldown.streamlit.app/api/callback"
)

# =========================
# GENERATE
# =========================
if st.button("🚀 Generate Video", use_container_width=True):
    if not api_key or not prompt:
        st.warning("⚠️ API Key & Prompt wajib diisi")
    else:
        with st.spinner("Mengirim task ke API..."):
            url = "https://api.kie.ai/api/v1/jobs/createTask"

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": "grok-imagine/text-to-video",
                "callBackUrl": callback_url,
                "input": {
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio,
                    "mode": mode
                }
            }

            try:
                res = requests.post(url, headers=headers, json=payload, timeout=60)

                if res.status_code == 200:
                    st.success("✅ Task berhasil dibuat")
                    st.json(res.json())
                else:
                    st.error(f"❌ Error {res.status_code}")
                    st.text(res.text)

            except Exception as e:
                st.exception(e)
