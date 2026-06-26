---
name: trading-briefing
description: 每日加密货币交易综合简报。当用户说"早报"、"简报"、"今天市场怎么样"、"交易情况"、"检查交易系统"、"系统状态"、"trading status"、"daily briefing"时触发。自动聚合：(1) BTC/ETH主流币价格 (2) 实盘机器人状态 (3) 持仓盈亏 (4) 系统健康 (5) 策略发现引擎状态。
---

# Trading Briefing

一站式交易系统简报。运行脚本聚合所有数据，输出格式化报告。

## 快速使用

```bash
python3 /root/.openclaw/workspace/skills/trading-briefing/scripts/briefing.py
```

输出包含：
1. 📊 市场行情 - BTC/ETH价格、24h涨跌
2. 🤖 机器人状态 - 运行状态、最后交易时间
3. 💰 持仓情况 - 当前持仓、浮动盈亏
4. ⚙️ 系统健康 - 磁盘、内存、关键进程
5. 🧠 策略发现 - 发现引擎状态、当前最佳策略

## 配置

编辑 `scripts/config.json` 设置关注的交易对和阈值。

## 依赖

- ccxt (OKX API)
- 无需额外配置，复用 live_trading/config.json 的 API 密钥
