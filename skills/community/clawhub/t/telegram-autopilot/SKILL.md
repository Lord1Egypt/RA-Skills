---
name: telegram-autopilot
description: Manage a Telegram userbot autopilot that responds to private messages as the user using AI. Use when the user wants to set up auto-replies on their personal Telegram account, manage allowed contacts, configure AI response style, or send messages/media as themselves. Triggers on "telegram autopilot", "auto reply telegram", "manage my telegram", "respond for me", "telegram userbot", "paid media telegram". Requires secrets — Telegram API credentials (api_id, api_hash), phone number, optional 2FA password, AI provider API key (Anthropic or OpenAI-compatible), optional Telegram bot token for owner notifications.
---

# Telegram Autopilot

> **Source:** https://github.com/Shor73/telegram-autopilot
> **Author:** [@Shor73](https://github.com/Shor73)
> **License:** MIT

AI-powered autopilot for personal Telegram accounts. Responds to private messages as the user when they're unavailable.

## Prerequisites

- Python 3.10+
- Telethon: `pip3 install telethon`
- Telegram API credentials (api_id + api_hash from https://my.telegram.org)
- An Anthropic API key (for AI responses)

## Setup

### 1. Get Telegram API Credentials

Direct the user to https://my.telegram.org → API Development Tools → create app.
They need: **API ID** (number) and **API Hash** (string).

### 2. Login Flow

Telegram login requires: phone → OTP code → optional 2FA password.

**Critical:** OTP codes expire in ~60 seconds. Minimize latency:
- Use a file-based code exchange (script polls a file every 200ms)
- Or serve a simple web form on a local port for instant code entry
- Never rely on chat round-trip for code delivery — too slow

Run `scripts/setup.py` with the user's credentials. It handles:
1. Requesting the OTP code
2. Waiting for code via file (`enter_code.txt`)
3. 2FA password if needed
4. Saving the session file

```bash
python3 scripts/setup.py --api-id 12345 --api-hash "abc123" --phone "+1234567890"
```

The session file (`.session`) persists auth — login is one-time only.

### 3. Configure Contacts

Edit `config.json` to define allowed contacts:

```json
{
  "contacts": {
    "username": {
      "name": "Display Name",
      "id": 123456789,
      "tone": "friendly",
      "language": "en"
    }
  },
  "ai": {
    "provider": "anthropic",
    "model": "claude-sonnet-4-6",
    "api_key": "sk-ant-...",
    "max_tokens": 300
  },
  "owner": {
    "name": "Owner Name",
    "bio": "Brief description for the AI persona",
    "telegram_id": 123456789
  },
  "notifications": {
    "bot_token": "optional-bot-token-for-notifications",
    "chat_id": "optional-chat-id"
  }
}
```

### 4. Start Autopilot

```bash
python3 scripts/autopilot.py --config config.json --session session_name
```

## Features

### Auto-Reply
- Responds only to allowed contacts in private chats
- Marks messages as read before replying (natural behavior)
- Simulates typing delay proportional to response length
- Maintains conversation history for context

### AI Persona
- System prompt configurable per-contact (tone, language)
- Never invents facts — says "I'll check and get back to you" for unknowns
- Never reveals it's AI

### Notifications
- Forwards received messages to owner via Telegram bot
- Forwards sent replies for monitoring

### Paid Media (Channels Only)
Telegram paid media (`inputMediaPaidMedia`) only works in channels, not private chats.

To send paid media:
1. Create a private channel
2. Post media with `InputMediaPaidMedia(stars_amount=N, extended_media=[...])`
3. Generate invite link and send to recipient

```bash
python3 scripts/send_paid_media.py --session session_name --target username --photo /path/to/photo.jpg --stars 1
```

### Management Commands

Stop autopilot: kill the process or send SIGTERM.
Add/remove contacts: edit `config.json` and restart.

## Architecture

```
telegram-autopilot/
├── SKILL.md
├── scripts/
│   ├── setup.py          — Login flow (OTP + 2FA)
│   ├── autopilot.py      — Main event loop
│   ├── send_paid_media.py — Paid media via channel
│   └── code_server.py    — Web form for fast OTP entry
└── references/
    └── telegram-auth.md  — Telegram auth flow documentation
```

## Required Credentials

| Secret | Purpose | Where used |
|---|---|---|
| Telegram API ID + Hash | MTProto client auth | `setup.py`, `autopilot.py` |
| Phone number + 2FA | Account login (one-time) | `setup.py` |
| AI API key | Response generation | `autopilot.py` |
| Bot token (optional) | Owner notifications | `autopilot.py` |

All secrets are stored in `config.json` — **never commit this file**.

## Security & Ethics

- **Session security:** The `.session` file grants full access to the account. Protect it like a password.
- **Transparency:** The AI is instructed to be honest if directly asked whether it's AI.
- **OTP server:** `code_server.py` binds to `127.0.0.1` (localhost only). Never expose it to the network.
- **Notifications:** The skill can forward messages to the owner via bot. Ensure you control the bot token and chat_id.
- **Rate limits:** Telegram may restrict accounts with aggressive automation. The autopilot uses natural delays.
- **One session at a time:** Only one process can use a session file. Stop autopilot before running other scripts.
- **Platform policies:** Using a userbot to auto-reply may violate Telegram ToS. Use at your own risk.
