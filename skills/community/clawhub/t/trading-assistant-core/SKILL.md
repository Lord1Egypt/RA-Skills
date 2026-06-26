---
name: trading-assistant
description: Market data analysis toolkit with technical indicators and portfolio tracking. Educational use only.
version: 1.0.0
author: XuXuClassMate
license: MIT
category: Education
tags:
  - education
  - finance
  - analysis
  - openclaw
metadata:
  openclaw:
    requires:
      env:
        - TWELVE_DATA_API_KEY
        - ALPHA_VANTAGE_API_KEY
      bins:
        - python3
        - pip
    primaryEnv: TWELVE_DATA_API_KEY
    emoji: 📊
    homepage: https://github.com/XuXuClassMate/trading-assistant
    safety:
      level: safe
      audit: manual
      notes: Educational tool only. Pure Python, no subprocess, no shell, no eval/exec. API keys from env vars. Read-only market data. No trade execution.
---

# Market Data Analysis Toolkit

Educational tool for learning technical analysis and portfolio tracking.

## What It Does

- Calculate technical indicators (RSI, MACD, Bollinger Bands)
- Track portfolio holdings and P&L
- Generate price alerts
- Analyze historical data

## Installation

```bash
pip install -r requirements.txt
export TWELVE_DATA_API_KEY=your_key
export ALPHA_VANTAGE_API_KEY=your_key
python3 trading_signals.py
```

## Security

- Pure Python code
- No subprocess or shell calls
- No eval/exec
- Environment variables for API keys
- Read-only API access

## Links

- GitHub: https://github.com/XuXuClassMate/trading-assistant
- Issues: https://github.com/XuXuClassMate/trading-assistant/issues
- Docker Hub: https://hub.docker.com/r/xuxuclassmate/trading-assistant

## License

MIT License - Educational use only, not financial advice.
