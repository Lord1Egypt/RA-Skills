---
name: proactive-daily-planner
description: "Proactive daily planning assistant that helps organize your day, track tasks, and provide motivation. Acts as a personal assistant to plan your day proactively."
metadata:
  {
    "openclaw":
      {
        "emoji": "📅",
        "author": "Akshay Memane",
        "version": "1.0.0",
        "category": "productivity",
        "tags": ["planning", "productivity", "proactive", "assistant", "daily"],
      },
  }
---

# Daily Planner Skill

A proactive personal assistant that helps you plan your day, track tasks, and stay motivated.

## 🎯 What It Does

- **Morning Planning**: Starts your day with goal setting and task prioritization
- **Progress Tracking**: Monitors task completion throughout the day
- **Motivation System**: Provides encouragement and reminders
- **Evening Review**: Helps reflect on accomplishments and plan for tomorrow
- **Proactive Alerts**: Anticipates needs and initiates planning automatically

## 🚀 Quick Start

### Installation

```bash
# Clone or copy the skill to your OpenClaw skills directory
cp -r daily-planner ~/.openclaw/workspace/skills/
```

### Configuration

Edit `config.json` to customize:
- Your name and timezone
- Planning schedule (morning/afternoon/evening times)
- Task categories and priorities
- Motivation messages

### Usage

The skill runs automatically based on your schedule, or you can trigger it manually:

```bash
# Manual trigger
openclaw skill daily-planner plan morning
openclaw skill daily-planner check-progress
openclaw skill daily-planner evening-review
```

## ⚙️ Configuration

### config.json

```json
{
  "user": {
    "name": "Akshay",
    "timezone": "Asia/Kolkata",
    "workHours": "9:00-18:00"
  },
  "schedule": {
    "morningCheckin": "8:00",
    "afternoonCheckin": "13:00",
    "eveningReview": "20:00"
  },
  "tasks": {
    "categories": ["work", "learning", "fitness", "personal"],
    "defaultPriority": "medium"
  },
  "notifications": {
    "enabled": true,
    "channel": "telegram",
    "motivationFrequency": "2h"
  }
}
```

## 📋 Features

### 1. Morning Planning
- Sets daily goals and priorities
- Reviews calendar events
- Creates task list for the day
- Provides motivational quote

### 2. Progress Tracking
- Tracks task completion
- Provides progress updates
- Suggests adjustments if falling behind
- Celebrates milestones

### 3. Motivation System
- 50+ motivational messages
- Progress-based encouragement
- Reminder system for important tasks
- Positive reinforcement

### 4. Evening Review
- Reviews accomplishments
- Identifies what went well
- Plans for tomorrow
- Provides closure for the day

## 🔧 Integration

### With OpenClaw Proactive Assistant
The skill integrates with OpenClaw's proactive system to:
- Run automatically on schedule
- Send notifications via configured channels
- Store planning data in memory files
- Work with other skills (calendar, email, etc.)

### With External Services
- **Calendar**: Check scheduled events (future)
- **Email**: Review important emails (future)
- **Task Managers**: Sync with Todoist/Things (future)

## 📊 Data Storage

Planning data is stored in:
- `~/.openclaw/workspace/memory/daily-plan-YYYY-MM-DD.md` - Daily plans
- `~/.openclaw/workspace/memory/task-history.json` - Task completion history
- `~/.openclaw/workspace/memory/progress-stats.json` - Progress statistics

## 🎨 Customization

### Templates
Edit the template files in `templates/` to customize:
- `morning.md` - Morning planning template
- `afternoon.md` - Afternoon check-in template
- `evening.md` - Evening review template

### Motivation Messages
Add your own motivational messages to `config.json`:
```json
"motivationMessages": [
  "You've got this! 💪",
  "One task at a time, you're making progress! 🚀",
  "Remember why you started. Keep going! 🌟"
]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built for OpenClaw AI Assistant
- Inspired by proactive assistant patterns
- Designed for personal productivity enhancement

---

**Happy Planning!** May your days be productive and fulfilling. 📅✨