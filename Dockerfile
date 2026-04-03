# Use a Python image that is stable but lightweight
FROM python:3.10-slim

# Install FFmpeg (Essential for Whisper to process audio)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Streamlit port
EXPOSE 8501

# Run the app and allow it to be seen outside the container
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]