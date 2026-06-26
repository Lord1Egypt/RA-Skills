---
name: runstr-analytics
description: Advanced RUNSTR fitness analytics with trend analysis, performance insights, training recommendations, and correlation tracking. Analyzes workout history, habits, mood, and steps to provide personalized coaching insights and identify patterns in training effectiveness.
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["nak","python3"],"python_packages":["pandas","numpy","scipy","requests"]},"install":[{"id":"go","kind":"go","package":"github.com/fiatjaf/nak@latest","bins":["nak"],"label":"Install nak via Go"},{"id":"python_deps","kind":"pip","packages":["pandas","numpy","scipy","requests"],"label":"Install Python analytics dependencies"}]}}
---

# RUNSTR Analytics Skill

Advanced fitness analytics and coaching insights for RUNSTR data. Provides trend analysis, performance tracking, habit correlation, and personalized training recommendations.

## Setup

**Required: RUNSTR_NSEC environment variable**

This skill requires your Nostr private key (nsec1...) to decrypt RUNSTR backup data.

**Option 1 - For OpenClaw/chat usage:**
Tell your bot: "Here's my RUNSTR nsec: nsec1..."

**Option 2 - For CLI/cron automation:**
```bash
export RUNSTR_NSEC="nsec1..."
```

⚠️ **Security note:** The nsec is passed securely via stdin (not CLI arguments) to prevent exposure in process lists. Cache files use restrictive permissions (0700/0600).

---

## Features

- **Advanced Trend Analysis**: Pace trends by activity type, seasonal comparisons, training load tracking
- **Performance Insights**: Personal records, weekly challenges, streak tracking
- **Correlation Analysis**: Mood vs training, habits vs performance, sleep vs recovery
- **Training Recommendations**: AI-driven tips for improvement, goal-based planning
- **Training Plan Integration**: Sync with external training plans, track adherence

## Quick Start

**Extended version** (recommended - with local cache):
```bash
# First run - fetch from Nostr and cache locally
python3 scripts/analyze_extended.py --nsec <NSEC> --days 60 --insights --force-refresh

# Subsequent runs - use cached data (no nsec needed!)
python3 scripts/analyze_extended.py --days 60 --insights
```

**Lightweight version** (basic analysis):
```bash
python3 scripts/analyze_light.py --nsec <NSEC> --days 30 --insights
```

**Full version** (requires pandas, numpy, scipy):
```bash
# Install dependencies first: pip3 install pandas numpy scipy
python3 scripts/analyze.py --nsec <NSEC> --days 60 --coaching-report
```

## Commands

| Flag | Description |
|------|-------------|
| `--nsec` | Your Nostr private key (nsec1...) |
| `--days` | Analysis period (default: 30) |
| `--insights` | Generate improvement tips |
| `--coaching-report` | Full coaching analysis |
| `--training-plan` | Path to training plan markdown file |
| `--trends` | Show trend visualizations |
| `--correlations` | Analyze habit/mood correlations |
| `--pb` | Show personal records |
| `--challenges` | Generate weekly challenges |

## Data Sources

1. **Nostr Encrypted Backup** (Kind 30078): Primary workout, habit, journal data
2. **Local Cache**: SQLite database for fast re-analysis
3. **Training Plans**: Markdown files with structured training schedules

## Extended Features (analyze_extended.py)

### Local Cache
- SQLite database stores workouts locally
- Fast subsequent analyses (no Nostr query needed)
- Automatic PR tracking across sessions
- Cache location: `~/.cache/runstr-analytics/`

### Week-to-Week Comparison
```bash
# Shows last 4 weeks with trends
python3 scripts/analyze_extended.py --insights
```

### Personal Records
- Automatically detects PRs for: 1K, 5K, 10K, Half Marathon
- Stores historical PRs in cache
- Shows date and pace for each PR

### Visual Charts
- ASCII bar charts for weekly stats
- Sparkline trend indicators (📈 📉 ➡️)
- Easy visual comparison between weeks

### Automated Daily Updates
```bash
# Set up daily cron job (runs at 07:00)
./setup_cron.sh

# View latest automated report
./view_report.sh

# Check update logs
tail -f ~/.cache/runstr-analytics/daily_update.log
```

The automation will:
- Check if cache is older than 12 hours
- Fetch fresh data from Nostr if needed
- Generate new report with charts
- Save to `~/.cache/runstr-analytics/latest_report.txt`

### Usage Examples
```bash
# First time setup - fetch and cache
python3 scripts/analyze_extended.py --nsec nsec1... --force-refresh

# Daily check - uses cache
python3 scripts/analyze_extended.py --insights

# Analyze last 90 days
python3 scripts/analyze_extended.py --days 90 --insights

# Force re-fetch from Nostr (after new backup)
python3 scripts/analyze_extended.py --nsec nsec1... --force-refresh

# Set up automatic daily updates
./setup_cron.sh

# View today's automated report
./view_report.sh
```

## Analytics Engine

### Trend Calculations
- Rolling averages (7-day, 30-day)
- Week-over-week comparisons
- Pace progression by distance bracket
- Training load (acute vs chronic)

### Correlation Analysis
- Pearson correlation for numeric relationships
- Mood distribution by activity type
- Habit impact on performance metrics

### Recommendation Engine
- Rule-based coaching tips
- Goal gap analysis
- Recovery recommendations

## Output Formats

- Terminal tables (default)
- JSON export (`--format json`)
- Markdown reports (`--format md`)

## Security Considerations

### Private Key Handling
- **RUNSTR_NSEC is your Nostr private key** — treat it like a password. Never share it.
- This skill passes the key via **stdin** (not command-line arguments) to prevent exposure in process lists (`ps`)
- For added security on multi-user systems, ensure your system is not configured to log environment variables

### Local Data Protection
- Decrypted workout/journal data is cached locally in `~/.cache/runstr-analytics/runstr_cache.db`
- Cache directory and database files are created with **restrictive permissions (0700/0600)** — only your user can access them
- Ensure your disk is encrypted (full-disk encryption) for maximum protection

### Recommended Installation
- Install on a personal machine with restricted access (single user, disk encryption enabled)
- Consider pinning the `nak` binary to a specific release rather than using `@latest`
- Review the cron setup before enabling automatic daily updates

## Privacy

- NSEC is never stored or logged in skill output
- All processing happens locally on your machine
- Nostr queries use encrypted connections (WSS/WebSocket Secure)
- No data is sent to external analytics services
