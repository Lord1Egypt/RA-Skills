# Leverage Policy — references/leverage-policy.md

## Lighter has no leverage endpoint

Unlike Binance-style APIs, Lighter exposes **no `set_leverage` call and no
per-position margin mode**. Margin is cross at account level. Therefore in
swarmArena leverage is purely a **client-side sizing cap**:

```
effective_leverage = notional / margin
margin = notional / leverage   ← sizing uses this
```

Nothing about leverage is ever sent to the exchange. The venue sees only
integer size and price. The leverage number controls how much of your
collateral a position may consume relative to its notional.

## Recommendation ladder (`recommend_leverage.py`)

| Confidence | Leverage |
|---|---|
| < 0.60 | `min_leverage` |
| 0.60 – 0.79 | midpoint of [min, max], rounded |
| ≥ 0.80 | `max_leverage` |
| high volatility | −1 (floor: `min_leverage`) |
| learning cap | min(result, `metrics.effective_leverage_cap`) |

Example with defaults (2–10): confidence 0.72 → midpoint 6; high volatility →
5; learning cap 4 → **4**.

## Learning interaction (bounded)

`update_metrics.py` can only move `effective_leverage_cap` **down** (losing
streak ≥ 3 → −1, floored at `min_leverage`) and back **up** toward
`max_leverage` (+1 per profitable review, never above). The config ceiling is
absolute:

```
effective_leverage_cap ≤ max_leverage   ← enforced after every adaptation
```

## Why not just always use max leverage?

Because margin is cross: an oversized position endangers the whole account,
not just itself. The client-side cap plus `max_notional_per_trade`,
`max_total_exposure`, and the mandatory reduce-only bracket together replace
the missing venue-side margin controls.

## Operator guidance

- Keep `max_leverage` at or below what the market's
  `default_initial_margin_fraction` implies (Lighter reports it per market in
  basis points of a percent; 500 ⇒ 20× ceiling at the venue). The agent's cap
  must be the stricter of the two.
- If you lower `max_leverage` in config, the learning cap follows on the next
  review (it is clamped to the new bound).
