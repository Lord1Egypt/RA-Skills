# Confluence Model — references/confluence-model.md

`compute_confluence.py` is the second gate after the signal score. A signal
says "direction looks right"; confluence asks "do the details line up well
enough to risk money?"

## The 9 checks

| # | Check | Passes when |
|---|---|---|
| 1 | `trend_alignment` | 4h trend **and** 1h trend both match the signal direction |
| 2 | `momentum_confirmation` | 1h momentum sign matches direction |
| 3 | `volume_confirmation` | 1h volume_ratio ≥ **0.75** |
| 4 | `rsi_zone` | long: 40 ≤ RSI ≤ 70 · short: 30 ≤ RSI ≤ 60 |
| 5 | `macd_alignment` | 1h MACD histogram sign matches direction |
| 6 | `reward_risk_ok` | |TP − entry| / |entry − SL| ≥ `min_reward_risk` (default 1.5) |
| 7 | `exposure_capacity_ok` | exposure **after** this trade < 90% of `max_total_exposure` |
| 8 | `position_capacity_ok` | open positions < `max_concurrent_positions` |
| 9 | `timeframe_confluence` | 5m trend or 5m price-vs-EMA20 agrees with direction |

`confidence = passed / 9`. Entry requires **≥ 0.55** (i.e. at least 5 of 9),
raised to **0.70** (7 of 9) under high volatility.

Note the wider RSI zone than the signal stage (40–70 vs 45–68 for longs):
the signal stage wants a *good* reading, confluence merely rejects *bad* ones.

## Bracket math (feeds check 6)

Stops and targets come from the 1h ATR:

```
long:   SL = entry − 1.5 × ATR     TP = entry + 2.5 × ATR
short:  SL = entry + 1.5 × ATR     TP = entry − 2.5 × ATR
```

Natural reward:risk = 2.5 / 1.5 ≈ **1.67**, comfortably above the default
`min_reward_risk` of 1.5. A setup only fails check 6 when something overrides
the ATR bracket (nothing in the default pipeline does).

## Context inputs

Confluence needs live account context, supplied by `market_scan_from_lighter.py`:

| Context key | Source |
|---|---|
| `entry_price`, `stop_loss`, `take_profit` | ATR bracket from 1h features |
| `min_reward_risk` | config |
| `current_exposure` | Σ |quantity × entry_price| over `state.known_open_positions` |
| `max_total_exposure`, `max_concurrent_positions` | config |
| `proposed_notional` | sizing output |
| `open_positions` | len(`state.known_open_positions`) |

Checks 7–8 treat zero/unset limits as "disabled" (consistent with
`risk_checks.py` — only limits set > 0 are enforced).

## Output contract

```json
{
  "passed": ["trend_alignment", "..."],
  "failed": ["volume_confirmation"],
  "count": 8, "total": 9, "confidence": 0.8889,
  "min_confidence": 0.55, "high_volatility": false,
  "direction": "long", "enter": true,
  "reason": "confluence 0.889 >= 0.55"
}
```

The same dict lands in every journal entry's `confluence` field, so the
review loop can later answer "which checks fail most often before losers?"
