---
name: unbeatable-condor-strategy
description: Check daily if given stocks hit the 4% volatility threshold condor signal. 无敌鹰式策略
version: 1.0.0
author: jinntrance
tags:
  - options
  - trading
  - quantitative
  - iron-condor
---

# Unbeatable Option Condor Strategy Signal Generator 🦅

## Description
This skill determines whether it's safe and profitable to sell a Short Iron Condor or Strangle on specific target stocks today. It uses the `us_hk_50b` stocks historic data (100 months) to train a LightGBM Quantile Regressor that predicts the 10% and 90% confidence boundaries for tomorrow's price relative to today's close.
If the width of this boundary exceeds `4.00%` (0.04), it issues a signal to SELL premium for extreme Theta collection at those strikes.

## Usage

### Dependencies
Before running the script, ensure the following Python libraries are installed:
```bash
pip install pandas numpy lightgbm yfinance
```

When the user asks you to check if a specific stock (e.g. AAPL, NVDA, TSLA or 0700.HK) hit the operational condor signal, you should run the `condor_signals.py` script passing the stock tickers.

```bash
# Make sure to run this using the appropriate python environment that has lightgbm, pandas, and yfinance installed.
python condor_signals.py AAPL NVDA TSLA 0700.HK
```

The script will automatically grab the latest market data directly up to the closing price, generate features, train the AI model, and output precise strike thresholds (Sell Put Strike, Sell Call Strike).

### Safe Boundary Measures
If the script outputs `[SIGNAL TRIGGERED]`, output to the user:
1. The exact Put strike price to Sell.
2. The exact Call strike price to Sell.
3. Remind them: "Please allocate max 25% of trading capital to this setup, and buy wings (further OTM options) to strictly cap tail-loss risk at 3X the collected premium (Risk=0.1)."

If the script outputs `[NO SIGNAL]`, inform the user that the implied risk-adjusted volatility width is too narrow and they should abstain from Condor trades on the stock today.
