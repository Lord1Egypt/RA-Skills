---
name: trivia
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [trivia, tool, utility]
description: "Host trivia rounds with question banks, scoring, and boards. Use when running quizzes, checking answers, analyzing scores, generating rounds."
---
# Trivia

Utility toolkit for running, checking, converting, analyzing, generating, previewing, batching, and comparing data. Log entries with timestamps, manage configurations, generate reports, and export data in multiple formats. All entries are stored locally for full traceability.

## Commands

### Core Operations

| Command | Description |
|---------|-------------|
| `trivia run [input]` | Run/execute an entry (no args = show recent runs) |
| `trivia check [input]` | Check/validate an entry (no args = show recent checks) |
| `trivia convert [input]` | Convert data (no args = show recent conversions) |
| `trivia analyze [input]` | Analyze data (no args = show recent analyses) |
| `trivia generate [input]` | Generate content (no args = show recent generations) |
| `trivia preview [input]` | Preview content (no args = show recent previews) |
| `trivia batch [input]` | Batch process entries (no args = show recent batches) |
| `trivia compare [input]` | Compare items (no args = show recent comparisons) |

### Management

| Command | Description |
|---------|-------------|
| `trivia export [input]` | Export data (no args = show recent exports) |
| `trivia config [input]` | Manage configuration (no args = show recent configs) |
| `trivia status [input]` | Check status (no args = show recent statuses) |
| `trivia report [input]` | Generate reports (no args = show recent reports) |

### Data & Reporting

| Command | Description |
|---------|-------------|
| `trivia stats` | Summary statistics across all entry types with counts |
| `trivia export <fmt>` | Export all data in json, csv, or txt format |
| `trivia search <term>` | Search across all log entries |
| `trivia recent` | Show last 20 activity log entries |
| `trivia status` | Health check: version, entry count, disk usage, last activity |

### Utility

| Command | Description |
|---------|-------------|
| `trivia help` | Show help with all available commands |
| `trivia version` | Show version number |

## Data Storage

All data is stored locally at `~/.local/share/trivia/` by default:

- `run.log`, `check.log`, `convert.log`, `analyze.log`, etc. — One log file per command type, entries stored as `timestamp|input`
- `history.log` — Unified activity history with timestamps for every command
- `export.json`, `export.csv`, `export.txt` — Generated export files

Each command supports two modes:
- **With arguments:** Saves the input with a timestamp and confirms the total entry count
- **Without arguments:** Shows the 20 most recent entries for that command type

## Requirements

- bash 4+
- Standard UNIX utilities (`date`, `wc`, `du`, `grep`, `tail`, `sed`, `cat`, `basename`)
- No external dependencies or API keys required

## When to Use

1. **Data processing pipeline** — Use `run` to execute tasks, `check` to validate results, `convert` to transform formats, and `analyze` to extract insights
2. **Content generation workflow** — Use `generate` to create content, `preview` to review it, `report` to summarize findings, then `export` to package the output
3. **Batch operations** — Use `batch` for bulk processing, `compare` to diff results, and `stats` to monitor overall activity
4. **Configuration management** — Use `config` to log settings changes and `status` to verify system health
5. **Audit and traceability** — Every action is logged with timestamps; use `search` to find specific entries, `recent` to see the latest activity, and `stats` for counts across all types

## Examples

```bash
# Run a task
trivia run "Process Q1 data set"

# View recent runs
trivia run

# Check/validate something
trivia check "Verify answer key for round 3"

# Convert data format
trivia convert "CSV to JSON for quiz bank"

# Analyze results
trivia analyze "Score distribution for last 5 rounds"

# Generate new content
trivia generate "20 science questions, medium difficulty"

# Preview before publishing
trivia preview "Round 7 questions with answers"

# Batch process multiple items
trivia batch "Import all question files from /data/new/"

# Compare two results
trivia compare "Round 5 scores vs Round 6 scores"

# Export all data as JSON
trivia export json

# Export as CSV for spreadsheets
trivia export csv

# Log a configuration change
trivia config "Set default difficulty to hard"

# Check system status
trivia status

# Generate a summary report
trivia report "Weekly activity summary"

# View overall statistics
trivia stats

# Search for specific entries
trivia search "science"

# View recent activity
trivia recent

# Show all commands
trivia help

# Show version
trivia version
```

## Tips

- Every command with input is automatically timestamped — your full history is preserved
- Run any command without arguments to review its last 20 entries
- Use `stats` for a bird's-eye view of entry counts across all command types
- Export supports `json` (structured), `csv` (spreadsheets), and `txt` (human-readable) formats
- All log files are plain text — you can grep, edit, or pipe them directly
- The `search` command scans across all log files, not just one type

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
