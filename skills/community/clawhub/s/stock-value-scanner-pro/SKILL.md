---
name: stock-value-scanner-pro
description: >
  美股逆向价值扫描专业版。40+标的+深度估值+宏观经济联动+超额收益归因。
  Serenity风格：回调深度+RSI超卖+EMA金叉+放量反弹+波动收缩。付费技能。
version: 1.0.0
tags: [stocks, value, trading, scanner, pro, us-stocks, paid]
license: MIT
author: Vane
repository: https://github.com/sgready/vane-signals
payment: 
  model: subscription
  price: $29/month
  method: USDT (Base/Arbitrum)
---

# Stock Value Scanner (Pro)

## 简介
专业版美股逆向价值扫描器。免费版所有功能 + Discovery Engine 40+标的 + 深度分析 + 宏观经济。

## Pro 额外功能

### ✅ Discovery Engine（40+标的全覆盖）
涵盖7大板块：
- **AI/半导体**: NVDA, AVGO, AMD, MRVL, ARM, TSMC, ASML
- **光学CPO**: POET, AAOI, CIEN, LITE, COHR
- **互联网**: META, GOOGL, AMZN, RDDT, SNAP, PINS
- **金融科技**: COIN, HOOD, SQ, PYPL, STRIPE
- **消费**: TSLA, AAPL, MSFT
- **通信**: T, VZ, TMUS
- **生物科技**: UNH, LLY, JNJ

### ✅ Discovery Engine评分体系
```
AI/半导体 × 0.30
光学CPO    × 0.20
宏观趋势   × 0.20
板块动量   × 0.15
风险溢价   × 0.15
────────────
总分 0~10
```

### ✅ 深度估值分析
- PE/PB/PS vs 历史分位数
- PEG增长率调整
- DCF 3场景(乐观/基准/悲观)
- 行业对标溢价/折价

### ✅ 宏观经济联动
- 利率预期 → 增长/价值风格轮动
- 美元指数 → 出口/进口板块影响
- 市场恐慌(VIX) → 仓位调整
- 板块轮动热力图

### ✅ 超额收益归因
- 每笔交易归因到: 市场beta / 板块 / 个股alpha
- CAPTURED胜出模式 → 加权提升
- FIX连续亏损 → 调整阈值

### ✅ 7日滚动回测
```
date       | stock | action | entry | exit  | pnl%  
2026-06-07 | NVDA  | hold   | 205.1 | 204.8 | -0.15
2026-06-06 | COIN  | watch  | 148.0 | 152.4 | +2.97 
2026-06-05 | AAOI  | buy    | 165.0 | 177.0 | +7.27 
2026-06-04 | MRVL  | watch  | 258.0 | 263.5 | +2.13 
2026-06-03 | AVGO  | hold   | 380.0 | 385.7 | +1.50 
```

## 使用方法
```bash
# 安装
clawhub install stock-value-scanner-pro

# 运行
openclaw run stock-value-scanner-pro
```

## 输出示例
```json
[
  {"symbol":"AAOI","action":"strong_buy","score":7.2,"price":177.0,"entry":165.0,"pnl_pct":7.27},
  {"symbol":"COIN","action":"watch","score":4.5,"price":152.4,"entry":148.0,"pnl_pct":2.97},
  {"symbol":"NVDA","action":"hold","score":2.1,"price":205.1,"backtest_7d_winrate":71.4}
]
```

## 订阅
**价格: $29/月 (USDT)**
联系 @sgreadybot 订阅
或支付 USDC (Base链) 到: [联系获取地址]
