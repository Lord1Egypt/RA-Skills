# skill-usage

A Claude Code skill that tracks and displays usage statistics for your installed skills. View how often each skill is called with beautiful TUI visualizations.

## Features

- **Time-based filtering** - View statistics for today, past 7/30/90 days, or all time
- **Visual bar charts** - See relative usage frequency at a glance
- **Bilingual support** - Automatically detects system language (Chinese/English)
- **Comprehensive tracking** - Analyzes both global and project-specific conversation history

## Installation

1. Clone this repository to `~/.claude/skills/skill-usage`:
```bash
git clone https://github.com/agiray/skill-usage.git ~/.claude/skills/skill-usage
```

2. Ensure the Python script is executable:
```bash
chmod +x ~/.claude/skills/skill-usage/stats.py
```

## Usage

Invoke the skill from Claude Code:

```
/skill-usage
```

Then select your desired time period:
- **Today** - From 00:00 to current time
- **Past 7 days** - Last week
- **Past 30 days** - Last month
- **Past 90 days** - Last three months
- **All** - Complete historical record

## Sample Output

```
📊 技能使用统计报告 (过去 7 天)
═══════════════════════════════════════

排名 | 技能名称        | 调用次数 | 使用频率
─────┼────────────────┼──────────┼──────────
 1   │ auto-skills    │    42    │ █████░░░░░ 49%
 2   │ idea-to-post   │    28    │ ███░░░░░░░ 33%
 3   │ humanizer-zh   │    15    │ █░░░░░░░░░ 18%
─────┼────────────────┼──────────┼──────────
     │ 总计           │    85    │
```

## How It Works

The skill analyzes your Claude Code conversation history from:
- `~/.claude/history.jsonl` (global history)
- `~/.claude/projects/*/*.jsonl` (project sessions)

It scans for `/skill-name` patterns in the `display` field of history entries, filtered by timestamp within your selected time period.

## Requirements

- Python 3.6+
- Claude Code with skills support

## License

MIT
