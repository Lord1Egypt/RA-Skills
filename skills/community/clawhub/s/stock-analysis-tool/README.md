# 📈 Stock Technical Analysis Tool

> Multi-market technical analysis for stocks and funds — A股, 港股, 美股, ETF/LOF/开放式基金

*[English](#english) / [中文](#中文)*

---

## ✨ Features | 功能亮点

| Feature | Description |
|---------|-------------|
| 🌏 **Multi-Market** | A股 (沪深), 港股, 美股, ETF/LOF/开放式基金 |
| 📊 **Technical Indicators** | MA, MACD, RSI, KDJ, Bollinger Bands, ATR, Volume Analysis |
| 🔀 **MACD Divergence** | Auto-detect bullish & bearish divergences |
| 🛡️ **Dual Data Sources** | Primary + fallback, automatic failover |
| 📈 **Quant Score** | 0-100 score across 6 dimensions + 5-tier trend judgment |
| ⚡ **Batch Analysis** | Multi-threaded concurrent analysis, mixed stock+fund |
| 📝 **Multiple Outputs** | JSON / Terminal Table / ASCII / File |
| 🔌 **Offline Test** | `--test` mode with mock data, no internet needed |

---

## 🚀 Quick Start | 快速开始

### Installation | 安装

```bash
# Core dependencies (required)
pip install pandas numpy requests

# Optional dependencies (extended data sources)
pip install akshare    # A股/基金备用数据源
pip install yfinance    # 港美股数据源
```

### Usage | 使用

```bash
# A股（自动识别沪深）
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

## 📊 Scoring System | 评分体系

| Score | Trend | Interpretation |
|-------|-------|---------------|
| ≥75 | 🚀 Strong Uptrend | Technically strong, multiple indicators bullish |
| 60-74 | 📈 Uptrend | Technically bullish, short-term trend up |
| 40-59 | ↔️ Consolidation | Neutral, direction unclear |
| 25-39 | 📉 Downtrend | Technically bearish, short-term trend down |
| <25 | 🔻 Strong Downtrend | Technically weak, multiple indicators bearish |

---

## 🗂️ Project Structure | 项目结构

```
stock-technical-analysis/
├── _meta.json              # Skill metadata
├── SKILL.md                # Skill documentation
├── requirements.txt        # Python dependencies
└── scripts/
    └── stock_analysis.py   # Main script
```

---

## ⌨️ Command Reference | 命令行参数

| Argument | Short | Description |
|----------|-------|-------------|
| `stock_code` | - | Stock/fund code (positional) |
| `--market` | `-m` | Market: `auto` / `ashare` / `hkstock` / `usstock` |
| `--type` | `-t` | Asset type: `stock` / `fund` |
| `--days` | `-d` | History days (default: `60`) |
| `--batch` | `-b` | Batch mode (comma-separated) |
| `--json` | `-j` | JSON output |
| `--pretty` | `-p` | Pretty-print JSON |
| `--test` | - | Offline test mode |
| `--ascii` | - | ASCII mode (no unicode issues) |
| `--watchlist` | `-w` | Analyze from watchlist |
| `--add` | - | Add to watchlist |
| `--list` | - | List watchlist |
| `--version` | `-v` | Show version |

---

## 📡 Data Sources | 数据来源

| Market | Primary | Fallback |
|--------|---------|---------|
| A股 | 新浪财经 API | akshare |
| 港股/美股 | yfinance | akshare |
| ETF/LOF | 新浪ETF接口 | 东财 API |
| 开放式基金 | 东财 fund_open_fund_info_em | LOF历史接口 |

---

## ⚠️ Disclaimer | 免责声明

本工具仅供技术分析参考，不构成投资建议。免费数据源可能有 15-20 分钟延迟，基金净值每日更新一次。投资有风险，决策需谨慎。

This tool is for technical analysis reference only, not investment advice. Free data sources may have 15-20 minute delays. Invest at your own risk.

---

## 📄 License | 许可证

MIT License

---

## 🔗 Related | 相关链接

- **GitHub**: https://github.com/write31bug/stock-technical-analysis
- **ClawHub**: https://clawhub.ai/skills/stock-analysis-tool
