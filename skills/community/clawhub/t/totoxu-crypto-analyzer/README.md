# crypto-market-analyzer

Professional cryptocurrency market data and technical analysis skill for OpenClaw.

## Features

- **Real-time Prices**: BTC, ETH, SOL, BNB, XRP, DOGE from multiple data sources
- **Multi-source Fallback**: Binance → CoinGecko → CoinCap → CryptoCompare
- **Technical Indicators**: SMA, EMA, MACD, RSI, Bollinger Bands, ATR
- **Trading Signals**: Automated buy/sell/neutral assessment with signal scoring
- **Historical Data**: OHLCV data up to 60+ days
- **Pay-per-use**: 0.001 USDT per call via SkillPay

## Quick Start

```bash
# Get current prices
python scripts/fetch_market.py --coins BTC,ETH,SOL --test-mode

# Run technical analysis
python scripts/calc_indicators.py --coin BTC --test-mode
```

## Installation

### From ClawHub
```bash
clawhub install crypto-market-analyzer
```

### Manual
```bash
cp -r crypto-market-analyzer ~/.openclaw/workspace/skills/
openclaw gateway restart
```

## Requirements

- Python 3.9+
- `requests` library (`pip install requests`)

## License

MIT
