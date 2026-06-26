# 🔍 Simmer Resolution Tracker

Every trade you place either wins or loses. This skill makes sure you find out immediately — logs the outcome, posts the alert, redeems the winnings on-chain — automatically, every 5 minutes. Without it you're flying blind on outcomes and leaving money on the table. Set it up once and forget it.

## Live Demo

```
🔍 Simmer Resolution Tracker — 2026-03-14 04:10 UTC
   Mode: LIVE
  📦 4 resolved positions (active=12, resolved=4)

  💰 Will BTC close above $85k today? | btc_momentum | +$18.42
    💰 Attempting redemption...
    ✅ Redeemed (tx: 0xabc123def456...)
  ❌ Will ETH hit $3,800 this week? | eth_midcandle | -$12.00
  💰 Will SOL close above $180 today? | sol_momentum | +$7.31
    💰 Attempting redemption...
    ✅ Redeemed (tx: 0x789fed012345...)
  ❌ Will XRP hit $2.50 this week? | xrp_momentum | -$5.00

  📊 4 new resolution(s) processed
  💰 2 position(s) redeemed | Total: $25.73
```

## Quick Start

### 1. Install
```bash
pip install simmer-sdk
```

### 2. Configure
```bash
export SIMMER_API_KEY=your_api_key
export WALLET_PRIVATE_KEY=your_wallet_key
export DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
```

### 3. Run
```bash
python resolution_tracker.py
```

Runs automatically via cron every 5 minutes. Done.

## What It Does

- **Polls resolved positions** every 5 minutes via Simmer API
- **Matches to original trade journal entry**, updates with outcome + PnL
- **Posts Discord alert** (WIN 💰 / LOSS ❌) with strategy name and P&L
- **Auto-redeems winning positions** on-chain via Simmer SDK
- **Writes to `resolved_trades.jsonl`** — append-only audit log
- **Dedupes** — never processes the same resolution twice
- **Tracks cooldowns** — records consecutive losses per strategy

## Files It Manages

| File | Purpose |
|------|---------|
| `trade_journal.jsonl` | Updated with resolved/outcome/pnl on resolution |
| `resolved_trades.jsonl` | Append-only audit log of all resolutions |
| `resolved_markets.json` | IDs already reported (dedup) |
| `redeemed_markets.json` | IDs already redeemed on-chain |
| `cooldown_state.json` | Consecutive loss tracking per strategy |

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SIMMER_API_KEY` | ✅ | — | Your Simmer API key |
| `WALLET_PRIVATE_KEY` | ✅ | — | Polymarket wallet private key for redemptions |
| `DISCORD_WEBHOOK` | No | — | Discord webhook URL for win/loss alerts |
| `POLY_MODE` | No | `live` | Set to `sim` to skip on-chain redemptions |
| `DATA_DIR` | No | `./data/live` | Override data directory path |

## CLI Reference

```bash
# Run once manually
python resolution_tracker.py

# Simulation mode (no on-chain redemptions)
POLY_MODE=sim python resolution_tracker.py

# Custom data directory
DATA_DIR=./data/backtest python resolution_tracker.py
```

Runs automatically via cron every 5 minutes when installed as a skill.

## Tips

- **`POLY_MODE=sim`** skips on-chain redemptions — safe for testing without touching the chain
- **If you miss a resolution window**, it'll catch up on the next run — the dedup set prevents double-processing
- **Discord webhook is optional** but highly recommended — you want to know immediately when a trade resolves
- **Budget limits** protect you: max 6 redemptions per run, 120-second time cap
- **Sweep mode** catches older redeemable positions you might have missed

## Troubleshooting

**"Trade not matched in journal"**
→ Resolution ran before the trade was logged. Not an error — will retry next run.

**"Redemption failed"**
→ Check `WALLET_PRIVATE_KEY` is correct and wallet has gas for the transaction.

**"No DISCORD_WEBHOOK"**
→ Alerts are silently skipped, not an error. Set the webhook when you're ready.

**"Success but no tx_hash"**
→ SDK reported success but couldn't confirm the transaction. Will retry next run automatically.

**"Budget limit reached"**
→ Hit the 6-redemption or 120-second cap. Remaining positions deferred to next run.

---

Built for [Simmer](https://www.simmer.markets/) — the AI trading agent platform for Polymarket.
