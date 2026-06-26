---
name: ticktick-go
version: 1.1.0
description: "Manage TickTick tasks and projects via the `ttg` CLI (github.com/dhruvkelawala/ticktick-go). Full CRUD, checklists/subtasks with progress display, reminders, recurring tasks, search, tags, natural language dates, and JSON output. Use when: adding tasks, listing tasks, marking complete, editing tasks, managing checklists, setting reminders, searching, or filtering by due date, priority, or tag."
metadata:
  openclaw:
    requires:
      bins:
        - ttg
    install:
      - id: ttg
        kind: shell
        label: "Build and install ttg CLI from source"
        script: "git clone https://github.com/dhruvkelawala/ticktick-go /tmp/ttg-install && cd /tmp/ttg-install && make install && rm -rf /tmp/ttg-install"
---

# TickTick CLI Skill (`ttg`)

A feature-rich terminal interface for [TickTick](https://ticktick.com) via the [`ticktick-go` CLI](https://github.com/dhruvkelawala/ticktick-go).

## Prerequisites

Install `ttg`:
```bash
git clone https://github.com/dhruvkelawala/ticktick-go
cd ticktick-go && make install
```

Create `~/.config/ttg/config.json` with your TickTick API credentials (get them at [developer.ticktick.com](https://developer.ticktick.com/manage)):
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "timezone": "Europe/London"
}
```

Authenticate:
```bash
ttg auth login      # opens browser OAuth2 flow
ttg auth status     # confirm you're logged in
```

## Task Commands

```bash
# List
ttg task list                              # Inbox (default)
ttg task list --all                        # Every task across all projects
ttg task list --project "Work"             # By project name
ttg task list --due today                  # Due today
ttg task list --due overdue                # Overdue tasks
ttg task list --priority high              # By priority
ttg task list --tag "urgent"               # By tag
ttg task list --completed                  # Show completed tasks
ttg task list --json                       # JSON output for scripting

# Add
ttg task add "Buy milk"
ttg task add "Review PR" --project "Work" --priority high --due "tomorrow 9am"
ttg task add "Call dentist" --today --high --remind "1h,on-time"
ttg task add "Weekly sync" --due "next friday" --repeat weekly
ttg task add "Quick note" -n "Don't forget the attachment" --tag "work,followup"

# Quick-add shorthands
ttg task add "Standup" --today --med
ttg task add "Submit report" --tomorrow --high
ttg task add "Urgent fix" --tmrw --remind "15m"

# Manage
ttg task get <id>                          # Full details
ttg task done <id>                         # Mark complete
ttg task delete <id>                       # Delete

# Edit
ttg task edit <id> --title "Updated title" --priority medium --due "next monday"
ttg task edit <id> --remind "1h,15m" --repeat monthly
ttg task edit <id> --tag "work,important" --start "tomorrow 9am"
ttg task edit <id> --kind checklist        # Convert to checklist

# Search
ttg task search "deploy"                   # Search tasks by title
```

## Checklists & Subtasks

```bash
# Create a checklist task with initial items
ttg task add "Pack for trip" --checklist --items "Passport,Charger,Clothes"

# Manage checklist items
ttg task items <task-id>                   # List all items
ttg task item-add <task-id> "Toothbrush"   # Add an item
ttg task item-done <task-id> <item-id>     # Complete an item
ttg task item-delete <task-id> <item-id>   # Delete an item
```

Checklist tasks show a visual progress bar (0–100%) in list and detail views:
```
☑️ Pack for trip [60%]
│ Progress: [██████░░░░] 60%
```

## Reminders

Add one or more reminders with `--remind` (comma-separated):

| Shorthand | Meaning |
|-----------|---------|
| `on-time` | At the due time |
| `5m`, `15m`, `30m` | Minutes before |
| `1h` | 1 hour before |
| `1d` | 1 day before |

```bash
ttg task add "Meeting" --due "3pm" --remind "15m,on-time"
ttg task edit <id> --remind "1h,30m"
```

## Recurring Tasks

```bash
ttg task add "Daily standup" --due "9am" --repeat daily
ttg task add "Monthly review" --due "1st" --repeat monthly
ttg task add "Custom recurrence" --repeat "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR"
```

Patterns: `daily` · `weekly` · `monthly` · `yearly` · custom RRULE

## Project Commands

```bash
ttg project list                           # All projects with task counts
ttg project get <id>                       # Project details
```

## Tag Commands

```bash
ttg tag list                               # List all tags used across tasks
ttg task list --tag "work"                 # Filter tasks by tag
ttg task add "New task" --tag "urgent,work" # Add with tags
```

## Due Date Formats

| Input | Result |
|-------|--------|
| `today`, `tomorrow` | Midnight of that day |
| `next monday` | Following Monday |
| `3pm`, `tomorrow 3pm` | Specific time |
| `in 2 days`, `in 3 hours` | Relative offset |
| `2026-03-20` | ISO date |
| `2026-03-20T15:00:00` | ISO datetime |

## Priority Values

`none` (default) · `low` · `medium` · `high`

Shorthand flags: `--high`, `--med`/`--medium`, `--low`

## JSON / Scripting

Every list command accepts `--json` / `-j`:

```bash
# Get all high-priority tasks as JSON
ttg task list --priority high --json

# Pipe into jq
ttg task list --all --json | jq '.[] | select(.dueDate != null) | .title'

# Export project task counts
ttg project list --json | jq '.[] | {name, taskCount}'
```

## Common Patterns

```bash
# Morning review — what's due today?
ttg task list --due today

# Quick capture while in flow
ttg task add "Follow up with Alex" --due "tomorrow 10am" --med --remind "1h"

# Create a shopping checklist
ttg task add "Groceries" --checklist --items "Eggs,Bread,Milk" --today

# End-of-day — mark things done
ttg task done <id>

# Weekly planning — see everything
ttg task list --all

# Find that task you can't remember
ttg task search "deploy"
```
