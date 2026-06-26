---
name: zero-strategy-selection
description: "choose the right trading strategy based on market conditions and operator history."
---

# strategy selection

before recommending a strategy, check 2 inputs:

## 1. market conditions

call `zero_get_heat`. if heat returns empty (count=0), fall back: call `zero_evaluate` on BTC, ETH, SOL, AVAX, DOGE individually.

also call `zero_get_approaching` for coins near threshold.

use CONSENSUS and DIRECTION from evaluations, not regime labels. the engine can show 5/9 SHORT even in "random_quiet" regime — trust the consensus number.

| market signal | recommend |
|---|---|
| 3+ coins at 5/9+ with same direction | momentum (clear trend, bread and butter) |
| 5+ coins at 4/9+ (many approaching) | scout (wide scan, patient) |
| 1-2 coins at 6/9+ (rare setups only) | sniper (precision, few trades) |
| 0 coins above 4/9 | defense or watch (nothing worth trading) |
| fear & greed < 20 with 3+ coins SHORT | momentum or fade (fear = opportunity) |
| fear & greed > 80 | defense (overheated, reversals likely) |

## 2. operator history

call `zero_session_history`.
- which strategies performed best for this operator?
- win rate by strategy?
- favor what works for THEM, not what's theoretically optimal.
- if no history: recommend momentum (default, most forgiving).

## handling errors

- if `zero_get_heat` returns `count: 0`: evaluate BTC, ETH, SOL, AVAX, DOGE individually. use those results.
- if `zero_session_history` returns `count: 0`: no history yet. recommend momentum.
- if any tool returns an error: tell the operator what failed. do not guess or hallucinate data.

## plan gating

not all strategies are available on all plans:

| plan | strategies |
|---|---|
| free | momentum, defense, watch |
| pro | + degen, scout, funding |
| scale | + sniper, fade, apex (all 9) |

if the operator asks for a locked strategy: "Degen needs Pro plan. try Momentum (free) or upgrade."

## recommendation format

always give: recommendation + reasoning + alternative.

"market favors momentum. 6 coins trending short, funding shorts pay.
your momentum win rate: 72%.
alternative: defense if you want to protect capital."

never just say "use momentum." explain WHY for this operator, this market, right now.

## the 9 strategies

| strategy | risk | stops | positions | best when |
|---|---|---|---|---|
| watch | none | — | 0 | uncertain, learning |
| defense | low | 2% | 3 max | protecting capital |
| funding | low | 2% | 4 max | funding rates are paying |
| momentum | medium | 3% | 5 max | clear trends, default choice |
| scout | medium | 3% | 5 max | wide scan, patient |
| fade | medium | 3% | 4 max | mean reversion, contrarian |
| sniper | high | 4% | 3 max | perfect setups only (9/9) |
| degen | high | 6% | 4 max | fast moves, short hold |
| apex | extreme | 8% | 4 max | maximum conviction, expert only |

## evolved variants

some strategies have evolved versions with improved parameters. check `zero_get_evolution_status` before recommending. if an evolved variant exists:
"evolved momentum available. sharpe improved 1.2 → 1.6. approve to promote?"

evolved variants are discovered through backtesting and must be approved by the operator before they replace the base strategy.

## strategy generation

the engine can generate new strategies for uncovered market conditions. if no existing strategy fits the current regime well, check whether the engine has proposed a new strategy via `zero_get_evolution_status`. new strategies go through the same approval flow as evolved variants.

## auto-pilot recommendation

before manual recommendation, offer auto-pilot as first option:

"based on current regime and your history, engine recommends [strategy]. [reason]."

call `zero_auto_select` to get the engine's recommendation. show:
- recommended strategy with confidence score
- regime context (what the market looks like)
- operator stats (their WR with this strategy)
- alternatives with scores

if operator accepts: deploy via `zero_start_session`.
if operator overrides: proceed with manual strategy selection above.

auto-pilot uses:
1. regime direction (SHORT/LONG/MIXED/QUIET) -> strategy affinity
2. fear & greed modifiers (extreme fear boosts degen, extreme greed boosts defense)
3. volatility modifiers (extreme vol boosts defense, low vol boosts funding)
4. operator history (WR > 65% boosts, WR < 35% penalizes)
5. plan gating (free/pro/scale limits available strategies)
