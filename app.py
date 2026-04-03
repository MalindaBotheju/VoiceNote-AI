import streamlit as st
import whisper
import ollama
import os

st.set_page_config(page_title="VoiceNote AI", page_icon="🎙️")

st.title("🎙️ VoiceNote AI: Local Summarizer")
st.markdown("Upload an audio or video file (MP3, WAV, M4A, MP4) to generate a transcript and summary.")

# --- NEW: Configure the Ollama Client for Docker ---
# This looks for the Docker environment variable, but falls back to localhost if you run it normally
ollama_host = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ollama_client = ollama.Client(host=ollama_host)
# ---------------------------------------------------

# 1. Load Whisper Model (Cached so it doesn't reload every time)
@st.cache_resource
def load_model():
    print("Downloading/Loading Whisper model...")
    return whisper.load_model("base")

try:
    with st.spinner("Loading AI Models... (First time might take a minute)"):
        model = load_model()
    st.success("AI System Ready!")
except Exception as e:
    st.error(f"Error loading models: {e}")

# 2. File Uploader
audio_file = st.file_uploader("Upload Audio or Video", type=["mp3", "wav", "m4a", "mp4"], label_visibility="collapsed")

if audio_file is not None:
    # Get the actual file extension (e.g., .mp4, .mp3)
    file_extension = os.path.splitext(audio_file.name)[1]
    temp_filename = f"temp_media{file_extension}"
    
    # Save file temporarily
    with open(temp_filename, "wb") as f:
        f.write(audio_file.getbuffer())
    
    # Display the correct media player in the browser
    if file_extension == ".mp4":
        st.video(audio_file)
    else:
        st.audio(audio_file)

    if st.button("Transcribe & Summarize"):
        col1, col2 = st.columns(2)

        # Step A: Transcribe (Speech to Text)
        with col1:
            st.info("👂 Listening & Transcribing...")
            try:
                result = model.transcribe(temp_filename, language="en")
                transcription = result["text"]
                st.success("Transcription Complete!")
                st.text_area("Transcript", transcription, height=300)
            except Exception as e:
                st.error(f"Transcription failed: {e}")
                transcription = None

        # Step B: Summarize (Llama 3)
        with col2:
            if transcription:
                st.info("🧠 Summarizing with Llama 3...")
                try:
                    prompt = f"Please summarize the following text into concise bullet points:\n\n{transcription}"
                    
                    # --- CHANGED: Call the client instead of local Ollama ---
                    response = ollama_client.chat(model='llama3', messages=[
                        {'role': 'user', 'content': prompt},
                    ])
                    # --------------------------------------------------------
                    
                    summary = response['message']['content']
                    st.success("Summary Ready!")
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"Summarization failed: {e}")

    # Cleanup temp file
    if os.path.exists(temp_filename):
        os.remove(temp_filename)