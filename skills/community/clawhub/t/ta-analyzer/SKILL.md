---
name: ta-analyzer
description: Multi-timeframe technical analysis skill using CCXT. Calculates 20+ indicators including RSI, MACD, Bollinger Bands, Ichimoku, Stochastic, Williams %R, ADX, MFI, CCI, Fibonacci, Pivot Points, Support/Resistance, and detects 10+ chart patterns. Use when user asks for technical analysis, chart analysis, indicator values, trading signals, or price predictions.
---

# TA Analyzer - Technical Analysis Skill

A comprehensive technical analysis skill that fetches real-time market data and calculates 20+ technical indicators.

## Features

### Price Data
- Fetches OHLCV data from Binance via CCXT
- Supports multiple timeframes: 15m, 1h, 4h, 1d
- Multi-timeframe analysis for better signal confirmation

### Technical Indicators

#### Trend Indicators
- EMA (9, 21, 50)
- SMA (20, 50)
- MACD (12, 26, 9)
- Supertrend

#### Momentum Indicators
- RSI (14)
- Stochastic (14, 3, 3)
- Williams %R (14)
- ADX (14)
- MFI (14)
- CCI (20)

#### Volatility Indicators
- Bollinger Bands (20, 2)
- ATR (14)
- Keltner Channel
- Donchian Channel

#### Volume Indicators
- OBV
- Volume SMA
- Volume analysis (healthy/divergence)

#### Support/Resistance
- Auto-detect local highs/lows
- Cluster nearby levels
- Calculate nearest support/resistance

### Chart Patterns

#### Single Candle Patterns
- Hammer
- Shooting Star
- Doji

#### Multi-Candle Patterns
- Engulfing (Bullish/Bearish)
- Morning/Evening Star
- Double Top/Bottom
- Head & Shoulders
- Triangle (ascending/descending/symmetrical)
- Flag

### Fibonacci & Pivot Points
- Fibonacci Retracements (0.236, 0.382, 0.5, 0.618, 0.786)
- Classic Pivot Points (PP, R1-R3, S1-S3)
- VWAP

## Usage

```javascript
const { analyze } = require('./index.js');

// Analyze BTC on all timeframes
const result = await analyze('BTC/USDT');

// Analyze specific timeframe
const { analyzeTimeframe } = require('./index.js');
const result = await analyzeTimeframe('BTC/USDT', '1h', 100);
```

## Output

The skill returns comprehensive analysis including:
- Current price and trend
- All indicator values
- Detected patterns
- Buy/Sell recommendations
- Stop loss and take profit levels

## Use Cases

- "Analyze BTC"
- "What's the RSI of ETH?"
- "Is there a bullish divergence on 4h?"
- "What are the support levels?"
- "Should I buy or sell?"

---

Author: Lucifer (路西法)
Created: 2026-03-05
Version: 1.0.0