---
name: valuation
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [valuation, tool, utility]
description: "Build DCF models and run comparable analysis for company valuation. Use when modeling cash flows, benchmarking peers, projecting growth, or pitching."
---

# Valuation

Utility toolkit for tracking and managing valuation-related operations. Log runs, checks, analyses, batch jobs, and reports — all with timestamped history and multi-format export.

## Commands

All data commands accept optional input. Without input, they display the 20 most recent entries. With input, they log a new timestamped entry.

### Core Operations

| Command | Description |
|---------|-------------|
| `valuation run [input]` | Log or view run entries — track execution tasks |
| `valuation check [input]` | Log or view check entries — record verification tasks |
| `valuation convert [input]` | Log or view convert entries — track conversion operations |
| `valuation analyze [input]` | Log or view analyze entries — record analysis results |
| `valuation generate [input]` | Log or view generate entries — track generation tasks |
| `valuation preview [input]` | Log or view preview entries — record preview operations |
| `valuation batch [input]` | Log or view batch entries — track batch processing jobs |
| `valuation compare [input]` | Log or view comparison entries — track A/B comparisons |
| `valuation export [input]` | Log or view export entries — record export operations |
| `valuation config [input]` | Log or view config entries — track configuration changes |
| `valuation status [input]` | Log or view status entries — record status observations |
| `valuation report [input]` | Log or view report entries — record generated reports |

### Utility Commands

| Command | Description |
|---------|-------------|
| `valuation stats` | Show summary statistics: entry counts per category, total entries, and data size |
| `valuation export <fmt>` | Export all data in `json`, `csv`, or `txt` format to the data directory |
| `valuation search <term>` | Search across all log files for a term (case-insensitive) |
| `valuation recent` | Show the 20 most recent entries from the activity history log |
| `valuation status` | Health check: version, data directory, total entries, disk usage, last activity |
| `valuation help` | Show full command listing |
| `valuation version` | Print version string (`valuation v2.0.0`) |

> **Note**: The `export` and `status` commands have dual roles. As core operations they log entries (when called with input). As utility commands they perform their special function (export data or show health check when called without arguments or with a format specifier).

## Data Storage

All data is stored locally in `~/.local/share/valuation/`:

- **Per-command logs**: `run.log`, `check.log`, `analyze.log`, `batch.log`, etc. — one file per command type
- **History log**: `history.log` — unified activity log with timestamps
- **Export files**: `export.json`, `export.csv`, `export.txt` — generated on demand
- **Format**: Each entry is stored as `YYYY-MM-DD HH:MM|<input>` (pipe-delimited)

Set the `VALUATION_DIR` environment variable to override the default data directory.

## Requirements

- **bash** (with `set -euo pipefail` strict mode)
- Standard Unix tools: `date`, `wc`, `du`, `head`, `tail`, `grep`, `basename`, `cat`
- No external dependencies or API keys required

## When to Use

1. **Tracking valuation model runs** — Log DCF runs, revenue projections, and model iterations with timestamped records
2. **Recording analysis and comparison results** — Use `analyze` and `compare` to document peer benchmarks, multiples, and scenario comparisons
3. **Managing batch processing pipelines** — Use `batch` and `export` to track large-scale valuation jobs across portfolios
4. **Auditing configuration changes** — Use `config` to log parameter changes (discount rates, growth assumptions, etc.) for reproducibility
5. **Generating compliance reports** — Export all logged data to JSON/CSV/TXT for audit trails, investor presentations, or regulatory filings

## Examples

```bash
# Log a valuation run
valuation run "DCF model for ACME Corp — 5yr projection, WACC 9.2%"

# Record an analysis result
valuation analyze "peer comparison: ACME trades at 12x EV/EBITDA vs 15x median"

# Log a batch processing job
valuation batch "processed 50 portfolio companies for Q4 revaluation"

# Track a configuration change
valuation config "updated discount rate from 8.5% to 9.2% per board directive"

# View recent check entries
valuation check

# Search for entries related to a specific company
valuation search "ACME"

# Get summary statistics across all categories
valuation stats

# Export everything to JSON for dashboard integration
valuation export json

# Show the 20 most recent activity entries
valuation recent
```

## How It Works

Valuation uses a simple append-only log architecture. Each command type writes to its own `.log` file, and all activity is also appended to a central `history.log` for chronological tracking. The `stats` command aggregates counts across all log files. The `export` command reads all logs and serializes them into the requested format (JSON array, CSV with headers, or plain text sections). The `search` command performs case-insensitive grep across all log files.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
