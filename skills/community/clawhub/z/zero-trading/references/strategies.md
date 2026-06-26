# strategy reference

detailed profiles for all 9 zero trading strategies.
values sourced from `scanner/v6/strategies/*.yaml` — the engine's canonical configs.

**note on consensus**: consensus scores (e.g. 5/7, 7/7) refer to the 7 quantitative layers. however, Layer 8 (LLM reasoning) can veto even a perfect 7/7 mechanical setup if it detects narrative risk, anomalous conditions, or context the quantitative layers miss. a 7/7 consensus is necessary but not sufficient — the LLM layer has final say.

## watch

- **risk**: none
- **stops**: n/a
- **max positions**: 0
- **duration**: 48 hours
- **plan**: free (score_minimum: 0)
- **scope**: top 50 coins
- **best when**: uncertain markets, learning the engine, observation mode
- **description**: pure observation. the engine evaluates all markets but takes no positions. use to learn how the engine thinks before committing capital.
- **evaluation threshold**: 5/7 consensus (but max_positions=0, so no entries)
- **position sizing**: n/a
- **reserve**: 100%

## defense

- **risk**: low
- **stops**: 2%
- **max positions**: 3
- **duration**: 168 hours (7 days)
- **plan**: free (score_minimum: 0)
- **scope**: top 20 coins
- **best when**: protecting capital, sideways markets, post-loss recovery
- **description**: capital preservation. tight stops, small positions, only the highest conviction setups. the engine's conservative mode.
- **evaluation threshold**: 6/7 consensus minimum
- **position sizing**: 7% of equity per position
- **max drawdown**: 6% (3 positions x 2% stop)
- **daily loss cap**: 3%
- **reserve**: 35%

## funding

- **risk**: low
- **stops**: 2%
- **max positions**: 4
- **duration**: 48 hours
- **plan**: pro (score_minimum: 5.0)
- **scope**: top 50 coins
- **best when**: funding rates are paying, sideways-to-trending markets
- **description**: funding rate harvester. enters positions where funding rates pay the holder. requires 6/7 consensus — tight filter to avoid noise. exits when funding signal disappears.
- **evaluation threshold**: 6/7 consensus minimum
- **position sizing**: 8% of equity per position
- **max drawdown**: 8% (4 positions x 2% stop)
- **daily loss cap**: 3%
- **reserve**: 30%
- **special**: entry_end_action=close (exits when signal disappears, unlike other strategies that hold)

## momentum

- **risk**: medium
- **stops**: 3%
- **max positions**: 5
- **duration**: 48 hours
- **plan**: free (score_minimum: 0)
- **scope**: top 50 coins
- **best when**: clear directional trends, 3+ coins trending same direction, default choice
- **description**: the bread and butter. follows established trends with medium conviction. most forgiving strategy for new operators. the engine's default recommendation.
- **evaluation threshold**: 5/7 consensus minimum
- **position sizing**: 10% of equity per position
- **max drawdown**: 15% (5 positions x 3% stop)
- **daily loss cap**: 5%
- **reserve**: 20%

## scout

- **risk**: medium
- **stops**: 3%
- **max positions**: 5
- **duration**: 72 hours
- **plan**: pro (score_minimum: 4.0)
- **scope**: top 200 coins (widest universe)
- **best when**: wide opportunity set, many coins approaching threshold, patient scanning
- **description**: patient wide-net scanner. monitors top 200 markets and enters when any coin breaks through. good when no single trend dominates but many coins are approaching.
- **evaluation threshold**: 5/7 consensus minimum
- **position sizing**: 10% of equity per position
- **max drawdown**: 15% (5 positions x 3% stop)
- **daily loss cap**: 5%
- **reserve**: 20%

## fade

- **risk**: medium
- **stops**: 3%
- **max positions**: 4
- **duration**: 168 hours (7 days)
- **plan**: scale (score_minimum: 6.0)
- **scope**: top 50 coins
- **best when**: mean reversion setups, overextended moves, regime=reverting
- **description**: contrarian. enters against extended moves when reversion signals align. requires regime layer to show reverting or stable. mean reversion takes time — long hold period.
- **evaluation threshold**: 5/7 consensus + regime must show reverting or stable
- **position sizing**: 10% of equity per position
- **max drawdown**: 12% (4 positions x 3% stop)
- **daily loss cap**: 5%
- **reserve**: 25%
- **special**: regime_shift_exit=true (exits if regime shifts to trending — fade thesis broken)

## sniper

- **risk**: high
- **stops**: 4%
- **max positions**: 3
- **duration**: 72 hours
- **plan**: scale (score_minimum: 5.0)
- **scope**: top 20 coins (narrow — only deepest books)
- **best when**: rare perfect setups (7/7 consensus), low frequency but high conviction
- **description**: precision mode. only enters on perfect 7/7 consensus. very few trades. when it fires, conviction is maximum. large position sizing because all 7 layers agree — that's the edge.
- **evaluation threshold**: 7/7 consensus required (all layers must pass)
- **position sizing**: 18% of equity per position
- **max drawdown**: 12% (3 positions x 4% stop)
- **daily loss cap**: 8%
- **reserve**: 22%
- **special**: min_regime=[trending] only — strictest regime filter

## degen

- **risk**: high
- **stops**: 6%
- **max positions**: 4
- **duration**: 24 hours
- **plan**: pro (score_minimum: 6.0)
- **scope**: top 100 coins
- **best when**: fast-moving markets, short hold periods, experienced operators
- **description**: aggressive short-duration. wider stops, larger positions, faster rotation. accepts more regimes (trending, stable, reverting). for operators who understand the risk and want exposure to fast moves.
- **evaluation threshold**: 5/7 consensus minimum
- **position sizing**: 15% of equity per position
- **max drawdown**: 24% (4 positions x 6% stop)
- **daily loss cap**: 10%
- **reserve**: 15%
- **special**: regime_shift_exit=false (rides through regime shifts)

## apex

- **risk**: extreme
- **stops**: 8%
- **max positions**: 4
- **duration**: 168 hours (7 days)
- **plan**: scale (score_minimum: 7.0)
- **scope**: top 100 coins
- **best when**: maximum conviction, expert operators only, specific high-confidence setups
- **description**: maximum aggression. widest stops, largest positions. all levers wide open. a $100 account can lose $32 in one cycle. adaptive — trades any regime. only for experienced operators who fully understand the downside.
- **evaluation threshold**: 6/7 consensus minimum
- **position sizing**: 18% of equity per position
- **max drawdown**: 32% (4 positions x 8% stop)
- **daily loss cap**: 15%
- **reserve**: 8%
- **special**: regime_shift_exit=false, min_regime=[trending, stable, reverting] — adaptive

## strategy quick reference

| strategy | tier | stops | positions | duration | size/pos | drawdown | daily cap | scope | threshold |
|---|---|---|---|---|---|---|---|---|---|
| watch | free | — | 0 | 48h | — | — | — | top 50 | 5/7 |
| defense | free | 2% | 3 | 168h | 7% | 6% | 3% | top 20 | 6/7 |
| funding | pro | 2% | 4 | 48h | 8% | 8% | 3% | top 50 | 6/7 |
| momentum | free | 3% | 5 | 48h | 10% | 15% | 5% | top 50 | 5/7 |
| scout | pro | 3% | 5 | 72h | 10% | 15% | 5% | top 200 | 5/7 |
| fade | scale | 3% | 4 | 168h | 10% | 12% | 5% | top 50 | 5/7 |
| sniper | scale | 4% | 3 | 72h | 18% | 12% | 8% | top 20 | 7/7 |
| degen | pro | 6% | 4 | 24h | 15% | 24% | 10% | top 100 | 5/7 |
| apex | scale | 8% | 4 | 168h | 18% | 32% | 15% | top 100 | 6/7 |

## strategy selection matrix

| market condition | primary | alternative |
|---|---|---|
| clear trend (3+ coins same direction) | momentum | scout |
| wide opportunity (5+ coins approaching) | scout | momentum |
| rare perfect setups (1-2 at 7/7) | sniper | momentum |
| nothing above 4/7 | defense | watch |
| extreme fear (F&G < 20) | momentum/fade | degen |
| extreme greed (F&G > 80) | defense | watch |
| sideways + funding paying | funding | defense |
| fast moves, short timeframe | degen | momentum |
| maximum conviction, expert | apex | sniper |

## drive modes

all strategies support 3 drive modes:

| mode | notifications | approval | heat push | approaching |
|---|---|---|---|---|
| comfort | entry, exit, brief, circuit_breaker | no | none | no |
| sport | + approaching, heat_shift, regime_shift | no | every 2h | yes |
| track | + eval_candidate | yes (5 min timeout) | every 1h | yes |

## evolved variants

strategies can evolve via the backtest-evolve loop. mutations (±10-20% on risk params) are backtested against 30 days. if a mutation beats the current config's Sharpe ratio by 0.05+, it's saved to evolved_configs/ with status "pending_approval".

check `zero_get_evolution_status` for pending approvals.

evolved configs preserve the strategy's identity (name, tier, scope) but adjust risk parameters (stop, position size, reserve, daily cap).

## co-evolution

strategies are also stress-tested via adversarial co-evolution. 5 attack scenarios (flash crash, funding spike, regime shift, correlation spike, liquidity drought) test survival. weak strategies get automatic tightening.
