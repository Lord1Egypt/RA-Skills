---
name: vikunja
description: >
  Interact with a self-hosted Vikunja task management instance via its REST API.
  Use when the user asks to create, update, delete, or list tasks/projects/labels,
  schedule reminders, check due dates, bulk-complete tasks.
  Also use for "add to my todo list", "remind me to", "schedule X", "what's on my
  task list", "mark done", "recurring task", or any Vikunja-specific
  request. Triggers on: task, todo, to-do, reminder, schedule, project, inbox,
  label, gantt, vikunja, recurring task.
---

# Vikunja

Self-hosted Vikunja integration via REST API. The instance is configured in
`references/vikunja.yaml` (or `~/.config/vikunja.yaml`).

## Quick Start

```bash
# Authenticate once, then use the token for all requests
TOKEN=$(python3 "$(skill-dir)/scripts/vikunja.py" login)

# Add a task to the Inbox project (id=1)
python3 "$(skill-dir)/scripts/vikunja.py" task create "Walk the dog" --project 1 --due "2026-05-20T18:00:00Z" --priority 2
```

## Configuration

Place `~/.config/vikunja.yaml` with:

```yaml
base_url: "http://192.168.1.230:3456"
username: "admin"
password: "admin123"
```

The helper script auto-detects this path. Override with env vars:
`VIKUNJA_BASE_URL`, `VIKUNJA_USER`, `VIKUNJA_PASS`.

## Important API Quirks

- **PUT** creates resources (not POST)
- **POST** updates resources (not PUT)
- **DELETE** works for deleting tasks/projects
- Tasks are created under a **project** — each project must exist first
- Token expires; the script re-authenticates automatically on 401

## Core Workflows

### 1. Create a Task

```bash
python3 "$(skill-dir)/scripts/vikunja.py" task create "Title" \
  --project 1 \
  --description "Details here" \
  --due "2026-05-20T18:00:00" \
  --start "2026-05-19T09:00:00" \
  --priority 2 \
  --label "work" \
  --reminder "before 1h"
```

Supported flags: `--project`, `--description`, `--due`, `--start`, `--end`,
`--priority`, `--label`, `--reminder`, `--repeat-every`, `--repeat-mode`
(0=default, 1=monthly, 2=from-current), `--color`.

### 2. List Tasks

```bash
# All tasks
python3 "$(skill-dir)/scripts/vikunja.py" task list

# Tasks in a specific project
python3 "$(skill-dir)/scripts/vikunja.py" task list --project 1

# Only undone tasks, sorted by priority descending
python3 "$(skill-dir)/scripts/vikunja.py" task list --filter "done=false" --sort-by "priority" --order "desc"
```

Filter syntax: see [API Reference](references/api_reference.md) for full query syntax.

### 3. Update a Task

```bash
# Mark as done
python3 "$(skill-dir)/scripts/vikunja.py" task update $TASK_ID --done

# Change due date
python3 "$(skill-dir)/scripts/vikunja.py" task update $TASK_ID --due "2026-05-21T10:00:00"

# Change priority
python3 "$(skill-dir)/scripts/vikunja.py" task update $TASK_ID --priority 3
```

### 4. Bulk Operations

```bash
# Mark multiple tasks done at once
python3 "$(skill-dir)/scripts/vikunja.py" tasks bulk-complete 12 15 18
```

### 5. Projects

```bash
# List all projects
python3 "$(skill-dir)/scripts/vikunja.py" project list

# Create a new project
python3 "$(skill-dir)/scripts/vikunja.py" project create "Side Projects" --identifier "SP" --color "#ff6600"
```

### 6. Labels

```bash
# List labels
python3 "$(skill-dir)/scripts/vikunja.py" label list

# Create a label
python3 "$(skill-dir)/scripts/vikunja.py" label create "urgent" --color "#ff0000"

# Assign label to task
python3 "$(skill-dir)/scripts/vikunja.py" task add-label $TASK_ID "urgent"
```

### 7. Delete

```bash
python3 "$(skill-dir)/scripts/vikunja.py" task delete $TASK_ID
python3 "$(skill-dir)/scripts/vikunja.py" project delete $PROJECT_ID
```

## AI Usage Patterns

When the user says "schedule X for Y date", parse the date and create a task:
- "remind me to buy milk tomorrow at 6pm" → task title "Buy milk", due "2026-05-19T18:00:00"
- "every monday review expenses" → task with `--repeat-every 604800 --repeat-mode 0`
- "add fix the login bug as high priority" → priority 3 or 4

For recurring tasks, compute `repeat_after` in seconds:
- daily = 86400, weekly = 604800, monthly = 2592000, yearly = 31536000

## Version Notes

- **Buckets/Kanban** (`bucket` commands) require Vikunja v2.4+ — not available in v2.3.0
- **Admin routes** (`/api/v1/admin/`) require Vikunja v2.4+ — not available in v2.3.0
- This skill works with Vikunja v2.3.0+ for all task/project/label operations

## Error Handling

- `401` → re-login automatically
- `403` → project access issue; list projects to check permissions
- `404` → task/project not found; try listing to find it
- `400` → invalid request body; check required fields (title is always required)
- Log errors to `memory/vikunja-errors.log` for debugging

## Resources

- [Full API Reference](references/api_reference.md) — endpoint details, schemas, examples
