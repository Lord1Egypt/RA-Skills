"""
Telegram Voice Bot v2.0
Automatically recognizes voice messages and responds with TTS voice.

Features:
- 🎤 Voice message recognition (Whisper)
- 🔊 Voice reply with TTS (edge-tts)
- 🇨🇳 Full Chinese language support

Usage:
    python bot.py
    
Environment variables:
    TELEGRAM_BOT_TOKEN - Your Telegram Bot Token (get from @BotFather)
    VOICE_REPLY - Set to "true" to enable voice reply (default: true)
"""
import os
import time
import asyncio
import requests
import whisper
import tempfile
import uuid
import edge_tts
from pathlib import Path

# Configuration
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
VOICE_REPLY = os.environ.get("VOICE_REPLY", "true").lower() == "true"

# Whisper model options: tiny, base, small, medium, large
MODEL_NAME = "base"

# Default voice for TTS
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"

def load_model():
    """Load Whisper model"""
    print(f"Loading Whisper model: {MODEL_NAME}...")
    model = whisper.load_model(MODEL_NAME)
    print("Model loaded!")
    return model

async def synthesize_speech(text, output_file):
    """Generate speech using edge-tts"""
    try:
        communicate = edge_tts.Communicate(text, DEFAULT_VOICE)
        await communicate.save(output_file)
        return True
    except Exception as e:
        print(f"TTS error: {e}")
        return False

def get_updates(offset=0):
    """Get updates from Telegram"""
    try:
        resp = requests.get(
            f"{BASE_URL}/getUpdates",
            params={"offset": offset, "timeout": 30},
            timeout=35
        )
        return resp.json()
    except Exception as e:
        print(f"Error getting updates: {e}")
        return {"ok": False, "error": str(e)}

def download_file(file_id):
    """Download voice file from Telegram"""
    try:
        resp = requests.get(f"{BASE_URL}/getFile", params={"file_id": file_id}, timeout=10)
        data = resp.json()
        
        if not data.get("ok"):
            return None
        
        file_path = data["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        resp = requests.get(file_url, timeout=30)
        return resp.content
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

def transcribe_audio(audio_data, model):
    """Transcribe audio using Whisper"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as f:
        f.write(audio_data)
        temp_path = f.name
    
    try:
        result = model.transcribe(temp_path, language="zh")
        return result["text"].strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return None
    finally:
        try:
            os.remove(temp_path)
        except:
            pass

def send_message(chat_id, text):
    """Send text message"""
    try:
        requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10
        )
    except Exception as e:
        print(f"Error sending message: {e}")

def send_voice(chat_id, text):
    """Send voice message using TTS"""
    if not VOICE_REPLY:
        send_message(chat_id, text)
        return
    
    # Generate speech
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        temp_path = f.name
    
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(synthesize_speech(text, temp_path))
        
        # Send voice
        with open(temp_path, "rb") as f:
            files = {"voice": ("reply.ogg", f, "audio/ogg")}
            data = {"chat_id": chat_id}
            requests.post(
                f"{BASE_URL}/sendVoice",
                data=data,
                files=files,
                timeout=30
            )
        print(f"Sent voice reply: {text[:30]}...")
    except Exception as e:
        print(f"Error sending voice: {e}")
        send_message(chat_id, text)
    finally:
        try:
            os.remove(temp_path)
        except:
            pass

def process_voice_message(chat_id, file_id, model):
    """Process a voice message"""
    print(f"Received voice from {chat_id}")
    
    # Download and transcribe
    audio_data = download_file(file_id)
    if not audio_data:
        send_message(chat_id, "Sorry, couldn't download the voice file.")
        return
    
    text = transcribe_audio(audio_data, model)
    if text:
        print(f"Transcribed: {text}")
        # Reply with voice
        reply = f"你说了：{text}"
        send_voice(chat_id, reply)
    else:
        send_message(chat_id, "Sorry, couldn't recognize the voice.")

def main():
    """Main loop"""
    global model
    
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set!")
        print("Set: export TELEGRAM_BOT_TOKEN='your_token'")
        return
    
    # Test API
    try:
        resp = requests.get(f"{BASE_URL}/getMe", timeout=10)
        if not resp.json().get("ok"):
            print("Error: Invalid bot token!")
            return
        print(f"Bot connected: @{resp.json()['result']['username']}")
    except Exception as e:
        print(f"Error connecting to Telegram: {e}")
        return
    
    # Load model
    model = load_model()
    
    print(f"Voice reply: {'enabled' if VOICE_REPLY else 'disabled'}")
    print("Bot started! Waiting for voice messages...")
    
    offset = 0
    while True:
        try:
            updates = get_updates(offset)
            
            if updates.get("ok"):
                for update in updates.get("result", []):
                    offset = update["update_id"] + 1
                    message = update.get("message", {})
                    voice = message.get("voice")
                    
                    if voice:
                        chat_id = message["chat"]["id"]
                        file_id = voice["file_id"]
                        process_voice_message(chat_id, file_id, model)
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\nBot stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    model = None
    main()
