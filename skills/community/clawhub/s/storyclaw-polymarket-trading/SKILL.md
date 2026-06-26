---
name: storyclaw-polymarket-trading
version: "0.1.0"
description: Self-evolving Polymarket trading bot. Design strategy with user, run paper trading, auto-improve until edge target met, then ask to switch to live.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯",
        "requires": { "bins": ["python3"], "env": ["POLYMARKET_PRIVATE_KEY"] },
        "primaryEnv": "POLYMARKET_PRIVATE_KEY",
      },
  }
---

# Polymarket Trading - Self-Evolving Trading Bot

Design a trading strategy with the user, run automated paper trading (dry-run), auto-improve parameters when underperforming, and ask permission to switch to live trading when edge target met.

Supports **any market type**: politics, sports, crypto prices, science, entertainment, etc.

## Critical Rules

1. NEVER default to any specific market — always ask user what they want to trade
2. NEVER show made-up prices or signals — only real script output
3. DRY RUN always on by default — only switch to live after explicit user confirmation
4. Auto-improve silently — adjust params and notify user
5. NEVER create a strategy or set up crons without explicit user confirmation

## Multi-User Support

Each user has their own `credentials/{USER_ID}.json`:

```json
{
  "private_key": "0x...",
  "funder_address": "0x...",
  "dry_run": true
}
```

Set `USER_ID` or `TELEGRAM_USER_ID` env var when calling scripts.

Or set `POLYMARKET_PRIVATE_KEY` env var.

## First-Time User Flow

### 1. Check credentials

```bash
USER_ID=$TELEGRAM_USER_ID python3 {baseDir}/scripts/polymarket.py check
```

If not configured, run interactive setup:

```bash
USER_ID=$TELEGRAM_USER_ID python3 {baseDir}/scripts/polymarket.py setup
```

### 2. Ask what they want to trade

Do NOT assume. Ask:

- What market type? (politics, sports, crypto, tech, etc.)
- Any specific keywords to focus on?

### 3. Propose strategy — WAIT FOR CONFIRMATION

Based on the conversation, derive and propose concrete values. Stop and wait for user to confirm before executing anything.

### 4. Create strategy (only after confirmation)

```bash
USER_ID=$TELEGRAM_USER_ID python3 {baseDir}/scripts/strategy_manager.py create --json '{
  "name": "<strategy name>",
  "market_filter": {
    "keywords": ["<keywords>"],
    "min_liquidity_usdc": 1000,
    "max_days_to_expiry": 30,
    "min_days_to_expiry": 1
  },
  "signal": {
    "method": "orderbook_imbalance",
    "params": { "threshold": 0.15, "max_entry_price": 0.60 }
  },
  "sizing": { "max_size_usdc": 5 },
  "targets": { "min_sample_size": 30, "min_edge": 0.05 }
}'
```

### 5. Set up crons

```bash
SKILL_PATH={baseDir}
STRATEGY_ID=<id from step 4>

# Signal scan: every 15 minutes
(crontab -l 2>/dev/null; echo "*/15 * * * * USER_ID=$TELEGRAM_USER_ID python3 $SKILL_PATH/scripts/signal_cron.py $STRATEGY_ID >> $SKILL_PATH/state/$TELEGRAM_USER_ID.$STRATEGY_ID.log 2>&1") | crontab -

# Performance review: daily at 09:00 UTC
(crontab -l 2>/dev/null; echo "0 9 * * * USER_ID=$TELEGRAM_USER_ID python3 $SKILL_PATH/scripts/review_cron.py $STRATEGY_ID >> $SKILL_PATH/state/$TELEGRAM_USER_ID.review.log 2>&1") | crontab -
```

## Strategy Lifecycle

```
dry_run → improving → pending_live → live
```

Go-live condition: `edge = win_rate - avg_entry_price >= min_edge` AND `total_pnl > 0`

## Strategy Management

```bash
USER_ID=$TELEGRAM_USER_ID python3 {baseDir}/scripts/strategy_manager.py status
USER_ID=$TELEGRAM_USER_ID python3 {baseDir}/scripts/strategy_manager.py review <strategy_id>
USER_ID=$TELEGRAM_USER_ID python3 {baseDir}/scripts/strategy_manager.py activate-live <strategy_id>
```

## Auto-Improvement Rules

| Condition                    | Action                                       |
| ---------------------------- | -------------------------------------------- |
| edge < min_edge - 10%        | Raise threshold (fewer but stronger signals) |
| edge < min_edge - 3%         | Lower max_entry_price (cheaper entries)      |
| 3+ adjustments still failing | Notify user to reconsider                    |
| edge >= min_edge AND pnl > 0 | Mark pending_live, notify user               |

## Signal Methods

| Method              | Best for                                |
| ------------------- | --------------------------------------- |
| orderbook_imbalance | Any liquid market with active orderbook |

New methods can be added to `scripts/signals.py`.

## Troubleshooting

| Error                        | Solution                                            |
| ---------------------------- | --------------------------------------------------- |
| py-clob-client not installed | `pip3 install py-clob-client`                       |
| USER_ID not set              | Add `USER_ID=xxx` prefix                            |
| No config found              | Run `python3 {baseDir}/scripts/polymarket.py setup` |
| API Error 401                | Re-run setup to re-derive keys                      |
| No markets found             | Broaden keywords or lower min_liquidity_usdc        |

## File Structure

```
polymarket-trading/
├── SKILL.md
├── scripts/
│   ├── strategy_manager.py   # Lifecycle: create/review/status/activate-live
│   ├── signal_cron.py        # Cron: scan markets, run signals, record trades
│   ├── review_cron.py        # Cron: daily review + auto-improve
│   ├── signals.py            # Pluggable signal methods
│   ├── market_scanner.py     # Gamma API market discovery
│   └── polymarket.py         # CLOB API primitives
├── credentials/
│   └── {USER_ID}.json
├── strategies/
│   └── {USER_ID}/{strategy_id}.json
└── state/
    └── {USER_ID}.{strategy_id}.perf.json
```
