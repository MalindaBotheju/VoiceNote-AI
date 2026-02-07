import streamlit as st
import whisper
import ollama
import os

st.set_page_config(page_title="VoiceNote AI", page_icon="🎙️")

st.title("🎙️ VoiceNote AI: Local Summarizer")
st.markdown("Upload an audio file (MP3, WAV) to generate a transcript and summary.")

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
audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    # Save file temporarily because Whisper needs a file path
    temp_filename = "temp_audio.mp3"
    with open(temp_filename, "wb") as f:
        f.write(audio_file.getbuffer())
    
    st.audio(audio_file, format="audio/mp3")

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
                    
                    # Call local Ollama
                    response = ollama.chat(model='llama3', messages=[
                        {'role': 'user', 'content': prompt},
                    ])
                    
                    summary = response['message']['content']
                    st.success("Summary Ready!")
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"Summarization failed: {e}")

    # Cleanup temp file
    # os.remove(temp_filename)