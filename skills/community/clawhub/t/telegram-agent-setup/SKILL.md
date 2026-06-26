---
name: telegram-agent-setup
description: Complete guide to connecting OpenClaw with Telegram. Set up bot, configure channels, handle groups/topics, voice messages, inline buttons, media, and troubleshoot common issues. Use when setting up a new Telegram bot for OpenClaw or debugging connection problems.
version: 1.0.1
author: mosoonpi-ai
license: MIT
tags: telegram, bot, setup, messaging, channels, voice, groups
---

# Telegram Agent Setup — Connect OpenClaw to Telegram

## What You Get

- ⏱️ **Working bot in 15 minutes** instead of 3+ hours reading scattered docs
- 🔒 **Security lockdown** — stop strangers from using your bot (most guides skip this)
- 👥 **Group & forum support** — route topics to different agents
- 🎤 **Voice messages working** — full STT setup with faster-whisper
- 🔧 **15+ troubleshooting fixes** — every problem we've hit running 5 production bots
- ✅ **Production checklist** — 8-point verification before going live

## When to Use

- Setting up a **new Telegram bot** for OpenClaw
- Configuring **group chats**, **forum topics**, or **private chats**
- Troubleshooting **connection issues** (bot not responding, messages not arriving)
- Setting up **voice messages** (STT transcription)
- Configuring **inline buttons**, **reactions**, and **media handling**
- Moving from basic setup to **production-ready** configuration

## Prerequisites

- OpenClaw installed and running (`openclaw gateway status` shows OK)
- Telegram account
- Access to @BotFather on Telegram

## Step 1: Create a Telegram Bot

1. Open Telegram, find **@BotFather**
2. Send `/newbot`
3. Choose a display name (e.g., "My AI Assistant")
4. Choose a username (must end in `bot`, e.g., `my_ai_assistant_bot`)
5. Copy the **API token** (looks like `7123456789:AAH...`)

### Important BotFather Settings

```
/setprivacy → Disable (so bot sees all messages in groups)
/setjoingroups → Enable (if you want to add bot to groups)
/setcommands → Set your commands:
  start - Start the bot
  help - Show help
  status - Check status
```

## Step 2: Connect to OpenClaw

### Method A: CLI (recommended)

```bash
openclaw telegram setup
```

Follow the interactive prompts. Paste your bot token when asked.

### Method B: Manual config

Edit `~/.openclaw/openclaw.json`:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN_HERE",
      "allowedChatIds": []
    }
  }
}
```

Then restart:
```bash
openclaw gateway restart
```

## Step 3: Verify Connection

1. Open your bot in Telegram
2. Send `/start` or any message
3. Bot should respond

If no response:
```bash
openclaw gateway status
openclaw gateway logs --tail 50
```

## Step 4: Security — Restrict Access

**Critical.** Without this, anyone who finds your bot can use your Claude subscription.

```json
{
  "channels": {
    "telegram": {
      "allowedChatIds": ["YOUR_TELEGRAM_USER_ID"],
      "rejectUnknown": true
    }
  }
}
```

Find your user ID: message @userinfobot on Telegram.

## Step 5: Group Chat Setup

### Regular group
1. Add bot to group
2. Get group chat ID from logs: `openclaw gateway logs | grep "chat_id"`
3. Add to `allowedChatIds` (group IDs are negative: `-1001234567890`)

### Forum (topics) group
- Each topic gets its own `topic_id`
- Route different topics to different agents
- Perfect for multi-agent setups (see `multi-agent-architecture` skill)

### Response behavior in groups
```json
{
  "groupBehavior": {
    "respondTo": "mention"
  }
}
```
Options: `"all"` (every message), `"mention"` (when tagged — recommended), `"command"` (only /commands).

## Step 6: Voice Messages

### Quick STT setup with faster-whisper:

```bash
python3 -m venv ~/.openclaw/venvs/stt-tools
source ~/.openclaw/venvs/stt-tools/bin/activate
pip install faster-whisper
```

Model sizes: `tiny` (fast, ~1GB RAM), `base` (better, ~2GB), `small` (best, ~4GB).

Create `scripts/transcribe_audio.py`:
```python
#!/usr/bin/env python3
import sys
from faster_whisper import WhisperModel

def transcribe(audio_path, model_size="tiny", language="ru"):
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path, language=language)
    print(" ".join(seg.text.strip() for seg in segments))

if __name__ == "__main__":
    transcribe(sys.argv[1],
               sys.argv[2] if len(sys.argv) > 2 else "tiny",
               sys.argv[3] if len(sys.argv) > 3 else "ru")
```

## Troubleshooting

### Bot not responding
1. `openclaw gateway status` — is it running?
2. `openclaw gateway logs --tail 100 | grep -i error` — any errors?
3. Check bot token — no extra spaces?
4. Check firewall — outbound HTTPS (port 443) open?

### Bot responds to strangers
→ Add `allowedChatIds` + `rejectUnknown: true`

### Messages delayed
→ Check server load (`htop`), check for rate limits in logs

### Voice not transcribed
→ Check STT venv exists and faster-whisper installed
→ Telegram sends .ogg (opus) — faster-whisper handles it natively

### "Webhook" vs "Polling"
→ OpenClaw uses long polling by default (no public IP needed)

## Production Checklist

- [ ] Bot token stored securely (not in git, not in chat)
- [ ] `allowedChatIds` configured
- [ ] `rejectUnknown: true` enabled
- [ ] Error policy: `"silent"` (no error messages to users)
- [ ] Voice transcription working (if needed)
- [ ] Group privacy mode disabled in BotFather (if using groups)
- [ ] Bot commands registered via BotFather
- [ ] Gateway auto-restarts on failure
