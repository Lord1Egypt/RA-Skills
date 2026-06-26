---
name: polymarket-copytrading
description: Build and run Polymarket copy-trading workflows (trader discovery, peak/decline cycle detection, candidate ranking, risk limits, and execution handoff). Use when user asks to follow高手/跟单, find top traders to copy, check whether traders are in peak form, or convert leaderboard data into executable copy-trade plans.
---

# Polymarket Copytrading

Create copy-trading plans from leaderboard data with strict risk controls.

## Workflow

1. Pull leaderboard snapshots from Data API (`OVERALL/POLITICS/CRYPTO` × `DAY/WEEK/MONTH/ALL`).
2. Score consistency (multi-period + multi-category presence).
3. Detect cycle phase (`巅峰` / `强势` / `观察`).
4. Output top 5 traders with wallet, rationale, and risk level.
5. Produce execution plan with hard limits (position size, max concurrent bets, daily stop).

## Commands

Use script:

```bash
python3 scripts/scan_copytraders.py --top 5
```

Optional category focus:

```bash
python3 scripts/scan_copytraders.py --categories OVERALL,CRYPTO --top 5
```

Auto monitor + threshold execution:

```bash
# dry-run once
python3 scripts/auto_copytrade.py --config references/auto-copytrade-config.example.json

# live execution loop (every 120s)
python3 scripts/auto_copytrade.py \
  --config references/auto-copytrade-config.example.json \
  --interval 120 \
  --execute
```

## Peak-phase rule (default)

- `巅峰`: DAY<=10 and WEEK<=10 and MONTH<=20
- `强势`: WEEK<=15 and MONTH<=30
- `观察`: MONTH<=20 but DAY>30
- else `普通`

## Risk template (small-account mode)

- Single bet <= 8 USDC
- Max concurrent positions = 2
- Stop for the day after 2 consecutive losses
- Start with 2 traders only; promote others after 20 observed signals

## Notes

- Prefer high-liquidity main markets; avoid noisy micro markets.
- If no clear edge exists, return `空仓等待` with next check time.
