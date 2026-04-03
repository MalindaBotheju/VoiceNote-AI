# 🎙️ VoiceNote AI: Local Summarizer

VoiceNote AI is a completely free, privacy-first, local web application that transcribes audio and video files and generates concise bullet-point summaries. 

It leverages **OpenAI's Whisper** for highly accurate speech-to-text and **Meta's Llama 3** (via Ollama) for intelligent summarization. Designed with a "Lean Docker" architecture, it ensures stability by running the app logic in a lightweight container while offloading heavy AI processing to the host machine.

## ✨ Features
* **100% Local & Private:** No data is sent to the cloud. Everything runs on your hardware.
* **Multi-Format Support:** Upload `.mp3`, `.wav`, `.m4a`, and `.mp4` files.
* **High-Accuracy Transcription:** Powered by Whisper (Base model).
* **Smart Summarization:** Extracts key points using Llama 3.
* **Lean Docker Setup:** Prevents "Out of Memory" crashes by keeping the Docker container small and connecting to the host machine's AI models.

## 📸 Screenshots

![VoiceNote AI Dashboard](dashboard.png)
*The clean, user-friendly Streamlit interface.*

![Transcription and Summary](dashboard1.png)
*Real-time transcription and Llama 3 generated bullet-point summaries.*

---

## 🛠️ Tech Stack
* **Frontend/Backend:** Python 3.10, Streamlit
* **Audio Processing:** FFmpeg, OpenAI Whisper
* **LLM Engine:** Ollama, Llama 3
* **Containerization:** Docker

---

## 🚀 Step-by-Step Local Setup & Run Instructions

Follow these instructions to get VoiceNote AI running on your local Windows machine.

### Step 1: Prerequisites
Before running the project, ensure you have the following installed on your Windows computer:
1. **Docker Desktop:** Installed and running (the whale icon in your taskbar should be green).
2. **Ollama:** Download and install the Windows app from [ollama.com](https://ollama.com/).

### Step 2: Prepare the AI Model
Open your Windows terminal (PowerShell or Command Prompt) and pull the Llama 3 model into your local Ollama instance:
```powershell
ollama run llama3

(Once it downloads and starts, you can type /bye to exit. Ollama will keep running in the background).

### Step 3: Set Up Your Project Files
Ensure your project directory contains the following files:

    app.py (The Streamlit application code)
    requirements.txt (Python dependencies: streamlit, openai-whisper, ollama)
    Dockerfile (The instructions to build the lightweight Python image)
    .dockerignore (Crucial: Must include venv/, __pycache__/, and media extensions like *.mp3, *.mp4 to keep the build fast and small)

### Step 4: Build the Docker Image
Open your terminal inside the VoiceNote-AI project folder and build the container image.
```PowerShell
   docker build -t voicenote-app .

Note: This will download Python and FFmpeg. It may take a few minutes the first time.

### Step 5: Run the App (The "Smart" Way)
Run the container using the following command. This specifically maps the port and tells the Docker container to look for Ollama on your Windows host machine (host.docker.internal), preventing memory crashes.

```PowerShell
docker run -p 8501:8501 -e OLLAMA_BASE_URL=[http://host.docker.internal:11434](http://host.docker.internal:11434) voicenote-app
(Optional: Add -d after run if you want it to run in the background).

### Step 6: Use the App!
Open your web browser.

Navigate to: http://localhost:8501

Upload an audio or video file, click "Transcribe & Summarize", and enjoy!

Note on first run: Whisper will automatically download its base model (~139MB) the first time you transcribe a file. Subsequent runs will be much faster.