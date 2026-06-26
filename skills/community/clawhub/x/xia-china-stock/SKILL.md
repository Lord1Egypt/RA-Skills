---
name: china-stock-analysis
description: Comprehensive A-share & HK stock analysis toolkit for OpenClaw agents. Technical indicators (MA/MACD/RSI/KDJ/BOLL), multi-source data (Eastmoney API, Akshare, Yahoo Finance), news aggregation, portfolio watchlist, and integrated reports. Activate when user asks about Chinese stock analysis, technical indicators, market trends, or investment research.
metadata:
  {
    "emoji": "📈",
    "requires": {},
    "install": [
      {
        "id": "pip-deps",
        "kind": "pip",
        "packages": ["pandas", "numpy", "requests"],
        "label": "Install Python dependencies"
      }
    ]
  }
---

# China Stock Analysis v1.0

A comprehensive stock analysis toolkit for Chinese A-share and Hong Kong markets. Provides technical indicators, financial data queries, news aggregation, and integrated analysis reports.

## Features

- 📊 **Technical Indicators** — MA, MACD, RSI, KDJ, Bollinger Bands, Volume
- 📡 **Multi-Source Data** — Eastmoney MX API, Akshare, Yahoo Finance with auto-fallback
- 📰 **News Aggregation** — Multi-source stock news search
- 👀 **Watchlist + Alerts** — Track stocks with price targets and signal alerts
- 📋 **Integrated Reports** — One-command comprehensive analysis with natural language output
- ⚡ **Daily Automation** — Cron-ready daily close analysis scripts

## Configuration

### No API Key Required!

This skill uses **100% free data sources** — no registration or API keys needed:
- **Sina Finance** — Real-time quotes + historical K-line (primary)
- **Akshare** — A-share market data (fallback)
- **Yahoo Finance** — Global market data (fallback)

### Optional Environment Variables

| Variable | Description |
|----------|-------------|
| `PYTHONIOENCODING` | Set to `utf-8` on Windows to avoid encoding errors |

## Usage

### 1. Technical Analysis

```bash
# A-share stock (6-digit code)
python {baseDir}/scripts/technical_indicators.py 002475
python {baseDir}/scripts/technical_indicators.py 600519

# Specify data source
python {baseDir}/scripts/technical_indicators.py 002475 --source eastmoney
python {baseDir}/scripts/technical_indicators.py 002475 --source akshare
python {baseDir}/scripts/technical_indicators.py 002475.SZ --source yahoo

# JSON output for automation
python {baseDir}/scripts/technical_indicators.py 002475 --format json
```

**Output includes:**
- MA (5/10/20/60/120/250) with alignment status
- MACD (DIF/DEA/histogram) with crossover detection
- RSI (6/14/24) with overbought/oversold signals
- KDJ with crossover detection
- Bollinger Bands (upper/mid/lower, bandwidth, position)
- Volume analysis (volume ratio, price-volume relationship)
- Composite trend score (-100 to 100) with signal summary

### 2. Integrated Analysis Report

```bash
# Full analysis (technical + news + recommendation)
python {baseDir}/scripts/integrated_analysis.py 002475

# With explicit stock name
python {baseDir}/scripts/integrated_analysis.py 002475 --name 立讯精密

# Multiple stocks
python {baseDir}/scripts/integrated_analysis.py 002475 002594 600938

# Daily close analysis (reads watchlist)
python {baseDir}/scripts/daily_close_analysis.py
python {baseDir}/scripts/daily_close_analysis.py --stocks 002475.立讯精密 002594.比亚迪
```

**Report includes:**
- Technical indicators summary
- Key support/resistance levels
- Recent news and catalysts
- Buy/Hold/Sell recommendation with rationale
- Risk warnings

### 3. Real-time Quote

```bash
# Single stock quote
python {baseDir}/scripts/sina_finance.py 002475 --mode quote

# Historical K-line
python {baseDir}/scripts/sina_finance.py 002475 --mode kline --period 6mo

# Batch quotes (multiple stocks in one request)
python {baseDir}/scripts/sina_finance.py --mode batch --symbols 002475 002594 600519
```

### 4. News Search

```bash
# Search stock news
python {baseDir}/scripts/news_search.py "立讯精密 最新消息"

# Search with date range
python {baseDir}/scripts/news_search.py "比亚迪" --days 7
```

### 5. Watchlist Management

```bash
# Add stock to watchlist
python {baseDir}/scripts/watchlist.py add 002475 --name 立讯精密

# Add with price alert
python {baseDir}/scripts/watchlist.py add 002475 --name 立讯精密 --target 45.00 --stop 30.00

# View watchlist
python {baseDir}/scripts/watchlist.py list

# Check alerts
python {baseDir}/scripts/watchlist.py check
```

## Cron Integration

For automated daily analysis, set up cron jobs:

```yaml
# Pre-market analysis (09:15 weekdays)
- cron: "15 9 * * 1-5"
  command: "python {baseDir}/scripts/integrated_analysis.py 002475 002594 600938 --mode pre-market"

# Morning summary (11:35 weekdays)
- cron: "35 11 * * 1-5"
  command: "python {baseDir}/scripts/daily_close_analysis.py --mode morning"

# Close analysis (15:05 weekdays)
- cron: "5 15 * * 1-5"
  command: "python {baseDir}/scripts/daily_close_analysis.py"
```

## Data Sources (All Free, No API Key)

| Source | Markets | Speed | Reliability | Key Required |
|--------|---------|-------|-------------|---------------|
| Sina Finance | A-share, HK, US | Fast | High | **No** ✅ |
| Akshare | A-share, HK, US | Medium | High | **No** ✅ |
| Yahoo Finance | A-share, HK, US | Medium | Medium | **No** ✅ |

**Fallback order:** Sina Finance → Akshare → Yahoo Finance

## Analysis Output Template

```
## 📊 {股票名称}({代码}) 综合分析

### 📈 技术指标概览
| 指标 | 数值 | 信号 |
|------|------|------|
| MA趋势 | 多头/空头排列 | 🟢/🔴 |
| MACD | DIF/DEA/柱状 | 金叉/死叉 |
| RSI(14) | XX | 超买/超卖/中性 |
| KDJ | K/D/J值 | 金叉/死叉 |
| 布林带 | 上/中/下轨 | 位置判断 |
| 综合评分 | XX/100 | 强看多→强看空 |

### 📰 近期资讯
- ...

### 💡 投资建议
**建议：买入/持有/卖出**
- 理由：...
- 关键位：支撑 XX / 压力 XX
- 风险：...

⚠️ 以上分析仅供参考，不构成投资建议。投资有风险，入市需谨慎。
```

## Supported Markets

| Market | Code Format | Examples |
|--------|-------------|---------|
| Shanghai A | XXXXXX.SH | 600519.SH (贵州茅台) |
| Shenzhen A | XXXXXX.SZ | 000001.SZ (平安银行) |
| Hong Kong | XXXX.HK | 0700.HK (腾讯) |
| Shorthand (A-share) | 6 digits | 002475 (立讯精密) |

## Dependencies

```
pandas>=1.5
numpy>=1.24
requests>=2.28
akshare>=1.10   # optional fallback, recommended
yfinance>=0.2    # optional fallback, recommended
```

## Limitations

- A-share data may have 15-20 min delay on some sources
- MX API requires valid API key (free tier available)
- Hong Kong stock coverage varies by data source
- Technical indicators based on historical data, not predictive

## Disclaimer

⚠️ **NOT FINANCIAL ADVICE.** For informational purposes only. Consult a licensed financial advisor before making investment decisions.
