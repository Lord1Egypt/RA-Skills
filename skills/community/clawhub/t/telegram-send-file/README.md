# telegram-send-file

[![PyPI version](https://badge.fury.io/py/python-telegram-bot.svg)](https://badge.fury.io/py/python-telegram-bot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Send files to Telegram via the Bot API — from the CLI, scripts, or inside [OpenClaw](https://github.com/wangwllu/openclaw).

Features:
- 🚀 **Auto-detection** of chat/topic from OpenClaw session (no args needed in most cases)
- 📎 **All file types** — images, video, audio, documents, archives
- 🔄 **Batch mode** — send multiple files in one command
- ⏳ **Progress feedback** for large files (> 5 MB)
- 🔇 **Silent send** option
- 📝 **Caption from filename** option
- 🐛 **Full error handling** — clear, actionable error messages
- 🔍 **Verbose debug mode** — see what's happening under the hood

---

## Requirements

- Python 3.9+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) ≥ 20.0

```bash
pip install python-telegram-bot>=20.0
```

---

## Getting a Bot Token

1. Open Telegram and message **@BotFather**
2. Send `/newbot`
3. Follow the prompts (pick a name and username)
4. Copy the token BotFather shows you — it looks like:

```
123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

5. Save it one of these ways:

```bash
# Option A: config file (recommended)
echo "YOUR_TOKEN" > ~/.telegram_bot_token

# Option B: environment variable
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN"

# Option C: OpenClaw with Telegram — auto-detected, no setup needed
```

---

## Quick Start

### 1. Find your chat ID

Send any message to your bot in Telegram, then visit:

```
https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
```

Look for `"id": 5866004662` in the JSON response — that's your personal chat ID.
For groups/channels, the ID will look like `-1003848180061`.

### 2. Send your first file

```bash
# Simple file send
python telegram_send_file.py --chat-id 5866004662 --file document.pdf

# With caption
python telegram_send_file.py --chat-id 5866004662 --file photo.png --caption "Look at this!"
```

---

## Usage

```
python telegram_send_file.py [options]
```

### Key Options

| Option | Description |
|--------|-------------|
| `--file PATH` | Local file to send |
| `--url URL` | URL to download and send |
| `--file-id ID` | Telegram file_id to forward |
| `--files PATH [PATH ...]` | Multiple files (batch, sequential) |
| `--chat-id ID` | Target chat ID |
| `--topic-id N` | Topic/thread ID for forum chats |
| `--caption TEXT` | File caption |
| `--caption-from-filename` | Use filename (minus extension) as caption |
| `--parse-mode MODE` | `Markdown`, `MarkdownV2`, or `HTML` |
| `--silent` | Send silently (no notification) |
| `--verbose`, `-v` | Debug output |
| `--token TOKEN` | Bot token override |

---

## Examples

### Auto-detect from OpenClaw

When running inside an OpenClaw Telegram session, context is automatic:

```bash
python telegram_send_file.py --file report.pdf
# No --chat-id needed — auto-detected!
```

### Batch send

```bash
python telegram_send_file.py \
  --files file1.pdf file2.jpg file3.zip \
  --caption "Weekly delivery"
```

### Silent + caption from filename

```bash
python telegram_send_file.py \
  --file bug_report_2024.pdf \
  --caption-from-filename \
  --silent
```

### HTML caption

```bash
python telegram_send_file.py --file doc.pdf \
  --caption "<b>Important</b> — Review by Friday" \
  --parse-mode HTML
```

### Send to a forum topic

```bash
python telegram_send_file.py \
  --chat-id -1003848180061 \
  --topic-id 5 \
  --file notes.pdf
```

### Verbose debug output

```bash
python telegram_send_file.py --file video.mp4 --verbose
```

```
[DEBUG] send_file: Sending video to chat ... (size: 120.4MB)
Upload: [##########] 100%  (120.4MB / 120.4MB)  3.2MB/s
[INFO] ✓ File sent successfully (message_id=42)
  file_id: AgADABC...
  Link: https://t.me/c/3848180061/42
```

---

## Configuration

### Environment Variables

```bash
export TELEGRAM_BOT_TOKEN="123456789:ABCdef..."        # Bot token
export TELEGRAM_DEFAULT_CHAT_ID="-1003848180061"      # Default chat
export TELEGRAM_DEFAULT_TOPIC_ID="3"                  # Default topic
```

### Token File Locations (checked in order)

1. `TELEGRAM_BOT_TOKEN` environment variable
2. `~/.config/telegram-send-file/config`
3. `~/.telegram_bot_token`
4. `~/.telegram_token`
5. `~/.openclaw/openclaw.json` → `channels.telegram.botToken` (OpenClaw)

---

## Error Codes

| Exit Code | Meaning |
|-----------|---------|
| `0` | Success |
| `1` | Error — file not found, invalid token, network failure, rate limit, etc. |

Common errors and fixes:

| Error | Cause | Fix |
|-------|-------|-----|
| `File not found` | Wrong path or file deleted | Verify the file path |
| `Invalid bot token` | Wrong or revoked token | Get a new one from @BotFather |
| `Chat not found` | Bot not in chat or wrong ID | Add bot to chat |
| `Bot was blocked` | User blocked the bot | Ask them to `/start` the bot |
| `Rate limit exceeded` | Too many requests | Wait a few seconds and retry |
| `Network error` | Connection problem | Check internet connection |

---

## Supported File Types

| Type | Extensions | Telegram Method |
|------|-----------|-----------------|
| Images | PNG, JPG, GIF, WEBP, BMP, SVG | `sendPhoto` |
| Video | MP4, AVI, MOV, MKV, WEBM | `sendVideo` |
| Audio | MP3, OGG, WAV, M4A, FLAC | `sendAudio` |
| Documents | PDF, DOC, DOCX, TXT, XLS, ZIP | `sendDocument` |

File type is automatically detected from the extension.

---

## File ID Reuse

Once a file is sent, Telegram assigns a permanent `file_id`. You can reuse it to re-send without re-uploading:

```bash
# Get file_id from --verbose output, then:
python telegram_send_file.py --chat-id 5866004662 --file-id "AgADABC..."
```

> **Note:** File IDs are bot-specific — a file_id from one bot cannot be used with another bot.

---

## OpenClaw Integration

This script is designed to work seamlessly inside OpenClaw:

- When run from an OpenClaw Telegram session, `chat_id` and `topic_id` are **auto-detected** from `~/.openclaw/session-state.json`
- This means in most cases you just need `--file`
- Works great as a skill in OpenClaw's skill system

---

## License

MIT — use freely, modify as needed.
