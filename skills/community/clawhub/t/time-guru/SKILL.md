---
slug: time-guru
name: Time Tracker / 时间追踪与生产力分析
version: 1.0.0
author: Golden Bean (coder)
category: Productivity
description: Natural language time tracking with smart activity classification, multi-dimensional reports, productivity analytics, and billing.
model: deepseek/deepseek-v4-flash
input_schema: schemas/input.schema.json
output_schema: schemas/output.schema.json
---

# Time Guru Skill

Zero-friction time tracking driven by natural language. Log activities by simply describing what you did. Get daily/weekly reports, productivity analysis, and billing summaries without remembering to start/stop timers.

## Core Capabilities

- **Natural Language Logging**: "9点到11点写代码", "下午开了两小时的会"
- **Instant Timer**: `start`/`stop` commands with auto-duration
- **Retroactive Entry**: Fill in past activities with fuzzy time parsing
- **Smart Classification**: Auto-categorize activities (dev, meeting, learning, etc.)
- **Multi-Dimensional Reports**: Daily, weekly, monthly, custom range
- **Productivity Analytics**: Peak hours, interruptions, deep work tracking
- **Project/Customer Billing**: Hourly rate × hours, exportable invoices
- **Goal Tracking**: Set daily/weekly time targets and monitor progress

## Privacy & Storage

- All data stored locally at `~/.openclaw/data/time-guru/`
- Organized as `YYYY/MM/DD.json` files (one day per file)
- Daily auto-backup (keeps last 7 backups)
- LLM only receives individual activity descriptions for parsing, never the full log

## Usage

```
clawhub run time-guru <action> [options]
```

### Actions

| Action | Description | Example |
|--------|-------------|---------|
| `log` | Log one or more activities | `log "9-11写代码, 11-12开会"` |
| `start` | Start a timer | `start "写周报" --project report` |
| `stop` | Stop the active timer | `stop` |
| `report` | Generate time report | `report --period today` |
| `analyze` | Productivity analysis | `analyze --period this_week` |
| `goal` | Set/check time goals | `goal set development 4h/day` |
| `project` | Project time summary | `project list` |

### Report Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--period` | enum | `today` | `today`, `yesterday`, `this_week`, `last_week`, `this_month`, `last_month`, `custom` |
| `--date-from` | date | — | Custom range start |
| `--date-to` | date | — | Custom range end |
| `--group-by` | enum | `category` | `category`, `project`, `day`, `week` |
| `--output-format` | enum | `text` | `text`, `json`, `csv`, `markdown` |
| `--billing` | bool | false | Include billing info |

## Sample Prompts

### 1. Natural language log (most common)
```text
clawhub run time-guru log "9点到11点写后端API，11点到12点开需求评审会"
# → ✅ 2 activities logged
#   ⏱ 09:00-11:00 (2h) 开发 · 写后端API
#   ⏱ 11:00-12:00 (1h) 会议 · 需求评审会
#   📊 Today: 3h total
```

### 2. Instant timer mode
```text
clawhub run time-guru start "写周报" --project company-report
# → ▶️ Timer started: 写周报 [company-report] @ 14:03
# ... later ...
clawhub run time-guru stop
# → ⏹ Stopped: 写周报 | Duration: 45 minutes
```

### 3. Daily report
```text
clawhub run time-guru report --period today
# → 📊 Today's Time Report (Mon 2026-06-14)
#   Development  ████████████████████ 4.5h (52.9%)
#   Meeting      ██████████▌          2.0h (23.5%)
#   Documentation ██████               1.0h (11.8%)
#   Break        ██████               1.0h (11.8%)
#   💰 Billable: 6.5h × ¥500/h = ¥3,250
```

### 4. Weekly productivity analysis
```text
clawhub run time-guru analyze --period this_week
# → 📈 Weekly Analysis
#   🔥 Peak hours: 09:00-11:00 (34% of output)
#   🧠 Deep work: 12.5h this week (↑ 15% vs last week)
#   ⚠️ Task switches: 7/day (high)
#   💡 Recommendation: Block 14:00-16:00 for meetings
```

### 5. Billing report
```text
clawhub run time-guru report --period this_month --billing
# → 💰 Monthly Billing (June 2026)
#   Project A (XYZ Corp) · 35h × ¥500 = ¥17,500
#   Project B (ABC Inc)  · 22h × ¥600 = ¥13,200
#   Internal             · 18h × ¥0   = ¥0
#   ────────────────────────────────────────
#   Total billable: ¥30,700
```

## First-Success Path

```
Step 1: Install → clawhub install time-guru
Step 2: Log → clawhub run time-guru log "刚才一直在写代码2小时"
Step 3: Confirm → see activity logged with auto-classification
Step 4: Report → clawhub run time-guru report --period today
Step 5: Insight → see where time went → habit-forming value
```

## Core Scripts

| File | Purpose |
|------|---------|
| `scripts/__init__.py` | Package init |
| `scripts/nl_parser.py` | Natural language time parsing |
| `scripts/timer.py` | Start/stop timer management |
| `scripts/logger.py` | Data persistence (JSON files) |
| `scripts/classifier.py` | Activity auto-classification |
| `scripts/reporter.py` | Daily/weekly/monthly reports |
| `scripts/analyzer.py` | Productivity analysis engine |
| `scripts/goal_tracker.py` | Time goal setting and tracking |
| `scripts/bill_calculator.py` | Billing calculation |
| `scripts/importer.py` | External data import |
| `scripts/exporter.py` | Data export (CSV/JSON) |
| `scripts/reminder.py` | Daily/weekly reminders |
