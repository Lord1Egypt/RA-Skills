# ClawhHub Publication Package
# telegram-voice-transcribe

## Campos para el formulario de ClawhHub

---

### Name (nombre)
```
telegram-voice-transcribe
```

### Tagline (descripción corta, 1 línea)
```
Transcribe voice notes from Telegram into text using local Whisper AI — free, private, no API cost.
```

### Description (descripción larga)
```
Send voice messages to your OpenClaw agent on Telegram and get instant transcriptions — 
completely free, running locally on your server with no API costs.

When you send a voice note, the agent automatically detects it, runs OpenAI Whisper locally, 
and responds to the content as if you had typed the message.

✅ 100% free — no OpenAI API key needed in local mode
✅ Private — audio never leaves your server
✅ Multilingual — Whisper supports 99 languages
✅ Flexible — also supports OpenAI Whisper API mode ($0.006/min) for ultra-low latency
✅ Auto-fallback — downloads static ffmpeg if not installed on the system

Tested on Ubuntu 22.04 with Python 3.10. Works with Telegram voice notes (.ogg format).
```

### Category
```
Messaging
```

### Tags
```
telegram, voice, transcription, whisper, speech-to-text, audio, stt, free
```

### Version
```
1.3.0
```

### Homepage / Repo
```
(dejar vacío o poner el repo de GitHub si lo creas)
```

### Requirements (lo que necesita el usuario)
```
- Python 3.9+
- pip install openai-whisper static-ffmpeg
- ~500MB de disco para el modelo small
- Optional: OPENAI_API_KEY si quieres usar modo API en vez de local
```

---

## README completo (para la página del skill)

# 🎙️ telegram-voice-transcribe

Transcribe Telegram voice messages into text using **local Whisper AI** — free, private, no API costs.

## What it does

1. You send a voice note on Telegram mentioning your agent
2. The agent detects `<media:audio>` in the incoming message
3. Reads the `.ogg` file from `~/.openclaw/media/inbound/` (auto-downloaded by OpenClaw)
4. Runs Whisper locally and gets the transcript
5. Responds to the content as if you had typed it

## Installation

```bash
pip3 install openai-whisper static-ffmpeg
```

First run downloads the Whisper model (~461MB for `small`). Cached after that.

## Usage (agent workflow)

When you see `<media:audio>` in an incoming message:

```bash
# Get the newest audio file
AUDIO=$(ls -t ~/.openclaw/media/inbound/*.ogg | head -1)

# Transcribe it
python3 ~/.openclaw/skills/telegram-voice-transcribe/scripts/transcribe.py \
  --file "$AUDIO" --local --model small --language es
```

Output:
```json
{"transcript": "hola necesito un cambio en el juego", "language": "es", "duration_s": 3.1}
```

## Models

| Model | Size | Speed (CPU) | Accuracy |
|-------|------|-------------|----------|
| `tiny` | 74MB | ~1s | Basic |
| `base` | 139MB | ~2s | Good |
| `small` | 461MB | ~5s | **Recommended** ✅ |
| `medium` | 1.5GB | ~15s | Excellent |

## API mode (optional)

If you prefer zero local compute:

```bash
export OPENAI_API_KEY=sk-...
python3 transcribe.py --file audio.ogg --language es
# Cost: ~$0.001 per 10-second voice note
```

## Languages

Pass `--language es` for Spanish, `--language en` for English, etc.  
Omit for auto-detection (slightly slower).

---

## Screenshots / demo para subir

(Capturas que deberías hacer tú en Telegram antes de subir)

1. **Screenshot 1** — Tú mandando un voice note al bot en Telegram
2. **Screenshot 2** — El bot respondiendo con la transcripción correcta
3. **Screenshot 3** — Terminal mostrando el JSON de salida del script

---

## Checklist antes de publicar

- [ ] Crear cuenta en clawhub.ai
- [ ] Subir el fichero: `skills/dist/telegram-voice-transcribe.skill`
- [ ] Rellenar los campos de arriba
- [ ] Subir 1-3 screenshots
- [ ] Publicar 🚀
