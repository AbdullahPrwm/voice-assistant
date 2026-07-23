# 🎙️ Voice Assistant - Speech-to-Speech AI Assistant

A Python application that creates a voice-to-voice AI assistant using state-of-the-art technologies.

## 🚀 Features
- **Speech-to-Text:** Uses OpenAI's Whisper to convert speech to text
- **Intelligent Responses:** Uses Cohere's LLM to generate smart, contextual replies
- **Short & Concise:** Responses are limited to 15 words for quick interaction
- **Text-to-Speech:** Uses gTTS to convert responses to natural-sounding speech
- **Voice Commands:** Say "stop", "goodbye", "bye", "exit", "quit", or "stop assistant" to end the session

## 🛠️ Technologies Used
- **Whisper** - Speech recognition
- **Cohere** - Language model for generating responses
- **gTTS** - Text-to-speech conversion
- **SoundDevice** - Audio recording
- **Playsound** - Audio playback

## 📋 Prerequisites
- Python 3.8 or higher
- FFmpeg (for audio processing)
- Cohere API key

## ⚙️ Installation

### 1. Clone the repository
``bash
git clone https://github.com/AbdullahPrwm/voice-assistant
- cd voice-assistant

## 2. Create a virtual environment
- python -m venv venv
- source venv/bin/activate  # On Windows: venv\Scripts\activate

## 3. Install dependencies
pip install -r requirements.txt

## 4. Install FFmpeg
Windows: Download from https://ffmpeg.org/ and add to PATH

## 5. Get Cohere API Key
- Sign up at Cohere Dashboard
- Create a new API key
- Replace YOUR_COHERE_API_KEY in main.py with your key

## 6. 🚀 Running the Application
python main.py


## 🎯 How to Use
- Speak clearly for 5 seconds when prompted
- Wait for the assistant to process and respond
- The assistant will reply with a short, concise response
- Say "stop", "goodbye", or "exit" to end the session
