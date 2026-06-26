---
name: telegram-md-uploader
description: Uploads and sends .md files from your OpenClaw workspace to a specific Telegram chat using the Telegram Bot API. Use when you need to share workspace files (e.g., drafts, code, content) with a Telegram recipient.
---

# Telegram MD Uploader

This skill enables you to send markdown files directly from your workspace to a Telegram chat.

## Prerequisites

1.  **Telegram Bot Token**: You need a bot token from [@BotFather](https://t.me/BotFather).
2.  **Chat ID**: You need the Chat ID for the recipient (the bot must be a member of the chat).

## Setup & Usage

### 1. Configure Environment Variables
To keep your credentials secure, set your tokens in your shell environment (e.g., add to `.bashrc` or `.zshrc`):

```bash
export TELEGRAM_BOT_TOKEN='your_token_here'
export TELEGRAM_CHAT_ID='your_chat_id_here'
```

### 2. Usage
Run the script directly from your terminal:

```bash
python3 scripts/upload.py <file_path.md>
```

## How It Works

This skill utilizes the Telegram Bot API `sendDocument` method. It takes the file path, validates that it is a `.md` file, wraps it in a POST request with `multipart/form-data`, and sends it to your specified chat.

## Troubleshooting

- **Error: TELEGRAM_BOT_TOKEN... must be set**: Verify your environment variables are exported.
- **Error: File not found**: Double-check the file path.
- **Error: Not a valid .md file**: Ensure the file ends with the `.md` extension.
