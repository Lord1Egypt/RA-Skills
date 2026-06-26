# 🎙️ VoiceClaw — Local Voice I/O for OpenClaw Agents

**ClawHub:** [clawhub.ai/Asif2BD/voiceclaw](https://clawhub.ai/Asif2BD/voiceclaw) · **GitHub:** [github.com/Asif2BD/VoiceClaw](https://github.com/Asif2BD/VoiceClaw)

> Created by **[M Asif Rahman](https://github.com/Asif2BD)** — Founder of [MissionDeck.ai](https://missiondeck.ai) · [xCloud](https://xcloud.host) · [WPDevelopers](https://github.com/WPDevelopers)

A local-only voice skill for [OpenClaw](https://openclaw.ai) agents. Transcribe inbound voice messages with **Whisper** and reply with synthesized speech via **Piper TTS** — no cloud, no API keys, no paid services.

---

## Install

**Option 1 — Via ClawHub** *(if ClawHub is installed)*
```bash
clawhub install voiceclaw
```

**Option 2 — Via Git** *(no ClawHub needed)*
```bash
git clone https://github.com/Asif2BD/VoiceClaw.git ~/.openclaw/custom-skills/voiceclaw
```

**Option 3 — Download release** *(manual, no tools needed)*
```bash
curl -L https://github.com/Asif2BD/VoiceClaw/releases/latest/download/voiceclaw.skill -o voiceclaw.skill
unzip voiceclaw.skill -d ~/.openclaw/custom-skills/voiceclaw
```

> After any install method, restart OpenClaw for the skill to be detected.

---

## Requirements

- `whisper` — whisper.cpp binary ([install guide](https://github.com/ggerganov/whisper.cpp))
- Whisper model: `ggml-base.en.bin` — auto-downloaded on first use, or manually:
  ```bash
  # One-time setup only — not run by the skill scripts
  mkdir -p ~/.cache/whisper
  curl -L -o ~/.cache/whisper/ggml-base.en.bin \
    https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
  ```
  > Set `WHISPER_MODEL=/path/to/ggml-base.en.bin` if your model is stored elsewhere.
- `piper` — TTS binary + `.onnx` voice models ([install guide](https://github.com/rhasspy/piper)). Set `VOICECLAW_VOICES_DIR=/path/to/voices/` to point to your voice models (default: `~/.local/share/piper/voices/`)
- `ffmpeg` — for audio format conversion

---

## What it does

- **Speech-to-Text**: Inbound voice/audio (OGG, MP3, WAV, M4A) → transcript text via Whisper.cpp
- **Text-to-Speech**: Agent text replies → voice audio via Piper TTS (7 English voices)
- **Agent behavior**: When a voice message arrives, the agent automatically responds with both voice + text
- **100% local**: No data sent anywhere — all inference runs on your server

---

## How it works

```
Inbound voice message (OGG/MP3/WAV)
        ↓
  ffmpeg → 16kHz mono WAV
        ↓
  whisper.cpp → transcript text
        ↓
  Agent reads transcript, composes reply
        ↓
  Piper TTS → WAV → OGG Opus
        ↓
  Voice reply + text transcript sent together
```

---

## Usage

```bash
# Transcribe a voice message
bash scripts/transcribe.sh /path/to/voice.ogg

# Generate a voice reply (returns path to WAV)
bash scripts/speak.sh "Your task is complete." /tmp/reply.wav

# Convert WAV → OGG Opus for Telegram
ffmpeg -i /tmp/reply.wav -c:a libopus -b:a 32k /tmp/reply.ogg -y
```

---

## Available Voices

| Voice ID | Style |
|---|---|
| `en_US-lessac-medium` | Neutral American (default) |
| `en_US-amy-medium` | Warm American female |
| `en_US-joe-medium` | American male |
| `en_US-kusal-medium` | Expressive American male |
| `en_US-danny-low` | Deep American male (fast) |
| `en_GB-alba-medium` | British female |
| `en_GB-northern_english_male-medium` | Northern British male |

Voice models live at `/opt/piper/voices/`. See `SKILL.md` for full agent integration instructions.

---

## Security

- **All processing is local** — no audio or text is sent to any cloud service or external API
- **Temp files are cleaned up** — audio is converted in `/tmp` and deleted immediately after transcription (bash `trap` on EXIT)
- **Voice names are sanitized** — input stripped to `[a-zA-Z0-9_-]` only, preventing path traversal
- **No network calls** — neither script makes any network request

---

## Author

**[M Asif Rahman](https://github.com/Asif2BD)**
- 🌐 [asif.im](https://asif.im)
- 🐙 [github.com/Asif2BD](https://github.com/Asif2BD)
- 🔑 [clawhub.ai/Asif2BD](https://clawhub.ai/Asif2BD)

---

## License

MIT © 2026 [M Asif Rahman](https://github.com/Asif2BD)
