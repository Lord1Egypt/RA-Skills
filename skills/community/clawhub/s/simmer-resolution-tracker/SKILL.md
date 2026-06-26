---
name: simmer-resolution-tracker
description: Monitors your Simmer positions for resolutions, logs wins/losses to your trade journal, and automatically redeems winning positions on-chain. Built for Simmer agents trading on Polymarket. Sends Discord webhook alerts on every resolution. Runs every 5 minutes via cron.
metadata:
  author: "DjDyll"
  version: "1.1.0"
  displayName: "Simmer Resolution Tracker"
  difficulty: "intermediate"
---

# Simmer Resolution Tracker

Every trade you place either wins or loses. This skill makes sure you find out immediately — logs the outcome, posts the alert, redeems the winnings on-chain — automatically, every 5 minutes. Set it up once and forget it.

> **This is a template.** Point it at your trade journals, set your Discord webhook, and the skill watches for you. It polls Simmer for resolved positions, matches them back to your journal entries, computes PnL, and handles on-chain redemptions. You bring the trades — it closes the loop.

## Setup

### 1. Install dependencies
```bash
pip install simmer-sdk
```

### 2. Set environment variables
```bash
export SIMMER_API_KEY=your_api_key
export WALLET_PRIVATE_KEY=your_wallet_key
export DISCORD_WEBHOOK=https://discord.com/api/webhooks/...  # optional
```

### 3. Run it
```bash
python resolution_tracker.py
```

That's it. Cron handles the rest — every 5 minutes, automatically.

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SIMMER_API_KEY` | ✅ | — | Your Simmer API key |
| `WALLET_PRIVATE_KEY` | ✅ | — | Polymarket wallet private key for on-chain redemptions |
| `DISCORD_WEBHOOK` | No | — | Discord webhook URL for win/loss alerts |
| `POLY_MODE` | No | `live` | Set to `sim` to skip on-chain redemptions |
| `DATA_DIR` | No | `./data/live` | Override data directory path |

## Quick Commands

```bash
# Run once manually
python resolution_tracker.py

# Dry run (no redemptions)
POLY_MODE=sim python resolution_tracker.py

# Custom data directory
DATA_DIR=./data/backtest python resolution_tracker.py
```

## Example Output

```
[2026-03-14 04:10 UTC] Checking positions...
Found 2 newly resolved markets

✅ WIN  btc_momentum — Will BTC close above $85k today?
        Outcome: YES | Shares: 147.3 | PnL: +$18.42
        Redeemed on-chain: 0xabc...def
        Discord alert sent ✓

❌ LOSS eth_midcandle — Will ETH hit $3,800 this week?
        Outcome: NO | Cost: $12.00 | PnL: -$12.00
        Discord alert sent ✓

Processed: 2 resolutions | 1 redeemed | 0 errors
```

## Troubleshooting

**Trade not matched in journal** — The resolution ran before the trade was logged. Not an error — the tracker will retry on the next run and match it then.

**WALLET_PRIVATE_KEY not set** — Redemptions will fail. The tracker still logs resolutions and posts Discord alerts — you just won't get automatic on-chain redemptions.

**Discord webhook errors** — Check the URL is valid and the webhook hasn't been deleted. Alerts are best-effort — webhook failures don't block resolution processing.

**POLY_MODE=sim** — Skips all on-chain redemptions. Use this for testing or when you want resolution tracking without touching the chain.
