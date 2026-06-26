---
name: telegram-bot
description: Create and manage Telegram bots. Use when user wants to build a Telegram bot for notifications, automation, customer support, group management, or interactive commands.
---

# Telegram Bot

Create and manage Telegram bots using the Bot API.

## Quick Start

```bash
# Get bot token from @BotFather on Telegram
# Create bot.py:
python scripts/bot.py --token YOUR_TOKEN --handler my_handler.py
```

## Bot Creation Steps

1. Open Telegram, search for @BotFather
2. Send /newbot to create new bot
3. Get API token
4. Configure webhooks or polling

## Core Features

- **Commands**: /start, /help, /settings
- **Callbacks**: Inline buttons, queries
- **Groups**: Admin tools, filters
- **Webhooks**: Receive updates via HTTP

## Script Usage

```bash
python scripts/bot.py [OPTIONS]

Options:
  --token TEXT        Bot API token (required)
  --handler PATH      Python handler file
  --webhook-url URL   Webhook endpoint URL
  --port PORT         Webhook server port (default: 8443)
  --poll              Use long polling instead of webhook
```

## Handler Format

```python
# my_handler.py
def handle_update(update, context):
    """Handle incoming updates."""
    if update.message:
        text = update.message.text
        if text == "/start":
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Hello! I'm your bot."
            )
```

## Examples

See `references/examples.md` for:
- Echo bot
- Inline keyboard bot
- Group admin bot
- Notification bot
- Weather bot
