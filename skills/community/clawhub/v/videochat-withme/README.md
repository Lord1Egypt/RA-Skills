# 🎥 videochat-withme

Real-time AI video chat skill for [OpenClaw](https://github.com/openclaw/openclaw). Talk face-to-face with your AI agent — it sees your camera, hears your voice, and responds with its own personality, memory, and voice.

https://github.com/user-attachments/assets/demo-placeholder

## ✨ Features

- **🎤 Voice conversation** — Groq Whisper for fast speech-to-text (~1s latency)
- **📷 Vision** — Your agent sees you via camera (base64 frames sent to LLM)
- **🔊 AI voice** — edge-tts for natural text-to-speech responses
- **🧠 Full personality** — Routes through your OpenClaw agent (memory, personality, tools)
- **📱 Mobile support** — HTTPS with self-signed certs, works on phone browsers
- **🔒 Privacy-conscious** — No recordings stored; audio processed via Groq Whisper (cloud STT), TTS via Microsoft edge-tts (cloud). Camera frames sent to your OpenClaw gateway → your LLM provider (⚠️ frames may reach cloud if using a cloud LLM)

## 🏗️ Architecture

```
🎤 Voice → Groq Whisper (STT)
📷 Camera → base64 frame
    ↓
OpenClaw /v1/chat/completions → Your Agent (personality + memory)
    ↓
edge-tts (TTS) → 🔊 Audio playback
```

## 🔐 Data Flows & Privacy

| Data | Destination | Type |
|------|-------------|------|
| 🎤 Audio recordings | `api.groq.com` (Groq Whisper) | ☁️ Cloud STT |
| 🔊 Text for speech | Microsoft edge-tts service | ☁️ Cloud TTS |
| 📷 Camera frames (base64) + text | `localhost` OpenClaw gateway → **your configured LLM** | ⚠️ Depends on LLM provider |
| 💬 Conversation | Your configured LLM (via gateway) | ⚠️ Depends on LLM provider |

> **⚠️ Important:** Camera frames are encoded as base64 and sent to your OpenClaw gateway's `/v1/chat/completions` endpoint. If your gateway forwards to a **cloud LLM** (e.g., Claude, GPT), those frames **will leave your machine**. If you want frames to stay local, configure your gateway to use a local/self-hosted model.

**What is NOT stored:**
- No recordings are saved to disk (beyond temporary `/tmp` files during processing)
- No conversation data is persisted on any server
- The API proxy is stateless

**Credentials accessed:**
- `GROQ_API_KEY` — for Whisper STT (from env var or `~/.openclaw/secrets/groq_api_key.txt`)
- OpenClaw gateway auth token — read from `~/.openclaw/openclaw.json` (required for chatCompletions API)

## 📋 Prerequisites

- **macOS** (uses launchd for service management)
- **Python 3.10+**
- **ffmpeg** (`brew install ffmpeg`)
- **OpenClaw** running with `chatCompletions` enabled
- **Groq API key** (free at [console.groq.com](https://console.groq.com/keys))

### Enable chatCompletions in OpenClaw

Add to `~/.openclaw/openclaw.json`:

```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true }
      }
    }
  }
}
```

Then restart OpenClaw.

## 🚀 Quick Start

### 1. Install as OpenClaw skill

```bash
# Clone into your skills directory
git clone https://github.com/sxu75374/videochat-withme.git ~/.openclaw/workspace/skills/videochat-withme
```

### 2. Run setup

```bash
cd ~/.openclaw/workspace/skills/videochat-withme
bash scripts/setup.sh
```

This interactive script handles everything:
- Installs Python dependencies (`fastapi`, `uvicorn`, `edge-tts`, `httpx`)
- Prompts for your Groq API key
- Generates SSL certificates (via [mkcert](https://github.com/FiloSottile/mkcert))
- Installs a `launchd` service for auto-start

### 3. Open in browser

Visit **https://localhost:8766** and allow camera/microphone access.

> 💡 First visit will show a certificate warning — click "Advanced → Continue" (self-signed cert).

## 📱 Mobile Access

The server runs with HTTPS so mobile browsers can access camera/mic:

- **Same WiFi:** `https://<your-local-ip>:8766`
- **Any network (via Tailscale):** `https://<tailscale-ip>:8766`

## 🤖 Agent Integration

Your OpenClaw agent can start calls automatically. See [SKILL.md](./SKILL.md) for agent instructions.

**Quick example** — when user says "video chat":
```bash
# Check if service is running
curl -sk https://localhost:8766/api/config

# Pop up incoming call notification (macOS)
bash scripts/call.sh
```

## 📁 Project Structure

```
videochat-withme/
├── SKILL.md              # OpenClaw skill definition + agent instructions
├── README.md             # This file
├── scripts/
│   ├── setup.sh          # One-time setup (deps, certs, launchd)
│   ├── server.py         # FastAPI server (STT, TTS, video, chat)
│   ├── call.sh           # Trigger incoming call notification
│   ├── start.sh          # Start service
│   └── stop.sh           # Stop service
└── assets/
    └── index.html         # Video chat UI (split-screen, push-to-talk)
```

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | `~/.openclaw/secrets/groq_api_key.txt` | Groq API key for Whisper STT |
| `PORT` | `8766` | Server port |
| `AGENT_NAME` | `AI Assistant` | Display name for the agent |
| `USER_NAME` | `User` | Display name for the user |
| `SSL_CERT` / `SSL_KEY` | Auto-detected | SSL certificate paths |

## 🛠️ Manual Control

```bash
# Start service
bash scripts/start.sh

# Stop service
bash scripts/stop.sh

# Check status
launchctl list | grep videochat
```

## 📄 License

MIT License — see [LICENSE](./LICENSE).

## 🙏 Credits

- [OpenClaw](https://github.com/openclaw/openclaw) — AI agent framework
- [Groq](https://groq.com) — Ultra-fast Whisper inference
- [edge-tts](https://github.com/rany2/edge-tts) — Free Microsoft TTS
- [mkcert](https://github.com/FiloSottile/mkcert) — Local HTTPS certificates
