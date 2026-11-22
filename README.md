# 🤖 Hybrid Personal Academic AI Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Local_LLM-Ollama_Qwen3-000000?style=for-the-badge)](https://ollama.com)
[![Groq](https://img.shields.io/badge/Cloud_Fallback-Groq_Llama3-F55036?style=for-the-badge)](https://groq.com)

A **hardware-aware, dual-mode Personal Academic AI Assistant** built with a modular Python backend and a custom glassmorphic Streamlit UI. It runs **100% locally offline via Ollama** on consumer CPU hardware and automatically switches to **Groq Cloud API** when deployed live on Streamlit Community Cloud.

🔗 **Live Demo:** [Add Your Streamlit Cloud URL Here]

---

## ✨ Key Features

- **🔄 Dual-Mode Inference Engine:** Automatically detects if a local Ollama server is running (`qwen3:1.7b`); seamlessly falls back to Groq Cloud (`llama-3.1-8b-instant`) in cloud/serverless environments.
- **🧱 Clean Modular Architecture:** Strict separation between LLM inference logic (`llm_backend.py`) and the graphical frontend (`app.py`).
- **📊 Real-Time Telemetry:** Displays live system/container RAM consumption, active model engine, context window (`2048` tokens), and per-response generation latency.
- **🧠 Multi-Turn Context Memory:** Retains session conversation history for context-aware follow-up academic Q&A, coding assistance, and exam prep, with one-click session reset.
- **🎨 Glassmorphic Dark UI:** Custom-styled responsive chat interface built with Streamlit and CSS.

---

## 🏗️ System Architecture

```text
User Input (Streamlit UI - app.py)
       │
       ▼
Backend Router (llm_backend.py)
       ├──► [Local Environment] ──► Ollama Server ──► qwen3:1.7b (100% Offline CPU)
       └──► [Cloud Deployment]  ──► Groq API      ──► llama-3.1-8b-instant (Live Demo)
```

---

## 📈 Hardware Benchmarking & Model Selection

Before selecting `qwen3:1.7b` as the primary local model, empirical benchmarks were conducted on consumer CPU hardware (**Intel Core i7-10610U, 4 Cores / 8 Threads, 16 GB DDR4 RAM, No Dedicated GPU**) at a `2048`-token context window:

| Metric | `qwen3:4b` (Q4_K_M) | `qwen3:1.7b` (Q4_K_M) |
| :--- | :---: | :---: |
| **Model Download Size** | 2.5 GB | 1.4 GB |
| **Execution Mode** | 100% CPU | 100% CPU |
| **Peak System RAM** | 11.80 GB (+2.80 GB) | **9.64 GB (+1.67 GB)** |
| **Avg. Response Time** | 458.32 sec | **12.24 sec (~37x faster)** |
| **Generation Speed** | 4.90 tokens/sec | **14.20 tokens/sec** |
| **Prompt Accuracy** | 5 / 5 | 3 / 5 |

**Takeaway:** While `qwen3:4b` achieved higher raw accuracy, its heavy reasoning overhead caused severe CPU latency. `qwen3:1.7b` delivered ~37x faster responses with a smaller memory footprint, making it optimal for real-time interactive chat.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Irtaza-Ghafoor/hybrid-academic-ai-assistant.git
cd hybrid-academic-ai-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Locally (Offline Mode via Ollama)
Make sure [Ollama](https://ollama.com) is installed and pull the local model:
```bash
ollama pull qwen3:1.7b
streamlit run app.py
```

### 4. Run in Cloud Mode (Groq Fallback)
Set your Groq API key as an environment variable or in `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```
Then launch the app:
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```text
hybrid-academic-ai-assistant/
├── app.py              # Streamlit glassmorphic frontend & session state management
├── llm_backend.py      # Dual-mode inference router (Local Ollama + Groq Cloud API)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation & benchmark insights
```

---

## 👨‍💻 Author

**Irtaza Ahmed**  
AI / ML Engineer & Full-Stack Developer  
- **GitHub:** [@Irtaza-Ghafoor](https://github.com/Irtaza-Ghafoor)
- **LinkedIn:** [Irtaza Ahmad](https://www.linkedin.com/in/irtaza-ahmad-ai/)