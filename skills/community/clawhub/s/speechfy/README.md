# Speechify TTS — Multi-Provider Text-to-Speech

> Generates `.ogg` (Opus) audio from text using **Speechify API** (primary)
> with automatic fallback to **Edge TTS** (Microsoft). Ready for voice
> messages on Telegram and other messaging platforms.

## Quick Start

```bash
# 1. Install dependencies
pip install edge-tts       # for fallback (optional)
sudo apt install ffmpeg    # for audio conversion

# 2. Set your API key
export SPEECHIFY_API_KEY="sk_..."

# 3. Generate speech
python3 scripts/speechfy-tts.py "Hello, how are you?" /tmp/hello.ogg

# 4. Send as voice message (Telegram)
# Include MEDIA:/tmp/hello.ogg in your response
```

## Architecture

```
┌─────────────┐     ┌───────────────────┐     ┌──────────────┐
│   Text      │────▶│  Speechify API    │────▶│  .mp3 base64 │
│   (CLI)     │     │  (primary)        │     │   ↓ decode   │
└─────────────┘     └───────────────────┘     │   ffmpeg     │
       │                                       │   .ogg       │
       │ (if fails)                            └──────────────┘
       ▼
┌─────────────┐     ┌───────────────────┐
│  Edge TTS   │────▶│  .ogg (Opus)      │
│  (fallback) │     └───────────────────┘
└─────────────┘
```

**Speechify fails when:**
- No API key configured
- Monthly quota exceeded (HTTP 402)
- Rate limited (HTTP 429)
- Network timeout

In all cases → automatic fallback to Edge TTS.

## Features

- ✨ **Dual provider** — Speechify for quality, Edge TTS for unlimited fallback
- 🎭 **SSML support** — emotions, pitch, rate, pauses, emphasis
- 🌍 **Multi-language** — pt-BR by default, configurable
- 🗣️ **10+ voices** — Cristiane (default), Bruno, Adriana, and more
- 🎵 **Opus output** — native Telegram voice bubble format
- 🔌 **Zero hardcoded config** — all via env vars
- 📦 **Python stdlib** — no external HTTP dependencies

## Prerequisites

| Tool | Required | Purpose |
|------|----------|---------|
| Python 3.10+ | ✅ | Runtime |
| ffmpeg (libopus) | ✅ | MP3 → Opus conversion |
| edge-tts (PyPI) | For fallback | Microsoft Edge TTS |
| vault-resolver | Optional | Vaultwarden integration |

## Configuration

All via environment variables. Copy `.env.example` to `.env` and fill in.

| Variable | Default | Description |
|----------|---------|-------------|
| `SPEECHIFY_API_KEY` | — | Speechify API key (`sk_...`) |
| `SPEECHIFY_VOICE` | `cristiane` | Voice ID |
| `SPEECHIFY_MODEL` | `simba-multilingual` | TTS model |
| `SPEECHIFY_LANG` | `pt-BR` | Language code |
| `EDGE_TTS_VOICE` | `pt-BR-FranciscaNeural` | Edge TTS voice |
| `EDGE_TTS_CMD` | `edge-tts` | Edge TTS CLI command |
| `SPEECHIFY_OUTPUT` | `/tmp/speech-output.ogg` | Default output path |
| `SPEECHIFY_VAULT_ITEM` | `speechfy_key` | Vaultwarden item name |
| `VAULT_RESOLVER` | `vault-resolver` | Vault path |

**Key resolution:** `SPEECHIFY_API_KEY` env var → vault-resolver → empty (skip).

## Usage

### Basic CLI

```bash
# Simple text
python3 scripts/speechfy-tts.py "Hello, how are you?"

# Custom output
python3 scripts/speechfy-tts.py "Text here" /tmp/output.ogg

# Custom voice
SPEECHIFY_VOICE=bruno python3 scripts/speechfy-tts.py "Voice test"

# Force fallback (simulate no API key)
SPEECHIFY_API_KEY="" python3 scripts/speechfy-tts.py "Edge TTS only"
```

### SSML (Speech Synthesis Markup Language)

```bash
# Emotion
python3 scripts/speechfy-tts.py \
  '<speak><speechify:style emotion="cheerful">Great news!</speechify:style></speak>'

# Pitch + rate
python3 scripts/speechfy-tts.py \
  '<speak><prosody pitch="+5%" rate="fast">Excited speech!</prosody></speak>'

# Combined
python3 scripts/speechfy-tts.py \
  '<speak><speechify:style emotion="cheerful">Great!</speechify:style><break time="300ms"/>Now <emphasis level="strong">this</emphasis> is important.</speak>'
```

See `examples/` for complete SSML recipes.

### Programmatic (Python)

```python
import subprocess

def speak(text, output="/tmp/speech.ogg"):
    subprocess.run(
        ["python3", "scripts/speechfy-tts.py", text, output],
        check=True, timeout=60
    )
    return output
```

### Telegram Voice Messages

Include the `.ogg` path with `MEDIA:` prefix:

```
MEDIA:/tmp/speech-output.ogg
```

Opus `.ogg` is the native Telegram voice bubble format — no conversion needed.

## Plans and Limits

| Tier | Speechify | Edge TTS |
|------|-----------|----------|
| **Free** | 50K chars/month (hard cap) | ✅ Unlimited |
| **Starter** ($10/mo) | 1M chars, overage $10/1M | ✅ Unlimited |
| **Pro** ($99/mo) | 3M chars, overage $8/1M | ✅ Unlimited |

Edge TTS is **free and unlimited** — always works as fallback.

## Project Structure

```
speechfy-tts/
├── README.md                  ← This file
├── SKILL.md                   ← Hermes/OpenClaw skill definition
├── .gitignore
├── .env.example               ← Credentials template
├── scripts/
│   └── speechfy-tts.py        ← Main TTS script (Python stdlib)
├── examples/
│   ├── usage-basic.sh         ← Basic usage examples
│   ├── ssml-emotions.sh       ← SSML emotion examples
│   └── ssml-pitch-rate.sh     ← SSML pitch/rate examples
├── references/
│   └── voices.md              ← Available voices table
└── docs/
    └── diagrama.svg           ← Architecture diagram
```

## Multi-platform

### Hermes Agent

Use via `terminal()` or `execute_code()`:

```python
terminal(f"python3 scripts/speechfy-tts.py {shlex.quote(text)} /tmp/out.ogg")
```

### OpenClaw

```bash
# Direct
python3 scripts/speechfy-tts.py "Hello" /tmp/out.ogg

# With mcporter (if Speechify MCP server configured)
mcporter call speechify.synthesize text="Hello"
```

## Troubleshooting

See the full list in `SKILL.md` or `examples/`.

## References

- [Speechify API Docs](https://docs.sws.speechify.com/)
- [Edge TTS (GitHub)](https://github.com/rany2/edge-tts)
- [SSML W3C Spec](https://www.w3.org/TR/speech-synthesis11/)
- `references/voices.md` — Complete voice table
