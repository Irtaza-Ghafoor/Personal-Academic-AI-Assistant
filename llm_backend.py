import os
import streamlit as st

LOCAL_MODEL = "qwen3:1.7b"
CLOUD_MODEL = "llama-3.1-8b-instant"
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


def get_active_engine_info() -> tuple[str, str]:
    """Returns (model_name, runtime_label) based on environment."""
    if is_local_ollama_available():
        return LOCAL_MODEL, "Ollama (100% Local)"
    return CLOUD_MODEL, "Groq Cloud API (Live Demo)"


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
    completion = client.chat.completions.create(
        model=CLOUD_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.6
    )
    return completion.choices[0].message.content.strip()