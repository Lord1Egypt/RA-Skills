# Voice Pipeline Setup Guide

## Prerequisites

- Linux machine with Python 3.10+
- ffmpeg installed (`apt install ffmpeg`)
- For GPU acceleration: NVIDIA GPU + CUDA (optional, CPU works fine for small/medium models)

## 1. Whisper STT (faster-whisper)

```bash
# Create virtual environment
python3 -m venv ~/whisper-env
source ~/whisper-env/bin/activate

# Install faster-whisper (CPU)
pip install faster-whisper

# Or with CUDA support
pip install faster-whisper[cuda]
```

### Model Sizes

| Model | Size | Speed (CPU) | Speed (GPU) | Quality |
|-------|------|-------------|-------------|---------|
| tiny | 75MB | ~10x realtime | ~30x | Basic |
| base | 142MB | ~7x realtime | ~25x | OK |
| small | 466MB | ~4x realtime | ~15x | Good |
| medium | 1.5GB | ~2x realtime | ~8x | Great |
| large-v3 | 3GB | ~1x realtime | ~5x | Best |

**Recommendation:** `small` for CPU servers, `medium` for GPU servers.

## 2. Piper TTS

```bash
# Download piper binary
mkdir -p ~/piper && cd ~/piper
wget https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz
tar xzf piper_linux_x86_64.tar.gz

# Download a voice (example: German - Thorsten Emotional)
mkdir -p voices && cd voices
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten_emotional/medium/de_DE-thorsten_emotional-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten_emotional/medium/de_DE-thorsten_emotional-medium.onnx.json
```

### Popular Voices

Browse all voices: https://rhasspy.github.io/piper-samples/

**German:**
- `thorsten_emotional` — Multi-speaker (neutral, amused, surprised, whisper)
- `thorsten` — Single speaker, clean

**English:**
- `amy` — British English, clear
- `lessac` — US English, natural
- `libritts_r` — Multi-speaker (904 speakers!)

### Multi-Speaker Models

Thorsten Emotional speakers:
- Speaker 0: amused
- Speaker 4: neutral (recommended default)
- Speaker 6: surprised
- Speaker 7: whisper

Use `--speaker <id>` when calling piper.

## 3. Running the Server

```bash
source ~/whisper-env/bin/activate

python3 voice-server.py \
  --port 9998 \
  --whisper-model small \
  --whisper-device cpu \
  --piper-bin ~/piper/piper/piper \
  --piper-model ~/piper/voices/de_DE-thorsten_emotional-medium.onnx \
  --piper-speaker 4 \
  --speed 0.9
```

## 4. Systemd Service (Auto-Start)

```ini
# /etc/systemd/system/voice-server.service
[Unit]
Description=Whisper STT + Piper TTS Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/home/your-user
ExecStart=/home/your-user/whisper-env/bin/python3 /path/to/voice-server.py \
  --port 9998 \
  --whisper-model small \
  --piper-bin /home/your-user/piper/piper/piper \
  --piper-model /home/your-user/piper/voices/your-voice.onnx
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable voice-server
sudo systemctl start voice-server
```

## 5. API Usage

### Transcribe Audio → Text
```bash
curl -X POST -F "file=@audio.ogg" http://localhost:9998/transcribe
# → {"text": "Hello world", "language": "en"}
```

### Text → Speech (OGG/Opus)
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text": "Hallo Welt", "speaker": "4"}' \
  http://localhost:9998/speak --output speech.ogg
```

## 6. Integration with OpenClaw

For Telegram voice messages, OpenClaw can:
1. Receive voice message (audio/ogg)
2. POST to `/transcribe` → get text
3. Process text with AI
4. POST response to `/speak` → get audio
5. Send audio back as voice message

The server handles both directions in a single process, on a single port.
