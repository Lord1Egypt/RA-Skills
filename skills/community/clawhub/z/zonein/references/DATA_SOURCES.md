# Data Sources Reference

The platform combines **3 real-time data sources** into a composite AI signal. Weights are user-configurable (defaults: SM=40%, TA=35%, Market=25%).

---

## 1. Smart Money (SM) — default 40% weight

Tracks ~500+ categorized Hyperliquid wallets. For each coin:

| Field | Range | Description |
|-------|-------|-------------|
| `sm.long_ratio` / `sm.short_ratio` | 0–100% | Position count ratio — % of wallets long vs short |
| `sm.long_count` / `sm.short_count` | int | Number of wallets with long/short positions |
| `sm.long_volume` / `sm.short_volume` | USD | Volume by direction |
| `sm.wallet_count` | int | Total active wallets (more = higher confidence) |
| `sm.direction` | str | Detected direction |

**Per-timeframe** (tf: `1h`, `4h`, `24h`): `sm.{tf}.long_count`, `sm.{tf}.short_count`, `sm.{tf}.wallet_count`, `sm.{tf}.long_volume`, `sm.{tf}.short_volume`

**Direction detection:** 
- With TA confirmation: `sm.long_ratio >= 50` = bullish, `sm.short_ratio >= 50` = bearish
- Standalone SM: `sm.long_ratio >= 55` = bullish, `sm.short_ratio >= 55` = bearish

> ⚠️ **Real market data:** SM long_ratio averages 44-46% and rarely exceeds 55%. Use >=50 when combined with TA, >=55 for SM-only strategies.

> **Note:** `sm.long_ratio` and `sm.short_ratio` are percentages (0-100), NOT decimals. 65% → `sm.long_ratio >= 65` (not 0.65).

### SM Wallet Categories (Perp)

| Category | Description | Best for |
|----------|-------------|----------|
| `short_term_trading` | Quick in-and-out (<24h) | Scalping agents |
| `swing_trading` | Hold days to weeks | Swing traders |
| `high_risk_high_return` | Aggressive, high volatility | Momentum agents |
| `high_win_rate` | Consistently >80% win rate | Conservative agents |
| `stable` | High win rate + low drawdown | Low-risk agents |
| `btc_trader` | >90% BTC volume | BTC specialists |
| `large_cap_trader` | BTC/ETH/SOL focus | Blue-chip agents |
| `low_cap_trader` | Small cap tokens | Alt-coin agents |
| `scalper` | Very short-term, tight targets | Scalping agents |
| `trend_follower` | Follows established trends | Trend agents |
| `momentum_trader` | Trades on momentum + volume | Momentum agents |

### SM Categories (HIP-3)

| Category | Description |
|----------|-------------|
| `scalper` | Ultra-short holds < 4h |
| `day_trader` | Intraday 4-48h |
| `swing_trader` | 2-14 days |
| `position_trader` | > 14 days |
| `trend_follower` | Strong long bias >=70% |
| `short_bias` | Predominantly short >=70% |
| `aggressive_leverage` | High leverage >=8x |
| `conservative` | Low leverage <=3x |
| `high_conviction` | Few big bets |
| `multi_asset` | 5+ assets |
| `alpha_generator` | Exceptional risk-adjusted returns |
| `perp_verified` | Also SM in perp trading |

---

## 2. Technical Analysis (TA) — default 35% weight

Multi-timeframe indicators via TAAPI.io across **15m, 1h, 4h, 1d**. All accessed as `ta.{tf}.{field}`.

| Category | Fields | Key thresholds |
|----------|--------|----------------|
| **Momentum** | `rsi`, `macd_hist`, `stoch_k`, `stoch_d`, `stochrsi_k`, `cci`, `mfi`, `willr`, `roc` | RSI: ≤30 oversold, ≥70 overbought. MACD: >0 bullish. Stoch: K<20 oversold, K>80 overbought |
| **Trend** | `supertrend_advice` ("buy"/"sell"), `adx`, `plus_di`, `minus_di`, `aroon_up`, `aroon_down`, `psar` | SuperTrend: clearest trend signal. ADX: <15 ranging, ≥15 trending, ≥25 strong |
| **Volatility** | `bb_upper`, `bb_middle`, `bb_lower`, `atr`, `natr` | BB: near lower=bounce, near upper=rejection. NATR >5%=high vol |
| **Volume** | `obv`, `vwap`, `cmf`, `adl` | VWAP: above=bullish, below=bearish. CMF: >0 buying, <0 selling |
| **Moving Avg** | `ema_9`, `ema_21`, `ema_55`, `sma_20`, `sma_50`, `sma_200` | EMA9>EMA21=bullish cross. Price>SMA50=bullish bias |

**Timeframe weights** (configurable, default): 15m(15%) + 1h(20%) + 4h(30%) + 1d(35%)

---

## 3. Market Data (Derivatives) — default 25% weight

Real-time derivatives indicators via CoinGlass:

| Metric | Field | Interpretation |
|--------|-------|----------------|
| **Funding Rate** | `market.funding_current` | Positive = crowded longs (contrarian bearish). Extreme >0.05% = very bearish |
| **Open Interest** | `market.oi_change_1h/4h/24h` | Rising OI + rising price = bullish. Rising OI + falling price = bearish |
| **Long/Short Ratio** | `market.long_ratio`, `market.short_ratio` | >65% long = contrarian bearish. <35% long = contrarian bullish |
| **Liquidations** | `market.liquidation_long_24h/4h/1h`, `market.liquidation_short_24h/4h/1h` | More short liquidations = short squeeze (bullish) |
| **Volume** | `market.volume_24h` | High volume = stronger signal confidence |
| **Price Change** | `market.price_change_24h` | Context for OI interpretation |

---

## Composite Signal

`composite = SM(sm_weight) + TA(ta_weight) + Market(market_weight)`

- Score > 55 → LONG, < 45 → SHORT, 45–55 → NEUTRAL
- Confidence boosted when all 3 sources agree (+15%)
- Custom weights example: TA-heavy → `{"sm":20,"ta":55,"market":25}`. Whale follower → `{"sm":60,"ta":20,"market":20}`
