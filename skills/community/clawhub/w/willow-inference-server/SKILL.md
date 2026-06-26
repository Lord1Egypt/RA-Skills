---
name: willow-inference-server
description: Local ASR and TTS inference server. Use when the user wants to transcribe audio to text (ASR) or convert text to speech (TTS). Requires a running Willow Inference Server instance. Supports Whisper for ASR and custom TTS voices.
metadata: {}
---

# Willow Inference Server Skill

Local ASR (speech-to-text) and TTS (text-to-speech) inference server.

## Setup

### 1. Start Willow Inference Server
```bash
git clone https://github.com/toverainc/willow-inference-server.git
cd willow-inference-server
./utils.sh install
./utils.sh gen-cert your-hostname
./utils.sh run
```

Server runs at `https://your-hostname:19000`

### 2. Configure Environment
Set the server URL:
```bash
export WILLOW_BASE_URL="https://your-hostname:19000"
```

Or configure per request (see below).

## ASR (Speech-to-Text)

### Transcribe Audio File
```bash
curl -X POST "${WILLOW_BASE_URL}/api/asr" \
  -F "audio_file=@/path/to/audio.m4a" \
  -F "language=auto"
```

### Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| audio_file | Audio file to transcribe | required |
| language | Language code (en, zh, etc.) or "auto" | auto |
| model | Whisper model (tiny, base, medium, large-v2) | server config |
| task | transcribe or translate | transcribe |

### Supported Formats
- MP3, WAV, M4A, OGG, FLAC, WebM

### Example: Transcribe with curl
```bash
# Basic transcription
curl -X POST "${WILLOW_BASE_URL}/asr" \
  -F "audio_file=@recording.m4a" \
  -F "language=zh"

# With specific model
curl -X POST "${WILLOW_BASE_URL}/asr" \
  -F "audio_file=@meeting.mp3" \
  -F "language=en" \
  -F "model=base"
```

## TTS (Text-to-Speech)

### Convert Text to Speech
```bash
curl -X POST "${WILLOW_BASE_URL}/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice": "af_sarah"}'
```

### Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| text | Text to convert to speech | required |
| voice | Voice ID (see below) | default voice |
| speed | Speech speed (0.5-2.0) | 1.0 |
| volume | Volume (0.0-1.0) | 1.0 |

### Available Voices
Common voices (format: `gender_voicename`):
- `af_sarah` - Sarah (Female)
- `af_bella` - Bella (Female)
- `am_michael` - Michael (Male)
- `am_alex` - Alex (Male)

Check server docs for full list: `${WILLOW_BASE_URL}/api/docs`

### Example: TTS with curl
```bash
# Basic TTS
curl -X POST "${WILLOW_BASE_URL}/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，这是测试"}' \
  -o output.wav

# With custom voice
curl -X POST "${WILLOW_BASE_URL}/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello!", "voice": "am_michael", "speed": 1.2}' \
  -o hello.mp3
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| WILLOW_BASE_URL | Server URL | https://localhost:19000 |

## Workflow Examples

### 1. Record and Transcribe
```bash
# Record audio (macOS)
rec test.wav

# Transcribe
curl -X POST "${WILLOW_BASE_URL}/asr" \
  -F "audio_file=@test.wav" \
  -F "language=auto"
```

### 2. Text to Speech
```bash
# Convert text to speech
curl -X POST "${WILLOW_BASE_URL}/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "今天的任务是学习新技能"}' \
  -o speech.wav
```

### 3. Batch Transcription
```bash
for f in *.m4a; do
  curl -X POST "${WILLOW_BASE_URL}/asr" \
    -F "audio_file=@$f" \
    -F "language=auto" \
    -o "${f%.m4a}.txt"
done
```

## API Documentation
Full API docs available at: `${WILLOW_BASE_URL}/api/docs`

## Notes
- All endpoints require HTTPS (or HTTP if configured)
- Audio files are processed locally on the server
- ASR latency depends on model size and hardware
- TTS voices can be customized with custom voice recordings
