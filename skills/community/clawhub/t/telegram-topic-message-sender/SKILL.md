---
name: telegram-topic-message-sender
description: Wrap sending a Telegram message to a fixed topic into one script call. Use when user wants to quickly send notifications/messages to a specific Telegram topic by running a script.
---

# Telegram Topic Message Sender

This skill packages Telegram topic messaging into a reusable script.
It now uses `openclaw message send` directly (no bot token env required).

## What it does

- Send a message to a Telegram supergroup topic (`message_thread_id`)
- Supports fixed defaults (chat/topic) so daily use can be one command
- Uses OpenClaw CLI `openclaw message send`

## Script

- Path: `scripts/send-topic-message.sh`

## Required env

- None (uses your configured OpenClaw channel auth)

## Optional defaults

- `TG_DEFAULT_CHANNEL`: default channel (default `telegram`)
- `TG_DEFAULT_CHAT_ID`: default chat id (e.g. `-1003574630717`)
- `TG_DEFAULT_TOPIC_ID`: default topic id (e.g. `96`)

## Usage

```bash
# 1) Use defaults from env (recommended)
export TG_DEFAULT_CHANNEL='telegram'
export TG_DEFAULT_CHAT_ID='-1003574630717'
export TG_DEFAULT_TOPIC_ID='96'

bash skills/telegram-topic-message-sender/scripts/send-topic-message.sh "测试消息"

# 2) Override target on call
bash skills/telegram-topic-message-sender/scripts/send-topic-message.sh \
  --channel telegram \
  --chat-id -1003574630717 \
  --topic-id 96 \
  "部署完成，已上线 ✅"
```

## Notes

- Bot must be in the target group and have permission to post.
- If topic id is wrong, Telegram will return an error.
- This script only sends plain text; markdown/html parse mode is intentionally not enabled to reduce formatting failures.
