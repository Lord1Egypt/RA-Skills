---
name: screenshot-telegram-direct
description: Capture website screenshots and send to Telegram via direct API. Works around OpenClaw's broken image delivery (issue #63137).
metadata:
  author: niccoreyes
  version: "1.0.0"
  license: MIT
  openclaw:
    requires:
      bins: [curl]
---

# Screenshot → Telegram (Direct)

Capture website screenshots and send them to Telegram, bypassing OpenClaw's broken image delivery pipeline.

## Quick Start

```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your tokens

# 2. Run the helper script
./screenshot-send.sh https://github.com
```

## Setup

### 1. Get API Credentials

**Telegram Bot Token:**
- Message [@BotFather](https://t.me/BotFather)
- Send `/mybots` → Select bot → Copy API token

**Telegram Chat ID:**
- Personal: Message [@userinfobot](https://t.me/userinfobot)
- Group: Add [@RawDataBot](https://t.me/RawDataBot) to group

**Snap API Key:**
```bash
# Register for free API key
curl -s -X POST https://snap.llm.kaveenk.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"my-agent"}'
# Save the "key" from response
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env:
# TELEGRAM_BOT_TOKEN=your_token
# TELEGRAM_CHAT_ID=your_chat_id
# SNAP_API_KEY=your_snap_key

# Source it (temporary)
source .env
```

### 3. Auto-Load .env (Recommended for OpenClaw)

**Option A: Add to shell profile (always available)**

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Auto-load screenshot-telegram-direct env vars
SKILL_DIR="$HOME/.openclaw/workspace/skills/screenshot-telegram-direct"
if [ -f "$SKILL_DIR/.env" ]; then
    export $(grep -v '^#' "$SKILL_DIR/.env" | xargs)
fi
```

Then reload: `source ~/.bashrc`

**Option B: Source before each OpenClaw session**

In your OpenClaw workspace, create `load-env.sh`:

```bash
#!/bin/bash
source "$HOME/.openclaw/workspace/skills/screenshot-telegram-direct/.env"
echo "✅ Environment loaded from screenshot-telegram-direct/.env"
```

Run before using: `source load-env.sh`

**Option C: Script auto-sources .env**

The `screenshot-send.sh` script automatically sources `.env` from its directory if present.

### 3. Make Script Executable

```bash
chmod +x screenshot-send.sh
```

## Usage

### Basic screenshot

```bash
./screenshot-send.sh https://example.com
```

### Custom caption

```bash
./screenshot-send.sh https://github.com "Latest PR status"
```

### Multiple URLs

```bash
for url in "https://github.com" "https://news.ycombinator.com"; do
  ./screenshot-send.sh "$url"
  sleep 2
done
```

## Configuration Options

### Snap API Options

Edit `screenshot-send.sh` to customize:

```bash
# Full page screenshot
curl -s -X POST "https://snap.llm.kaveenk.com/api/screenshot" \
  -H "Authorization: Bearer $SNAP_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "'$URL'",
    "full_page": true,
    "width": 1920,
    "height": 1080,
    "dark_mode": true,
    "wait_ms": 2000
  }' \
  -o "$OUTPUT_FILE"
```

| Option | Description |
|--------|-------------|
| `full_page` | Capture entire scrollable page |
| `width`/`height` | Viewport size |
| `dark_mode` | Emulate dark color scheme |
| `wait_ms` | Wait for JS rendering |
| `format` | png or jpeg |

### Send as Document (No Compression)

Replace `sendPhoto` with `sendDocument` in the script:

```bash
curl -s -X POST \
  -F "chat_id=$CHAT_ID" \
  -F "document=@$OUTPUT_FILE" \
  -F "caption=$CAPTION" \
  "https://api.telegram.org/bot$TOKEN/sendDocument"
```

## Automation (Cron)

```bash
# Daily dashboard screenshot
0 9 * * * cd /home/pi/.openclaw/workspace/skills/screenshot-telegram-direct && ./screenshot-send.sh https://status.example.com

# Hourly monitoring
0 * * * * cd /home/pi/.openclaw/workspace/skills/screenshot-telegram-direct && ./screenshot-send.sh https://uptime.example.com
```

## File Structure

```
screenshot-telegram-direct/
├── SKILL.md              # This documentation
├── skill.md              # Alias for ClawHub
├── .env.example          # Template for env vars
├── .env                  # Your secrets (gitignored)
├── .gitignore            # Excludes .env
└── screenshot-send.sh    # Main script
```

## Security

- ✅ `.env` is gitignored — never commit secrets
- ✅ `.env.example` shows required variables without values
- ✅ Script fails if env vars are missing
- ✅ No hardcoded credentials

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `Missing environment variables` | Check `.env` exists and is sourced |
| `Failed to capture screenshot` | Check SNAP_API_KEY is valid |
| `chat not found` | Verify TELEGRAM_CHAT_ID |
| `bot was blocked` | Send `/start` to bot in Telegram |

## Why Not Use OpenClaw Native?

See OpenClaw issue #63137: Images sent via `read` tool render locally but never reach mobile clients — silent failure with no error logs.

This skill bypasses OpenClaw's Telegram channel entirely using direct HTTP API calls.

## Publishing Notes

This skill is ready for publication:
- No hardcoded secrets
- `.env.example` for configuration
- `.gitignore` excludes secrets
- Clear documentation
- MIT licensed