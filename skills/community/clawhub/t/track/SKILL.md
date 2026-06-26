---
name: track
description: Habit, goal, and progress tracking system with visual progress and accountability. Use when user mentions tracking habits, goals, progress, streaks, or accountability. Tracks daily habits, monitors goal progress, maintains streaks, visualizes trends, and provides accountability reminders. Builds sustainable tracking systems that actually stick.
---

# Track

Progress tracking system. Build habits, achieve goals, see progress.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All tracking data stored locally only**: `memory/track/`
- **No external tracking apps** connected
- **No data sharing** with fitness or productivity platforms
- **Personal goals and habits** stay private
- User controls all data retention and deletion

### Data Structure
Tracking data stored locally:
- `memory/track/habits.json` - Habit tracking data
- `memory/track/goals.json` - Goal definitions and progress
- `memory/track/streaks.json` - Streak records
- `memory/track/metrics.json` - Key metrics over time

## Core Workflows

### Track Habit
```
User: "I meditated for 20 minutes today"
→ Use scripts/track_habit.py --habit "meditation" --value 20 --unit minutes
→ Log completion, update streak, show progress
```

### Update Goal
```
User: "Update my savings goal progress"
→ Use scripts/update_goal.py --goal "emergency-fund" --current 5000
→ Track progress, show percentage, estimate completion
```

### View Trends
```
User: "Show my exercise trends this month"
→ Use scripts/view_trends.py --habit "exercise" --period month
→ Visualize patterns, identify trends, highlight improvements
```

### Check Streaks
```
User: "What are my current streaks?"
→ Use scripts/check_streaks.py
→ Show active streaks, at-risk habits, milestone achievements
```

## Module Reference
- **Habit Tracking**: See [references/habits.md](references/habits.md)
- **Goal Setting**: See [references/goals.md](references/goals.md)
- **Progress Visualization**: See [references/visualization.md](references/visualization.md)
- **Accountability Systems**: See [references/accountability.md](references/accountability.md)
- **Streak Psychology**: See [references/streaks.md](references/streaks.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `track_habit.py` | Log habit completion |
| `update_goal.py` | Update goal progress |
| `view_trends.py` | View progress trends |
| `check_streaks.py` | Check current streaks |
| `create_habit.py` | Create new habit tracker |
| `set_goal.py` | Define new goal |
| `export_data.py` | Export tracking data |
