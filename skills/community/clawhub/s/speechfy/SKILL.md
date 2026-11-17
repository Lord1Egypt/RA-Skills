---
name: speechfy-tts
description: "Multi-provider Text-to-Speech: Speechify API (primary) + Edge TTS (fallback). Gera .ogg (Opus) para voice messages."
version: 1.1.0
tags: [tts, speech, speechify, edge-tts, voice, audio]
metadata:
  hermes:
    tags:
      - tts
      - speech
      - speechify
      - voice
    category: messaging
    related_skills: [voice-speech-config]
    requires_toolsets: [terminal]
  openclaw:
    os: [linux, darwin]
    requires:
      bins: [python3, ffmpeg]
      optional_bins: [edge-tts, vault-resolver]
    install:
      pip: null
---

# Speechify TTS

> Multi-provider Text-to-Speech: **Speechify API** (primary, Cristiane voice)
> with automatic **Edge TTS** fallback (FranciscaNeural). Outputs `.ogg` (Opus)
> ready for voice messages.

## ⚡ Quick Start

```bash
# Basic usage
python3 scripts/speechfy-tts.py "Hello, world!" /tmp/hello.ogg

# With custom voice via env
SPEECHIFY_VOICE=bruno python3 scripts/speechfy-tts.py "Texto" /tmp/saida.ogg
```

## Architecture

```
Text (CLI)
    │
    ├── Speechify API ──► .mp3 ──► ffmpeg ──► .ogg (Opus)
    │   (primary)
    │
    └── Edge TTS ──────► .ogg (Opus)
        (fallback)
```

**Speechify fails when:**
- No API key configured (env var or vault missing)
- Monthly quota exceeded (HTTP 402 — `spend_cap_exceeded`)
- Rate limited (HTTP 429)
- Network timeout

## Prerequisites

| Tool | Required | Install |
|------|----------|---------|
| Python 3.10+ | ✅ | System package |
| ffmpeg (libopus) | ✅ | `apt install ffmpeg` / `pacman -S ffmpeg` |
| edge-tts (PyPI) | For fallback | `pip install edge-tts` |
| vault-resolver | Optional | Hermes ecosystem |

## Configuration

All via environment variables (no hardcoded config):

| Variable | Default | Description |
|----------|---------|-------------|
| `SPEECHIFY_API_KEY` | — | Speechify API key (`sk_...`) |
| `SPEECHIFY_VOICE` | `cristiane` | Voice ID (see voices reference) |
| `SPEECHIFY_MODEL` | `simba-multilingual` | TTS model |
| `SPEECHIFY_LANG` | `pt-BR` | Language code |
| `EDGE_TTS_VOICE` | `pt-BR-FranciscaNeural` | Edge TTS voice |
| `EDGE_TTS_CMD` | `edge-tts` | Edge TTS CLI command |
| `SPEECHIFY_OUTPUT` | `/tmp/speech-output.ogg` | Default output path |
| `SPEECHIFY_VAULT_ITEM` | `speechfy_key` | Vaultwarden item name |
| `VAULT_RESOLVER` | `vault-resolver` | Vault resolver path |
| `SPEECHIFY_API_KEY` | — | Overrides vault (highest priority) |

Resolution order: `SPEECHIFY_API_KEY` env var → vault-resolver → empty (skip).

## Usage

### CLI

```bash
# Simple text, default output
python3 scripts/speechfy-tts.py "Hello, how are you?"

# Custom output path
python3 scripts/speechfy-tts.py \
  "Important announcement" /tmp/alert.ogg

# SSML (Speech Synthesis Markup Language)
python3 scripts/speechfy-tts.py \
  '<speak><prosody pitch="+5%">Excited</prosody></speak>'
```

### Voice Messages (Telegram)

Include the `.ogg` path with `MEDIA:` prefix:

```
MEDIA:/tmp/speech-output.ogg
```

`.ogg` with Opus codec is the native voice bubble format on Telegram.

### Programmatic (Python)

```python
import subprocess

def generate_speech(text, output="/tmp/speech.ogg"):
    proc = subprocess.run(
        ["python3", "scripts/speechfy-tts.py", text, output],
        capture_output=True, text=True, timeout=60
    )
    if proc.returncode == 0:
        return output
    raise RuntimeError(f"TTS failed: {proc.stderr}")
```

### Hermes Agent (skill integration)

```python
import subprocess
output = "/tmp/response.ogg"
subprocess.run([
    "python3", "scripts/speechfy-tts.py",
    text, output
], check=True)
```

## SSML Cheat Sheet

Speechify supports SSML via the `input` field. Pass XML as the text argument.

### Emotions (`<speechify:style>`)

```xml
<speak>
  <speechify:style emotion="cheerful">Great news!</speechify:style>
  <break time="300ms"/>
  <speechify:style emotion="calm">Let's analyze calmly.</speechify:style>
</speak>
```

| Emotion | Effect | Typical use |
|---------|--------|-------------|
| `cheerful` | Optimistic, excited | Good news |
| `calm` | Serene, composed | Explanations |
| `bright` | Light, positive | Subtle irony |
| `warm` | Friendly, welcoming | Personal chats |
| `assertive` | Confident, authoritative | Direct instructions |
| `sad` | Melancholic | Sadness |
| `angry` | Intense, irritated | Discontent |
| `surprised` | Astonished | Reactions |
| `energetic` | Dynamic, lively | Excitement |
| `direct` | Straight, no frills | Objective warnings |

### Prosody (pitch, rate, volume)

```xml
<speak>
  Normal tone.
  <prosody pitch="+5%">5% higher pitch</prosody>
  <prosody pitch="-10%" rate="slow">Lower and slower</prosody>
  <prosody pitch="high" rate="fast">High and fast</prosody>
</speak>
```

**Pitch:** percentage (`-83%` to `+100%`) or levels (`x-low` to `x-high`)
**Rate:** percentage or levels (`x-slow` to `x-fast`)

### Pauses and Emphasis

```xml
<speak>
  This is <emphasis level="strong">very</emphasis> important.
  <break time="500ms"/>
  And now <emphasis level="moderate">this</emphasis>.
</speak>
```

### SSML Limitations

- ⚠️ **Input limit:** 2,000 chars on `/v1/audio/speech` (including SSML tags)
- ⚠️ For longer text: use streaming `/v1/audio/stream` (20,000 chars)
- ⚠️ **Escape special chars:** `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`

## Plans and Limits

| Tier | Speechify | Edge TTS |
|------|-----------|----------|
| **Free** | 50K chars/month (hard cap) | ✅ Unlimited |
| **Starter** ($10/mo) | 1M chars, overage $10/1M | ✅ Unlimited |
| **Pro** ($99/mo) | 3M chars, overage $8/1M | ✅ Unlimited |

Edge TTS is **free and unlimited** — always works as fallback.

## Multi-platform

### Hermes Agent

Use via `terminal()` or `execute_code()`:

```python
import subprocess
result = terminal(
    f"python3 scripts/speechfy-tts.py {shlex.quote(text)} /tmp/out.ogg"
)
```

### OpenClaw

```bash
# Direct invocation
python3 scripts/speechfy-tts.py "Hello" /tmp/out.ogg

# With mcporter (if configured for Speechify MCP)
mcporter call speechify.synthesize text="Hello"
```

## Troubleshooting

### "No API key found"
- Set `SPEECHIFY_API_KEY` env var, or
- Add item to Vaultwarden with name matching `SPEECHIFY_VAULT_ITEM`

### "Speechify HTTP 402"
- Monthly quota exhausted (50K chars on free tier)
- Script automatically falls back to Edge TTS

### "Speechify HTTP 429"
- Too many concurrent requests (free limit: 3 simultaneous)
- Wait a few seconds and retry

### Edge TTS not working
```bash
pip install edge-tts
edge-tts --voice pt-BR-FranciscaNeural --text "test" --write-media /tmp/test.ogg
```

### ffmpeg not found
```bash
# Debian/Ubuntu
sudo apt install ffmpeg

# Arch/Manjaro
sudo pacman -S ffmpeg
```

## Related

- [Speechify API Docs](https://docs.sws.speechify.com/)
- [Edge TTS (GitHub)](https://github.com/rany2/edge-tts)
- [SSML W3C Spec](https://www.w3.org/TR/speech-synthesis11/)
- `references/voices.md` — Available voices reference
- `docs/diagrama.svg` — Architecture diagram
