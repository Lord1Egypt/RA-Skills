---
name: whisper-piper-voice
description: Set up and run a local voice pipeline combining Whisper STT (speech-to-text) and Piper TTS (text-to-speech) as a single HTTP server. Use when asked to set up voice capabilities, transcribe audio, generate speech, configure STT/TTS, or build a voice assistant pipeline. Handles both directions — audio-to-text and text-to-audio — on a single port. Runs fully offline on CPU or GPU (NVIDIA CUDA). NOT for cloud-based TTS (ElevenLabs, Google TTS) — this is 100% local and free.
---

# Whisper + Piper Voice Pipeline

Local STT (speech-to-text) and TTS (text-to-speech) as a single HTTP server. Zero cloud dependencies.

## Architecture

```
Audio In → POST /transcribe → Whisper (faster-whisper) → JSON {text, language}
Text In  → POST /speak       → Piper TTS → ffmpeg → audio/ogg (Opus)
```

Both endpoints run in one Python process on one port (default: 9998).

## Quick Start

1. Install dependencies:
```bash
python3 -m venv ~/whisper-env && source ~/whisper-env/bin/activate
pip install faster-whisper
apt install ffmpeg  # or brew install ffmpeg on macOS
```

2. Download Piper + a voice:
```bash
mkdir -p ~/piper && cd ~/piper
wget https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz
tar xzf piper_linux_x86_64.tar.gz
mkdir voices && cd voices
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten_emotional/medium/de_DE-thorsten_emotional-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten_emotional/medium/de_DE-thorsten_emotional-medium.onnx.json
```

3. Run the server (`scripts/voice-server.py`):
```bash
python3 voice-server.py --port 9998 \
  --whisper-model small --whisper-device cpu \
  --piper-bin ~/piper/piper/piper \
  --piper-model ~/piper/voices/de_DE-thorsten_emotional-medium.onnx
```

## API

**Transcribe** (audio → text):
```bash
curl -X POST -F "file=@message.ogg" http://HOST:9998/transcribe
# {"text": "Hallo Welt", "language": "de"}
```

**Speak** (text → audio):
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text": "Hallo Welt", "speaker": "4"}' \
  http://HOST:9998/speak -o response.ogg
```

## Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | 9998 | Server port |
| `--whisper-model` | small | tiny/base/small/medium/large-v3 |
| `--whisper-device` | cpu | cpu or cuda |
| `--piper-bin` | (required) | Path to piper binary |
| `--piper-model` | (required) | Path to .onnx voice file |
| `--piper-speaker` | 4 | Speaker ID (multi-speaker models) |
| `--speed` | 0.9 | TTS speed (lower = faster) |

## Choosing Models

**Whisper:** `small` for CPU (good balance), `medium` for GPU (best quality without large-v3 overhead).

**Piper voices:** Browse https://rhasspy.github.io/piper-samples/ — download .onnx + .onnx.json files.

## Full Setup Guide

Read `references/setup-guide.md` for systemd service config, all voice options, model comparison table, and OpenClaw integration details.
