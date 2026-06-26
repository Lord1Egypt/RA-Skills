---
name: videochat-withme
description: |
  Real-time AI video chat that routes through your OpenClaw agent. Uses Groq Whisper (cloud STT),
  edge-tts (cloud TTS via Microsoft), and OpenClaw chatCompletions API for conversation. Your agent
  sees your camera, hears your voice, and responds with its own personality and memory.
  Requires: GROQ_API_KEY for speech recognition. Reads ~/.openclaw/openclaw.json for gateway port and auth token.
  Data flows: audio → Groq cloud (STT), TTS text → Microsoft cloud (edge-tts), camera frames (base64) + text
  → OpenClaw gateway → your configured LLM provider (may be cloud — frames leave the machine if using a cloud LLM).
  Installs a persistent launchd service (optional). Trigger phrases: "video chat", "voice call",
  "call me", "视频一下", "语音", "打电话给我", "我要和你视频", "videochat-withme".
metadata:
  {
    "openclaw":
      {
        "emoji": "🎥",
        "requires":
          {
            "bins": ["python3", "ffmpeg"],
            "env": ["GROQ_API_KEY"],
            "config": ["gateway.http"],
          },
      },
  }
---

# videochat-withme

Real-time video call with your OpenClaw agent — full personality, memory, and vision.

## First-Time Setup

New users run once after installing the skill:

```bash
bash skills/videochat-withme/scripts/setup.sh
```

This handles everything: dependencies, Groq API key, SSL certs, launchd service.

## Prerequisites

- macOS (launchd required)
- Python 3.10+, ffmpeg
- OpenClaw gateway running with chatCompletions enabled

### Groq API Key (required for voice recognition)

1. Get a free key at: https://console.groq.com/keys
2. Save it:
   ```bash
   mkdir -p ~/.openclaw/secrets
   echo "your-key-here" > ~/.openclaw/secrets/groq_api_key.txt
   ```
   Or set env var: `export GROQ_API_KEY="your-key-here"`

### Enable chatCompletions

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

## How to Use (Agent Instructions)

When the user requests a video/voice call:

**Step 1: Check if service is running:**
```bash
curl -sk https://localhost:8766/api/config 2>/dev/null || curl -s http://localhost:8766/api/config 2>/dev/null
```

**Step 2: If no response, setup needed:**
1. Check Groq key: `cat ~/.openclaw/secrets/groq_api_key.txt 2>/dev/null`
   - If missing, ask user to get one at https://console.groq.com/keys
   - Save it: `echo "key" > ~/.openclaw/secrets/groq_api_key.txt`
2. Ask user: "What name should I display for you in the video call?"
3. Run setup:
   ```bash
   bash skills/videochat-withme/scripts/setup.sh --auto --agent-name "YourName" --user-name "TheirName"
   ```

**Step 3: Initiate the call based on context:**

Determine how the user is connecting and pick the best method:

1. **User is at the computer** (message from webchat/desktop):
   ```bash
   bash skills/videochat-withme/scripts/call.sh
   ```
   This pops up a macOS incoming call notification → user clicks Accept → browser opens.

2. **User is on mobile/remote** (message from Telegram/phone):
   Pick the right URL automatically:
   ```bash
   # Prefer Tailscale IP (works from any network)
   TS_IP=$(tailscale ip -4 2>/dev/null)
   # Fallback to local IP (same WiFi only)
   LOCAL_IP=$(python3 -c "import socket; s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.connect(('8.8.8.8',80)); print(s.getsockname()[0]); s.close()" 2>/dev/null)
   ```
   - If Tailscale is available → send `https://<tailscale-ip>:8766` (works everywhere)
   - Otherwise → send `https://<local-ip>:8766` (same WiFi only)
   - Note: first visit requires tapping "Advanced → Continue" (self-signed cert)

## Architecture

```
🎤 Voice → Groq Whisper (STT)
📷 Camera → base64 frame
    ↓
OpenClaw /v1/chat/completions → Your Agent
    ↓
edge-tts (TTS) → 🔊 Audio playback
```

## Scripts

**Agent runs these automatically:**

| Script | When |
|--------|------|
| `setup.sh --auto` | First use (service not running) |
| `call.sh` | Every call request |

**User can run manually if needed:**

| Script | Purpose |
|--------|---------|
| `setup.sh` | Interactive setup (without --auto) |
| `start.sh` | Start service |
| `stop.sh` | Stop service |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | (secrets file) | Groq API key for Whisper STT |
| `PORT` | `8766` | Server port |
| `AGENT_NAME` | `AI Assistant` | Display name for the agent |
| `USER_NAME` | `User` | Display name for the user |
| `SSL_CERT` | (auto-detect) | Path to SSL certificate |
| `SSL_KEY` | (auto-detect) | Path to SSL private key |
