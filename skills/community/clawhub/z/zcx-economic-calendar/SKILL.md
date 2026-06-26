---
name: economic-calendar
description: Track and analyze global economic data releases, central bank meetings, and key financial events. Covers US, China, EU, Japan, UK, and other major economies with impact ratings, market expectations, and trading strategies.
emoji: 📅
tags: [macroeconomics, forex, trading, calendar, central-bank, data-release]
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Economic Calendar — 经济日历 & 宏观数据

Track important economic releases and their potential market impact across global markets. Covers data schedules, consensus expectations, and trading implications.

## Key Data Sources

### 1. China Economic Data (国家统计局)

```bash
# Recent China economic indicators
curl -s "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgnd&rowcode=zb&colcode=sj&wds=[]&dfwds=[]"
```

**Key indicators:**
| Indicator | Frequency | Impact | Market |
|:----------|:----------|:-------|:-------|
| GDP (国内生产总值) | 季度 | 🔴高 | 股指/商品 |
| CPI (居民消费价格指数) | 月度 | 🔴高 | 国债 |
| PPI (工业生产者出厂价格) | 月度 | 🟡中 | 商品 |
| PMI (制造业采购经理指数) | 月度 | 🔴高 | 股指/商品 |
| Industrial Production (工业增加值) | 月度 | 🟡中 | 商品 |
| Retail Sales (社会消费品零售总额) | 月度 | 🟡中 | 股指 |
| Fixed Asset Investment (固定资产投资) | 月度 | 🟡中 | 商品 |
| Loan Prime Rate (LPR) | 每月20日 | 🟡中 | 国债/汇率 |

### 2. US Economic Data

```bash
# Federal Reserve economic data
curl -s "https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&series=bcb44e57fb57efbe90002369321bfb3f&lastobs=&from=&to=&filetype=csv"
```

**Key indicators:**
| Indicator | Schedule | Impact | Market |
|:----------|:---------|:-------|:-------|
| Non-Farm Payrolls (非农) | 每月第一个周五 20:30 | 🔴高 | 所有市场 |
| CPI (消费者物价指数) | 月度 20:30 | 🔴高 | 债券/美元 |
| PCE (核心个人消费支出) | 月度 20:30 | 🔴高 | 美联储预期 |
| FOMC Rate Decision | 每6周 02:00 | 🔴高 | 所有市场 |
| Initial Jobless Claims | 每周四 20:30 | 🟢低 | 短期波动 |
| GDP (季度) | 季度 20:30 | 🔴高 | 股市/美元 |
| Retail Sales | 月度 20:30 | 🟡中 | 消费股 |

### 3. EU & Other Regions

**Eurozone:** ECB rate decisions, CPI, GDP, PMI (Markit)
**Japan:** BOJ rate decisions, CPI, Tankan survey
**UK:** BOE rate decisions, CPI, GDP, employment

## Market Impact Guide

| Impact | Typical Move | Trading Strategy |
|:-------|:-------------|:-----------------|
| 🔴 High | 0.5-2% | Wait 30s for initial spike, trade the retrace |
| 🟡 Medium | 0.2-0.5% | Trade the breakout with tight stops |
| 🟢 Low | <0.2% | Ignore or trade mean reversion |

## Format Output

### Daily Calendar
```
📅 今日经济数据 (2026-05-22)

🇨🇳 中国
时间   数据              预期      前值      影响
09:30  5月LPR 1年期     3.45%    3.45%    🟡
09:30  5月LPR 5年期     3.85%    3.85%    🟡

🇺🇸 美国
20:30  初请失业金        23.5万   22.8万   🟢
22:00  4月成屋销售       420万    419万    🟡
22:30  EIA天然气库存     +80B     +76B     🟢

🇪🇺 欧元区
17:00  5月消费者信心    -14.0    -14.7    🟡

🏦 央行事件
02:00  FOMC 5月会议纪要公布 🟡
```

### Weekly Preview
```
📅 本周重要事件 (2026-05-18 ~ 2026-05-24)

🔥 重点关注
• 周三 02:00 FOMC 5月会议纪要 — 关注缩表信号
• 周四 09:30 中国5月LPR — 是否降息？
• 周五 20:30 美国4月核心PCE — 通胀风向标

📊 市场预期
• 美联储6月加息概率: 15%
• 中国LPR降息概率: 30%
```

## Trading Tips

- **Before the data:** Reduce position size by 50%, widen stops by 2x
- **At the release:** DO NOT trade the first 30 seconds (liquidity hole + spreads widen)
- **After the data:** Wait for the 5-minute candle to confirm direction
- **Key principle:** "Buy the rumor, sell the news" — price often reverses after the initial spike
- **Correlation:** Strong NFP → USD up → Gold down → BTC down (risk-off)
- **Event clusters:** Multiple releases at same time = extra volatility (trade smaller)

## Data Timings (GMT+8)

| Time | Release Region | Notes |
|:-----|:---------------|:------|
| 07:50 | 🇯🇵 Japan | BOJ data |
| 09:30 | 🇨🇳 China | Official data |
| 14:00 | 🇩🇪 Germany | Industrial data |
| 15:00-17:00 | 🇪🇺 Eurozone | Various |
| 20:30 | 🇺🇸 US | Main batch |
| 22:00-23:00 | 🇺🇸 US | Late data |
| 02:00 (next day) | 🇺🇸 US | FOMC days |
