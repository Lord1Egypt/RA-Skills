---
name: trade-tracker
description: |
  交易追踪与归因分析 v1.1.0。从交易记录逐笔追踪盈亏、
  按股票/月度/季度/年度归因、交易成本分析(佣金+滑点)、
  持仓时间分析、策略标签归类、多策略对比、ASCII盈亏分布图。

  Use when: 需要复盘交易记录、归因分析、
  查看按股票/时间段的盈亏分布、成本分析、持仓结构。

  🎉 v1.1.0 新增:
  - 月度/季度/年度归因分解(--by month/quarter/year)
  - 交易成本分析(--cost: 佣金占比、滑点估算)
  - 持仓时间分析(--hold: 平均持仓天数、区间分组)
  - 策略标签归类(--tag: 按策略标签汇总)
  - 多策略/多时段对比(--compare)
  - ASCII盈亏分布图(--chart: K线图风格)
  - 自动识别更多日期格式

  触发关键词：交易复盘、归因分析、交易统计、投资收益、持仓分析
  适用范围：CSV 交易记录(含盈亏、日期列)
  运行模式：纯本地
---

# 💰 Trade Tracker

## Overview
从交易记录中提取关键信息，按股票和时间维度进行归因分析。支持成本分析、持仓结构、策略标签归类，帮助你全面理解交易表现。

## Usage
```bash
# 基本分析
python3 scripts/trade_tracker.py --file trades.csv

# 月度归因
python3 scripts/trade_tracker.py --file trades.csv --by month

# 交易成本分析
python3 scripts/trade_tracker.py --file trades.csv --cost

# 持仓时间分析
python3 scripts/trade_tracker.py --file trades.csv --hold

# 策略标签归类（需CSV有 tag 或 strategy 列）
python3 scripts/trade_tracker.py --file trades.csv --tag

# 多策略对比
python3 scripts/trade_tracker.py --file trades.csv --compare

# ASCII盈亏分布图
python3 scripts/trade_tracker.py --file trades.csv --chart

# 输出JSON
python3 scripts/trade_tracker.py --file trades.csv --output analysis.json
```

## 输出示例
```
📊 交易归因分析
    =======================================================
    总交易: 156 (买入82 / 卖出74)
    总盈亏: +45,280.00
    胜率:   58.3% (91/156)
    平均每笔: +290.26

    ── 月度归因 ──
    期间       交易      盈亏          胜率   最佳              最差
    ---------------------------------------------------------------------------
    2026-01    18    +18,500.00   66.7%  比亚迪 (+12,500)    药明康德 (-8,200)
    2026-02    12     +8,200.00   58.3%  宁德时代 (+5,600)   茅台 (-2,300)

    ── 交易成本 ──
    总佣金: +12,450.00
    平均佣金率: 0.080%
    估算滑点: +15,600.00
    成本/盈亏比: 25.3%

    ── 持仓时间 ──
    平均持仓: 4.2天 (最短1天 / 最长22天)
    持仓区间    交易      盈亏
    ------------------------------
    0-1天       45     +12,000.00
    2-3天       38      -3,200.00
    4-7天       48     +18,500.00

    ── 策略标签归因 ──
    策略          交易      盈亏          胜率    平均每笔
    --------------------------------------------------
    突破追涨       45    +12,500.00   62.2%      +277.78
    低吸埋伏       38     +8,200.00   55.3%      +215.79
    日内短线       25     -2,100.00   48.0%       -84.00
```

## 命令详解
| 命令 | 说明 |
|------|------|
| (默认) | 综合交易分析 |
| --by month/quarter/year | 归因周期 |
| --cost | 交易成本分析 |
| --hold | 持仓时间分析 |
| --tag | 策略标签归类 |
| --compare | 多策略对比 |
| --chart | ASCII盈亏分布图 |

## CSV列自动识别
| 字段 | 匹配列名 |
|------|---------|
| 盈亏 | pnl, profit, 盈亏, net_pnl |
| 方向 | direction, action, 方向, side |
| 日期 | date, 日期, trade_date |
| 股票 | stock, 代码, symbol, name |
| 价格 | price, 成交价, avg_price |
| 佣金 | commission, 佣金, fee |
| 策略 | tag, strategy, 策略 |

## Security
- ✅ 纯本地运行，无网络请求
- ✅ 只读交易记录CSV
- ❌ 无任意代码执行
