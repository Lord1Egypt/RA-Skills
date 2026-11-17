# Strategy Framework — references/strategy-framework.md

The strategy is a weighted multi-timeframe trend/momentum follower. Three
timeframes with distinct jobs: **4h = trend filter**, **1h = signal frame**,
**5m = timing frame**.

## Features (`compute_features.py`)

Per timeframe, from candles (oldest → newest, ≥ 30 bars):

| Feature | Definition |
|---|---|
| `ema20`, `ema50`, `ema12`, `ema26` | EMA seeded with the SMA of the first N closes |
| `rsi14` | Wilder RSI over 14 bars |
| `atr14` | Wilder ATR over 14 bars (true range vs previous close) |
| `macd`, `macd_signal`, `macd_histogram` | EMA12−EMA26, EMA9 of the line, difference |
| `volume_ratio` | last bar volume ÷ mean of the prior 20 bars |
| `trend` | `up` if EMA20 > EMA50, `down` if EMA20 < EMA50, else `neutral` |
| `momentum` | 10-bar rate of change, percent |
| `high_volatility` | ATR14 > 1.5 × its own 20-bar mean |
| `funding_rate` | passthrough of Lighter's current funding rate for the market |

## Signal scoring (`compute_signal.py`)

Long and short are scored **independently**. A component contributes its full
weight when it supports that direction:

| Component | Weight | Long fires when | Short fires when |
|---|---|---|---|
| `trend_4h` | 2.0 | 4h trend `up` | 4h trend `down` |
| `trend_1h` | 2.0 | 1h trend `up` | 1h trend `down` |
| `rsi_zone` | 1.5 | 45 ≤ RSI(1h) ≤ 68 | 32 ≤ RSI(1h) ≤ 55 |
| `macd_cross` | 1.0 | MACD line > signal (1h) | line < signal |
| `timing_5m` | 0.5 | 5m trend up **or** 5m price > EMA20 | 5m trend down **or** price < EMA20 |
| `volume` | 1.0 | volume_ratio ≥ 0.8 | volume_ratio ≥ 0.8 |
| `ema20_position` | 1.0 | price > EMA20 (1h) | price < EMA20 |
| `funding_bias` | 0.5 | funding < 0 | funding > 0 |

Total possible score: **9.5**. `confidence = score / 9.5`.

The RSI zones are asymmetric on purpose: the long zone (45–68) excludes
overbought readings, while the short zone (32–55) excludes oversold ones —
the model buys strength within reason and sells weakness within reason.

Funding bias: a negative funding rate means shorts pay longs — being long is
subsidized and the crowd is short. Positive funding mirrors that for shorts.

### Thresholds

- Base entry threshold: **confidence ≥ 0.55**.
- Under `high_volatility` (1h): threshold rises to **0.70**.
- Both sides below threshold → `wait`. Perfect tie → `wait`.
- Every outcome — including `wait` — is journaled.

### Learning interaction

`trade_loop.py` applies two learning adjustments before entry:
`adjusted_confidence = confidence × metrics.confidence_multiplier`, and the
threshold becomes `max(base_threshold, metrics.recommended_min_confidence)`.
Both adjustments can only make entry harder, never easier.

## Regimes

The journal tags each decision with a regime for the review loop:
`trend_up`, `trend_down`, `range`, or `high_volatility` (which overrides the
trend label). Per-regime win/loss stats let the review surface conditions
where the agent underperforms.

## Worked example

1h: trend up, RSI 54, MACD line 6.3 > signal 4.0, volume ratio 1.31, price
above EMA20. 4h: trend up. 5m: trend up. Funding slightly negative.

Long components: trend_4h (2) + trend_1h (2) + rsi_zone (1.5) + macd_cross (1)
+ timing_5m (0.5) + volume (1) + ema20_position (1) + funding_bias (0.5)
= 9.5 → confidence 1.00. Short components: none → 0.00.

Signal: **long**, confidence 1.00 ≥ 0.55 → proceed to confluence.
