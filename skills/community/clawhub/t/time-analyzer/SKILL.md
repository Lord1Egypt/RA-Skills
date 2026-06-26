---
name: time-analyzer
description: Time tracking and analysis skill for automatic activity monitoring and productivity insights. Use when the user wants to track time spent on activities, analyze time usage patterns, get productivity suggestions, or generate time reports. Triggers on phrases like "track my time", "analyze my time", "time report", "productivity analysis", "how am I spending my time", "time tracking", "start tracking", "stop tracking", "time suggestions", "time optimization".
---

# Time Analyzer

Time Analyzer is a time tracking and analysis tool that helps users record activities, analyze time usage patterns, and generate practical suggestions for improvement.

## Features

- **Time Tracking**: Automatic activity start/end tracking, support for manual entries
- **Activity Categorization**: 8 preset categories (work, study, meeting, break, exercise, entertainment, sleep, other)
- **Time Analysis**: Category statistics, active period analysis, high-frequency activity identification
- **Optimization Suggestions**: Personalized time management suggestions based on data
- **Report Generation**: Generate comprehensive time usage reports

## Usage

### CLI Commands

```bash
# Start tracking an activity
time-analyzer start <category> [description] [tags]

# Stop current activity
time-analyzer stop

# View current status
time-analyzer status

# Analyze time data (default: past 7 days)
time-analyzer analyze [days]

# Generate optimization suggestions
time-analyzer suggest

# Generate full report
time-analyzer report [days]

# Manually add a record
time-analyzer add <category> <description> <minutes>

# List all categories
time-analyzer categories

# Show help
time-analyzer help
```

### Activity Categories

| Category | Description | Icon |
|----------|-------------|------|
| work | Work | 💼 |
| study | Study | 📚 |
| meeting | Meeting | 👥 |
| break | Break | ☕ |
| exercise | Exercise | 🏃 |
| entertainment | Entertainment | 🎮 |
| sleep | Sleep | 😴 |
| other | Other | 📌 |

### Usage Examples

```bash
# Start tracking work
time-analyzer start work "Developing new feature"

# Start tracking study
time-analyzer start study "Reading technical documentation"

# End current activity
time-analyzer stop

# Analyze past 30 days
time-analyzer analyze 30

# Get optimization suggestions
time-analyzer suggest

# Manually add 1 hour meeting record
time-analyzer add meeting "Weekly sync" 60
```

## Data Storage

Data is stored in the `.time-analyzer/` folder in the user's home directory:
- `records.json`: All activity records
- `config.json`: Configuration and current session state

## Report Content

Analysis reports include:
1. **Overview**: Total activities, total duration, daily average statistics
2. **Category Details**: Time percentage and frequency for each category
3. **Active Periods**: Most active time periods during the day
4. **High-Frequency Activities**: Top 5 most common activities
5. **Optimization Suggestions**: Time management suggestions based on data

## Automatic Tracking

The current version supports manual start/stop tracking. Automatic reports can be enabled via cron jobs:

```bash
# Add to crontab to generate daily report at 22:00
echo "0 22 * * * /usr/local/bin/time-analyzer report" | crontab -
```

## Dependencies

- Node.js >= 18.0.0
- No external dependencies (pure Node.js implementation)

## Installation

```bash
# Global installation
npm install -g time-analyzer

# Or use npx
npx time-analyzer
```