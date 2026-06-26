---
name: crypto-market-analyzer
description: Fetch real-time crypto prices and calculate technical indicators (SMA, EMA, MACD, RSI, Bollinger Bands, ATR) for BTC, ETH, SOL, BNB, XRP, DOGE. Powered by multi-source data (Binance, CoinGecko, CoinCap, CryptoCompare).
version: 1.0.0
author: crypto-tools
requires:
  binaries:
    - python3
  env: ["SKILL_BILLING_API_KEY", "SKILL_ID"]
metadata:
  clawdbot:
    requires:
      env: ["SKILL_BILLING_API_KEY", "SKILL_ID"]
    files:
      - "scripts/*"
---

# Crypto Market Analyzer

This skill provides two core capabilities for cryptocurrency analysis:

1. **Real-time Market Data** — Get current prices, 24h changes, volume, and highs/lows
2. **Technical Indicator Analysis** — Calculate professional-grade indicators with trading signals

## Supported Coins

BTC, ETH, SOL, BNB, XRP, DOGE

## Dependencies

The scripts require the `requests` Python library. Install it if not available:

```bash
pip install requests
```

## Billing

This is a paid skill. Each invocation costs **0.001 USDT**, charged via SkillPay.
Pass the `--user` flag with the user's ID for billing. If the user's balance is low,
the script will return a `payment_url` — present this link to the user.

---

## Command 1: Fetch Market Data

**When to use:** When the user asks about current crypto prices, market conditions, or needs real-time price data.

### Get Current Prices

```bash
python scripts/fetch_market.py --user USER_ID --coins BTC,ETH,SOL
```

**Parameters:**
- `--coins` (required): Comma-separated coin symbols (e.g. `BTC,ETH,SOL`)
- `--user` (required): User ID for billing
- `--test-mode` (optional): Skip billing for testing

**Output format (JSON):**
```json
{
  "status": "success",
  "data": {
    "BTC": {
      "price": 95432.10,
      "change_24h": 2.35,
      "high_24h": 96000.00,
      "low_24h": 93800.50,
      "volume_24h": 28500000000,
      "source": "binance"
    }
  },
  "coins_requested": ["BTC"],
  "timestamp": 1709654321
}
```

### Get Historical Prices

```bash
python scripts/fetch_market.py --user USER_ID --coins BTC --historical --days 30
```

**Additional parameters:**
- `--historical`: Enable historical mode
- `--days` (default 30): Number of days of history

**Output includes OHLCV data** (open, high, low, close, volume) for each time period.

---

## Command 2: Technical Indicator Analysis

**When to use:** When the user asks about technical analysis, trading signals, trend analysis, support/resistance levels, or whether to buy/sell a coin.

```bash
python scripts/calc_indicators.py --user USER_ID --coin BTC --days 30
```

**Parameters:**
- `--coin` (required): Single coin symbol (e.g. `BTC`)
- `--days` (default 30): Days of data for analysis
- `--user` (required): User ID for billing
- `--test-mode` (optional): Skip billing for testing

**Output format (JSON):**
```json
{
  "status": "success",
  "coin": "BTC",
  "current_price": 95432.10,
  "moving_averages": {
    "sma_7": 94800.50,
    "sma_14": 93200.30,
    "sma_30": 91500.00,
    "ema_12": 94600.80,
    "ema_26": 93100.20
  },
  "macd": {
    "macd_line": 1500.60,
    "signal_line": 1200.30,
    "histogram": 300.30
  },
  "rsi_14": 62.5,
  "bollinger_bands": {
    "upper": 97000.00,
    "middle": 93200.00,
    "lower": 89400.00,
    "bandwidth": 8.15,
    "position": 0.79
  },
  "atr_14": 1850.30,
  "momentum": {
    "change_7d_pct": 3.25,
    "change_30d_pct": 8.50
  },
  "volatility_pct": 2.15,
  "support_resistance": {
    "support": 89400.00,
    "resistance": 97000.00
  },
  "signals": [
    "RSI leaning bullish",
    "MACD bullish crossover → BUY signal",
    "Uptrend: Price & SMA7 above SMA30"
  ],
  "signal_score": 45,
  "overall_assessment": "STRONG BUY"
}
```

## Interpreting the Output

When presenting results to the user, focus on these key elements:

### For Market Data:
- **Price** and **24h change** are the most important
- Mention **volume** for context on market activity
- Flag if **change_24h** is extreme (> ±5%)

### For Technical Analysis:
- **overall_assessment** gives the summary: STRONG BUY / BUY / NEUTRAL / SELL / STRONG SELL
- **signal_score** ranges from -100 (extremely bearish) to +100 (extremely bullish)
- **signals** array lists the specific reasons behind the assessment
- **RSI**: <30 = oversold (buy opportunity), >70 = overbought (sell opportunity)
- **MACD histogram** > 0 = bullish momentum, < 0 = bearish momentum
- **Bollinger Band position**: <0.1 = near support, >0.9 = near resistance

### Important Disclaimer:
Always remind users that technical indicators are for educational/analysis purposes only and do not constitute financial advice. Cryptocurrency markets are highly volatile.

## Error Handling

If a script returns an error, check:
1. **Payment error** — Present the `payment_url` to the user to top up balance
2. **Data source error** — All APIs failed; suggest trying again in a few minutes
3. **Invalid coin** — List the supported coins: BTC, ETH, SOL, BNB, XRP, DOGE
