---
name: schedule-task
description: Schedule and run recurring tasks on Linux/Unix systems. Use when user wants to set up cron jobs, scheduled backups, periodic data sync, automated reports, or any recurring task automation.
---

# Schedule Task

Schedule and manage recurring tasks using cron.

## Quick Start

```bash
# Add a scheduled task
python scripts/scheduler.py add --cron "0 9 * * *" --command "backup.sh"

# List all tasks
python scripts/scheduler.py list

# Remove a task
python scripts/scheduler.py remove --id 1
```

## Core Features

- **Cron Expression Parser**: Validate and understand cron expressions
- **Task Management**: Add, list, remove scheduled tasks
- **Health Checks**: Monitor task execution status
- **Notifications**: Alert on task failure

## Cron Format

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6)
│ │ │ │ │
* * * * *
```

## Common Examples

| Expression | Meaning |
|------------|---------|
| `0 9 * * *` | Daily at 9 AM |
| `0 * * * *` | Every hour |
| `*/15 * * * *` | Every 15 minutes |
| `0 0 * * 0` | Weekly on Sunday |
| `0 0 1 * *` | Monthly on 1st |

## Script Usage

```bash
python scripts/scheduler.py [COMMAND] [OPTIONS]

Commands:
  add         Add a new scheduled task
  list        List all scheduled tasks
  remove      Remove a task
  enable      Enable a disabled task
  disable     Disable a task without removing
  log         Show task execution log
  health      Check task health status
```

## Options

```
--cron TEXT      Cron expression (required for add)
--command TEXT   Command to run (required for add)
--name TEXT      Task name for identification
--log PATH       Log file path
--notify EMAIL   Email notification on failure
--timeout SECS   Task timeout in seconds
```

## Examples

### Daily Backup
```bash
python scripts/scheduler.py add \
  --cron "0 2 * * *" \
  --command "/home/user/backup.sh" \
  --name "daily-backup" \
  --log /var/log/backup.log
```

### Hourly Sync
```bash
python scripts/scheduler.py add \
  --cron "0 * * *" \
  --command "sync-data.sh" \
  --name "hourly-sync"
```

### Weekly Report
```bash
python scripts/scheduler.py add \
  --cron "0 9 * * 1" \
  --command "generate-report.sh" \
  --name "weekly-report"
```

## Integration

### With Web Monitor
```bash
# Monitor website every hour
python scripts/scheduler.py add \
  --cron "0 * * *" \
  --command "python /path/to/web-monitor/scripts/monitor.py --url https://example.com --compare last.json"
```

### With Telegram Bot
```bash
# Send daily summary
python scripts/scheduler.py add \
  --cron "0 8 * * *" \
  --command "telegram-send 'Good morning! Daily summary ready'"
```

## Best Practices

1. **Use absolute paths** in commands
2. **Log output** for debugging
3. **Set timeouts** to prevent hanging tasks
4. **Test commands manually** before scheduling
5. **Use UTC** for server schedules
