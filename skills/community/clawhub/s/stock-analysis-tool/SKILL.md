---
name: stock-technical-analysis
description: Professional stock & fund technical analysis tool for A-share, HK, US markets — MA, MACD, RSI, KDJ, Bollinger Bands, ATR, scoring system. 股票技术分析工具，支持A股/港股/美股/基金技术分析，量化评分系统。
metadata:
  {
    "openclaw":
      { "requires": { "bins": ["python"] }, "install": [{ "id": "python", "kind": "python", "label": "Python 3.8+" }] },
    "tags": ["stock", "finance", "technical-analysis", "A股", "量化", "MACD", "RSI", "KDJ"],
    "homepage": "https://github.com/write31bug/stock-technical-analysis"
  }
---

# 📈 Stock Technical Analysis Tool

> Multi-market technical analysis CLI tool for stocks and funds — A股, 港股, 美股, ETF/LOF/开放式基金

---

## ✨ Feature Highlights | 功能亮点

| | Feature | 功能 |
|--|---------|------|
| 🌏 | **Multi-Market** | A股（沪深）、港股、美股、ETF/LOF/开放式基金 |
| 📊 | **Full Indicators** | MA, MACD, RSI, KDJ, Bollinger Bands, ATR, Volume |
| 🔀 | **MACD Divergence** | Automatic bullish/bearish divergence detection |
| 🛡️ | **Dual Data Sources** | Primary + fallback with auto-failover |
| 📈 | **Quant Score** | 0-100 score across 6 dimensions + 5-tier trend |
| ⚡ | **Batch Mode** | Multi-threaded concurrent analysis |
| 📝 | **Multiple Outputs** | JSON / Terminal Table / ASCII / File |
| 🔌 | **Offline Test** | `--test` mode with mock data |

---

## 📊 Scoring System | 评分体系

| Score | Trend | 趋势 |
|-------|-------|------|
| ≥75 | 🚀 Strong Uptrend | 强势上涨 |
| 60-74 | 📈 Uptrend | 上涨趋势 |
| 40-59 | ↔️ Consolidation | 震荡整理 |
| 25-39 | 📉 Downtrend | 下跌趋势 |
| <25 | 🔻 Strong Downtrend | 强势下跌 |

---

## 🚀 Quick Start

### Installation

```bash
# Core dependencies
pip install pandas numpy requests

# Optional
pip install akshare    # A股/基金备用数据源
pip install yfinance   # 港美股数据源
```

### Usage

```bash
# A股
python scripts/stock_analysis.py 600519

# 港股
python scripts/stock_analysis.py 00700 -m hkstock

# 美股
python scripts/stock_analysis.py AAPL -m usstock

# ETF 基金
python scripts/stock_analysis.py 159934 -t fund

# 开放式基金
python scripts/stock_analysis.py 001316 -t fund

# JSON 输出
python scripts/stock_analysis.py 600519 --json --pretty

# 批量分析
python scripts/stock_analysis.py -b 600036,600900,510310

# 离线测试
python scripts/stock_analysis.py 600519 --test
```

---

## ⌨️ Command Reference

| Argument | Short | Description |
|----------|-------|-------------|
| `stock_code` | - | Stock/fund code |
| `--market` | `-m` | Market: `auto` / `ashare` / `hkstock` / `usstock` |
| `--type` | `-t` | Asset type: `stock` / `fund` |
| `--days` | `-d` | History days (default: `60`) |
| `--batch` | `-b` | Batch mode (comma-separated) |
| `--json` | `-j` | JSON output |
| `--pretty` | `-p` | Pretty-print JSON |
| `--test` | - | Offline test mode |
| `--ascii` | - | ASCII mode (no unicode) |
| `--watchlist` | `-w` | Analyze from watchlist |
| `--add` | - | Add to watchlist |
| `--list` | `-l` | List watchlist |
| `--version` | `-v` | Show version |

---

## 🗂️ Project Structure

```
stock-technical-analysis/
├── _meta.json              # Skill metadata
├── SKILL.md                # This file
├── requirements.txt        # Python dependencies
└── scripts/
    └── stock_analysis.py   # Main script
```

---

## 📡 Data Sources

| Market | Primary | Fallback |
|--------|---------|----------|
| A股 | 新浪财经 API | akshare |
| 港股/美股 | yfinance | akshare |
| ETF/LOF | 新浪ETF接口 | 东财 API |
| 开放式基金 | 东财 fund_open_fund_info_em | LOF历史接口 |

---

## ⚠️ Disclaimer

本工具仅供技术分析参考，不构成投资建议。This tool is for technical analysis reference only, not investment advice.

---

## 🔗 Links

- **GitHub**: https://github.com/write31bug/stock-technical-analysis
- **ClawHub**: https://clawhub.ai/skills/stock-analysis-tool
