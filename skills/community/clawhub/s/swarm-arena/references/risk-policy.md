# Risk Policy — references/risk-policy.md

Risk control is layered: sizing math first, hard gates second, kill rules
third. Every layer is enforced on every cycle, in every mode.

## Sizing math (`size_position.py`)

```
risk_usd           = equity × risk_pct_per_trade
stop_distance_pct  = |entry − stop| / entry
notional           = risk_usd / stop_distance_pct
notional           = min(notional, max_notional_per_trade)   # scale-down
margin             = notional / leverage
quantity           = floor_to_size_decimals(notional / entry)
notional           = quantity × entry                        # recompute post-rounding
```

Suppressed (no trade) when the result falls below the market's
`min_quote_amount` or `min_base_amount` — a position that small is fee noise.

Intuition: risking 1% of a $10,000 account ($100) with a 1.4% stop distance
implies `100 / 0.014 ≈ $7,143` of notional — which the
`max_notional_per_trade` cap then scales down to $500. The cap, not the stop
math, binds in most default-config trades; that is deliberate: risk-based
sizing says what the market setup *allows*, the cap says what the account
*permits*.

## Hard gates (`risk_checks.py`)

Blocks — any single failure vetoes the trade:

| Gate | Blocks when |
|---|---|
| `halt` | `state.halt` is true |
| `circuit_breaker` | `state.circuit_breaker` is true |
| `allow_short` | short signal and `allow_short: false` |
| `zero_notional` | notional or quantity ≤ 0 |
| `daily_loss_limit` | `state.daily_loss` ≥ `max_daily_loss` |
| `total_exposure` | current exposure + new notional > `max_total_exposure` |
| `per_trade_notional` | notional > `max_notional_per_trade` (post scale-down) |
| `available_margin` | required margin > account available margin |
| `stop_loss_required` | `require_stop_loss` and order lacks a stop |
| `take_profit_required` | `require_take_profit` and order lacks a target |

**Only limits set > 0 are enforced.** Setting `max_daily_loss: 0` disables
that gate (not recommended). `halt`, `circuit_breaker`, `allow_short`,
`zero_notional`, and the SL/TP requirements are always on.

## Kill rules

- **Daily loss limit**: realized losses accumulate into `state.daily_loss`
  (reset at UTC midnight). Hitting the limit blocks all new entries until the
  reset; open positions keep their protective brackets.
- **Circuit breaker**: 5 consecutive cycle errors trip it; every trading path
  refuses to run. Any clean cycle resets the counter to 0. Human `resume.py`
  required to clear the flag.
- **Halt**: operator-initiated (`halt.py`), sets both flags, optionally cancels
  orders and flattens. See `emergency-controls.md`.

## Margin-mode reality (Lighter)

Margin is cross at account level — there is no per-position isolation to set.
swarmArena replaces venue-side isolation with:

1. `max_notional_per_trade` + `max_total_exposure` client-side caps,
2. a mandatory **reduce-only** SL/TP bracket on every live trade (a bracket
   leg can never open a new position),
3. the daily-loss kill rule.

## No silent risk expansion

Learning can tighten but never loosen these bounds. Any future code change
that raises a limit must come from a human editing `config.json`, and
`validate_config.py` warns on aggressive values (risk > 5%, notional >
exposure cap).
