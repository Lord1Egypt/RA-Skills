---
name: Stock Browser Fetcher
slug: stock-browser-fetcher
version: 1.0.0
homepage: https://github.com/openclaw/stock-browser-fetcher
description: "通过浏览器控制实时抓取A股市场数据，支持东方财富、新浪财经等金融网站，绕过反爬机制。输出：上证/深证/创业板指数、北向资金、涨跌家数、涨停跌停数据。"
changelog: "初始版本 - A股数据抓取功能"
metadata: {"clawdbot":{"emoji":"📈","os":["linux","darwin","win32"]}}
---

# Stock Browser Fetcher 📈

通过浏览器控制实时抓取 A 股市场数据，绕过反爬机制。

## 功能

- 📊 实时获取上证、深证、创业板指数
- 💰 北向资金数据
- 📈 涨跌家数统计
- 🔥 涨停跌停数量

## 使用方法

```python
from skills.stock_browser_fetcher import fetch_market_data

# Fetch today's market data
data = fetch_market_data()
print(data)
```

## 输出格式

```json
{
  "date": "2026-03-05",
  "sh_index": {"close": 3000.12, "change_pct": 0.5},
  "sz_index": {"close": 9500.45, "change_pct": 0.8},
  "chi_index": {"close": 2000.33, "change_pct": 1.2},
  "north_flow": 10.5,
  "up_count": 2500,
  "down_count": 2300,
  "limit_up": 50,
  "limit_down": 10
}
```

## 数据源

- 东方财富 (eastmoney.com)
- 新浪财经 (finance.sina.com.cn)

## 依赖

- OpenClaw `browser` tool
- Python 3.8+

## 使用场景

- 量化交易数据采集
- 金融数据分析
- 投资组合监控
- 市场情绪跟踪