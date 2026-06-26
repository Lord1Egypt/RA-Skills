---
name: whale-alert-monitor
description: |
  虚拟币大户账户预警监测助手 - 实时监控鲸鱼钱包动向、大额转账、交易所资金流向。
  当用户需要以下功能时触发此skill：
  (1) 监控特定大户/鲸鱼钱包的交易活动
  (2) 追踪大额资金流入/流出交易所
  (3) 设置自定义阈值的大额转账预警
  (4) 分析鲸鱼持仓变化和积累/派发模式
  (5) 接收Telegram/Discord实时预警通知
  (6) 生成鲸鱼行为报告和趋势分析
---

# Whale Alert Monitor

> 💰 **本 Skill 已接入 SkillPay 付费系统**
> - 每次调用费用：**0.01 USDT**
> - 支付方式：BNB Chain USDT
> - 请先确保账户有足够余额

虚拟币大户账户预警监测助手 — 追踪聪明钱的每一步

## 核心能力

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

### 5. 预警管理
- **分级预警** - 按金额分级（普通/重要/紧急）
- **冷却机制** - 防止重复预警
- **历史记录** - 保存所有预警历史

## 使用工作流

### 快速开始

```bash
# 1. 监控特定钱包
python scripts/whale_tracker.py --wallet 0x... --chain ethereum

# 2. 设置大额转账预警
python scripts/transfer_monitor.py --min-eth 1000 --notify telegram

# 3. 监控交易所流入流出
python scripts/exchange_flow.py --exchange binance --threshold 5000000

# 4. 分析鲸鱼持仓
python scripts/holding_analyzer.py --wallet 0x... --days 30

# 5. 启动全面监控
python scripts/monitor_daemon.py --config config.yaml
```

### 配置示例

```yaml
# config/whale_monitor.yaml
monitoring:
  # 监控的钱包列表
  wallets:
    - address: "0x742d35Cc6634C0532925a3b8D4E6D3b6e8d3e8D3"
      label: "Smart Whale A"
      chains: [ethereum, arbitrum]
    - address: "0x8ba1f109551bD432803012645Hac136c82C3e8D3"
      label: "Institution B"
      chains: [ethereum]
  
  # 大额转账阈值
  thresholds:
    ETH: 1000
    WBTC: 50
    USDC: 1000000
    USDT: 1000000
  
  # 交易所监控
  exchanges:
    - name: binance
      addresses:
        - "0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE"
      in_threshold: 5000000
      out_threshold: 5000000
    - name: coinbase
      addresses:
        - "0x71660c4005BA85c37ccec55d0C4493E66Fe775d3"
  
  # 通知设置
  notifications:
    telegram:
      enabled: true
      bot_token: ${TELEGRAM_BOT_TOKEN}
      chat_id: ${TELEGRAM_CHAT_ID}
    discord:
      enabled: true
      webhook_url: ${DISCORD_WEBHOOK_URL}
    
  # 检查间隔（秒）
  interval: 60
```

## 脚本说明

### scripts/whale_tracker.py
追踪特定鲸鱼钱包的所有活动

```bash
# 基础用法
python scripts/whale_tracker.py --wallet 0x742d... --chain ethereum

# 查看历史交易
python scripts/whale_tracker.py --wallet 0x742d... --history --days 7

# 分析持仓变化
python scripts/whale_tracker.py --wallet 0x742d... --analyze
```

### scripts/transfer_monitor.py
监控大额转账并发送预警

```bash
# 监控ETH大额转账
python scripts/transfer_monitor.py --token ETH --min-value 1000 --interval 60

# 监控USDT转账
python scripts/transfer_monitor.py --token USDT --min-value 1000000 --notify telegram

# 多链监控
python scripts/transfer_monitor.py --config thresholds.yaml
```

### scripts/exchange_flow.py
监控交易所资金流向

```bash
# 监控币安
python scripts/exchange_flow.py --exchange binance --threshold 5000000

# 对比多个交易所
python scripts/exchange_flow.py --compare binance,coinbase,okx

# 生成流向报告
python scripts/exchange_flow.py --report --days 7
```

### scripts/holding_analyzer.py
分析鲸鱼持仓和盈亏

```bash
# 分析持仓
python scripts/holding_analyzer.py --wallet 0x742d...

# 追踪成本基础
python scripts/holding_analyzer.py --wallet 0x742d... --cost-basis

# 生成持仓报告
python scripts/holding_analyzer.py --wallet 0x742d... --report
```

### scripts/alert_manager.py
预警管理系统

```bash
# 列出所有预警
python scripts/alert_manager.py --list

# 测试预警通知
python scripts/alert_manager.py --test --channel telegram

# 导出预警历史
python scripts/alert_manager.py --export --since 2024-01-01
```

### scripts/monitor_daemon.py
守护进程模式（持续监控）

```bash
# 启动监控
python scripts/monitor_daemon.py --config config.yaml

# 后台运行
python scripts/monitor_daemon.py --config config.yaml --daemon

# 停止监控
python scripts/monitor_daemon.py --stop
```

## 数据源

### 推荐API

| 数据源 | 用途 | 免费额度 |
|--------|------|----------|
| Etherscan | 基础链上数据 | 100K calls/day |
| Alchemy | 高级链上查询 | 300M CU/month |
| Moralis | 跨链数据 | 免费版可用 |
| Arkham | 地址标签 | 免费版有限制 |

### 交易所地址库

内置主要交易所的热钱包地址：
- Binance
- Coinbase
- OKX
- Bybit
- KuCoin
- Huobi
- Bitfinex

## 预警级别

### 🔴 紧急 (Critical)
- 单笔转账 > 10,000 ETH
- 单笔转账 > 500 BTC
- 单笔转账 > $50M USDT/USDC

### 🟠 重要 (Warning)
- 单笔转账 > 1,000 ETH
- 单笔转账 > 50 BTC
- 单笔转账 > $10M USDT/USDC

### 🟡 普通 (Info)
- 单笔转账 > 100 ETH
- 单笔转账 > 5 BTC
- 单笔转账 > $1M USDT/USDC

## 最佳实践

1. **设置合理的阈值** - 避免过多的噪音预警
2. **多源验证** - 结合多个数据源确认信号
3. **关注模式** - 不只看单笔交易，关注行为模式
4. **设置冷却时间** - 防止同一交易重复预警
5. **记录历史** - 追踪鲸鱼的历史准确率

## 风险提示

⚠️ **本工具仅供信息监控，不构成投资建议**

- 鲸鱼行为不代表市场方向
- 大户可能分散在多个钱包
- 交易所地址可能变更
- 链上数据可能有延迟

## 高级功能

### 行为模式识别

```python
# 识别积累模式
if balance_change > 0 and duration > 7_days:
    pattern = "accumulating"

# 识别派发模式  
if balance_change < 0 and exchange_inflow > threshold:
    pattern = "distributing"

# 识别洗盘模式
if frequent_transfers and small_amounts:
    pattern = "wash_trading"
```

### 智能预警

```python
# 只在特定条件下预警
if whale_score > 80 and token_safety > 70:
    send_alert()
```

---

*追踪聪明钱，但要有自己的判断。*
