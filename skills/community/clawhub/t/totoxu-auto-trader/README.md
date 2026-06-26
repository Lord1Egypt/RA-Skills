# Auto Crypto Trader

Professional cryptocurrency automated trading skill for OpenClaw.

## Features

- **Market Analysis**: Built-in 14-period RSI, SMA, MACD, Bollinger Bands, and standard deviation calculations to determine BUY/SELL/HOLD opportunities.
- **Auto-Trading Execution**: Safe integration with the Binance API using the official `ccxt` library.
- **Customizable**: Set your own trading pairs, intervals, and position sizes.
- **Billing Integration**: Pay-per-use at incredibly low rates (0.001 USDT per call via SkillPay).

## Prerequisites

To use this skill, the host system needs python dependencies:

```bash
pip install requests ccxt
```

To execute real trades, the AI agent will require you to set the `BINANCE_API_KEY` and `BINANCE_SECRET` environment variables.

## How to use

Once installed, simply chat with your OpenClaw agent:

> "I want you to analyze the BTCUSDT market on the 1h timeframe. If there's a strong buy signal, buy 0.001 BTC on Binance using my API keys."

## Safety Notice
This skill interacts with real money if connected to production Binance keys. Use the `testnet` flag first to ensure the agent understands your strategy before trading real funds.
