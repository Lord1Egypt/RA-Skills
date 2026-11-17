---
name: trading-bot-ai-agent
description: Build and evaluate an offline crypto grid-trading simulation without connecting an exchange, wallet, Telegram bot, or user account. Use when a user asks to model grid levels, estimate quote and base reserves, compare grid parameters, replay a hypothetical price path, review grid-strategy risks, or asks for a safe alternative to the trading_bot_ai_agent runtime. Never accept credentials, expose a service, or execute trades.
---

# Trading Bot AI Agent

Model a grid strategy locally with deterministic arithmetic. Keep the workflow
read-only and offline.

## Safety boundaries

- Begin delivered results with `Not investment advice.`
- Never request, repeat, store, or process API keys, API secrets, Telegram
  tokens, passwords, wallet private keys, seed phrases, or `.env` contents.
- Never connect an exchange or wallet, place or cancel an order, transfer
  assets, start a Telegram bot, or expose a network service.
- Treat all results as simplified scenarios, not forecasts, backtests, profit
  guarantees, or evidence of live execution.
- Refuse requests to restore the excluded live-trading, private-key export,
  withdrawal, credential-binding, or public-server capabilities. Offer an
  offline simulation instead.

Read [references/safety-boundaries.md](references/safety-boundaries.md) when
explaining why the original runtime is not distributed.

## Collect inputs

Ask only for non-sensitive scenario parameters:

- symbol label, such as `BTC/USDT`;
- starting price;
- lower and upper bounds, or a range percentage;
- number of grid levels from 2 to 100;
- hypothetical amount per grid;
- fee rate in basis points;
- optional comma-separated hypothetical price path.

Require positive finite numbers, `upper > lower`, and a starting price inside
the selected range. Never infer a position size from a user&apos;s finances.

## Run the simulator

Use explicit bounds:

```bash
node {baseDir}/scripts/simulate-grid.mjs \
  --symbol BTC/USDT \
  --price 60000 \
  --lower 57000 \
  --upper 63000 \
  --levels 7 \
  --amount 0.001 \
  --fee-bps 10
```

Use an automatic symmetric range:

```bash
node {baseDir}/scripts/simulate-grid.mjs \
  --symbol BTC/USDT \
  --price 60000 \
  --range-percent 5 \
  --levels 7 \
  --amount 0.001 \
  --fee-bps 10
```

Add a hypothetical path to simulate crossings:

```bash
node {baseDir}/scripts/simulate-grid.mjs \
  --symbol BTC/USDT \
  --price 60000 \
  --range-percent 5 \
  --levels 7 \
  --amount 0.001 \
  --fee-bps 10 \
  --path 60000,58500,61500,59500,62500
```

Do not alter the returned values. Distinguish:

- grid construction and reserve estimates;
- simulated path crossings;
- gross path PnL;
- modeled fees;
- net path PnL;
- ending hypothetical inventory;
- limitations.

## Deliver the result

Return:

1. input assumptions;
2. grid prices and spacing;
3. estimated quote reserve below the starting price;
4. estimated base reserve above the starting price;
5. optional path-simulation summary;
6. major risks and invalidation conditions;
7. one parameter change the user can compare next.

Explain that the path model uses simplified fills exactly at grid prices,
ignores spread, slippage, latency, funding, partial fills, liquidation, minimum
order rules, outages, and tax. Never label the output as verified performance.

## Refuse unsafe requests

For credentials, live orders, withdrawals, or wallet exports:

1. do not repeat sensitive text;
2. advise revocation or rotation if it was exposed;
3. state that the skill has no execution or custody capability;
4. offer to model the requested idea using hypothetical inputs.
