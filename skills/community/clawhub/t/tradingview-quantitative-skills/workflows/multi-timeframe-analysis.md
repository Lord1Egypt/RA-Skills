---
description: Multi-Timeframe Analysis Workflow - Cross-period trend confirmation and entry timing selection
---

# Multi-Timeframe Analysis Workflow

Use candlestick data and technical indicators across multiple timeframes to confirm trend direction consistency and select optimal entry timing.

## Core Concept

**Higher timeframe defines direction, lower timeframe finds entry**: Monthly/weekly confirms primary trend, daily confirms medium-term trend, hourly selects entry point.

## Execution Steps

### Step 1: Get Multi-Period Chart Data

Call in parallel to get 4 timeframes:

```
tradingview_get_price(symbol, timeframe='M', range=24)    # Monthly - 2 years
tradingview_get_price(symbol, timeframe='W', range=52)    # Weekly - 1 year
tradingview_get_price(symbol, timeframe='D', range=120)   # Daily - 6 months
tradingview_get_price(symbol, timeframe='60', range=120)  # Hourly - 5 days
```

Optional: Use `type='HeikinAshi'` to get Heikin Ashi candles, filtering noise for clearer trend identification.

### Step 2: Get Technical Analysis Signals

```
tradingview_get_ta(symbol, include_indicators=true)
```

The TA tool returns multi-period signals (1-minute to monthly) directly providing buy/sell/neutral signal aggregation for each period.

### Step 3: Trend Assessment for Each Period

Assess trend direction for each timeframe:

**Monthly (Strategic Direction)**:
- Price above SMA20 → Long-term uptrend
- Price below SMA20 → Long-term downtrend
- MACD direction confirmation

**Weekly (Tactical Direction)**:
- Moving average alignment (SMA5 > SMA10 > SMA20 = bullish)
- RSI position (40-70 healthy uptrend range)
- MACD golden cross/death cross status

**Daily (Operating Period)**:
- Short-term vs medium-term moving average relationship
- Volume cooperation (volume surge on rise/volume contraction on pullback)
- Support/resistance levels

**Hourly (Entry Timing)**:
- Pullback near daily support level
- RSI bouncing from oversold zone
- Bullish candlestick pattern appears

### Step 4: Trend Consistency Assessment

| Monthly | Weekly | Daily | Signal Strength | Trading Recommendation |
|---------|--------|-------|----------------|------------------------|
| ↑ | ↑ | ↑ | Strong Bull | Aggressive long, trend following |
| ↑ | ↑ | ↓ | Medium Bull | Wait for daily pullback stabilization before buying |
| ↑ | ↓ | ↓ | Weak Bull | Wait and see, wait for weekly stabilization |
| ↓ | ↓ | ↓ | Strong Bear | Avoid or short |
| ↓ | ↓ | ↑ | Weak Bear | Likely a bounce, not suitable for chasing |
| ↓ | ↑ | ↑ | Medium Bear | Possible early reversal, light position test |

### Step 5: Generate Analysis Report

```markdown
# [Symbol] Multi-Timeframe Analysis

## Trend Status by Period
| Period | Trend | Key Indicators | TA Signal |
|--------|-------|----------------|-----------|
| Monthly | ↑/↓/→ | SMA20, MACD | Buy/Sell/Neutral |
| Weekly | ↑/↓/→ | MA alignment, RSI | Buy/Sell/Neutral |
| Daily | ↑/↓/→ | Volume, MA | Buy/Sell/Neutral |
| Hourly | ↑/↓/→ | Short-term momentum | Buy/Sell/Neutral |

## Trend Consistency: [Strong Bull/Medium Bull/Weak Bull/Neutral/Weak Bear/Strong Bear]

## Key Price Levels
- Monthly support: ¥XX
- Weekly support: ¥XX
- Daily support: ¥XX
- Daily resistance: ¥XX

## Trading Recommendations
- Direction: ...
- Entry conditions: ...
- Stop loss: ...
- Target: ...
```

## Example

**User**: "Multi-timeframe analysis of BTCUSDT"

**Execution**:
1. `get_price` × 4 timeframes (M/W/D/60)
2. `get_ta(include_indicators=true)` → Multi-period signals
3. Assess trend consistency across periods
4. Identify key support/resistance levels
5. Output trend consistency report and entry recommendations
