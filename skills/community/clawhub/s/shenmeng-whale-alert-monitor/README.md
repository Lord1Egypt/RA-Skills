# Whale Alert Monitor 🐋

虚拟币大户账户预警监测助手 — 追踪聪明钱的每一步

## 功能特性

### 1. 鲸鱼钱包监控
- **地址追踪** - 监控特定钱包地址的所有链上活动
- **标签系统** - 为已知大户添加标签（交易所、机构、鲸鱼）
- **行为分析** - 识别积累、派发、洗盘等模式

### 2. 大额转账预警
- **自定义阈值** - 设置ETH、BTC、USDT等代币的预警金额
- **多链支持** - 支持以太坊、BSC、Arbitrum等主流链
- **实时通知** - Telegram/Discord/Webhook多渠道推送

### 3. 交易所资金流向
- **流入监控** - 检测大额资金转入交易所（潜在抛压）
- **流出监控** - 检测资金从交易所流出（积累信号）
- **净流量分析** - 计算交易所净流入/流出

### 4. 持仓变化分析
- **余额追踪** - 监控钱包余额变化
- **成本估算** - 估算鲸鱼持仓成本
- **盈亏分析** - 追踪未实现盈亏

## 快速开始

```bash
# 监控特定钱包
python scripts/whale_tracker.py --wallet 0x... --chain ethereum

# 设置大额转账预警
python scripts/transfer_monitor.py --min-eth 1000 --notify telegram

# 监控交易所流入流出
python scripts/exchange_flow.py --exchange binance --threshold 5000000

# 启动全面监控
python scripts/monitor_daemon.py --config config.yaml
```

## 配置示例

```yaml
monitoring:
  wallets:
    - address: "0x742d35Cc6634C0532925a3b8D4E6D3b6e8d3e8D3"
      label: "Smart Whale A"
      chains: [ethereum, arbitrum]
  
  thresholds:
    ETH: 1000
    WBTC: 50
    USDC: 1000000
  
  notifications:
    telegram:
      enabled: true
      bot_token: ${TELEGRAM_BOT_TOKEN}
      chat_id: ${TELEGRAM_CHAT_ID}
```

## 预警级别

- 🔴 **紧急** - 单笔转账 > 10,000 ETH / $50M USDT
- 🟠 **重要** - 单笔转账 > 1,000 ETH / $10M USDT
- 🟡 **普通** - 单笔转账 > 100 ETH / $1M USDT

## 数据来源

- Etherscan API
- Alchemy
- Moralis
- Arkham Intelligence

## 作者

@shenmeng

## 许可证

MIT
