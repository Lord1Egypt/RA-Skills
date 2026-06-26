---
name: receipt
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [receipt, tool, utility]
description: "Scan, categorize, and total receipts for expenses. Use when recording purchases, categorizing spending, balancing monthly totals, forecasting budgets."
---

# Receipt

A command-line finance toolkit for recording, categorizing, and analyzing receipts and expenses. Track purchases, monitor spending trends, forecast budgets, set alerts, compare periods, and annotate tax-relevant items — all stored locally with timestamped history, full-text search, and multi-format export.

## Commands

The following commands are available via `receipt <command> [args]`:

### Finance Operations

| Command | Description |
|---------|-------------|
| `record <input>` | Record a receipt or purchase entry (e.g. "Lunch at cafe $12.50"). Called without args, shows recent record entries. |
| `categorize <input>` | Categorize a spending item (e.g. "Office supplies — Q1 budget"). Called without args, shows recent categorize entries. |
| `balance <input>` | Log a balance update or reconciliation note (e.g. "Monthly balance: $3,420"). Called without args, shows recent balance entries. |
| `trend <input>` | Record a spending trend observation (e.g. "Groceries up 15% vs last month"). Called without args, shows recent trend entries. |
| `forecast <input>` | Log a budget forecast (e.g. "Projected Q2 spend: $8,000"). Called without args, shows recent forecast entries. |
| `export-report <input>` | Save an export/report note (e.g. "Monthly PDF sent to accountant"). Called without args, shows recent export-report entries. |
| `budget-check <input>` | Record a budget check result (e.g. "Travel budget 78% used, $440 remaining"). Called without args, shows recent budget-check entries. |
| `summary <input>` | Log a summary note (e.g. "Week 12 total: $327.50 across 14 transactions"). Called without args, shows recent summary entries. |
| `alert <input>` | Record a spending alert (e.g. "Dining budget exceeded by $65"). Called without args, shows recent alert entries. |
| `history <input>` | Log a history note. Called without args, shows recent history entries. |
| `compare <input>` | Record a comparison note (e.g. "March vs February: +$200 on utilities"). Called without args, shows recent compare entries. |
| `tax-note <input>` | Annotate a tax-relevant item (e.g. "Home office deduction — $150/mo"). Called without args, shows recent tax-note entries. |

### Utility Commands

| Command | Description |
|---------|-------------|
| `stats` | Show summary statistics — entry counts per category, total entries, data size, and earliest record timestamp. |
| `export <fmt>` | Export all data in `json`, `csv`, or `txt` format. Output file saved to the data directory. |
| `search <term>` | Full-text search across all log files (case-insensitive). |
| `recent` | Show the 20 most recent activity entries from the global history log. |
| `status` | Health check — version, data directory path, total entries, disk usage, last activity, and OK status. |
| `help` | Display the full command reference. |
| `version` | Print the current version (`v2.0.0`). |

## Data Storage

All data is persisted locally in `~/.local/share/receipt/`:

- **Per-command logs** — Each command (record, categorize, balance, etc.) writes to its own `.log` file with `YYYY-MM-DD HH:MM|<input>` format.
- **Global history** — Every action is also appended to `history.log` with `MM-DD HH:MM <command>: <input>` format for unified audit trail.
- **Export files** — Generated exports are saved as `export.json`, `export.csv`, or `export.txt` in the same directory.

No external services, databases, or network connections are required. Everything runs locally via bash.

## Requirements

- **Bash 4+** (uses `local` variables, `set -euo pipefail`)
- Standard Unix utilities: `date`, `wc`, `du`, `head`, `tail`, `grep`, `basename`, `cat`
- No root privileges needed
- No external dependencies or package installs

## When to Use

1. **Logging daily purchases** — Use `record` to capture receipts as they happen, building a searchable expense journal over time.
2. **Organizing spending by category** — Use `categorize` and `budget-check` to track how much goes to groceries, dining, transport, subscriptions, etc.
3. **Monthly financial reviews** — Use `summary`, `compare`, and `trend` to analyze spending patterns across periods.
4. **Tax preparation** — Use `tax-note` to flag deductible items throughout the year so they're easy to find at tax time.
5. **Budget forecasting and alerts** — Use `forecast` to project upcoming spend and `alert` to document when budgets are exceeded.

## Examples

```bash
# Record a new receipt
receipt record "Grocery store — $67.30, weekly shopping"

# Categorize a purchase
receipt categorize "Amazon order $42.99 — Office Supplies"

# Check budget status
receipt budget-check "Food budget: $320 of $400 used, 8 days remaining"

# Log a spending trend
receipt trend "Utility bills trending 12% higher than same quarter last year"

# Add a tax note
receipt tax-note "Professional development course $299 — deductible education expense"

# Compare two months
receipt compare "April total $2,180 vs March $1,950 — +$230, mostly dining"

# View summary statistics
receipt stats

# Export all data as CSV
receipt export csv

# Search for all entries mentioning 'Amazon'
receipt search Amazon

# View recent activity
receipt recent
```

## How It Works

Each command follows the same pattern:

1. **With arguments** — Timestamps the input, appends it to the command-specific log file, increments the entry count, and writes to the global history log.
2. **Without arguments** — Displays the 20 most recent entries from that command's log file.

The `stats` command aggregates counts across all log files. The `export` command iterates through all logs and produces a unified output in your chosen format. The `search` command performs a case-insensitive grep across every log file.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
