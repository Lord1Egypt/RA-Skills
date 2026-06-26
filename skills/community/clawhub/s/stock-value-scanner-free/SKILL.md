---
name: stock-value-scanner-free
description: >
  美股逆向价值扫描入门版。11只核心标的实时评分(NVDA/AVGO/MSFT等)，
  5维评分(回调深度/RSI/金叉/放量/筑底)，带回测数据。免费。
version: 1.0.0
tags: [stocks, value, trading, scanner, free, us-stocks]
license: MIT
author: Vane
repository: https://github.com/sgready/vane-signals
---

# Stock Value Scanner (Free)

## 简介
Serenity逆向价值风格的美股扫描器。找回调到位的优质标的。
每天UTC 00:00自动运行一次回测验证，附7日回测记录。

## 功能
- ✅ 11只核心标的实时评分（NVDA/AVGO/MSFT/AMZN/META/GOOGL/RDDT/TSLA/COIN/HOOD/AAPL）
- ✅ 5维评分体系：回调深度 / RSI超卖 / EMA金叉 / 放量反弹 / 波动收缩
- ✅ 每日回测记录（7天滚动）
- ✅ 信号输出JSON格式

## 评分规则
| 维度 | 权重 | 条件 |
|------|------|------|
| 回调深度 | 0.25 | 从高点回调>15%得高分 |
| RSI超卖 | 0.25 | RSI<30 → 满分, RSI<35 → 高分 |
| EMA金叉 | 0.20 | 20EMA上穿50EMA → 满分 |
| 放量反弹 | 0.15 | 成交量>均值1.5倍 + 收阳 |
| 波动收缩 | 0.15 | ATR持续收缩 |

## 回测数据样例（最近7天）
```
date       | stock | score | entry  | exit   | pnl%  
2026-06-07 | NVDA  | 2.1   | 205.1  | 204.8  | -0.15
2026-06-06 | COIN  | 4.5   | 148.0  | 152.4  | +2.97 ✓
2026-06-05 | AAOI  | 6.2   | 165.0  | 177.0  | +7.27 ✓
2026-06-04 | MRVL  | 3.8   | 258.0  | 263.5  | +2.13 ✓
2026-06-03 | AVGO  | 2.5   | 380.0  | 385.7  | +1.50 ✓
```

## 使用方法
```bash
# 安装
clawhub install stock-value-scanner-free

# 运行
openclaw run stock-value-scanner-free

# 输出示例
[
  {"symbol": "NVDA", "score": 2.1, "action": "hold"},
  {"symbol": "COIN", "score": 4.5, "action": "watch"},
  {"symbol": "AAOI", "score": 6.2, "action": "buy"},
  {"symbol": "MRVL", "score": 3.8, "action": "watch"}
]
```

## 数据来源
- Yahoo Finance实时行情
- 无需API Key，无需VPN

## 限制
- ❌ 仅11只核心标的
- ❌ 无多平台支持（仅Yahoo Finance）
- ❌ 无深度市场分析
- ❌ 无资金管理建议

## 升级
需要完整版？安装 Pro 版：
- ✅ 40+标的扫描（Discovery Engine）
- ✅ 深度估值分析
- ✅ 宏观经济联动
- ✅ 超额收益归因
- ✅ 多平台数据(Yahoo/新浪/腾讯)
- ✅ Telegram推送

`clawhub install stock-value-scanner-pro`
