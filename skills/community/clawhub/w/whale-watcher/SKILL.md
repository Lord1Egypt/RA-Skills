---
name: whale-watcher
version: 1.0.0
description: |
  Monitor crypto whale wallets for large transactions.
  Track big moves on Ethereum, BSC, and other chains.
  Get alerts when whales move significant amounts.
metadata:
  openclaw:
    emoji: 🐋
    requires:
      env:
        - TELEGRAM_BOT_TOKEN
      bins:
        - python3
        - curl
  pricing:
    type: freemium
    free:
      description: "监控 1 个钱包，阈值$50,000"
      limits:
        wallets: 1
        minThreshold: 50000
    pro:
      price: 1.99
      currency: USD
      period: monthly
      description: "监控 10 个钱包，阈值$10,000，实时推送"
      features:
        - "监控 10 个钱包"
        - "最低$10,000 阈值"
        - "Telegram 实时推送"
        - "历史数据分析"
        - "多链支持 (ETH, BSC, ARB, OP)"
---

# 🐋 Whale Watcher - 巨鲸钱包监控

Monitor crypto whale wallets and get alerts for large transactions.

## Features

- 🔍 Track specific whale wallets
- 💰 Set minimum transaction threshold
- ⛓️ Support multiple chains (ETH, BSC, etc.)
- 📱 Telegram alerts
- 📊 Transaction history

## Usage

```bash
# Monitor a wallet
/whale-watcher monitor 0x123...abc --threshold 1000000

# Check recent transactions
/whale-watcher txs 0x123...abc

# Set alert threshold
/whale-watcher alert --min 5000000
```

## API Sources

- Etherscan API
- BscScan API
- On-chain data

## Setup

Add to environment:
```bash
export ETHERSCAN_API_KEY="your_key"
export BSCSCAN_API_KEY="your_key"
```

