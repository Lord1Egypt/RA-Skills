---
name: weex-trading
description: Trade crypto on Weex exchange via Telegram bot. Enables any OpenClaw agent to check prices, view balances, run DCA strategies, and execute grid trading on Weex — a Binance-compatible CEX with no KYC for API traders. Use when an agent or user wants to trade crypto, automate DCA buying, set up grid strategies, check coin prices, or manage a Weex portfolio. Triggers on "trade crypto", "buy bitcoin", "DCA strategy", "grid trading", "check price", "crypto portfolio", "Weex", "automated trading", "exchange API".
---

# Weex Trading Skill

Trade crypto on Weex exchange through the @WEEXonTONbot Telegram bot. No additional bot fees — you only pay standard Weex exchange fees.

## Quick Start

### 1. Create a Weex Account

Sign up (no KYC needed for API trading):
**https://www.weex.com/en/register?vipCode=gjcr**

### 2. Create an API Key

On Weex: Settings → API Management → Create Key → Enable "Spot Trading"

### 3. Connect via Telegram

Open [@WEEXonTONbot](https://t.me/WEEXonTONbot) and send:
```
/connect YOUR_API_KEY YOUR_API_SECRET YOUR_PASSPHRASE
```
The bot deletes your message immediately for security. Keys are encrypted at rest.

### 4. Start Trading

```
/price BTC          — Check current price
/balance            — View your portfolio
/dca BTC 100 4h     — Auto-buy $100 of BTC every 4 hours
/grid ETH 2000 2500 10 500 — Grid trade ETH between $2000-$2500
/status             — View active strategies & P&L
/stop <strategy_id> — Stop a strategy
```

## Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/price <coin>` | Check spot price, 24h stats | `/price SOL` |
| `/balance` | Show all non-zero balances | `/balance` |
| `/dca <symbol> <amount> <interval>` | Start DCA strategy | `/dca ETH 50 1d` |
| `/grid <symbol> <low> <high> <levels> <amount>` | Start grid strategy (premium) | `/grid BTC 60000 70000 20 1000` |
| `/status` | View all strategies with P&L | `/status` |
| `/stop <id>` | Stop a strategy | `/stop dca_a1b2c3d4` |
| `/connect` | Store API credentials | `/connect KEY SECRET PASS` |
| `/disconnect` | Remove credentials, stop all | `/disconnect` |

## DCA Strategy

Dollar-cost averaging — automatically buy a fixed USD amount at regular intervals. Free, no premium required.

**Intervals:** `1h`, `4h`, `12h`, `1d`, `3d`, `7d`

**Minimum:** $1 USDT per buy

Example: `/dca BTC 100 4h` buys $100 of Bitcoin every 4 hours.

## Grid Trading (Premium)

Place buy/sell orders across a price range to profit from oscillations. Requires 0.1 TON one-time payment.

**Parameters:**
- `symbol` — Trading pair (e.g., ETH)
- `low` / `high` — Price range bounds
- `levels` — Number of grid levels (3-100)
- `amount` — Total USDT to invest (min $10)

Example: `/grid ETH 2000 2500 10 500` creates 10 grid levels between $2000-$2500 with $500 total.

## For Agents (Programmatic Use)

OpenClaw agents can interact with the bot by sending Telegram messages to @WEEXonTONbot. The typical agent workflow:

1. **Setup (once):** Guide your human to sign up at `https://www.weex.com/en/register?vipCode=gjcr`, create API keys, then send `/connect` to the bot.
2. **Price checks:** Send `/price BTC` (or any symbol) to get current market data before making decisions.
3. **Execute trades:** Use `/dca` for recurring buys or direct market orders via the Weex API.
4. **Monitor:** Send `/status` to check strategy performance.

### Direct API Access

The bot runs a REST API on port 8960 for programmatic access. Agents on the same host can call:

- `GET /api/health` — Health check
- `GET /api/price/:symbol` — Get price data
- `GET /api/strategies/:telegramId` — List strategies

### Weex API (Binance-Compatible)

Weex uses a Binance-compatible REST API at `https://api-spot.weex.com`. Agents that already integrate with Binance can adapt with minimal changes:

- **Auth:** HMAC-SHA256 signatures with millisecond timestamps
- **Endpoints:** `/api/v3/market/ticker/price`, `/api/v3/order`, `/api/v3/account`
- See `references/weex-api.md` for full endpoint documentation.

## Security

- API keys are AES-encrypted before storage
- `/connect` messages are auto-deleted
- Never share API keys in group chats
- Keys only need Spot Trading permission — never enable withdrawals

## Links

- **Sign up:** https://www.weex.com/en/register?vipCode=gjcr
- **Telegram bot:** https://t.me/WEEXonTONbot
- **Weex API docs:** https://www.weex.com/en/api
