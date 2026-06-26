# Three-Factor Analysis Methodology

## Overview

This system combines three distinct investment approaches to generate high-confidence buy signals:

1. **Value Investing (DCF)** - Determines if stock is undervalued
2. **Trend Trading (Livermore)** - Determines if trend is favorable
3. **Sentiment Analysis (VIX)** - Determines market environment

**Buy signal only triggers when ALL THREE factors confirm.**

---

## Factor 1: DCF Valuation (40% weight)

### Model Overview
Free Cash Flow to Equity (FCFE) discounted cash flow model.

### Formula
```
Intrinsic Value = Σ(FCF_t / (1+r)^t) + Terminal Value / (1+r)^n

Where:
- FCF_t = Free Cash Flow in year t
- r = Discount rate (WACC)
- n = Projection period (10 years)
- Terminal Value = FCF_n × (1+g) / (r-g)
- g = Terminal growth rate (2.5%)
```

### Scoring (0-100 points)

| Component | Max Points | Criteria |
|-----------|------------|----------|
| Margin of Safety | 40 | >30%: 40pts, >20%: 30pts, >10%: 20pts, >0%: 10pts |
| Return on Equity | 15 | >15%: 15pts, >10%: 10pts, >5%: 5pts |
| Debt to Equity | 15 | <50%: 15pts, <100%: 10pts, <200%: 5pts |
| Profit Margin | 20 | >20%: 20pts, >10%: 15pts, >5%: 10pts, >0%: 5pts |
| P/E Ratio | 10 | <15: 10pts, <25: 5pts |

### Buy Condition
```
Value Score >= 60 AND Margin of Safety >= 20%
```

---

## Factor 2: Livermore Trend Rules (35% weight)

### Core Principles

1. **Trade with the trend**
   - Only buy in uptrends
   - Define trend using moving averages (MA20 > MA60)

2. **Key pivotal points**
   - Identify support and resistance
   - Wait for breakout above resistance

3. **Volume confirmation**
   - Breakout must have 1.5x average volume

4. **Sector alignment**
   - Stock trend confirmed by sector ETF trend

5. **Pyramid into strength**
   - Scale in on confirmed moves
   - Never average down

### Scoring (0-100 points)

| Component | Max Points | Criteria |
|-----------|------------|----------|
| Trend Direction | 40 | Uptrend: 40pts, Sideways: 20pts, Downtrend: 0pts |
| MA Alignment | 20 | Price > MA20 > MA60: 20pts, Price > MA60: 10pts |
| Pivot Break | 15 | Break above recent high: 15pts |
| Volume Confirm | 15 | >1.5x avg volume: 15pts |
| Sector Align | 10 | Sector in uptrend: 10pts |

### Buy Condition
```
Trend Score >= 60 AND Uptrend AND Pivot Break AND Volume Confirm
```

### Key Levels

| Level | Definition | Use |
|-------|------------|-----|
| Resistance | Recent pivot high | Entry trigger when broken |
| Support | Recent pivot low | Stop loss placement |
| 20-day high | Max high last 20 days | Short-term momentum |
| 20-day low | Min low last 20 days | Risk level |

---

## Factor 3: VIX Sentiment (25% weight)

### Components

1. **VIX Absolute Level**
   - < 15: Complacency (slight concern)
   - 15-20: Normal/optimal
   - 20-25: Elevated caution
   - 25-30: High fear
   - > 30: Panic (avoid)

2. **VIX Percentile (IV Rank)**
   - Measures where current VIX is vs 1-year range
   - Lower = calmer = better for buying

3. **Put/Call Ratio**
   - < 0.7: Greed/caution
   - 0.7-1.2: Normal
   - > 1.5: Fear (contrarian bullish)

4. **Market Breadth**
   - SPY trend direction
   - Confirms overall market health

### Scoring (0-100 points)

| Component | Max Points | Criteria |
|-----------|------------|----------|
| VIX Level | 30 | Normal: +30, Low: +20, Elevated: +10, High: -20, Panic: -40 |
| VIX Percentile | 20 | <30%: +20, <50%: +15, <70%: +5, <85%: -10, >85%: -20 |
| Put/Call Ratio | 20 | Normal: +20, Low: -10, Very Low: -20, Very High: +10 |
| Market Breadth | 30 | SPY up: +30, Neutral: +15, Down: -10 |

### Buy Condition
```
Sentiment Score >= 60 AND VIX < 25 AND Breadth = UP
```

---

## Composite Decision

### Scoring Formula
```
Composite = (Value × 0.40) + (Trend × 0.35) + (Sentiment × 0.25)
```

### Final Buy Signal
```
BUY = Value >= 60 AND Trend >= 60 AND Sentiment >= 60 AND Composite >= 70
```

### Confidence Levels

| Composite | Confidence |
|-----------|------------|
| >= 80 | HIGH |
| 70-79 | MEDIUM |
| < 70 | LOW |

### Position Sizing

| Confidence | Max Position |
|------------|--------------|
| HIGH | 10-15% |
| MEDIUM | 5-10% |
| LOW | 0-5% (or wait) |

---

## Data Sources

| Data | Source | Frequency |
|------|--------|-----------|
| Price/Volume | Yahoo Finance (yfinance) | Daily |
| Financial Statements | FMP API | Quarterly |
| VIX | CBOE via Yahoo | Daily |
| Options | Alpha Query / CBOE | Daily |
| Sector ETFs | Yahoo Finance | Daily |

---

## Limitations

1. **DCF Sensitivity**: Highly sensitive to growth and discount rate assumptions
2. **Trend Lag**: Moving averages lag price action
3. **Sentiment Timing**: VIX can spike unexpectedly
4. **Data Quality**: Depends on accuracy of financial reports
5. **Market Regime**: Strategy works best in trending markets

## Best Practices

1. **Use as screening tool**, not sole decision factor
2. **Review weekly** for existing positions
3. **Adjust thresholds** for different market conditions
4. **Keep a trading journal** of signals and outcomes
5. **Consider macro factors** not captured by model
