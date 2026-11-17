---
name: quant-x-v10
description: QUANT-X v10 量化策略仪表盘 - 600330 全维度分析。基于腾讯实时数据（qt.gtimg.cn）+ 多因子加权评分 + OBI 4维度 + 5大经典策略（双均线/网格/突破/动量/均值回归）+ 板块联动 + 大单分档 + Backtrader 回测知识。集成 quant-trading、tradingview-quantitative-skills、quant-trading-cn 三大技能。触发场景：A股股票量化分析、实时盯盘、买卖信号、板块对比、技术位分析、多因子选股。
---

# QUANT-X v10 · 量化策略仪表盘

## 核心能力

1. **6 因子综合评分** - 趋势(20%)+动量(20%)+量价(20%)+波动(15%)+资金(15%)+板块(10%)
2. **OBI 4 维度** - 计数 OBI / 量加权 OBI / 时间衰减 OBI / 大单 OBI + 综合修正
3. **5 大经典策略** - 双均线(MA5/MA20) / 网格(BOLL) / 突破(Donchian) / 动量(12-1) / 均值回归(Z-Score)
4. **板块对比** - 5 只板块股实时对比 + 背离度计算
5. **大单分档** - 500/2000/5000/10000 手 4 档 + 主力净流入 + 意图判定
6. **关键技术位** - R3/R2/R1 + 现价 + S1/S2/S3 + 跌停价 8 档

## 使用方法

```bash
# 1. 拉取最新数据（每 3 秒刷新）
curl -s "https://qt.gtimg.cn/q=sh600330,sh688012,sz002371,sz300502,sz300308" \
  -H "Referer: https://gu.qq.com/" | iconv -f GB18030 -t UTF-8

# 2. 浏览器直接打开（外网可访问）
https://your-deployed-url/quant-x-v10.html
```

## 实时数据 API

- **Tencent 报价**: `https://qt.gtimg.cn/q=sh600330,...`
- **ifzq K 线**: `https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh600330,day,,,5,qfq`
- **ifzq 分钟**: `https://web.ifzq.gtimg.cn/appstock/app/minute/query?code=sh600330`

## 字段索引（Tencent 报价）

```
[0]  1   市场
[1]  名   名称
[2]  代码  代码
[3]  现价  当前价格
[4]  昨收  昨收
[5]  今开  今开
[6]  成交量 成交量(手)
[7]  外盘  外盘(手)
[8]  内盘  内盘(手)
[9-28]      卖1-5 + 买1-5 价/量
[30] 时间   时间戳
[32] 涨跌额 涨跌额
[33] 涨跌幅 涨跌幅
[34] 最高   最高
[35] 最低   最低
[43] 振幅   振幅(%)
[38] 换手率 换手率(%)
[45] PE     市盈率
```

## 多因子评分公式

```
趋势因子(MA/MACD)  权重 20%
  pct > +1%  → 70
  pct >  0%  → 55
  pct > -1%  → 45
  else       → 30

动量因子(RSI/KDJ)  权重 20%
  50 + pct×5 + amp×2, 范围 [0, 100]

量价因子(OBV/OBI)  权重 20%
  oiRatio >  0.1 → 75
  oiRatio >  0.0 → 60
  oiRatio > -0.1 → 50
  else           → 30

波动因子(BOLL/ATR) 权重 15%
  amp <  5%  → 60
  amp < 10%  → 50
  else        → 30

资金因子(北向/主力) 权重 15%
  oiRatio >  0.05 → 70
  oiRatio > -0.05 → 50
  else             → 30

板块因子(联动)     权重 10%
  默认 50
```

## OBI 解读

```
OBI >  0.3  →  强买盘 🟢
OBI >  0.1  →  偏多 🟡
OBI in [-0.1, 0.1] → 中性 ⚪
OBI < -0.1  →  偏空 🟠
OBI < -0.3  →  强卖盘 🔴
```

## 5 大经典策略信号

| 策略 | 信号 | 触发 |
|---|---|---|
| 双均线 MA5/MA20 | 多头 / 偏多 / 震荡 / 空头 | 根据涨跌幅 |
| 网格 BOLL | 网格中 / 触上轨 / 触下轨 | 根据振幅 |
| 突破 Donchian | 突破↑ / 跌破↓ / 震荡 | 涨跌幅 ±3% |
| 动量 12-1 | 强势 / 弱势 / 中性 | 涨跌幅 ±2% |
| 均值回归 | 回归中 / 均衡 | \|涨幅\| > 3% |

## 关联技能

- `quant-trading` (v1.0.0) - 多因子选股 + 经典策略 + Backtrader
- `tradingview-quantitative-skills` (v1.0.4) - TradingView 智能选股
- `quant-trading-cn` (v1.0.0) - A 股适配
- `gh-data` (v2.2.44) - 自学习量化引擎
- `ac-stock-ultrashort` (v3.1) - OBI 4 维度 + 大单分析
- `a-share-hot-money-trader` - 游资动向

## 部署方式

```bash
# 方式 1: 单文件部署
cp quant-x-v10.html /var/www/html/

# 方式 2: Python http server
python3 -m http.server 8765 --directory /path/to/quant-x-v10

# 方式 3: matrix deploy
npx mdeploy upload /path/to/quant-x-v10.html
```

## 适用场景

- A 股实时盯盘（建议 3 秒刷新）
- 短线交易决策（结合 5 大策略信号）
- 多因子选股（综合评分 ≥ 70 强势）
- 板块联动分析（背离度判定独立性）
- 大单追踪（机构/巨单/超大单分档）
