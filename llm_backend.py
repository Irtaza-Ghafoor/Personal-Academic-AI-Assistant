import os
import streamlit as st

LOCAL_MODEL = "qwen3:1.7b"
PREFERRED_CLOUD_MODELS = [
    "llama-3.3-70b-versatile",
    "qwen/qwen3-32b",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
]
CONTEXT_LENGTH = 2048

SYSTEM_PROMPT = (
    "You are a helpful, accurate, and concise personal academic assistant built by Irtaza Ahmed. "
    "Help with Computer Science concepts, coding problems, exam preparation, and study planning. "
    "Always remember previous details shared in the conversation and keep answers clear and well-structured."
)


def _get_groq_api_key() -> str | None:
    """Checks Streamlit secrets first, then environment variables."""
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY")


def is_local_ollama_available() -> bool:
    """Returns True if local Ollama server is reachable."""
    try:
        import ollama
        ollama.list()
        return True
    except Exception:
        return False


@st.cache_data(ttl=3600)
def get_available_cloud_model(api_key: str) -> str:
    """Automatically picks an active chat model from Groq so it never hits NotFoundError."""
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        models = [
            m.id for m in client.models.list().data
            if "whisper" not in m.id.lower() and "guard" not in m.id.lower()
        ]
        for preferred in PREFERRED_CLOUD_MODELS:
            if preferred in models:
                return preferred
        if models:
            return models[0]
    except Exception:
        pass
    return PREFERRED_CLOUD_MODELS[0]


def get_active_engine_info() -> tuple[str, str]:
    """Returns (model_name, runtime_label) based on environment."""
    if is_local_ollama_available():
        return LOCAL_MODEL, "Ollama (100% Local)"
    api_key = _get_groq_api_key()
    cloud_model = get_available_cloud_model(api_key) if api_key else PREFERRED_CLOUD_MODELS[0]
    return cloud_model, "Groq Cloud API (Live Demo)"


def get_assistant_reply(chat_history: list) -> str:
    """
    Uses local Ollama when available on laptop; automatically switches to
    Groq Cloud API when deployed live on Streamlit Community Cloud.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history

    # 1. Try Local Ollama first
    if is_local_ollama_available():
        import ollama
        response = ollama.chat(
            model=LOCAL_MODEL,
            messages=messages,
            options={"num_ctx": CONTEXT_LENGTH},
            think=False
        )
        return response["message"]["content"].strip()

    # 2. Fallback to Groq API for live Streamlit Cloud deployment
    api_key = _get_groq_api_key()
    if not api_key:
        return (
            "⚠️ **Live Demo Setup Needed:** Local Ollama is not running, and `GROQ_API_KEY` "
            "is not configured in Streamlit Cloud Secrets."
        )

    from groq import Groq
    client = Groq(api_key=api_key)
    active_cloud_model = get_available_cloud_model(api_key)
    completion = client.chat.completions.create(
        model=active_cloud_model,
        messages=messages,
        max_tokens=1024,
        temperature=0.6
    )
    return completion.choices[0].message.content.strip()
