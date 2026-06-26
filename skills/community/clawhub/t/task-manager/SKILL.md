---
name: task-manager
description: SQLite-based task management with priority, tags, and stats. Database stored in skill directory for natural isolation.
version: 1.1.0
type: component
metadata:
  clawdbot:
    emoji: "📋"
    requires:
      bins: [python3]
      files: [task-manager.py]
---

# Task Manager

> SQLite-powered task management with CRUD, priorities, tags, and statistics.

## Database Location

```
<skill-dir>/data/tasks.db
```

**Data Isolation**: Each agent has their own copy of this skill → natural data isolation, no configuration needed.

## Usage

```bash
# Direct call
python3 <skill-dir>/task-manager.py <command>

# Or set alias
alias task="python3 <skill-dir>/task-manager.py"
```

## Commands

| Command | Description |
|---------|-------------|
| `task add "title" [options]` | Create task |
| `task list [options]` | List tasks |
| `task show <id>` | Show task details |
| `task update <id> [options]` | Update task |
| `task start <id>` | Mark as in progress |
| `task complete <id>` | Mark as completed |
| `task archive <id>` | Archive task |
| `task delete <id>` | Delete task |
| `task stats` | Show statistics |

## Options

**add**:
- `--priority, -p` P0/P1/P2/P3 (default: P2)
- `--tags, -t` Comma-separated tags
- `--due` Due date
- `--desc, -d` Description

**list**:
- `--status` Filter by status
- `--priority` Filter by priority (comma-separated)
- `--sort` priority/due/created (default: created)

## Priority Levels

| Level | Meaning | Icon |
|-------|---------|------|
| P0 | Urgent | 🔴 |
| P1 | High | 🟠 |
| P2 | Normal | 🟡 |
| P3 | Low | 🟢 |

## Status

| Status | Icon | Description |
|--------|------|-------------|
| pending | ⏳ | Todo |
| in_progress | 🔄 | In progress |
| completed | ✅ | Done |
| archived | 📁 | Archived |