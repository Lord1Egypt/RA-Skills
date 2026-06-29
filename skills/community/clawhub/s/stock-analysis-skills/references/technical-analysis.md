# Technical Analysis Framework — Reference Guide

Methodology for Module 2: Stock Trend Analysis. Used to interpret technical indicators and form a directional bias.

---

## Core Principles

Technical analysis evaluates the **sentiment and momentum** embedded in price and volume. It does not predict fundamentals — rather, it reflects the composite outcome of market participant behavior. In equity research, technical and fundamental analysis are complementary:
- Fundamentals tell you **what to buy**
- Technicals help you decide **when to buy** (entry timing, trend confirmation)

Never rely on a single indicator in isolation. Observe **convergence** or **divergence** across multiple indicators to form a view.

---

## 1. Moving Averages

### Simple Moving Average (SMA)
- **50-day SMA**: Tracks intermediate-term trend. Price trading persistently above = intermediate-term bullish.
- **200-day SMA**: Tracks long-term trend; one of the most widely watched technical levels.
- **Price-to-MA relationship**:
  - Price > 200-day SMA: Long-term uptrend — bullish backdrop
  - Price < 200-day SMA: Long-term downtrend — bearish backdrop
  - Price breaking above 50-day SMA: Potential short-term bullish reversal

### Golden Cross & Death Cross
| Event | Definition | Implication |
|-------|------------|-------------|
| Golden Cross | 50-day SMA crosses above 200-day SMA | Bullish long-term signal |
| Death Cross | 50-day SMA crosses below 200-day SMA | Bearish long-term signal |

*Note: These are lagging indicators — useful for confirming trend changes, not predicting them.*

### Exponential Moving Average (EMA)
- EMA assigns higher weight to recent prices, reacting faster to price changes
- 20-day EMA is commonly used for short-term trend assessment
- Many traders use 12-day and 26-day EMAs as the foundation for MACD

---

## 2. Relative Strength Index (RSI)

**Formula**: RSI = 100 – [100 / (1 + RS)], where RS = 14-period average gain / average loss

**Standard interpretation:**
| RSI Level | Interpretation |
|-----------|---------------|
| > 70 | Overbought — potential pullback or consolidation |
| 50–70 | Bullish momentum zone |
| 50 | Neutral — mixed trend signals |
| 30–50 | Bearish momentum zone |
| < 30 | Oversold — potential bounce or short-term reversal |

**Stronger signals:**
- **Bullish Divergence**: Price makes a new low, but RSI makes a higher low — buying is absorbing selling pressure, often precedes reversal.
- **Bearish Divergence**: Price makes a new high, but RSI makes a lower high — upward momentum is fading.
- **RSI 50-line cross**: RSI breaking above 50 = momentum strengthening; breaking below 50 = momentum weakening.

---

## 3. MACD (Moving Average Convergence Divergence)

**Components:**
- **MACD Line**: 12-day EMA − 26-day EMA
- **Signal Line**: 9-day EMA of the MACD Line
- **Histogram**: MACD Line − Signal Line (reflects momentum acceleration/deceleration)

**Interpretation:**
| Signal | Meaning |
|--------|---------|
| MACD crosses above Signal Line | Bullish crossover — often treated as a buy signal |
| MACD crosses below Signal Line | Bearish crossover — often treated as a sell signal |
| Histogram positive bars lengthening | Upward momentum accelerating |
| Histogram positive bars shortening | Upward momentum decelerating (potential near-term top) |
| MACD above zero line | Overall trend bullish |
| MACD below zero line | Overall trend bearish |

**MACD Divergence**: Same principle as RSI divergence. Divergence between price and the MACD histogram can signal trend exhaustion.

---

## 4. Bollinger Bands

**Construction**: 20-day SMA ± 2 standard deviations

**Key signals:**
| Situation | Interpretation |
|-----------|----------------|
| Price touches upper band | Short-term overbought — often leads to pullback or sideways |
| Price touches lower band | Short-term oversold — often leads to bounce |
| Band squeeze (narrowing) | Low volatility phase — often precedes a sharp breakout |
| Band expansion | High volatility phase — trend may be extending |
| Price riding the upper band | Strong uptrend — bullish continuation |
| Price riding the lower band | Strong downtrend — bearish continuation |

*Bollinger Bands are best used as a volatility tool, not a mechanical buy/sell signal.*

---

## 5. Volume Analysis

Volume confirms or undermines the validity of price moves:

| Price Move | Volume | Interpretation |
|------------|--------|----------------|
| Price up | Strong | Accumulation / institutional buying — bullish |
| Price up | Weak | Lack of conviction — potential reversal |
| Price down | Strong | Distribution / institutional selling — bearish |
| Price down | Weak | Limited selling pressure — potential base building |

**Volume indicators to watch:**
- **OBV (On-Balance Volume)**: Cumulative volume indicator. OBV trending in sync with price confirms the trend; OBV divergence may warn of a reversal.
- **Capitulation volume on reversal days**: Panic selling volume often appears near intermediate-term bottoms (not a guarantee).

---

## 6. Support & Resistance

**Support**: Price levels where buying pressure historically overwhelms selling — acts as a "floor."
**Resistance**: Price levels where selling pressure historically overwhelms buying — acts as a "ceiling."

**Identification methods:**
- Prior swing highs and swing lows
- Round numbers (psychological levels: e.g., $10, $50, $100, $200)
- 52-week highs and 52-week lows
- Prior broken levels (support that was broken often becomes resistance)
- Moving averages (50-day and 200-day SMA often act as dynamic support/resistance)

**Rule of Polarity**: Key support, once decisively broken, often becomes resistance; key resistance, once decisively broken, often becomes support.

---

## 7. Trend Synthesis: Forming a Directional Bias

When assessing short/medium/long-term orientation, weight indicators by timeframe:

| Timeframe | Primary Indicators | Secondary Indicators |
|-----------|-------------------|---------------------|
| Short-term (1–4 weeks) | RSI, MACD, Bollinger Bands | 20-day EMA, Volume |
| Medium-term (1–6 months) | 50-day SMA, MACD trend | RSI trend, key resistance levels |
| Long-term (6–18 months) | 200-day SMA, Golden/Death Cross | Alignment with fundamental trend |

**Directional bias classification:**
- **Bullish**: Most relevant indicators are positive or confirming each other
- **Bearish**: Most relevant indicators are negative or showing divergence
- **Neutral**: Mixed signals or insufficient confirmation; indicators conflict

**Technical Module Scoring Guide:**
- Score of 5: Price in an uptrend, trading above both key MAs, RSI 50–70, MACD bullish, volume confirming, clear upside room and downside support
- Score of 3: Mixed signals — some indicators bullish, some bearish; or in a consolidation phase
- Score of 1: Price in a downtrend, trading below both key MAs, RSI < 40, MACD bearish, volume shows distribution characteristics
