---
name: ticktick
description: Manage TickTick tasks and projects
triggers:
  - "/tasks"
  - "/ticktick"
---

# TickTick Skill

Manage your TickTick tasks and projects directly from OpenClaw.

## Setup

Before using, authenticate once (OAuth2):

```bash
cd ~/.openclaw/workspace/skills/ticktick
bun run scripts/ticktick.ts auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
```

Follow the OAuth flow. Credentials are stored securely in `~/.clawdbot/credentials/ticktick-cli/`.

Check status: `bun run scripts/ticktick.ts auth --status`

## Commands

### List Projects
`/tasks projects` or `/ticktick projects`

Shows all your TickTick projects with IDs and names.

### List Tasks
`/tasks [options]` or `/ticktick tasks [options]`

List tasks with powerful filtering and sorting.

**Options:**
- `--project <name>` – Filter by project name or ID
- `--status <pending|completed>` – Filter by status
- `--due <filter>` – Filter by due: `today`, `overdue`, `none`, `unspecified`
- `--priority <level>` – Filter: `high`, `medium`, `low`, `none`
- `--sort <field>` – Sort by: `due`, `priority`, `title`, `created`
- `--limit <N>` – Maximum number of tasks to return
- `--offset <N>` – Skip first N tasks (for pagination)
- `--group` – Group output by project
- `--format <type>` – Output format: plain, rich, json, yaml
- `--verbose` – Show API requests for debugging

Examples:
```
/tasks --project Work --status pending --sort due
/tasks --due overdue --format rich
/tasks --priority high --limit 20
/tasks --project Hobbies --group
```

### Create Task
`/tasks add "<title>" [options]`

**Options:**
- `--list <project>` – Project (required if no default configured)
- `--due <when>` – Due date: "today", "tomorrow", "in 3 days", or ISO date
- `--priority <low|medium|high>` – Priority level
- `--content "<notes>"` – Task description/notes
- `--tags <tag1 tag2 ...>` – Tags to apply

Example:
```
/tasks add "Upgrade thermostat firmware" --list Hillcrest --due today --priority medium --content "Flash new firmware from repo"
```

### Edit Task
`/tasks edit <task-id> [options]`

Modify an existing task. **Task ID (24-character hex) is required.** Obtain IDs from `/tasks --json`.

**Options:**
- `--title "<new title>"` – Change title
- `--content "<new notes>"` – Replace content/notes
- `--due <date>` – Change due date
- `--priority <level>` – Change priority (none, low, medium, high)
- `--tags <tags...>` – Replace tags (space-separated)
- `--json` – Output updated task as JSON
- `--verbose` – Show diagnostic info

Examples:
```
/tasks edit 65a54fce2026ccc8b729349b --priority high
/tasks edit 65a54fce2026ccc8b729349b --due "in 3 days" --content "Urgent: complete this week"
```

### Complete Task
`/tasks complete <task-id> [--json]` or `/tasks done <task-id> [--json]`

Mark a task as complete. Both `complete` and `done` are aliases. **Task ID is required.**

### Abandon Task
`/tasks abandon <task-id> [--json]`

Mark a task as "won't do" (abandoned). **Task ID is required.**

### Task Details
`/tasks details <task-id> [options]`

Show full information about a single task. **Task ID is required.**

**Options:**
- `--json` – Output as JSON
- `--verbose` – Show full task object

Example:
```
/tasks details 65a54fce2026ccc8b729349b
```

### Batch Abandon
`/tasks batch-abandon <task-id-1> <task-id-2> ...`

Abandon multiple tasks in a single API call using their IDs.

### Config
`/tasks config get <key>` – Get a configuration value
`/tasks config set <key> <value>` – Set a configuration value
`/tasks config list` – Show all config

**Configuration keys:**
- `default.project` – Default project for `add` when `--list` omitted
- `default.due` – Default due date for new tasks ("none", "today", "tomorrow")
- `display.colors` – Enable/disable colored output (true/false)
- `display.timezone` – Timezone for date display (e.g., "America/New_York")

Example:
```
/tasks config set default.project Personal
/tasks config set default.due none
/tasks config list
```

Config is stored in `~/.config/ticktick-skill/config.json`.

---

## ADHD-Friendly Usage

### Morning Triage
Use the following to start your day:
```
/tasks --due overdue --format rich
/tasks --due today --format rich
/tasks --priority high --format rich
```
Or combine: `/tasks --format rich` (shows all pending, sorted by urgency)

### Quick Wins
Find small tasks to build momentum:
```
/tasks --priority low --limit 10 --sort title
```
Or use `/tasks details <id>` to assess quickly.

### Focus Mode
Show only what needs attention today:
```
/tasks --due today --sort due
```

### Reduce Overwhelm
- Use `--limit` to avoid seeing everything at once
- Group by project: `/tasks --group` to break into chunks
- Use colored output (`--format rich`) to prioritize by color

---

## Notes

- **Task IDs**: All commands that operate on a specific task require the 24-character hex ID for reliability. Get IDs from `/tasks --json`.
- **Project names**: Case-insensitive, partial match works (e.g., "Hill" matches "Hillcrest")
- **Due dates**: Flexible parsing supports "today", "tomorrow", "in 3 days", "next monday", and ISO dates (YYYY-MM-DD)
- **Rate limits**: TickTick API allows ~100 requests/minute. The CLI respects limits; if you hit them, wait a minute and retry.
- **JSON output**: Add `--json` to any command for machine-readable output (useful for scripts)

## Troubleshooting

**"Task not found"**
- Verify you're using the correct 24-char task ID
- Get fresh IDs with `/tasks --json`

**"Project not found"**
- List all projects with `/tasks projects`
- Project names are case-insensitive but must match exactly (partial match works)

**Authentication errors**
- Re-run: `bun run scripts/ticktick.ts auth`
- Check credentials exist: `ls ~/.clawdbot/credentials/ticktick-cli/`

**Rate limit exceeded**
- Wait ~60 seconds and retry
- Use `--verbose` to see request counts

**Dates not parsing**
- Use ISO format: `2026-03-25`
- Or natural language: `tomorrow`, `in 5 days`, `next friday`

## Implementation

Wrapper skill uses `bun run scripts/ticktick.ts` with `--json` flag and parses responses. Authentication stored in `~/.clawdbot/credentials/ticktick-cli/`.

### Command Reference Table

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `projects` | List all projects | – |
| `tasks` | List tasks | `--project`, `--status`, `--due`, `--priority`, `--sort`, `--limit`, `--group` |
| `add` | Create task | `--list`, `--due`, `--priority`, `--content`, `--tags` |
| `edit` | Modify task | `--title`, `--content`, `--due`, `--priority`, `--tags` |
| `complete` / `done` | Mark complete | – |
| `abandon` | Mark won't-do | – |
| `details` | Show full task info | `--json`, `--verbose` |
| `batch-abandon` | Abandon multiple | `<task-id>...` |
| `config` | Manage config | `get`, `set`, `list` |

---

*Happy task managing!*
