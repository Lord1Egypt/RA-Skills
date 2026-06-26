---
name: telegram-send-file
description: Send local files, URLs, or reusable Telegram file_ids into a Telegram chat via Bot API. Use when the task is to deliver a file to Telegram, especially from inside an OpenClaw Telegram session where chat_id and topic/thread_id can often be auto-detected. Do not use for normal chat replies; use OpenClaw's built-in message routing for that.
---

# Telegram Send File

Use this skill for **file delivery to Telegram**, not for ordinary chat messages.

## Scope

- Send a local file to Telegram
- Send a file by URL or existing Telegram `file_id`
- Reuse the current OpenClaw Telegram session context when available
- Send one file or a batch of files into a chat/topic

## Do not use this skill for

- Normal assistant replies in the current chat
- Cross-session messaging between OpenClaw sessions
- Rich Telegram bot workflows beyond file delivery

## Core commands

```bash
# Use current OpenClaw Telegram context when available
python3 scripts/telegram_send_file.py --file document.pdf

# Explicit target
python3 scripts/telegram_send_file.py --chat-id -1001234567890 --topic-id 3 --file screenshot.png

# Batch mode (preserves topic/thread)
python3 scripts/telegram_send_file.py --files a.pdf b.png --caption "Batch delivery"

# Send by URL or prior Telegram file_id
python3 scripts/telegram_send_file.py --url https://example.com/report.pdf
python3 scripts/telegram_send_file.py --file-id AQAD...
```

## Workflow

1. If running inside an OpenClaw Telegram session, try auto-detected `chat_id` and `topic_id` first.
2. If auto-detection is unavailable, pass `--chat-id` and optionally `--topic-id`.
3. For local files, let the script choose the Telegram method from file extension.
4. For URL and `file_id` sends, default to document delivery unless you intentionally extend the script.
5. Use batch mode for sequential delivery when multiple files should go to the same destination.

## Notes

- Auto-detection is best-effort, not guaranteed in every runtime context.
- Local-file type detection is more precise than URL / `file_id` sending.
- For Telegram Bot API details and limits, see `references/api_reference.md`.
