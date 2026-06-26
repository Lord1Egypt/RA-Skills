---
name: voiceclaw-jp
description: Voice conversation interface for OpenClaw using wake word detection, streaming LLM responses, and text-to-speech. Use when a user wants to talk to their OpenClaw agent by voice, set up a voice assistant, or add speech input/output to OpenClaw. Supports configurable wake words, VOICEVOX TTS, and sentence-level streaming for low-latency responses.
---

# voiceclaw

Voice conversation skill for OpenClaw: wake word → STT → LLM (streaming) → TTS → playback.

## Requirements

- **OpenClaw** running locally (gateway with `chatCompletions` enabled)
- **Node.js** 18+
- **VOICEVOX** running on localhost:50021 ([download](https://voicevox.hiroshiba.jp/))
- **Chrome/Edge** (Web Speech API for STT)
- **HTTPS** for remote mic access (localhost works without HTTPS)

## Quick Start

```bash
# Install
git clone https://github.com/kentoku24/voiceclaw.git
cd voiceclaw
npm install

# Start (no .env needed if OpenClaw is running locally)
npm start
# → [voiceclaw] OpenClaw config loaded from ~/.openclaw/openclaw.json
# → [voiceclaw] listening on http://127.0.0.1:8788

# Open browser
open http://127.0.0.1:8788
```

Press **開始**, say the wake word (default: **アリス**), then speak your command.

## Configuration

All settings are optional. Set in `.env` or environment variables:

| Variable | Default | Description |
|---|---|---|
| `WAKE_WORDS` | アリスちゃん,アリス,... | Comma-separated wake words |
| `STT_LANG` | ja-JP | Speech recognition language |
| `OPENCLAW_MODEL` | openclaw | LLM model name |
| `VOICEVOX_URL` | http://127.0.0.1:50021 | VOICEVOX endpoint |
| `VOICEVOX_SPEAKER` | 1 | VOICEVOX speaker ID |
| `HOST` | 127.0.0.1 | Server bind address |
| `PORT` | 8788 | Server port |

Gateway token is auto-detected from `~/.openclaw/openclaw.json`. Override with `OPENCLAW_GATEWAY_TOKEN` if needed.

## Architecture

```
Wake word (browser STT) → voiceclaw server → OpenClaw Gateway (streaming)
                                           → sentence-level TTS (VOICEVOX)
                                           → audio playback (Web Audio API)
```

See [docs/architecture.md](docs/architecture.md) for the full sequence diagram.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/config` | Client-safe settings (wake words, STT lang) |
| POST | `/api/chat-stream` | Streaming LLM → sentence-level SSE |
| POST | `/api/chat` | Non-streaming LLM (fallback) |
| POST | `/api/tts` | Text → VOICEVOX → WAV audio |
