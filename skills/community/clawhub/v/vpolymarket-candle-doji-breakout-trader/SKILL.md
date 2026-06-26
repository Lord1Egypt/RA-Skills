---
name: polymarket-candle-doji-breakout-trader
description: Detects doji patterns (48-52% probability) in crypto 5-minute interval markets on Polymarket and trades the post-doji breakout in the direction of the pre-doji trend. In candlestick analysis a doji after a directional trend signals indecision before a breakout -- the next interval tends to continue the prior trend direction. Targets BTC, ETH, SOL, and XRP Up or Down bundles with conviction-based position sizing.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Candle Doji Breakout Trader
  difficulty: advanced
---

# Candle -- Doji Breakout Trader

> **This is a template.**
> The default signal detects doji patterns in crypto 5-minute interval markets and trades the post-doji breakout using conviction-based sizing. The skill handles all the plumbing (interval parsing, doji detection, trend analysis, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists 5-minute interval markets for BTC, ETH, SOL, and XRP: "Will Bitcoin be Up or Down in the 10:50AM-10:55AM ET interval?" These resolve to YES (up) or NO (down) based on the actual price movement. A doji is a 5-minute interval where probability sits at 48-52% -- zero directional conviction. In candlestick analysis, a doji appearing after a clear directional trend (2-3 consecutive UP or DOWN intervals) signals indecision before a breakout. The next interval after the doji tends to break out strongly, continuing the pre-doji trend direction, because the underlying momentum has only paused -- not reversed.

## Edge

Unlike a generic mean-reversion or momentum strategy, the doji breakout specifically targets the transition from indecision back to trend continuation. The edge arises because:

1. **Doji = temporary pause, not reversal** -- when a coin trends UP for 3 intervals then prints a doji (48-52%), retail participants read this as "the move is over" and price the next interval near 50%. But the underlying trend momentum typically resumes.
2. **Market mispricing of continuation** -- the post-doji interval is systematically underpriced for continuation because participants anchor on the doji's neutrality rather than the preceding trend.
3. **Candlestick pattern validity** -- doji-after-trend is one of the most robust patterns in technical analysis, documented across equities, forex, and crypto on multiple timeframes.
4. **Bundle independence** -- each 5-minute interval resolves independently; the doji's neutral price does not mechanically prevent the next interval from continuing the trend.

## Signal Logic

1. Discover crypto interval markets via keyword search (`Bitcoin Up or Down`, `Ethereum Up or Down`, `Solana Up or Down`, `XRP Up or Down`) with a `get_markets(limit=200)` fallback
2. Parse each question to extract (coin, date, start_time_minutes, end_time_minutes) using regex
3. Group intervals by (coin, date) and sort by time
4. Classify each interval: UP if p > 0.55, DOWN if p < 0.45, NEUTRAL if 0.45-0.55
5. Scan for doji intervals (p between 48-52%, tunable via `SIMMER_DOJI_RANGE`)
6. Check the `TREND_LENGTH` intervals before each doji -- if ALL show the same direction (all UP or all DOWN), the post-doji interval is a breakout target
7. Trade the post-doji interval:
   - Pre-doji trend = UP and post-doji priced < YES_THRESHOLD -> buy YES (breakout not priced in)
   - Pre-doji trend = DOWN and post-doji priced > NO_THRESHOLD -> buy NO (breakout not priced in)
8. Size by conviction (distance from threshold), not flat amount

### Remix Signal Ideas

- **Volume-weighted doji detection** -- require the doji interval to have above-average trading volume for a stronger signal; low-volume dojis are less meaningful
- **Multi-timeframe confirmation** -- check if the trend also holds on a 15-minute or 1-hour timeframe before trading the breakout
- **Order book imbalance** -- use Polymarket order book depth to detect hidden buying/selling pressure during the doji interval
- **Cross-coin doji sync** -- if BTC prints a doji while ETH/SOL are still trending, the breakout signal is stronger (BTC leads)
- **Volatility filter** -- skip doji patterns during low-volatility regimes where breakouts are weaker and less profitable

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` mean nothing runs automatically until configured in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade at full conviction |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `1` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_DOJI_RANGE` | `0.02` | Half-width of doji zone around 50% (48-52% by default) |
| `SIMMER_TREND_LENGTH` | `3` | Min consecutive same-direction intervals before doji to qualify as trend |

## Edge Thesis

Crypto 5-minute interval markets on Polymarket exhibit a systematic mispricing after doji patterns. When a coin trends in one direction for 2-3 intervals then prints a doji (48-52% probability), the market prices the post-doji interval near 50% -- interpreting the doji as trend exhaustion. In reality, the doji represents a temporary pause in an ongoing trend; the next interval continues the pre-doji direction more often than the market implies. This is the classic doji-breakout pattern from candlestick analysis, adapted to Polymarket's 5-minute interval structure. The skill exploits this gap with conviction-based sizing that scales with the distance from the trading threshold.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
