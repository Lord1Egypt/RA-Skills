# Telegram Autopilot — OpenClaw Skill

> 🐾 An [OpenClaw](https://openclaw.ai) skill that turns your AI agent into a Telegram autopilot.

AI-powered autopilot for personal Telegram accounts. Your OpenClaw agent responds to private messages as you when you're unavailable — like a smart secretary that knows your style.

## Install via ClawHub

```bash
clawhub install telegram-autopilot
```

Or manually: copy this folder into your OpenClaw workspace `skills/` directory.

## Features

- 🤖 **AI Auto-Reply** — Responds naturally using Claude, GPT, Llama, or any OpenAI-compatible model
- 📖 **Read Receipts** — Marks messages as read before replying (looks natural)
- ⌨️ **Typing Simulation** — Shows "typing..." proportional to response length
- 🔒 **Contact Whitelist** — Only responds to contacts you approve
- 📩 **Owner Notifications** — Forwards every message and reply to you via bot
- 💫 **Paid Media** — Send photos that require Telegram Stars to unlock (via channels)
- 🧠 **Conversation Memory** — Maintains context across messages

## Quick Start

### 1. Install

```bash
pip3 install telethon
```

### 2. Get Telegram API Credentials

Go to https://my.telegram.org → API Development Tools → Create app.
Note your **API ID** and **API Hash**.

### 3. Login

```bash
# Start the code entry web server (optional, for fast OTP)
python3 scripts/code_server.py --port 19997 &

# Run setup
python3 scripts/setup.py \
  --api-id YOUR_API_ID \
  --api-hash "YOUR_API_HASH" \
  --phone "+1234567890" \
  --password "your_2fa_password"  # optional
```

Enter the OTP code via the web form at `http://localhost:19997` or write it to `enter_code.txt`.

### 4. Configure

Create `config.json`:

```json
{
  "contacts": {
    "johndoe": {
      "name": "John Doe",
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
    "name": "Your Name",
    "bio": "Developer, coffee lover",
    "telegram_id": 123456789
  },
  "notifications": {
    "bot_token": "your-bot-token",
    "chat_id": "your-chat-id"
  }
}
```

**Tone options:** `friendly`, `formal`, `brief`
**Language:** Any ISO code (`en`, `it`, `es`, `fr`, `de`, etc.)

### 5. Run

```bash
python3 scripts/autopilot.py \
  --config config.json \
  --session user \
  --api-id YOUR_API_ID \
  --api-hash "YOUR_API_HASH"
```

### 6. Paid Media (Optional)

Send a photo that requires Stars to view:

```bash
python3 scripts/send_paid_media.py \
  --session user \
  --api-id YOUR_API_ID \
  --api-hash "YOUR_API_HASH" \
  --target johndoe \
  --photo /path/to/photo.jpg \
  --stars 5
```

> Note: Telegram only allows paid media in channels. The script automatically creates a private channel, posts the media, and sends the invite link to the target.

## AI Providers

### Anthropic (Claude)
```json
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-6",
  "api_key": "sk-ant-..."
}
```

### OpenAI-compatible (GPT, Llama, Mistral, etc.)
```json
{
  "provider": "openai",
  "model": "gpt-4o",
  "api_key": "sk-...",
  "base_url": "https://api.openai.com/v1/chat/completions"
}
```

## How It Works

1. Listens for incoming private messages via Telegram MTProto API
2. Checks if sender is in the whitelist
3. Marks message as read (✓✓)
4. Waits 2 seconds (human-like delay)
5. Generates response via AI with conversation context
6. Shows typing indicator
7. Sends response
8. Notifies owner

## Security & Ethics

- **Session files** grant full account access — keep them private
- **Never commit** `config.json` (contains API keys) or `.session` files
- **OTP server** binds to `127.0.0.1` only — never expose it to the network
- **Transparency:** If someone directly asks if they're talking to AI, the bot is honest
- **Notifications** forward messages to the owner — ensure you control the bot token
- Telegram may restrict accounts with aggressive automation — natural delays are built in
- Only one process can use a session file at a time
- Using a userbot may violate Telegram ToS — use at your own risk

## What is OpenClaw?

[OpenClaw](https://openclaw.ai) is an open-source AI agent platform that connects to your messaging apps (Telegram, Discord, WhatsApp, etc.) and runs skills autonomously. This skill extends your OpenClaw agent with Telegram userbot capabilities.

- 🌐 [OpenClaw Website](https://openclaw.ai)
- 📖 [OpenClaw Docs](https://docs.openclaw.ai)
- 🛠️ [ClawHub Skills](https://clawhub.com)
- 💬 [Discord Community](https://discord.com/invite/clawd)

## License

MIT
