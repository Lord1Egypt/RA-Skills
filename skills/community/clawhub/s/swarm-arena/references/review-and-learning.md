# Review & Learning — references/review-and-learning.md

swarmArena learns from its own journal, within hard bounds. The loop runs on
the review cron (every 30 min) and inside the runner every 5 newly closed
trades.

## Stage 1 — outcomes (`fetch_trade_outcomes.py`)

Open journaled trades are resolved:

- **Live modes**: the position is gone from the account read → realized PnL is
  derived from `/api/v1/trades` (closing-direction fills after `opened_at`,
  matched against the journaled entry price; fallback: entry-vs-current-price
  delta).
- **Paper**: the current last price touching the recorded SL or TP closes the
  trade at that level.

Each close gets `outcome` (`win` / `loss` / `breakeven` at ±$0.01),
`close_reason`, `closed_at`, and feeds `state.daily_loss` when negative.

## Stage 2 — review (`review_trades.py`)

Over closed trades: win rate, avg/total PnL, current streak, longest losing
streak, per-symbol table, per-regime table, and **lesson tags** — heuristics
like "SOL repeatedly stopped out (4/5)" or "regime range net negative over 6
trades".

## Stage 3 — bounded adaptation (`update_metrics.py`)

| Metric | Tightens when | Recovers | Hard bounds |
|---|---|---|---|
| `confidence_multiplier` | losing streak ≥ 3 → −0.10 | +0.05 per profitable review | [0.70, 1.00] |
| `effective_leverage_cap` | losing streak ≥ 3 → −1 | +1 per profitable review | [min_leverage, max_leverage] |
| `recommended_min_confidence` | losing streak ≥ 3 → +0.05 | −0.05 per profitable review | [0.55, 0.75] |
| `underperforming_symbols` | per-symbol PnL ≤ −$100 | informational only | none (never blocks) |
| `lessons` | review lesson tags appended | capped at 20 kept | — |

Bounds are re-clamped after every update, so no code path — present or
future — can adapt past them.

## What learning can NEVER do

- raise leverage above `max_leverage`
- switch to a riskier mode
- remove or weaken SL/TP requirements
- suppress or edit journaling
- raise `max_daily_loss`, exposure, or notional caps
- set `autonomous_live_consent`

## How the adjustments bite

`trade_loop.py` applies them at entry time:

```
threshold            = max(base_threshold, metrics.recommended_min_confidence)
adjusted_confidence  = confidence × metrics.confidence_multiplier
leverage             = min(recommended, metrics.effective_leverage_cap)
```

All three adjustments only ever make entries harder or smaller. Recovery
toward neutral happens automatically after profitable reviews.

## Reading the journal for yourself

```bash
python3 scripts/review_trades.py config.json            # full stats
python3 scripts/review_trades.py config.json --hours 24 # daily digest
python3 scripts/journal_trade.py trades.json --last 10  # raw entries
```
