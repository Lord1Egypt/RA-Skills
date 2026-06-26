# 📈 AI Stock Research Team

> **One message triggers a full AI investment research workflow.**

A multi-role AI stock research team skill for [OpenClaw](https://github.com/anthropics/claude-code). When you say "analyze NVDA" or "分析贵州茅台", this skill orchestrates **6 specialized analysts** to produce a comprehensive research report — complete with technical analysis, fundamental review, bull-bear debate, trading strategy, risk assessment, and a director's final verdict.

Supports both **A-shares (China)** and **US stocks**.

---

## Features

- **Multi-Role Analysis** — 6 specialized AI roles: Technical Analyst, Fundamental Analyst, Macro Analyst, Sentiment Analyst, Bull/Bear Debaters, Trader, and Risk Officer
- **Real-Time Data** — MCP Server fetches live market data via akshare (A-shares) and yfinance (US stocks)
- **5 MCP Tools** — Stock quotes, K-line history, financial indicators, technical indicators, and a one-stop overview
- **Bull-Bear Debate** — Structured adversarial analysis with data-backed arguments
- **Composite Scoring** — 100-point system: Technical (25%) + Fundamental (30%) + Macro (20%) + Sentiment (25%)
- **Cross-Platform** — Works on OpenClaw, WorkBuddy, and any MCP-compatible client
- **Auto Market Detection** — Automatically identifies A-share (numeric codes) vs US stock (alphabetic tickers)
- **HTML Report Template** — Beautiful dark-theme report template included for visual presentation

---

## Installation

### Step 1: Install the Skill

```bash
npx clawhub@latest install stock-research-team
```

### Step 2: Run Setup (auto-configures Python + MCP)

```bash
bash ~/.openclaw/skills/stock-research-team/scripts/setup.sh
```

The setup script automatically:
1. Detects Python ≥ 3.10 on your system
2. Creates a virtual environment (`.venv`)
3. Installs dependencies: `mcp`, `akshare`, `yfinance`
4. Registers the `stock-analyzer` MCP Server

### Step 3: Restart

```bash
openclaw gateway restart
```

### Prerequisites

- **Python 3.10+** — Install via `brew install python@3.12` (macOS) or `apt install python3.12` (Ubuntu)
- **OpenClaw** or any MCP-compatible AI client

---

## Usage

### Full Analysis

```
分析一下贵州茅台
```
```
analyze NVDA
```
```
帮我分析 000001 平安银行
```

### Quick Look

```
快速看 AAPL
```

### Compare Stocks

```
对比 600519 000858
```

---

## MCP Tools

| Tool | Function | Data Source |
|------|----------|------------|
| `get_stock_quote` | Real-time quote (price, change, market cap) | akshare / yfinance |
| `get_stock_history` | Historical K-line data | akshare / yfinance |
| `get_financial_indicators` | Financial metrics (ROE, margins, EPS) | akshare / yfinance |
| `get_technical_indicators` | Technical indicators (MA, RSI, MACD, Bollinger) | Calculated from K-line |
| `get_stock_overview` | One-stop comprehensive overview | All above combined |

---

## Report Structure

Each analysis report follows this structure:

1. **Data Collection** — Fetch real-time market data via MCP
2. **Four-Dimension Analysis** — Technical, Fundamental, Macro, Sentiment (each scored 1-10)
3. **Bull-Bear Debate** — 3 bullish vs 3 bearish arguments with data citations
4. **Trading Strategy** — Buy/Hold/Sell/Watch with specific price targets and stop-loss levels
5. **Risk Review** — Aggressive/Moderate/Conservative advice + Top 3 risk factors
6. **Director's Verdict** — Final composite score (out of 100) and actionable conclusion

---

## File Structure

```
stock-research-team/
├── SKILL.md                    # Core skill definition (frontmatter + instructions)
├── README.md                   # This file
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT-0 License
├── scripts/
│   ├── setup.sh                # Post-install configuration script
│   ├── uninstall.sh            # Cleanup script
│   └── server.py               # MCP Server (FastMCP + akshare + yfinance)
├── references/
│   └── requirements.txt        # Python dependencies
└── assets/
    └── report-template.html    # HTML report template for visual display
```

---

## Uninstall

```bash
# Remove MCP Server and virtual environment
bash ~/.openclaw/skills/stock-research-team/scripts/uninstall.sh

# Remove the skill
npx clawhub@latest uninstall stock-research-team

# Restart
openclaw gateway restart
```

---

## Disclaimer

This skill is a technical demonstration of AI-powered stock analysis. All generated reports are **for reference only and do not constitute investment advice**. Investing involves risk; please exercise caution.

---

## License

[MIT-0](LICENSE)
