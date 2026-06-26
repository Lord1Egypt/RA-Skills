---
name: skill-crypto-threshold-watcher
description: Monitor any crypto token against configurable price/volume thresholds. Fires alerts when entry conditions are met. Use when you need proactive notification that a watchlist token has crossed its threshold — not reactive price checks. Supports multiple tokens, multiple threshold types (price above/below, volume spike), and custom alert messages.
---

# Crypto Threshold Watcher

Proactive alert engine for any token on any exchange. Checks watchlist against configurable thresholds and fires signals.

## Watchlist Config

Stored at: `~/.openclaw/workspace/trading/watchlist.json`

```json
{
  "tokens": [
    {
      "symbol": "GRASSUSDT",
      "exchange": "binance",
      "thresholds": {
        "price_above": 0.30,
        "price_below": 0.20,
        "volume_24h_above": 50000000
      },
      "notes": "AI data network — entry above $0.30"
    },
    {
      "symbol": "FETUSDT",
      "exchange": "binance",
      "thresholds": {
        "price_above": 0.20,
        "volume_24h_above": 100000000
      },
      "notes": "ASI Alliance token — volume spike = breakout signal"
    }
  ]
}
```

## Usage

### Check all watchlist tokens
```bash
node ~/.openclaw/workspace/scripts/trading/threshold-watcher.js
```

### Add a token to watchlist
```bash
node ~/.openclaw/workspace/scripts/trading/threshold-watcher.js --add --symbol BTCUSDT --price-above 90000
```

### Check single token
```bash
node ~/.openclaw/workspace/scripts/trading/threshold-watcher.js --symbol ETHUSDT
```

## Output

When threshold is crossed:
```
🚨 THRESHOLD ALERT — GRASSUSDT
  Price: $0.3245 (threshold: $0.30 ↑)
  Volume 24h: $62.3M
  Signal: ENTRY — price above threshold
  Time: 2026-03-17 18:30 UTC
  Notes: AI data network — entry above $0.30
```

When no threshold crossed:
```
✅ GRASSUSDT — $0.28 (below $0.30 threshold, watching)
```

## Data Sources

- Primary: Binance API (no auth required for market data)
- Fallback: CoinGecko API (free tier)

## Cron Integration

Add to TASKS.md cron:
```
Every 1h: node scripts/trading/threshold-watcher.js
```

Alerts delivered to Telegram DM automatically.

## Threshold Types

| Type | Field | Description |
|------|-------|-------------|
| Price breakout | `price_above` | Price crosses above level |
| Price breakdown | `price_below` | Price drops below level |
| Volume spike | `volume_24h_above` | 24h volume exceeds threshold |
| RSI overbought | `rsi_above` | RSI > value (requires OHLC data) |
| RSI oversold | `rsi_below` | RSI < value |

## Integration with Trading Pipeline

This skill feeds signals to:
- `backtest-expert` — validate signal before acting
- `skill-trading-journal` — log signal + decision
- `binance-pro` — execute if approved
