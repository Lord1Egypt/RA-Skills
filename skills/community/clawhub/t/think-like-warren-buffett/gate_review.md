# Buffett Oracle — Gate Review

*Last updated: 2026-03-26*

## Why This Exists

Backtest accuracy headlines are not enough.
The more important question is: **which gates are filtering real junk, and which gates are systematically causing false negatives?**

Generate the live snapshot with:

```bash
python3 oracle.py gate-review
```

## Current Reading

Across the current archived set, the false negatives are not evenly distributed.
They cluster around two gates:

- `Gate 2 (FCF / Net Income)`
- `Gate 6 (Earnings Yield)`

The current expansion-track false negatives are:

- `PTR_2003.json`
- `WMT_2005.json`
- `BUD_2005.json`
- `MCO_2001.json`
- `COST_1999.json`
- `DVA_2011.json`

Those misses imply:

1. `Gate 2` is too blunt when raw free cash flow is depressed by **value-creating reinvestment** rather than by weak economics.
2. `Gate 6` is too blunt when a business is an **elite asset-light tollbooth** or a **dense recurring-service oligopoly** and the market persistently pays up for that quality.

As of the current archive snapshot:

- `Framework-wrong cases`: `6`
- `Gate 2` false-negative hits: `3`
- `Gate 6` false-negative hits: `4`

## Gate-by-Gate View

### Gate 1 — Normalized ROE / ROIC

No current evidence says this hurdle is causing false negatives.
Keep it hard.

### Gate 2 — FCF / Net Income

This gate is useful, but the raw version confuses two things:

- bad cash conversion
- heavy but productive reinvestment

Going forward, every `Gate 2` fail should include an **owner earnings note**:

- What portion of capex looks maintenance-like?
- What portion looks like expansion capex that may still create value?
- Is the business still genuinely capital hungry even after that adjustment?

### Gate 3 — Leverage

No current false negatives are coming from this gate.
Balance-sheet discipline remains non-negotiable.

### Gate 4 — Structural Revenue Decline

This gate still looks sensible.
It is not currently the source of false negatives.

### Gate 5 — Gross Margin Trend

This is a secondary deterioration check, not a primary stock picker.
Low signal, but not obviously broken.

### Gate 6 — Earnings Yield

The current `6%` floor is a conservative default, not a law of nature.
It is missing some businesses where:

- moat quality is exceptional
- incremental capital needs are low
- balance-sheet risk is low
- the business sits inside market infrastructure, category leadership, or a recurring-service oligopoly with durable local density

Going forward, every `Gate 6` fail on a clear-moat business should include a **quality multiple note**:

- Is the market paying for genuine durability or for hype?
- Is the low yield justified by asset-light compounding?
- Is this a strategic-buyer story, a compounding story, a recurring-service density story, or just overpayment?

### Gate 7 — Moat

This remains the strongest qualitative gate.
So far it is rejecting weak businesses without showing up as a clear source of false negatives.

## Operating Rule

For now, the project keeps the 7 hard gates unchanged so the benchmark remains comparable over time.

But new live and expansion memos should now do two extra checks:

1. Add an **owner earnings note** whenever `Gate 2` fails.
2. Add a **quality multiple note** whenever `Gate 6` fails on a high-moat business.
