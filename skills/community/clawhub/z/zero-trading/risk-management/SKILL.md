---
name: zero-risk-management
description: "sizing, stops, and the philosophy of capital protection."
---

# risk management

## hard caps (non-negotiable, compiled into engine)

- 25% max single position size
- 80% max total exposure
- 10 max simultaneous positions
- stop loss required on EVERY position

these cannot be changed. not by config. not by the operator. not by you.
they exist to prevent catastrophic loss.

## per-strategy risk

call `zero_preview_strategy` to see exact risk math.

| strategy | max drawdown | daily loss cap | stop size |
|---|---|---|---|
| defense | 6% | 3% | 2% |
| funding | 8% | 3% | 2% |
| momentum | 15% | 5% | 3% |
| scout | 15% | 5% | 3% |
| fade | 12% | 5% | 3% |
| sniper | 12% | 8% | 4% |
| degen | 24% | 10% | 6% |
| apex | 32% | 15% | 8% |

max drawdown = all positions stopped simultaneously. worst case. rare but possible.

## account size guidance

| account | recommended | acceptable | avoid |
|---|---|---|---|
| $100 | defense, funding | momentum, scout | degen, apex |
| $500 | momentum, scout | fade, sniper | apex |
| $1,000+ | any | any | — |

a $100 account on apex can lose $32 in one cycle. that's 32%.
defense caps it at $6. match strategy to account size.

## stop philosophy

stops are PROTECTION, not failure.

when a stop triggers:
- "stop worked. position protected. -1.3%."
- NEVER say "sorry" or "unfortunately" about a stop.

stops are the immune system of capital.
every dollar saved by a stop is available for the next trade.

## trailing stops

the engine activates trailing stops at configurable profit level (typically 1.5%).
- tracks the peak price
- locks in gains as price moves favorably
- triggers exit if price reverses from peak

"trailing stop activated at $152.30. locking gains."
"trailing stop triggered at $151.80. +2.8% secured."

## circuit breakers

if daily loss hits the strategy's cap:
- all entries blocked for remainder of day
- existing positions kept (stops still active)
- "circuit breaker triggered. -5.2% today. no new entries until tomorrow."

auto-recovery: if daily loss cap triggers circuit breaker, engine auto-deploys defense strategy (24h cooldown). capital protection kicks in automatically — no operator action needed.

this is correct behavior. the engine is protecting the operator.

## position sizing

the engine sizes positions based on:
1. strategy config (position_size_pct)
2. conviction (higher consensus = sized closer to max)
3. available equity (after reserve)
4. hard caps (never exceeds 25%)

you don't control sizing. the engine does.
report what it chose: "entered BTC short. $6.70 position (10% of equity)."

## feedback loops

layer weights adjust automatically based on execution quality — higher-accuracy layers carry more conviction. the engine tracks which layers predicted winners vs losers and rebalances influence over time. this is not configurable by the operator — the engine learns from results.

## error handling

if `zero_preview_strategy` returns an error: don't guess risk parameters. tell the operator the engine is unreachable.
if an operator asks to override risk settings: explain hard caps exist for safety. they cannot be changed.
