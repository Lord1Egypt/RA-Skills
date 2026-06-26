---
name: skill-woocommerce-stock-monitor
version: 1.0.0
description: Monitor WooCommerce products for out-of-stock changes and send Telegram alerts. Run daily via cron.
metadata:
  openclaw:
    requires: { bins: ["node"] }
---

# skill-woocommerce-stock-monitor v1.0.0

Monitor WooCommerce products for out-of-stock changes and send Telegram alerts. Tracks instock → outofstock transitions and alerts your team daily.

## Usage

```bash
node scripts/stock-monitor.js
```

## Configuration

Set via environment variables:

| Variable | Default | Description |
|---|---|---|
| `WOO_API_PATH` | `~/woo-api.json` | Path to WooCommerce API credentials JSON |
| `TELEGRAM_BOT_TOKEN` | — | Telegram bot token for alerts |
| `TELEGRAM_CHAT_ID` | — | Telegram chat/group ID to send alerts to |

### woo-api.json format

```json
{
  "url": "https://your-store.com",
  "consumer_key": "ck_...",
  "consumer_secret": "cs_..."
}
```

## Cron setup

```bash
# Run daily at 07:00 UTC
0 7 * * * TELEGRAM_BOT_TOKEN=xxx TELEGRAM_CHAT_ID=yyy node /path/to/scripts/stock-monitor.js
```

## Behavior

- **First run:** Sends a baseline report of all currently OOS products
- **Subsequent runs:** Only alerts on new instock → outofstock transitions
- **State file:** Saved to `memory/stock-state.json` (tracks previous run)

## Alerts

- `📦 Stock Monitor — Baseline Report` — first run summary
- `⚠️ Stock Alert — Out of Stock` — when products go OOS
