import os
import whisper
import cohere
import sounddevice as sd
from scipy.io.wavfile import write
from gtts import gTTS
import playsound
import tempfile
import time
import warnings
import re  # Add this for better text processing

# Suppress FP16 warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# ============================================
# 🔑 Put your Cohere API key here
# ============================================
COHERE_API_KEY = "cohere_6gW4TQIbMPFYv3ORSCfYGaB6xFnToQabC5a37hbT1TnhE8"  # Replace with your actual key

# Initialize Cohere
co = cohere.Client(COHERE_API_KEY)

# ============================================
# 📥 Load Whisper model
# ============================================
print("🔄 Loading Whisper model... (may take a minute)")
whisper_model = whisper.load_model("base")  # Use "tiny" for speed
print("✅ Model loaded successfully!")

# Audio settings
SAMPLE_RATE = 16000
DURATION = 6  # Recording duration in seconds

# Extended stop phrases
STOP_PHRASES = [
    "stop", "goodbye", "bye", "exit", "quit", 
    "good bye", "see you", "end", "finish", 
    "stop assistant"
]

# ============================================
# 🎙️ Function 1: Speech-to-Text
# ============================================
def record_and_transcribe():
    """Record audio from microphone and convert to text using Whisper"""
    print("\n🎙️ Recording... Please speak for 6 seconds")
    
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), 
                        samplerate=SAMPLE_RATE, 
                        channels=1, 
                        dtype='int16')
    sd.wait()
    
    temp_audio_path = "temp_audio.wav"
    write(temp_audio_path, SAMPLE_RATE, audio_data)
    
    print("🗣️ Converting speech to text...")
    result = whisper_model.transcribe(temp_audio_path, language="en")
    user_text = result["text"]
    print(f"📝 You said: {user_text}")
    
    os.remove(temp_audio_path)
    return user_text

# ============================================
# 🔍 Function to check if input contains stop command
# ============================================
def contains_stop_command(text):
    """Check if the input text contains any stop phrase"""
    if not text:
        return False
    
    # Convert to lowercase and remove extra spaces
    text_lower = text.strip().lower()
    
    # Remove punctuation
    text_clean = re.sub(r'[^\w\s]', '', text_lower)
    words = text_clean.split()
    
    # Check each word and phrase
    for phrase in STOP_PHRASES:
        if phrase in text_clean:
            return True
        # Also check each word individually
        for word in words:
            if word == phrase:
                return True
            # Check if phrase is part of a word (e.g., "goodbye" in "goodbyefriend")
            if phrase in word:
                return True
    
    return False

# ============================================
# 🧠 Function 2: Generate short response using Cohere
# ============================================
def get_llm_response(prompt):
    """Send text to Cohere to generate a short, concise response"""
    print("🧠 Thinking about a response...")
    try:
        response = co.chat(
            model="command-r-08-2024",
            message=prompt,
            preamble="You are a smart and helpful assistant. Give very short, direct, and concise answers. Maximum 15 words. Be friendly but brief."
        )
        llm_response = response.text
        
        # Ensure response is short (max 20 words)
        words = llm_response.split()
        if len(words) > 20:
            llm_response = " ".join(words[:20]) + "..."
        
        print(f"💬 Assistant's reply: {llm_response}")
        return llm_response
    except Exception as e:
        print(f"❌ Cohere error: {e}")
        return "Sorry, please try again."

# ============================================
# 🔊 Function 3: Text-to-Speech
# ============================================
def text_to_speech(text):
    """Convert text to audio file and play it"""
    print("🔊 Converting text to speech...")
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        temp_audio_path = "temp_speech.mp3"
        tts.save(temp_audio_path)
        playsound.playsound(temp_audio_path)
        time.sleep(0.5)
        os.remove(temp_audio_path)
        print("✅ Audio reply played successfully.")
    except Exception as e:
        print(f"❌ An error occurred while playing audio: {e}")

# ============================================
# 🔄 Main loop with improved stop detection
# ============================================
def main():
    print("\n" + "="*50)
    print("🤖 Hello! I'm your smart voice assistant")
    print("="*50)
    print("💡 Speak for 5 seconds, and I will reply to you")
    print("💡 Say 'stop', 'goodbye', 'bye', 'exit', or 'quit' to stop")
    print("💡 Press Ctrl+C at any time to stop")
    print("="*50 + "\n")
    
    while True:
        try:
            # 1. Record and convert speech to text
            user_input = record_and_transcribe()
            
            # 2. Check for stop command using improved function
            if contains_stop_command(user_input):
                print("👋 Goodbye! See you soon")
                text_to_speech("Goodbye, see you soon")
                break
            
            # 3. Process text and generate response
            if user_input and user_input.strip():
                # Skip if input is too short (probably misheard)
                if len(user_input.strip()) < 2:
                    print("⚠️ I couldn't understand that, please speak clearly.")
                    continue
                    
                assistant_reply = get_llm_response(user_input)
                text_to_speech(assistant_reply)
            else:
                print("⚠️ I couldn't hear you clearly, please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Program stopped by user (Ctrl+C)")
            text_to_speech("Goodbye")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("🔄 Resuming operation...")

# ============================================
# 🚀 Run the program
# ============================================
if __name__ == "__main__":
    main()