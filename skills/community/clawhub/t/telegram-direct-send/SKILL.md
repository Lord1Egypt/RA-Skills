---
name: telegram-direct-send
description: Send images to Telegram via direct Bot API using curl. Works around OpenClaw's broken image delivery pipeline (issue #63137).
metadata:
  author: niccoreyes
  version: "1.0.0"
  license: MIT
  openclaw:
    requires:
      bins: [curl]
---

# Telegram Direct Send

Send images to Telegram using direct HTTP API calls. Bypasses OpenClaw's native Telegram channel which fails silently for images.

## Quick Start

```bash
# 1. Copy example env file and edit
cp .env.example .env
# Edit .env with your tokens

# 2. Source the env file (or add to ~/.bashrc for auto-load)
source .env

# 3. Send an image
curl -s -X POST \
  -F "chat_id=${TELEGRAM_CHAT_ID}" \
  -F "photo=@/path/to/image.png" \
  -F "caption=My screenshot" \
  "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto"
```

## Setup

### 1. Get Telegram Bot Token

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` or `/mybots` for existing
3. Copy the API token (format: `123456789:ABC...`)

### 2. Get Chat ID

**For personal messages:**
- Message [@userinfobot](https://t.me/userinfobot)
- It will reply with your ID

**For groups:**
- Add [@RawDataBot](https://t.me/RawDataBot) to your group
- It will reply with the chat ID (starts with `-100`)

### 3. Configure Environment

```bash
# Option A: Export in shell (temporary)
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# Option B: Create .env file (recommended)
cp .env.example .env
# Edit .env with your values
source .env
```

**Security:** `.env` is gitignored — never commit secrets!

### 4. Auto-Load .env (Optional but Recommended)

**For OpenClaw sessions:**
Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Auto-load telegram-direct-send env vars
if [ -f "$HOME/.openclaw/workspace/skills/telegram-direct-send/.env" ]; then
    source "$HOME/.openclaw/workspace/skills/telegram-direct-send/.env"
fi
```

**For skill directory only:**
Create a wrapper script `send-image.sh`:

```bash
#!/bin/bash
# Load env vars from skill directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/.env" ]; then
    source "$SCRIPT_DIR/.env"
fi

# Now use the vars
curl -s -X POST \
  -F "chat_id=${TELEGRAM_CHAT_ID}" \
  -F "photo=@$1" \
  -F "caption=${2:-Image}" \
  "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto"
```

Then: `chmod +x send-image.sh && ./send-image.sh ./photo.png "My caption"`

## Usage Examples

### Send image with caption

```bash
curl -s -X POST \
  -F "chat_id=${TELEGRAM_CHAT_ID}" \
  -F "photo=@./screenshot.png" \
  -F "caption=Screenshot from $(date)" \
  "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto"
```

### Send as document (no compression)

```bash
curl -s -X POST \
  -F "chat_id=${TELEGRAM_CHAT_ID}" \
  -F "document=@/path/to/image.png" \
  -F "caption=Original quality" \
  "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument"
```

### Send with inline keyboard

```bash
curl -s -X POST \
  -F "chat_id=${TELEGRAM_CHAT_ID}" \
  -F "photo=@./image.png" \
  -F "caption=Choose:" \
  -F "reply_markup={\"inline_keyboard\":[[{\"text\":\"Yes\",\"callback_data\":\"yes\"},{\"text\":\"No\",\"callback_data\":\"no\"}]]}" \
  "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto"
```

## API Reference

| Endpoint | Purpose |
|----------|---------|
| `sendPhoto` | Send image (compressed) |
| `sendDocument` | Send file (no compression) |
| `sendMessage` | Text only |
| `sendMediaGroup` | Multiple images |

## Troubleshooting

| Error | Solution |
|-------|----------|
| `chat not found` | Check `TELEGRAM_CHAT_ID` |
| `bot was blocked` | User must `/start` the bot |
| `file too large` | Use `sendDocument` |

## Why This Skill Exists

OpenClaw issue #63137: Images sent via `read` tool render in agent context but never reach Telegram mobile clients. This skill bypasses OpenClaw's gateway entirely.

## Publishing Notes

- `.env.example` shows required variables
- `.gitignore` excludes `.env`
- No hardcoded secrets
- Users configure via env or .env file
