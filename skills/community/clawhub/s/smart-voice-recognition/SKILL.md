---
name: voice-recognition
description: |
  Intelligent speech-to-text using local OpenAI Whisper (no API key needed, fully private).
  Use when you need to transcribe audio files, convert voice messages to text,
  recognize spoken content, or process speech input in any of 99+ languages.
  Key differentiator: smart auto-model selection analyzes audio length and complexity
  to choose the optimal Whisper model — short clean clips use the fast base model,
  long or mixed-language clips automatically upgrade to small/medium for accuracy.
---

# 🎤 Voice Recognition — Smart Auto-Model Selection

Transcribe audio to text using **local OpenAI Whisper**. No API keys, no internet required, 100% private.

**Smart auto-selection** dynamically picks the best model based on your audio characteristics — you never have to think about which model to use.

## Quick Start

```bash
# Auto mode — analyzes audio, picks best model automatically
scripts/transcribe.py voice.ogg

# Force a specific model
scripts/transcribe.py voice.ogg --model small

# Specify language (auto-detect if omitted)
scripts/transcribe.py voice.ogg --language zh   # Chinese (Mandarin)
scripts/transcribe.py voice.ogg --language en   # English
scripts/transcribe.py voice.ogg --language yue  # Cantonese

# Show segment timestamps
scripts/transcribe.py voice.ogg --segments

# Save transcript to file
scripts/transcribe.py voice.ogg -o transcript.txt
```

## Smart Auto-Selection

The script analyzes audio duration + complexity and selects the optimal model automatically:

| Audio Characteristic | Model Used | Why |
|---|---|---|
| Short (<10s), clean speech | **base** | Fast (2-3s). Accurate enough for simple content. |
| Short (<10s), mixed languages | **small** | Better multilingual handling for code-switching. |
| Medium (10-60s), clean | **base** | Balanced speed and accuracy. |
| Medium (10-60s), mixed | **small** | Handles accents and language transitions. |
| Long (1-2min) | **small** | Maintains context, still fast enough. |
| Very long (2min+) | **medium** | Maximum accuracy for extended recordings. |

You don't need to think about models. Just send audio.

## Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Via bundled installer

```bash
python3 scripts/install.py
```

### Manual

```bash
pip install openai-whisper soundfile numpy
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Using requirements.txt

```bash
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

> **Note:** First run downloads the Whisper model (~139MB for base, ~461MB for small).
> Subsequent runs use the cached model (`~/.cache/whisper/`) and load instantly.

## Model Reference

| Model | Size | Speed | Accuracy | Best For |
|---|---|---|---|---|
| tiny | 72MB | ⚡⚡⚡ | ⭐⭐ | Real-time preview, very short clips |
| base | 139MB | ⚡⚡ | ⭐⭐⭐ | General use (auto-select default for short audio) |
| small | 461MB | ⚡ | ⭐⭐⭐⭐ | Mixed languages, accents (auto-select for long/complex) |
| medium | 1.5GB | 🐢 | ⭐⭐⭐⭐⭐ | Maximum accuracy, long recordings |
| large | 2.9GB | 🐢 | ⭐⭐⭐⭐⭐ | Research-grade transcription |

## Language Support

Whisper supports **99 languages** including:

- 🇨🇳 Chinese (Mandarin, Cantonese)
- 🇺🇸 English
- 🇪🇸 Spanish
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇫🇷 French
- 🇩🇪 German

Auto-detects language by default. Use `--language` to provide a hint for better accuracy.

## Features

| Feature | Description |
|---|---|
| 🔒 **100% Private** | Everything runs locally. No data leaves your machine. |
| 🆓 **No API Costs** | Free unlimited transcription. No quotas, no keys. |
| 🌐 **99 Languages** | Supports virtually all major world languages. |
| 🧠 **Smart Auto-Model** | Analyzes audio → picks optimal model automatically. |
| ⚡ **Fast by Default** | Short clips → base model (2-3s). Long clips → small/medium. |
| 🎯 **Accurate When Needed** | Complex/mixed audio automatically upgrades the model. |
| 📊 **Segment Timestamps** | Sentence-level timing for long recordings. |
| 📁 **Multiple Formats** | OGG, WAV, MP3, M4A, FLAC, OPUS and more. |

## Supported Audio Formats

| Format | Extension | Notes |
|---|---|---|
| OGG Opus | `.ogg` | Common voice message format ✅ |
| WAV | `.wav` | Uncompressed, high quality |
| MP3 | `.mp3` | Compressed audio |
| M4A | `.m4a` | Apple/MPEG-4 audio |
| FLAC | `.flac` | Lossless compressed |
| OPUS | `.opus` | Pure Opus stream |

## Usage Examples

### Quick transcription (auto model)

```bash
$ scripts/transcribe.py meeting.ogg
📂 Loading audio: meeting.ogg
⏱  Duration: 32.0s | Sample rate: 16000Hz
🧠 Auto-selected model: BASE
✓ Model loaded (1.0s)
🎯 Transcribing...
✅ Done (4.1s total)
Meeting notes: Today we discuss three topics. First, project progress...
```

### Transcription in context

```bash
# Chinese
scripts/transcribe.py voice.ogg --language zh

# English lecture with timestamps
scripts/transcribe.py lecture.m4a --language en --segments

# Mixed Chinese-English interview (auto complexity detection)
scripts/transcribe.py interview.ogg

# Save to file
scripts/transcribe.py podcast.mp3 -o transcript.txt

# Force high accuracy
scripts/transcribe.py important.wav --model medium
```

### Output with segments

```bash
$ scripts/transcribe.py message.ogg --segments
📂 Loading audio: message.ogg
⏱  Duration: 7.5s | Sample rate: 16000Hz
🧠 Auto-selected model: BASE
✓ Model loaded (1.0s)
🎯 Transcribing...
✅ Done (2.4s total)
Now I'm sending this voice message to XiaoA, can you recognize what I said?

📝 Segments:
   [0.0s - 3.6s] Now I'm sending this voice message
   [3.6s - 7.4s] to XiaoA, can you recognize what I said?
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `No module` error | Use the venv Python: `python3 scripts/transcribe.py` or run `scripts/install.py` |
| Slow transcription | First download caches the model (~139-461MB). Normal for first run. |
| Wrong language detected | Pass `--language en` or `--language zh` for a hint |
| Background noise | Use `--model small` or `--model medium` for noisy environments |

## Token Savings Examples

| Scenario | Cloud API Cost | This Skill | Savings |
|---|---|---|---|
| 10 short voice messages/day | ~$0.60/day (Whisper API) | **$0** | ∞ |
| 1 hour meeting transcription | ~$2.88 (Deepgram) | **$0** | ∞ |
| 1000 files for a project | ~$50-200 | **$0** | ∞ |
| Agent processing voice inputs | LLM tokens + API fees | **0 tokens** | Full token budget saved |

## Privacy & Security

- **100% offline** — no data leaves your machine.
- **No API keys** — no third-party services, no accounts.
- **No telemetry** — zero tracking.
- **No cloud** — everything runs locally.
- **Zero token consumption** — frees your LLM budget for reasoning.

Your audio is yours. Always.
