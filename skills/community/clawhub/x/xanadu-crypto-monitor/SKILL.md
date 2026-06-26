---
name: crypto-monitor
description: Monitor cryptocurrency prices, set alerts, track whale transactions, and analyze on-chain data. Use when: (1) Setting price alerts for crypto, (2) Tracking whale transactions, (3) Monitoring on-chain metrics (volume, TVL, gas), (4) Portfolio tracking for crypto assets.
---

# Crypto Monitor

Monitor cryptocurrency prices, alerts, whale activity, and on-chain metrics.

## Quick Start

```bash
# Check prices
python scripts/monitor.py price BTC ETH SOL

# Set alert
python scripts/monitor.py alert --symbol BTC --above 100000

# Track whale transactions
python scripts/monitor.py whales --symbol BTC --min-value 1000000

# On-chain stats
python scripts/monitor.py stats BTC
```

## Core Features

### 1. Price Monitoring

- Real-time prices from major exchanges
- Price alerts (above/below thresholds)
- 24h change tracking
- Multi-exchange comparison

### 2. Whale Tracking

- Large transaction alerts
- Exchange flows (in/out)
- Wallet tracking (optional)
- Min value thresholds

### 3. On-Chain Metrics

- Network volume
- Gas prices (ETH)
- TVL (Total Value Locked)
- Active addresses
- Hash rate

### 4. Portfolio Tracking

- Hold multiple cryptos
- P&L calculation
- Cost basis tracking
- Performance vs benchmarks

## Usage

### Check Prices
```bash
python scripts/monitor.py price BTC ETH SOL ADA XRP
```

### Set Price Alert
```bash
python scripts/monitor.py alert --symbol BTC --above 100000 --below 90000
python scripts/monitor.py alert --symbol ETH --below 2000
```

### List Alerts
```bash
python scripts/monitor.py alerts
```

### Track Whales
```bash
python scripts/monitor.py whales --symbol BTC --min-value 1000000
python scripts/monitor.py whales --symbol ETH --min-value 500000
```

### On-Chain Stats
```bash
python scripts/monitor.py stats BTC
python scripts/monitor.py stats ETH
```

### Portfolio
```bash
python scripts/monitor.py portfolio --add BTC:0.5 --add ETH:10
python scripts/monitor.py portfolio --show
```

## Supported Cryptos

- BTC (Bitcoin)
- ETH (Ethereum)
- SOL (Solana)
- ADA (Cardano)
- XRP (Ripple)
- DOT (Polkadot)
- MATIC (Polygon)
- AVAX (Avalanche)
- LINK (Chainlink)
- And 100+ more...

## Alert Configuration

Alerts stored in `~/.openclaw/crypto-monitor/alerts.json`

Alert types:
- `--above` price above threshold
- `--below` price below threshold
- `--change` 24h change % threshold

## Data Sources

- CoinGecko API (free tier)
- CoinMarketCap (API key optional)
- On-chain data from public APIs

## Requirements

- Python 3.10+
- `requests` package
- Optional: API keys for higher rate limits

---

## Monetization (SkillPay)

This skill supports SkillPay integration for premium features.

### Pricing Tiers
| Tier | Price | Features |
|------|-------|----------|
| Basic | Free | Basic prices, 1 alert |
| Pro | $19/mo | Unlimited alerts, whale tracking, portfolio |
| Premium | $39/mo | API access, real-time push, priority support |

Owner: Xanadu Studios
