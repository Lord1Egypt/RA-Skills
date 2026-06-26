# Technical Indicators Reference

## Moving Averages (MA)

### Simple Moving Average (SMA)
- **Formula**: `MA(n) = average(close prices over n periods)`
- **Common periods**: 5, 10, 20, 60, 120, 250 (trading days)
- **Interpretation**:
  - Price above MA → bullish (short-term)
  - MA5 > MA10 > MA20 → uptrend (bullish alignment)
  - MA5 < MA10 < MA20 → downtrend (bearish alignment)
  - Golden Cross: MA5cross above MA10 → buy signal
  - Death Cross: MA5cross below MA10 → sell signal

### Exponential Moving Average (EMA)
- Gives more weight to recent prices (smoother, faster response)
- Same interpretation as SMA but reacts quicker

---

## Momentum Oscillators

### RSI (Relative Strength Index)
- **Period**: 14 days standard
- **Range**: 0-100
- **Formula**: `RSI = 100 - (100 / (1 + RS))` where `RS = Avg(Gain) / Avg(Loss)` over period
- **Signals**:
  - RSI > 70 → Overbought (potential pullback)
  - RSI < 30 → Oversold (potential bounce)
  - RSI Divergence: price makes new high but RSI doesn't → bearish warning
  - Centerline (50): Above = momentum bullish, Below = momentum bearish

### MACD (Moving Average Convergence Divergence)
- **Components**:
  - MACD Line: `EMA(12) - EMA(26)`
  - Signal Line: `EMA(9) of MACD Line`
  - Histogram: `MACD Line - Signal Line`
- **Signals**:
  - Bullish: MACD Line crosses above Signal Line (bottom of histogram turns positive)
  - Bearish: MACD Line crosses below Signal Line (top of histogram turns negative)
  - Divergence: price high but MACD lower → reversal warning
  - Zero line: Above = bullish bias, Below = bearish bias

### KDJ (Stochastic Oscillator variant)
- **Components**: K (fast), D (slow, SMA of K), J (weighted)
- **Range**: 0-100
- **Signals**:
  - Overbought: K/D > 80
  - Oversold: K/D < 20
  - Golden Cross: K crosses above D → buy
  - Death Cross: K crosses below D → sell
  - J > 100 → extremely overbought
  - J < 0 → extremely oversold

---

## Volatility Indicators

### ATR (Average True Range)
- **Measures**: Average price range (high-low and gaps) over period (usually 14)
- **Interpretation**: Higher ATR = higher volatility
- **Usage**: Set stop-loss levels (e.g., 2x ATR below entry)

### Bollinger Bands
- **Components**:
  - Middle: SMA(20)
  - Upper: SMA(20) + 2 * σ (standard deviation)
  - Lower: SMA(20) - 2 * σ
- **Signals**:
  - Price touching Upper → potential overbought
  - Price touching Lower → potential oversold
  - Squeeze: Bands narrow → upcoming volatility expansion
  - Width: (Upper - Lower) / SMA → volatility measure

---

## Volume Indicators

### On-Balance Volume (OBV)
- **Cumulative**: adds volume on up days, subtracts on down days
- **Interpretation**: Volume should confirm price trend
  - Price ↑ + OBV ↑ → bullish confirmation
  - Price ↑ + OBV ↓ → bearish divergence (weakness)

### Volume Ratio
- **Formula**: `today_volume / average_volume_20`
- **Interpretation**:
  - > 1.5 → volume surge (breakout or distribution)
  - < 0.5 → low volume (lack of interest)

---

## Support & Resistance

### How to Identify
- **Support**: Previous reaction lows, round numbers, 50/200-day MA
- **Resistance**: Previous peaks, round numbers, volume-based (high volume nodes)
- **Role Reversal**: Once broken, support becomes resistance (and vice versa)

### Trading Implications
- Buy near support, sell near resistance
- Break above resistance → bullish breakout (with volume)
- Breakdown below support → bearish breakdown

---

## Trend Assessment Checklist

1. **Primary trend** (MA60/120/250):
   - Price > MA60 → bullish trend
   - Price < MA60 → bearish trend
2. **Secondary trend** (MA20):
   - MA20 slope: up = bullish, down = bearish
3. **Momentum** (RSI):
   - RSI > 50 + rising → bullish momentum
   - RSI < 50 + falling → bearish momentum
4. **Confirmation**:
   - MACD histogram positive and expanding → bullish
   - Volume increasing on up days → healthy trend

---

## Notes

- All indicators are lagging (use price as primary)
- Avoid overloading charts; 3-5 indicators max
- Always consider the broader market context (index trend, sector rotation)
