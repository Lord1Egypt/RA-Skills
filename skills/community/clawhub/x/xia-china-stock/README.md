# China Stock Analysis (中国股市分析)

A comprehensive AI agent skill for analyzing Chinese A-share and Hong Kong stocks. Provides multi-source technical indicators, financial data queries, news aggregation, watchlist management, and automated daily analysis reports.

## ✨ Features

- **📊 Technical Indicators** — MA, MACD, RSI, KDJ, Bollinger Bands, Volume Analysis
- **📡 Multi-Source Data** — Eastmoney MX API, Akshare, Yahoo Finance with auto-fallback
- **📰 News Aggregation** — Multi-source stock news and catalyst search
- **👀 Watchlist + Alerts** — Track stocks with price targets and signal change alerts
- **📋 Integrated Reports** — One-command comprehensive analysis with buy/hold/sell signals
- **⏰ Cron-Ready** — Automated pre-market, morning, and daily close analysis
- **🇨🇳 China-First** — Optimized for A-share market conventions (Shanghai/Shenzhen codes)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenClaw agent with this skill installed

### Install Dependencies
```bash
pip install pandas numpy requests
# Optional but recommended (for fallback data sources):
pip install akshare yfinance
```

### That's It!
No API keys, no registration, no configuration needed.

### Basic Usage
```bash
# Technical analysis
python scripts/technical_indicators.py 002475

# Full integrated report
python scripts/integrated_analysis.py 002475 --name 立讯精密

# Financial data query
python scripts/mx_data.py "立讯精密最新价、市盈率"
```

## 📂 Project Structure

```
china-stock-analysis/
├── SKILL.md                          # Agent instruction document (core)
├── README.md                         # This file
├── scripts/
│   ├── technical_indicators.py       # Multi-source technical analysis
│   ├── integrated_analysis.py        # Comprehensive analysis reports
│   ├── daily_close_analysis.py       # Automated daily close reports
│   ├── mx_data.py                    # Eastmoney MX API data query
│   ├── mx_search.py                  # Eastmoney news/research search
│   ├── news_search.py                # Multi-source news aggregation
│   ├── data_source_manager.py        # Unified data source with fallback
│   ├── watchlist.py                  # Watchlist management
│   ├── analysis_scratchpad.py        # Analysis scratchpad utilities
│   └── requirements.txt              # Python dependencies
├── templates/
│   ├── market_brief_template.md      # Market overview template
│   └── research_report_template.md   # Research report template
└── references/
    └── china-stocks.md               # Popular Chinese stock code reference
```

## 📊 Supported Markets

| Market | Code Format | Example |
|--------|-------------|---------|
| Shanghai A-share | XXXXXX.SH | 600519.SH (Kweichow Moutai) |
| Shenzhen A-share | XXXXXX.SZ | 000001.SZ (Ping An Bank) |
| Hong Kong | XXXX.HK | 0700.HK (Tencent) |
| Shorthand | 6 digits | 002475 (Luxshare Precision) |

## 🔄 Data Sources (100% Free)

```
Sina Finance (fastest, no key needed, primary)
        ↓ (if unavailable)
    Akshare (good A-share coverage)
        ↓ (if unavailable)
    Yahoo Finance (global coverage)

## ⏰ Cron Integration

Designed for automated daily analysis:

| Time | Script | Purpose |
|------|--------|---------|
| 09:15 | integrated_analysis.py --mode pre-market | Pre-market briefing |
| 11:35 | daily_close_analysis.py --mode morning | Morning session summary |
| 15:05 | daily_close_analysis.py | Daily close technical analysis |

## 🤝 Contributing

Issues and pull requests welcome. This skill is designed to work with any OpenClaw-compatible agent.

## ⚠️ Disclaimer

This tool is for informational purposes only. It does not constitute financial advice. Always consult a licensed financial advisor before making investment decisions.

## License

MIT
