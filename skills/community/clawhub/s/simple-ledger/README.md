# Simple Ledger · Personal Finance & Investment Tracker

A natural-language expense tracker for everyday spending, plus investment tracking for stocks, funds, and ETFs. Just talk to your AI agent in plain English (or Chinese) — it parses your sentence and appends a row to a plain-text CSV ledger. No database, no cloud sync, no vendor lock-in.

## Why Simple Ledger?

Most personal finance apps force you into their schema, their cloud, their subscription plan. Simple Ledger does the opposite:

- **One CSV file** — open it in Excel, Numbers, vim, or `cat`
- **Natural language** — say "spent 50 on lunch today" and it's logged
- **Offline-first** — all daily ledger features work without internet
- **You own the data** — files live at `~/.openclaw/workspace/data/ledger/`
- **Optional investments** — track stocks/funds/ETFs with opt-in live quotes

## Features

| Feature | Description | Network? |
|---------|-------------|----------|
| 📝 Natural-language logging | One sentence → CSV row | No |
| 📊 Spending queries | By month, category, account | No |
| 💰 Multi-account balances | WeChat Pay, Alipay, bank, cash | No |
| 📐 Budgets | Per-category caps, overspend alerts | No |
| 📈 Monthly reports | ASCII bar chart, top categories | No |
| 🎯 Savings goals | Track progress, deposit reminders | No |
| 💹 Investment tracking | Buy/sell, portfolio P&L | Opt-in |
| 📡 Live quotes | Real-time prices via Sina/Eastmoney | Yes (opt-in) |

## Quick Start

Talk to your AI agent:

```
Lunch cost 50 today
Spent 23.5 on a taxi yesterday
Salary arrived, 8000
Bought a jacket for 299, paid with Alipay
```

The agent parses your sentence, shows the parsed entry for confirmation, then appends a row to `~/.openclaw/workspace/data/ledger/default.csv`.

## Example Ledger

```csv
# 日期,类型,金额,分类,描述,账户
余额,微信钱包,1000.00
余额,支付宝,2000.00
余额,银行卡,50000.00
余额,现金,500.00
2026-05-21,支出,50,餐饮,午餐,微信钱包
2026-05-22,收入,8000,工资,5月工资,银行卡
2026-05-23,支出,299,购物,外套,支付宝
```

## Installation

```bash
clawhub install simple-ledger
```

Or update to latest:

```bash
clawhub update simple-ledger --version 1.8.0
```

## Requirements

- **Python 3** (built-in on macOS)
- **akshare** (only for investment code lookup & live quotes): `pip install akshare`

## Privacy & Data

All data lives in plain CSV/JSON files under `~/.openclaw/workspace/data/ledger/`. **Nothing is uploaded to any server.**

The only network operations are:

1. Security code lookup (you say "buy 有色金属ETF南方", we ask Sina for its code)
2. Live stock/fund quotes (when you opt-in)

Both only send the security name/code to public APIs — no balance, no transaction history, no account info.

## File Structure

```
simple-ledger/
├── SKILL.md                    # Agent-facing documentation (Chinese + English)
├── README.md                   # This file (user-facing English)
├── _meta.json                  # Publishing metadata
├── scripts/
│   ├── parse_entry.py          # Parse natural language → CSV row
│   ├── validate_line.py        # Validate CSV row format
│   ├── query_ledger.py         # Read & filter ledger
│   ├── generate_report.py      # Monthly report generator
│   ├── budget.py               # Budget CRUD + alerts
│   ├── goal.py                 # Savings goals CRUD
│   ├── invest.py               # Investment tracking
│   ├── lookup_code.py          # Security code lookup (network)
│   └── _fund_loader.py         # Fund data loader
├── references/
│   ├── ledger_format.md
│   ├── budget_guide.md
│   ├── goal_guide.md
│   ├── invest_guide.md
│   ├── invest_api.md           # Investment command reference
│   ├── user_guide.md
│   ├── financial_benchmarks.md
│   └── education.md
├── examples/                   # Sample ledgers
└── tests/
    ├── test_ledger.py
    ├── test_comprehensive.py
    ├── test_security.py
    ├── run_tests.py
    ├── test_runner.sh
    ├── validate_skill.sh
    └── eval_cases.yaml
```

## License

MIT-0 (free to use, modify, redistribute, no attribution required)

## Links

- ClawHub: https://clawhub.com/skills/simple-ledger
- Issues: https://github.com/openclaw/clawhub/issues
