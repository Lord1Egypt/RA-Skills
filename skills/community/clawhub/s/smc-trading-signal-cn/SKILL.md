---
name: smc-trading-signal
description: SMC 聪明钱交易信号监控，1H 定方向 +15M 入场，ATR 动态止盈止损。支持黄金/加密货币/外汇。
author: 小爪 AI
version: 1.0.0
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["python3","uv"]}}}
---

# SMC 交易信号监控

基于 SMC（Smart Money Concepts）聪明钱交易理念，自动监控市场信号并推送交易机会。

## 核心策略

### 📊 多时间周期分析

- **1H（1 小时）** - 确定趋势方向
  - BULLISH（偏多）→ 只做多
  - BEARISH（偏空）→ 只做空

- **15M（15 分钟）** - 精确入场点
  - IFC 机构蜡烛确认
  - SSL 流动性扫损
  - CHOCH 趋势转变

### 💰 ATR 动态止盈止损

基于 15 分钟 ATR（平均真实波幅）动态计算：

| 项目 | 计算方式 |
|------|----------|
| **止损** | 入场价 ± 1 × ATR |
| **TP1** | 入场价 ± 1.5 × ATR (1:1.5) |
| **TP2** | 入场价 ± 3 × ATR (1:3.0) |
| **TP3** | 入场价 ± 5 × ATR (1:5.0) |

**优势**:
- ✅ 自适应市场波动
- ✅ 风险回报比合理
- ✅ 避免固定点数的弊端

## 功能特点

- 📈 **多品种支持**: 黄金/加密货币/外汇
- ⏰ **实时监控**: 每小时自动检查
- 🎯 **精准信号**: 1H 方向 + 15M 入场
- 💡 **教学模式**: 解释每个信号的含义
- 📊 **回测数据**: 历史信号统计

## 快速开始

### 1. 安装技能

```bash
clawhub install smc-trading-signal
```

### 2. 配置监控品种

编辑 `config/symbols.json`:

```json
{
  "symbols": [
    {
      "name": "黄金",
      "code": "GC",
      "source": "akshare",
      "enabled": true
    },
    {
      "name": "比特币",
      "code": "BTCUSDT",
      "source": "binance",
      "enabled": true
    }
  ]
}
```

### 3. 设置推送

编辑 `config/notify.json`:

```json
{
  "channels": ["qqbot", "wechat"],
  "min_risk_reward": 1.5,
  "max_signals_per_day": 5
}
```

### 4. 启用监控

```bash
# 手动测试
python3 scripts/monitor.py --test

# 启用定时任务（每小时）
openclaw cron add smc-trading-signal --interval 60
```

## 输出示例

```
📈 SMC 交易信号 - 黄金 (GC)
⏰ 2026-03-24 16:30

【趋势分析】
├ H1 趋势：BEARISH (看跌)
├ 当前价格：2156.80
└ 日内范围：2142.30 - 2168.90

【交易信号】做空
├ 入场：2156.80 附近
├ 止损：2142.30 (1 × ATR)
├ TP1: 2171.30 (1:1.5)
├ TP2: 2185.80 (1:3.0)
└ TP3: 2200.30 (1:5.0)

【信号依据】
1. ✅ SSL 流动性扫损
   H1 跌破前低，触发卖盘流动性
   
2. ✅ IFC 机构蜡烛
   15M 大阴线，成交量放大

【风险提示】
⚠️ 风险回报比：1:3.0
⚠️ 建议仓位：总资金 2-3%
⚠️ 严格执行止损

---
💡 SMC 策略 | H1 定方向 + 15M 入场 | ATR 动态风控
```

## 配置说明

### 时间周期配置

```json
{
  "trend_timeframe": "1H",
  "entry_timeframe": "15M",
  "check_interval_minutes": 60
}
```

### ATR 配置

```json
{
  "atr_period": 14,
  "stop_loss_atr": 1.0,
  "take_profit_levels": [1.5, 3.0, 5.0]
}
```

### 风险控制

```json
{
  "max_position_size": 0.03,
  "daily_loss_limit": 0.05,
  "min_risk_reward": 1.5
}
```

## SMC 术语解释

| 术语 | 含义 |
|------|------|
| **IFC** | Institutional Fair Candle，机构公平蜡烛 |
| **SSL** | Sell Side Liquidity，卖方流动性 |
| **BSL** | Buy Side Liquidity，买方流动性 |
| **CHOCH** | Change of Character，趋势转变 |
| **OB** | Order Block，订单块 |
| **FVG** | Fair Value Gap，公允价值缺口 |

## 适用市场

| 市场 | 推荐 | 说明 |
|------|------|------|
| **黄金 (XAU/USD)** | ✅ 强烈推荐 | 波动适中，SMC 信号清晰 |
| **比特币** | ✅ 推荐 | 高波动，需调整 ATR 系数 |
| **外汇主要货币对** | ✅ 推荐 | EUR/USD, GBP/USD 等 |
| **原油** | ⚠️ 谨慎 | 地缘政治影响大 |
| **股票** | ❌ 不推荐 | 不适合 SMC 策略 |

## 常见问题

**Q: 信号频率是多少？**  
A: 每小时检查一次，平均每天 2-5 个信号。

**Q: 准确率如何？**  
A: SMC 策略胜率约 55-65%，但风险回报比高（1:3+）。

**Q: 需要手动执行吗？**  
A: 是的，信号仅供参考，需自行判断执行。

**Q: 可以自动交易吗？**  
A: 暂不支持，建议手动执行以确保风控。

## 风险提示

⚠️ **重要声明**:
- 本技能提供的信号仅供参考，不构成投资建议
- 交易有风险，入市需谨慎
- 请严格执行止损，控制仓位
- 过往表现不代表未来收益

## 更新日志

### v1.0.0 (2026-03-24)
- ✅ 首次发布
- ✅ 1H+15M 多周期分析
- ✅ ATR 动态止盈止损
- ✅ 黄金/加密货币支持

## 许可证

MIT License

## 反馈

GitHub: https://github.com/zt6558609-cpu/smc-trading-signal

---

**交易有风险，请理性投资！** 📉📈
