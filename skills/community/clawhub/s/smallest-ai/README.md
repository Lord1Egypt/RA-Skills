# Smallest AI — OpenClaw Voice Skill

The fastest TTS/STT skill for [OpenClaw](https://openclaw.ai). Sub-100ms text-to-speech via Lightning v3.1. 64ms speech-to-text via Pulse.

> **"My OpenClaw now speaks faster than I can think"** — what you'll say after installing this

## Why This Exists

| Provider | Latency (TTFB) | Price | Voice Cloning |
|----------|---------------|-------|---------------|
| **Smallest AI** | **~100ms** | **Free tier + $5/mo** | **5 sec of audio** |
| ElevenLabs | ~300ms | $5/mo (30min) | 30 sec of audio |
| OpenAI TTS | ~200ms | Pay per token | Not available |
| Kokoro (Local) | Varies | Free (GPU needed) | Not available |

Smallest AI is faster, cheaper, and needs 6x less audio for voice cloning.

## Quick Install

```bash
# Option 1: ClawHub (recommended)
clawhub install smallest-ai

# Option 2: Manual
git clone https://github.com/smallest-inc/smallest-ai-openclaw.git
cp -r smallest-ai-openclaw ~/.openclaw/skills/smallest-ai

# Set your API key
export SMALLEST_API_KEY="your_key_here"
# Get one free at https://waves.smallest.ai
```

Then restart the gateway: `openclaw gateway stop && openclaw gateway start`

## What You Get

### Text-to-Speech (Lightning v3.1)
```
"Say good morning in a male voice"
"Read my latest email summary aloud"
"Generate a voice note saying the meeting is at 3pm"
```

### Speech-to-Text (Pulse)
```
"Transcribe this voice note" [attach audio]
"What did they say in this recording? Include speaker labels"
"Convert this meeting audio to text with timestamps"
```

### Multilingual
```
"Say 'नमस्ते, कैसे हैं आप?' in Hindi"
"Read this in Spanish: Hola, buenos días"
"Say bonjour le monde in French"
```

### Voice Note Loop
Send a WhatsApp voice note → Pulse transcribes it → agent processes → replies as a voice note via Lightning. Full voice-in, voice-out.

## Voices

| Voice | Gender | Accent | Best For |
|-------|--------|--------|----------|
| `sophia` | Female | American | General use (default) |
| `robert` | Male | American | Professional, reports (default) |
| `advika` | Female | Indian | Hindi, code-switching |
| `vivaan` | Male | Indian | Bilingual English/Hindi |
| `camilla` | Female | Mexican/Latin | Spanish content |
| `zara` | Female | American | Conversational |
| `melody` | Female | American | Storytelling |
| `arjun` | Male | Indian | English/Hindi bilingual |
| `stella` | Female | American | Expressive, warm |

80+ more voices available — the agent auto-selects based on language and gender preference.

## File Structure

```
smallest-ai/
├── SKILL.md                 # Skill definition (required)
├── scripts/
│   ├── tts.sh               # TTS via curl (zero deps)
│   ├── tts.py               # TTS via Python (SDK + fallback)
│   ├── stt.sh               # STT via curl
│   ├── stt.py               # STT via Python
│   └── voices.sh            # List available voices
├── references/
│   ├── voices.md            # Voice catalog
│   ├── languages.md         # 30+ supported languages
│   └── api-reference.md     # API quick reference
└── README.md                # This file
```

## Requirements

- OpenClaw (any version)
- `curl` (included on macOS/Linux)
- `python3` (optional, for advanced features)
- `SMALLEST_API_KEY` environment variable

Optional: `pip install smallestai` for the official SDK with async support and streaming.

## Examples

### Voice Note Loop (WhatsApp)
```
Send a voice note saying "summarize my day" →
Agent transcribes → processes → replies with voice note
```

### Morning Briefing Agent
```
"Every morning at 7am, check my calendar and email,
 summarize the day ahead, and read it to me on WhatsApp
 using the robert voice"
```

### Hindi/English Code-Switching
```
"Hey, mujhe aaj ke weather ka summary do in advika's voice"
```

### Meeting Transcription
```
"Transcribe this meeting recording, identify who said what,
 and create a summary with action items"
```

## Pricing

| Plan | TTS | STT | Voice Clones | Cost |
|------|-----|-----|-------------|------|
| Free | 30 min/mo | Limited | 0 | $0 |
| Basic | 3 hrs/mo | Included | 1 | $5/mo |
| Premium | 24 hrs/mo | Included | 2 | $29/mo |

## Links

- [Smallest AI](https://smallest.ai) — Main site
- [Waves Console](https://waves.smallest.ai) — Get API key
- [API Docs](https://waves-docs.smallest.ai) — Full documentation
- [Python SDK](https://github.com/smallest-inc/smallest-python-sdk) — Official SDK
- [OpenClaw](https://openclaw.ai) — OpenClaw main site
- [ClawHub](https://clawhub.ai) — Skills marketplace

## Contributing

PRs welcome! If you add a new feature or voice integration, please include:
1. Updated SKILL.md instructions
2. Tests or usage examples
3. Updated references if API surface changes

## License

MIT — use it, fork it, ship it.

---

Built with ⚡ by [Abhishek](https://twitter.com/stalwartcoder) at [Smallest AI](https://smallest.ai)
