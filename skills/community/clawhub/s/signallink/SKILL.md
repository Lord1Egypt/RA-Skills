---
name: signallink
version: 1.0.0
description: Forward trading alerts and webhook events from TradingView to Telegram instantly. No subscriptions, no middlemen.
author: Shinzzyak
tags: ["tradingview", "telegram", "webhook", "trading", "signal", "fastapi", "alert"]
metadata:
  openclaw:
    requires:
      env:
        - TELEGRAM_BOT_TOKEN
        - TELEGRAM_CHAT_ID
      bins:
        - python3
        - docker
      optional_env:
        - WEBHOOK_SECRET
        - PORT
    primaryEnv: TELEGRAM_BOT_TOKEN
    emoji: "📡"
    homepage: https://github.com/Shinzzyak/SignalLink
---

# SignalLink — Webhook-to-Telegram Signal Router

A lightweight, open-source bridge that receives webhook alerts (e.g. from TradingView) and forwards them as clean, formatted messages to a Telegram bot. No paid services, no third-party subscriptions — just deploy and route.

## When To Use This Skill

Use SignalLink when the user wants to:
- Forward TradingView price alerts or strategy signals to Telegram
- Route any webhook event (uptime monitors, CI/CD pipelines, custom alerts) to Telegram
- Set up a self-hosted trading signal notification system
- Replace paid signal routing services with a free, open-source alternative

## Setup

### Step 1 — Get a Telegram Bot Token

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Copy the bot token — it looks like `123456789:ABCdef...`

### Step 2 — Get Your Chat ID

1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. It will reply with your Chat ID

### Step 3 — Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
WEBHOOK_SECRET=your_secret_here   # Optional but recommended
PORT=8000
```

### Step 4 — Run

**With Docker (recommended):**

```bash
docker compose up -d
```

**With Python:**

```bash
pip install -r requirements.txt
python -m App.main
```

Server starts at `http://localhost:8000`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Detailed health status |
| POST | `/webhook` | Main endpoint — auto-detects signal format |
| POST | `/webhook/raw` | Raw key-value formatter for generic alerts |

## Usage Instructions

When a user asks to forward trading signals or webhook alerts to Telegram:

1. Ask for their `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` if not already set
2. Guide them to set up the `.env` file using `.env.example` as a template
3. Start the server using Docker or Python
4. Point their webhook source (e.g. TradingView) to `http://<server-ip>:8000/webhook`
5. Optionally set `WEBHOOK_SECRET` and instruct the user to pass it as the `X-Webhook-Secret` header

## TradingView Integration

In TradingView, set the alert webhook URL to:

```
http://your-server-ip:8000/webhook
```

Set the alert message body to JSON:

```json
{
  "action":   "buy",
  "symbol":   "XAUUSD",
  "price":    "{{close}}",
  "interval": "{{interval}}",
  "strategy": "My Strategy",
  "sl":       "2330.00",
  "tp":       "2370.00",
  "lot":      "0.1",
  "message":  "Signal confirmed."
}
```

## Supported Payload Fields

| Field | Alias | Description |
|-------|-------|-------------|
| `action` | `signal` | Signal direction: `buy`, `sell`, `close`, `neutral` |
| `symbol` | `ticker` | Trading pair, e.g. `XAUUSD`, `EURUSD`, `BTCUSD` |
| `price` | `close` | Entry or current price |
| `interval` | `timeframe` | Chart timeframe, e.g. `1H`, `4H`, `1D` |
| `strategy` | `strategy_name` | Strategy name |
| `sl` | `stop_loss` | Stop loss level |
| `tp` | `take_profit` | Take profit level |
| `lot` | `quantity` | Lot size or quantity |
| `message` | `msg` | Custom note or description |

## Testing

Send a test webhook with curl:

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: your_secret_here" \
  -d '{
    "action": "buy",
    "symbol": "XAUUSD",
    "price": "2345.50",
    "interval": "1H",
    "sl": "2330.00",
    "tp": "2370.00"
  }'
```

## Example Telegram Output

```
🟢 BUY Signal

🥇 Pair:       XAUUSD
💰 Price:      2345.50
⏱️ Timeframe:  1H
🧠 Strategy:   EMA Crossover

🛑 Stop Loss:  2330.00
🎯 Take Profit: 2370.00
📦 Lot / Qty:  0.1

📝 Signal confirmed.

─────────────────────
⚡ Powered by SignalLink
```

## Project Structure

```
SignalLink/
├── App/
│   ├── main.py        # FastAPI entry point
│   ├── webhook.py     # Request handler & auth
│   ├── formatter.py   # Payload → Telegram message
│   ├── telegram.py    # Telegram Bot API client
│   └── config.py      # Environment config
├── Examples/
│   ├── tradingview_payload.json
│   └── custom_payload.json
├── .env.example
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Security Notes

- Always set `WEBHOOK_SECRET` in production to prevent unauthorized requests
- The secret is validated via constant-time comparison to prevent timing attacks
- Never expose your `TELEGRAM_BOT_TOKEN` publicly
