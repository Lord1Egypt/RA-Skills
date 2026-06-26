---
name: score
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [score, tool, utility]
description: "Track game scores, brackets, and player statistics. Use when recording results, scoring rounds, ranking leaderboards, reviewing game history, computing stats."
---

# Score

Gaming toolkit for tracking scores, rankings, challenges, leaderboards, and rewards from the command line. Log entries, review history, export data, and search across all records.

## Overview

Score is a versatile CLI tool for game and competition tracking. Each command logs or retrieves entries with timestamps. Pass arguments to record new data, or run a command with no arguments to view recent entries. Built-in utilities provide statistics, data export, search, and health checks.

## Commands

| Command | Description |
|---------|-------------|
| `score roll [input]` | Log a roll entry, or view recent rolls |
| `score score [input]` | Log a score entry, or view recent scores |
| `score rank [input]` | Log a rank entry, or view recent rankings |
| `score history [input]` | Log a history note, or view recent history |
| `score stats [input]` | Log a stats note, or view recent stats entries |
| `score challenge [input]` | Log a challenge, or view recent challenges |
| `score create [input]` | Log a creation event, or view recent creates |
| `score join [input]` | Log a join event, or view recent joins |
| `score track [input]` | Log a tracking entry, or view recent tracks |
| `score leaderboard [input]` | Log a leaderboard entry, or view recent standings |
| `score reward [input]` | Log a reward, or view recent rewards |
| `score reset [input]` | Log a reset event, or view recent resets |
| `score stats` | Show summary statistics across all log files |
| `score export <fmt>` | Export all data (json, csv, or txt) |
| `score search <term>` | Search all entries for a term |
| `score recent` | Show last 20 lines of activity history |
| `score status` | Health check (version, entries, disk usage, last activity) |
| `score help` | Show usage help |
| `score version` | Show version (v2.0.0) |

## Data Storage

- **Location:** `~/.local/share/score/`
- **Per-command logs:** Each command (roll, score, rank, etc.) writes to its own `<command>.log` file
- **History:** `history.log` — timestamped action log recording every operation
- **Export:** `export.<fmt>` — generated export files (json, csv, txt)
- Format: `YYYY-MM-DD HH:MM|value` per line in each log file
- All data is plain text. No database or cloud service.

## Requirements

- bash (with `set -euo pipefail`)
- Standard Unix utilities (`date`, `wc`, `du`, `tail`, `grep`, `cat`, `head`)
- No external dependencies or API keys

## When to Use

1. **Tracking game scores** — Use `score score "Player1 25pts"` to log scores during a game night or tournament
2. **Running leaderboards** — Use `score leaderboard "Player1 #1"` to maintain standings, then `score export csv` for spreadsheets
3. **Dice rolling & randomness** — Log dice results with `score roll "d20: 17"` for tabletop RPG sessions
4. **Challenge tracking** — Create and track challenges between players with `score challenge "speed run level 3"`
5. **Data analysis & export** — Use `score stats` for summary counts, `score search` to find specific entries, and `score export json` for programmatic analysis

## Examples

```bash
# Log a dice roll
score roll "d20: natural 17"
#  Output: [Score] roll: d20: natural 17
#          Saved. Total roll entries: 1

# Record a game score
score score "Alice 2500pts round-3"
#  Output: [Score] score: Alice 2500pts round-3
#          Saved. Total score entries: 1

# Update the leaderboard
score leaderboard "Alice #1, Bob #2, Charlie #3"
```

```bash
# View recent rolls (no argument = read mode)
score roll

# Check overall statistics
score stats
#  Output: history: 5 entries
#          roll: 3 entries
#          Total: 8 entries
#          Data size: 4.0K

# Search across all entries
score search "Alice"
```

```bash
# Export everything as JSON
score export json
#  Output: Exported to ~/.local/share/score/export.json (245 bytes)

# Export as CSV for spreadsheets
score export csv

# Check system health
score status
#  Output: Version: v2.0.0, Data dir, Entries count, Disk usage, Last activity

# View recent activity
score recent
```

## How It Works

Each domain command (roll, score, rank, challenge, etc.) has dual behavior:

- **With arguments:** Appends a timestamped entry to `<command>.log` and logs the action to `history.log`
- **Without arguments:** Displays the last 20 entries from that command's log file

The `stats` utility aggregates entry counts across all log files. The `export` command converts all logs into JSON, CSV, or plain text format. The `search` command performs case-insensitive grep across every log file.

## Tips

- Each command is its own namespace — you can track dozens of game types simultaneously
- Use `recent` for a quick dashboard of the last 20 actions
- Pipe `export json` output to `jq` for advanced analysis
- Override data directory: `export SCORE_DIR=...` (set in your environment before sourcing)

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
