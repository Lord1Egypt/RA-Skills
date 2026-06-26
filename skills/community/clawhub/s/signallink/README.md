# 📡 Webhook-to-Telegram Signal Router

> Lightweight, open-source bridge for forwarding trading alerts and webhook events directly to Telegram — no subscriptions, no middlemen.

---

## ✨ Features

- 🔔 Receives webhooks from **TradingView**, uptime monitors, CI/CD pipelines, or any custom source
- 📨 Formats alerts into clean, readable **Telegram messages** with emojis, markdown, and risk info
- 🔐 Optional **webhook secret** validation to protect your endpoint
- 🐳 **Docker-ready** — deploy in seconds with `docker compose up`
- ⚡ Built on **FastAPI** — async, fast, and production-grade
- 🛠️ Fully **configurable via `.env`** — no code changes needed

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Shinzzyak/webhook-to-telegram.git
cd webhook-to-telegram
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
WEBHOOK_SECRET=your_secret_here   # Optional but recommended
```

> **How to get your Bot Token:** Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot`  
> **How to get your Chat ID:** Message [@userinfobot](https://t.me/userinfobot) on Telegram

### 3. Run with Docker (Recommended)

```bash
docker compose up -d
```

### 3b. Or Run Locally with Python

```bash
pip install -r requirements.txt
python -m app.main
```

Server starts at `http://localhost:8000`

---

## 📬 Sending a Webhook

### TradingView Alert Setup

In TradingView, set your alert **Webhook URL** to:

```
http://your-server-ip:8000/webhook
```

Set the **Alert Message** to JSON format:

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
  "message":  "EMA crossover confirmed."
}
```

If you configured a `WEBHOOK_SECRET`, add this header in TradingView:

```
X-Webhook-Secret: your_secret_here
```

---

## 📊 Supported Payload Fields

| Field | Alias | Description |
|-------|-------|-------------|
| `action` | `signal` | Signal direction: `buy`, `sell`, `close`, etc. |
| `symbol` | `ticker` | Trading pair, e.g. `XAUUSD`, `EURUSD` |
| `price` | `close` | Current or entry price |
| `interval` | `timeframe` | Chart timeframe, e.g. `1H`, `4H` |
| `strategy` | `strategy_name` | Strategy name |
| `sl` | `stop_loss` | Stop loss level |
| `tp` | `take_profit` | Take profit level |
| `lot` | `quantity` | Lot size or quantity |
| `message` | `msg` | Custom note or description |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/health` | Detailed health status |
| `POST` | `/webhook` | Main endpoint — auto-detects signal format |
| `POST` | `/webhook/raw` | Raw key-value formatter for non-trading alerts |

---

## 📁 Project Structure

```
webhook-to-telegram/
├── app/
│   ├── main.py        # FastAPI entry point
│   ├── webhook.py     # Incoming request handler & auth
│   ├── formatter.py   # Payload → Telegram message formatter
│   ├── telegram.py    # Telegram Bot API client
│   └── config.py      # Environment config loader
├── examples/
│   ├── tradingview_payload.json
│   └── custom_payload.json
├── .env.example
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 🧪 Testing Locally

Send a test webhook with `curl`:

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: your_secret_here" \
  -d '{
    "action": "buy",
    "symbol": "XAUUSD",
    "price": "2345.50",
    "interval": "1H",
    "strategy": "EMA Crossover",
    "sl": "2330.00",
    "tp": "2370.00"
  }'
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

Made with ❤️ by [Shinzzyak](https://github.com/Shinzzyak)

</div>
