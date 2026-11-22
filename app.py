import time
import psutil
import streamlit as st
from llm_backend import CONTEXT_LENGTH, get_active_engine_info, get_assistant_reply

st.set_page_config(
    page_title="Irtaza's Academic AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Detect whether running locally via Ollama or live on Cloud via Groq
ACTIVE_MODEL, RUNTIME_LABEL = get_active_engine_info()

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top right, #161b33 0%, #0b0e17 55%, #07090f 100%);
    color: #f1f5f9;
}
.block-container {
    padding-top: 3.3rem !important;
    padding-bottom: 1rem !important;
    max-width: 1180px;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111629 0%, #0b0e18 100%);
    border-right: 1px solid rgba(139, 92, 246, 0.25);
}
.hero-card {
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.24) 0%, rgba(147, 51, 234, 0.18) 50%, rgba(14, 165, 233, 0.20) 100%);
    border: 1px solid rgba(167, 139, 250, 0.40);
    border-radius: 16px;
    padding: 16px 22px;
    margin-bottom: 14px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    gap: 16px;
}
.hero-title {
    font-size: 1.65rem;
    font-weight: 800;
    background: linear-gradient(90deg, #e0e7ff, #c084fc, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.25;
}
.hero-sub {
    font-size: 0.88rem;
    color: #cbd5e1;
    margin-top: 7px;
}
.badge {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 6px;
    background: rgba(139, 92, 246, 0.22);
    border: 1px solid rgba(167, 139, 250, 0.45);
    color: #e9d5ff;
}
.badge-green {
    background: rgba(16, 185, 129, 0.18);
    border: 1px solid rgba(52, 211, 153, 0.45);
    color: #a7f3d0;
}
div[data-testid="stChatMessage"] {
    background: rgba(22, 28, 48, 0.68);
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 14px;
    padding: 10px 14px;
    margin-bottom: 8px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.22);
}
.side-box {
    background: rgba(30, 41, 59, 0.55);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 12px;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(139, 92, 246, 0.55);
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

mem = psutil.virtual_memory()
used_gb = round((mem.total - mem.available) / (1024 ** 3), 2)
total_gb = round(mem.total / (1024 ** 3), 1)

with st.sidebar:
    st.markdown("### 👨‍💻 Developer Profile")
    st.markdown(
        '<div class="side-box">'
        '<div style="font-size:0.80rem; color:#94a3b8;">BUILT BY</div>'
        '<div style="font-size:1.05rem; font-weight:700; color:#f8fafc; margin-bottom:8px;">Irtaza Ahmed</div>'
        '<div style="font-size:0.82rem; color:#cbd5e1;">AI / ML Engineer & Full-Stack Developer</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### ⚙️ Inference Engine")
    st.markdown(
        f'<div class="side-box">'
        f'<div style="margin-bottom:6px;"><b>Model:</b> <code style="color:#38bdf8;">{ACTIVE_MODEL}</code></div>'
        f'<div style="margin-bottom:6px;"><b>Runtime:</b> {RUNTIME_LABEL}</div>'
        f'<div style="margin-bottom:6px;"><b>Context Window:</b> {CONTEXT_LENGTH} tokens</div>'
        f'<div><b>Container RAM:</b> {used_gb} / {total_gb} GB ({mem.percent}%)</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.progress(min(mem.percent / 100.0, 1.0))

    st.write("")
    if st.button("🗑️ Clear / Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

BOT_LOGO_SVG = (
    '<svg width="54" height="54" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0;">'
    '<defs><linearGradient id="botGrad" x1="10" y1="10" x2="90" y2="90" gradientUnits="userSpaceOnUse">'
    '<stop offset="0%" stop-color="#e0f2fe"/><stop offset="50%" stop-color="#c4b5fd"/><stop offset="100%" stop-color="#bae6fd"/>'
    '</linearGradient></defs>'
    '<path d="M50 14C29 14 14 28 14 46V52C10 53 7 57 7 62C7 67 10 71 14 72C18 82 32 88 50 88C57 88 64 87 70 85L82 91C84 92 86 90 85 88L81 78C84 75 86 73 87 72C91 71 94 67 94 62C94 57 91 53 87 52V46C87 28 71 14 50 14Z" '
    'stroke="url(#botGrad)" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>'
    '<rect x="26" y="38" width="48" height="32" rx="13" stroke="url(#botGrad)" stroke-width="6"/>'
    '<circle cx="41" cy="54" r="4.5" fill="url(#botGrad)"/>'
    '<circle cx="59" cy="54" r="4.5" fill="url(#botGrad)"/>'
    '</svg>'
)

top_left, top_right = st.columns([4.6, 1.2])
with top_left:
    hero_html = (
        f'<div class="hero-card">'
        f'{BOT_LOGO_SVG}'
        f'<div>'
        f'<div class="hero-title">Personal Academic AI Assistant</div>'
        f'<div class="hero-sub">'
        f'<span class="badge">👤 Irtaza Ahmed</span>'
        f'<span class="badge">⚡ Hybrid Local + Cloud AI</span>'
        f'<span class="badge badge-green">🧠 {ACTIVE_MODEL}</span>'
        f'</div></div></div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

with top_right:
    st.write("")
    st.write("")
    if st.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "latency" in msg:
            st.caption(f"⚡ Generated by `{ACTIVE_MODEL}` in **{msg['latency']}s**")

user_prompt = st.chat_input("Ask your personal academic assistant anything...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner(f"Generating response via {ACTIVE_MODEL}..."):
            start_t = time.time()
            api_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            reply = get_assistant_reply(api_history)
            elapsed = round(time.time() - start_t, 2)
            st.markdown(reply)
            st.caption(f"⚡ Generated by `{ACTIVE_MODEL}` in **{elapsed}s**")

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "latency": elapsed
    })