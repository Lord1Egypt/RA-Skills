---
name: stock-monitor-fixed
description: Use when building a manual stock watchlist, defining alert thresholds, or documenting a repeatable monitoring routine with public market data.
tags: [stock, finance, monitor, alerts, tracking, portfolio, real-time]
version: 1.0.1
---

# Stock Monitor

This skill helps design a repeatable monitoring workflow. It does not ship a background daemon, alert bot, or proprietary market-data service.

## When to use

- You want a watchlist for holdings or names you are considering.
- You need threshold rules for price moves, volume spikes, or gap opens.
- You want a simple routine for checking public market data and recording follow-up actions.

## Suggested workflow

1. Build a watchlist.
   Record ticker, market, thesis, baseline price, and the event you care about.
2. Define alert thresholds.
   Examples: percentage move, break above resistance, break below support, or unusual volume.
3. Decide the review cadence.
   Intraday, daily close, weekly review, or earnings-only monitoring.
4. Record observations.
   Note what changed, whether the thesis still holds, and what action should happen next.

## Example watchlist template

```json
{
  "watchlist": [
    {
      "ticker": "AAPL",
      "market": "NASDAQ",
      "baseline_price": 190.0,
      "alert_rules": [
        "price moves more than 5% from baseline",
        "close breaks above previous 20-day high"
      ],
      "review_notes": "Watch the next earnings call and hardware guidance."
    }
  ]
}
```

## Good outputs

- A clean watchlist
- Explicit threshold rules
- Review cadence
- Notes for what to do when a rule triggers

## Guardrails

- Treat all public quotes as delayed or vendor-dependent unless verified.
- Do not claim that automatic alerts were sent unless an actual notification system exists.
- Keep records of thresholds and rationale so later reviews are comparable.
- This skill is for monitoring and planning, not for trade execution.
