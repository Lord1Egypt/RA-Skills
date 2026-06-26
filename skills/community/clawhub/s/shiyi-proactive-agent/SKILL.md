---
name: proactive-agent
description: A proactive agent that anticipates needs and takes initiative. Monitors environment, suggests actions, and proposes tasks based on context. Perfect for agents that need to be proactive rather than reactive.
version: 1.0.0
author: shiyi
tags:
  - agent
  - proactive
  - automation
  - productivity
metadata:
  openclaw:
    requires:
      bins: [python3]
---

# Proactive Agent

A proactive agent that anticipates needs and takes initiative. Monitors environment, suggests actions, and proposes tasks based on context.

## Features

- **Context Analysis**: Analyzes current time, market status, content pipeline
- **Action Suggestion**: Predicts needs and generates actionable suggestions
- **Task Initiation**: Proactively proposes tasks based on context
- **Priority Management**: 3-tier priority system (Trading > Content > Learning)

## Quick Start

```bash
# Get next suggested action
python scripts/action_suggester.py --next

# Analyze current context
python scripts/context_analyzer.py --json

# Propose tasks
python scripts/task_initiator.py --propose
```

## Components

### 1. Context Analyzer (`scripts/context_analyzer.py`)
Analyzes:
- Current time slot (morning_startup, trading_hours, content_window, etc.)
- Market status (open/closed)
- Content pipeline status
- Pending tasks
- Recent interactions

### 2. Action Suggester (`scripts/action_suggester.py`)
Generates suggestions based on:
- Time-based rules (trading hours, content window)
- Market conditions
- Content pipeline status
- Pending tasks
- Learning optimization needs

### 3. Task Initiator (`scripts/task_initiator.py`)
Proactively proposes tasks with:
- Task ID and timestamp
- Priority level
- Step-by-step instructions
- Auto-save to file

### 4. Proactive Monitor (`scripts/proactive_monitor.py`)
Continuous monitoring:
- Daemon mode for background operation
- Configurable check intervals
- Alert cooldown management

## Configuration

Edit `config/proactive_config.yaml`:

```yaml
proactive_level: 7          # 1-10, higher = more proactive
monitor_interval: 300       # Check interval in seconds
alert_cooldown: 1800        # Alert cooldown in seconds

priority_weights:
  trading: 10
  content: 8
  tasks: 6
  learning: 4
  routine: 3
```

## Time Rules

The agent recognizes these time slots:

| Time Slot | Hours | Typical Actions |
|-----------|-------|-----------------|
| morning_startup | 06:00-09:00 | Check portfolio, review today's plan |
| trading_hours | 09:30-15:00 | Monitor stocks, evaluate opportunities |
| content_window | 15:00-17:00 | Publish content, optimize posts |
| evening_routine | 17:00-22:00 | Log daily summary, update memory |
| night_quiet | 22:00-06:00 | Stay quiet, minimal alerts |

## Integration

### With AGENTS.md
Add to session startup:
```
1. Run proactive-agent: python skills/proactive-agent/scripts/action_suggester.py --next
```

### With HEARTBEAT.md
Add to heartbeat checks:
```
python skills/proactive-agent/scripts/action_suggester.py --next
```

## Example Output

```
[HIGH] 盘中交易时段
Suggestion: 观察候选股票，等待买入机会

[HIGH] 下午内容发布窗口
Suggestion: 检查待发布内容，准备发布小红书笔记

[MEDIUM] 晚间例行检查
Suggestion: 检查今日数据，记录交易日志
```

## Use Cases

1. **Trading Assistant**: Monitor market hours, suggest buy/sell decisions
2. **Content Creator**: Remind to publish at optimal times
3. **Task Manager**: Proactively propose tasks based on schedule
4. **Learning Agent**: Suggest performance analysis and improvements

## Requirements

- Python 3.7+
- Works on Windows/Linux/macOS

## Changelog

### v1.0.0 (2026-03-25)
- Initial release
- Context analyzer, action suggester, task initiator, proactive monitor
- Configuration system
- Time-based rules
