---
name: stock-trader
description: A股股票分析助手。支持实时股价查询、批量查询、财经新闻、潜力股分析、行业资金流向、龙头股分析、消息面情感分析、激进型模拟交易。触发场景：(1) 查询股票实时价格 (2) 分析消息面预测走势 (3) 行业资金+龙头分析 (4) 激进型模拟交易 (5) 制定买卖策略。
---

# Stock Trader - A股投资助手

## 🚀 快速开始

### 1. 查询单只股票

```bash
python scripts/get_price.py <股票代码>
```

### 2. 消息面分析 + 走势预测

```bash
python scripts/analyze_sentiment.py <股票代码>
```

### 3. 激进型模拟交易 ⭐⭐⭐

```bash
# 启动模拟交易
python scripts/simulate_trading.py

# 查看交易报告
python scripts/simulate_trading.py report

# 每日收盘报告
python scripts/simulate_trading.py daily

# 重置账户
python scripts/simulate_trading.py reset
```

**策略配置：**
- 💰 初始资金：5万元
- 📈 风格：激进型（高仓位、追涨杀跌、快进快出）
- 🔥 特点：追强势股(>5%涨幅)，果断割肉(<-3%止损)
- ⏰ 每日收盘自动输出收益报告

### 4. 资金流入行业 + 龙头股分析

```bash
python scripts/analyze_fund_flow.py
```

### 5. 单独分析行业龙头股

```bash
python scripts/analyze_leaders.py <行业名称>
```

### 6. 其他功能

```bash
python scripts/analyze_potential.py    # 潜力股分析
python scripts/batch_query.py          # 批量查询
python scripts/get_news.py             # 财经新闻
```

---

## 📈 股票代码规则

| 市场 | 前缀 | 示例 |
|------|------|------|
| 深圳主板 | sz | sz000001 |
| 深圳创业板 | sz | sz300750 |
| 上海主板 | sh | sh600519 |
| 上海科创板 | sh | sh688981 |

---

## 📊 功能一览

| 功能 | 命令 | 说明 |
|------|------|------|
| 🎮 **模拟交易** | `simulate_trading.py` | 激进型策略模拟炒股 ⭐⭐⭐ |
| 📰 消息面分析 | `analyze_sentiment.py` | 新闻情感+走势预测 |
| 💰 资金+龙头股 | `analyze_fund_flow.py` | 资金流入行业+龙头股 |
| 🏆 行业龙头 | `analyze_leaders.py` | 指定行业龙头分析 |
| 🔥 潜力股 | `analyze_potential.py` | TOP10潜力股 |
| 📰 财经新闻 | `get_news.py` | 新浪财经要闻 |
| 📊 股价查询 | `get_price.py` | 实时股价 |
| 📈 批量查询 | `batch_query.py` | 多股票同时查 |
| ⏰ 价格监控 | `set_alert.py` | 到价提醒 |

---

## 🎮 模拟交易详解

### 激进型策略特点

```
💰 初始资金: 50,000元
📊 仓位管理: 高仓位运行(8-9成)
🔥 追涨策略: 涨幅>5%的强势股
📉 杀跌策略: 亏损>-3%果断割肉
⚡ 交易风格: 短线为主，快进快出
```

### 使用方法

```bash
# 1. 初始化账户
python scripts/simulate_trading.py reset

# 2. 每日查看交易建议
python scripts/simulate_trading.py

# 3. 收盘后查看收益报告
python scripts/simulate_trading.py daily
```

### 输出示例

```
📈 每日收盘报告 - 2026-03-10
💰 资产情况:
  现金: 50000.00元
  持仓: 0.00元 (0只)
  总资产: 50000.00元
  总收益: +0.00元 (+0.00%)
```

---

## 💰 买卖策略模板

### 激进型策略

```
仓位: 保持8-9成高仓位
追涨: 强势股涨幅>5%时追入
杀跌: 亏损>-3%时果断止损
止盈: 盈利>15%时分批止盈
```

### 消息面策略

```
强烈看多 + 技术面突破 → 考虑加仓
偏空 + 技术面走弱 → 考虑减仓
中性 + 震荡行情 → 观望为主
```

---

## ⚠️ 风险提示

- 所有分析仅供参考，**不构成投资建议**
- 股市有风险，投资需谨慎
- 模拟交易仅供参考学习，不代表真实收益
- 激进型策略风险较高，需严格执行止损
- 建议分散投资，控制单只股票仓位不超过20%
- 严格执行止损，保护本金安全

---

## 📦 版本更新

**v1.5.0** - 重磅新功能：
- 🎮 激进型模拟交易功能
- 💰 初始资金5万元
- ⚡ 追涨杀跌策略
- 📈 每日收盘收益报告

**v1.4.1** - 新增功能：
- 📰 股票消息面分析 + 情感评分
- 🎯 基于消息面的股价走势预测

**v1.3.0** - 新增功能：
- 💰 行业资金流向 + 龙头股综合分析

**v1.2.0** - 新增功能：
- 行业主力资金流向分析

**v1.1.0** - 新增功能：
- 财经新闻获取
- 潜力股自动分析

**v1.0.0** - 首发：
- 实时股价查询
- 批量查询
- 价格监控提醒
