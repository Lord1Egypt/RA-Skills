---
name: trading-journal
description: Record, manage, and analyze futures/stock trading journals. Use when the user needs to: (1) log trade entries with standardized templates, (2) calculate P&L and statistical summaries, (3) archive and search trade notes, (4) generate performance analysis and reports, (5) export journals to Markdown or CSV format.
emoji: 📓
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Trading Journal — 交易日志管理

Record and analyze futures/stock trading journals. Supports structured trade logging, P&L tracking, performance analytics, and multi-format export.

## Architecture

```
Trade Entry → [Journal] → Log → [Analysis] → Stats / Reports
                 ↑                        ↓
           Template Driven          Export (MD/CSV)
```

## Core Workflows

### Workflow 1: Log a Trade Entry

Use the standardized template to record a trade:

**Template fields:**

| Field | Description | Example |
|:------|:------------|:--------|
| date | Trade date | 2026-05-20 |
| symbol | Contract/stock code | IF2606, 000001 |
| direction | Long or Short | long / short |
| entry_price | Entry price | 3850.0 |
| exit_price | Exit price | 3900.0 |
| quantity | Number of contracts/shares | 2 |
| multiplier | Contract multiplier (futures) | 300 |
| entry_time | Entry timestamp | 09:35 |
| exit_time | Exit timestamp | 14:20 |
| fees | Commission + slip | 45.60 |
| strategy | Strategy tag | trend_follow |
| notes | Free-text notes | "突破前高入场" |
| tags | Custom tags | ["股指", "日内"] |

**Full JSON template:**
```json
{
  "date": "2026-05-20",
  "symbol": "IF2606",
  "direction": "long",
  "entry_price": 3850.0,
  "exit_price": 3900.0,
  "quantity": 2,
  "multiplier": 300,
  "entry_time": "09:35",
  "exit_time": "14:20",
  "fees": 45.60,
  "strategy": "trend_follow",
  "notes": "突破前高入场，尾盘止盈",
  "tags": ["股指", "日内", "趋势"]
}
```

To log a trade:
1. Ask user for trade details, or accept them in free-text format
2. Map to the standard template
3. Append to the daily journal file via the `scripts/trade_logger.py` script
4. Calculate P&L and confirm with user

### Workflow 2: Calculate P&L

Auto-calculated based on template fields:

**Futures P&L:**
```
P&L = (exit_price - entry_price) × quantity × multiplier × direction_sign - fees
```

**Stock P&L:**
```
P&L = (exit_price - entry_price) × quantity - fees
```

Where `direction_sign` = 1 for long, -1 for short.

The system handles:
- Open trades (no exit price — show unrealized P&L using current market price)
- Partial fills (quantity adjustments)
- Multi-leg strategies (aggregate P&L)

### Workflow 3: Performance Analysis

Run analytics on journal entries using `scripts/trade_analyzer.py`:

**Metrics computed:**

| Metric | Formula |
|:-------|:--------|
| Win Rate | wins / total_closed × 100% |
| Total P&L | Σ(closed_trade_P&L) |
| Avg Win | Σ(win_P&L) / wins |
| Avg Loss | Σ(loss_P&L) / losses |
| Profit Factor | Σ(gross_profit) / Σ(gross_loss) |
| Sharpe Ratio | avg_return / std_return × √252 |
| Max Drawdown | Max peak-to-trough decline |
| Best/Worst Trade | Max/min single trade P&L |
| Daily Average | Total P&L / trading_days |

**Analysis frequency:**
- **Daily**: Quick summary of today's trades
- **Weekly**: Performance trends, strategy comparison
- **Monthly**: Full analytics report
- **Custom**: Any date range specified by user

### Workflow 4: Archive & Search

Journal files are organized by date:

```
journals/
├── 2026/
│   ├── 2026-05/
│   │   ├── 2026-05-18.json    # Day trades
│   │   ├── 2026-05-19.json
│   │   └── 2026-05-20.json
│   └── 2026-06/
│       └── 2026-06-01.json
└── archive/
    └── 2025-journal.jsonl
```

Search across journals by:
- Date range (YYYY-MM-DD to YYYY-MM-DD)
- Symbol (e.g., IF, IC, CU)
- Direction (long/short)
- Strategy tag
- P&L range
- Custom text search in notes

### Workflow 5: Export

Export journals to preferred format:

| Format | Use Case | Command |
|:-------|:---------|:--------|
| Markdown | Human-readable report, docs | `python journal_export.py --format md --output report.md` |
| CSV | Spreadsheet analysis, import | `python journal_export.py --format csv --output trades.csv` |
| JSON | Data interchange, backup | `python journal_export.py --format json --output trades.json` |

## Usage Guide

### A) Recording a New Trade

When user says "记一笔交易" or provides trade details:

1. Parse trade info from user's natural language
2. Confirm parsed fields with user
3. Run: `python scripts/trade_logger.py add <json_string>`
4. Show calculated P&L and confirmation

**Example interaction:**
```
User: 今天IF2606做多2手，3850进场，3900平仓
Agent: 📓 记录交易：
  IF2606 | LONG | 3850 → 3900 | 2手
  P&L: (3900-3850)×2×300 - 费用 = ¥29,954.40
  确认记录？(是/否)
```

### B) Checking Performance

When user asks "看看收益" / "我的交易怎么样":

1. Determine time range (today/this week/this month/custom)
2. Run analyzer: `python scripts/trade_analyzer.py --range 2026-05-01 2026-05-20`
3. Present formatted results

**Example output:**
```
📊 交易绩效报告 (2026-05-01 ~ 2026-05-20)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
  总交易数:  24
  胜率:      70.83% (17/24) 🟢
  总盈亏:    +¥186,520.00 🟢
  平均盈利:  +¥16,250.00
  平均亏损:  -¥4,830.00
  盈亏比:    3.36
  最大回撤:  -¥12,400.00
  最佳交易:  +¥45,000.00 (IF2606, 05-08)
  最差交易:  -¥8,200.00 (IC2609, 05-12)
```

### C) Exporting Data

When user asks to export:

1. Confirm format and date range
2. Run export script with appropriate parameters
3. Show export path and summary

## Scripts

### `scripts/trade_logger.py`
Core trade logging — add, edit, delete, and list journal entries.

### `scripts/trade_analyzer.py`
Performance analysis — compute metrics, generate reports for any date range.

### `scripts/journal_export.py`
Multi-format export — output journals to Markdown, CSV, or JSON.

## Special Notes

- Journal files are stored in `journals/` directory within this skill folder
- Each day gets one JSON file; multiple trades append to the same file
- P&L is calculated on entry, not just on display
- Open positions are tracked with `exit_price: null` and `open: true`
- All monetary values are in CNY (¥)
- Fees should include commission + slippage + stamp duty where applicable
- Journal data is local-only — no external API calls
