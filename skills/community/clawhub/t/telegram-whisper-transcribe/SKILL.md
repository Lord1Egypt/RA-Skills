---
name: telegram-whisper-transcribe
description: Standalone Telegram bot for voice message transcription via OpenAI Whisper API. No LLM overhead — audio goes directly to Whisper and text comes back in 2-5 seconds. Use when you want a dedicated Telegram bot that only transcribes voice messages, audio files, and video notes without routing through an LLM agent. Supports automatic language detection, runs as a systemd user service, and costs only Whisper API pricing ($0.006/min).
env_vars:
  - name: TELEGRAM_BOT_TOKEN
    description: Telegram Bot API token from @BotFather
    required: true
  - name: OPENAI_API_KEY
    description: OpenAI API key for Whisper transcription
    required: true
---

# Telegram Whisper Transcribe

Standalone Telegram bot for fast voice transcription. Bypasses LLM orchestration entirely — Telegram audio goes straight to OpenAI Whisper API and the transcript comes back as a reply.

## Why standalone?

OpenClaw routes audio through an LLM agent that then calls Whisper via tool use. That adds 10-30s latency and LLM token costs per transcription. This bot eliminates both — direct API call, 2-5s response time.

## Requirements

- Python 3.12+
- Telegram Bot Token (from @BotFather)
- OpenAI API Key (for Whisper)

## Setup

### 1. Install

```bash
mkdir -p ~/transcribe-bot
cp {baseDir}/scripts/bot.py ~/transcribe-bot/
python3 -m venv ~/transcribe-bot/venv
~/transcribe-bot/venv/bin/pip install python-telegram-bot openai
```

### 2. Configure systemd service

```bash
{baseDir}/scripts/install.sh <telegram-bot-token> <openai-api-key>
```

Or manually:

```bash
# Create environment file with secrets (restricted permissions)
cat > ~/transcribe-bot/.env << EOF
TELEGRAM_BOT_TOKEN=<your-token>
OPENAI_API_KEY=<your-key>
EOF
chmod 600 ~/transcribe-bot/.env

# Create systemd service
cat > ~/.config/systemd/user/transcribe-bot.service << EOF
[Unit]
Description=Telegram Transcribe Bot (Whisper API)
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=$HOME/transcribe-bot/venv/bin/python3 $HOME/transcribe-bot/bot.py
Restart=always
RestartSec=5
EnvironmentFile=$HOME/transcribe-bot/.env

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable transcribe-bot
systemctl --user start transcribe-bot
```

### 3. Verify

```bash
systemctl --user status transcribe-bot
```

## Features

- Voice messages, audio files, and video notes
- Automatic language detection
- Transcript as direct reply to the original message
- No LLM tokens consumed — only Whisper API ($0.006/min audio)
- Auto-restart via systemd

## Manage

```bash
systemctl --user status transcribe-bot
systemctl --user restart transcribe-bot
journalctl --user -u transcribe-bot -f
```

## OpenClaw integration note

If you already have OpenClaw running with a Telegram channel, use a **separate** Telegram bot token for this service. Do not reuse the same bot token — Telegram only allows one poller per bot.
