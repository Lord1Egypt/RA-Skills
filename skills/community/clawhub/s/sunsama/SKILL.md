---
name: sunsama
description: |
  Sunsama MCP integration with managed authentication. Manage daily tasks, calendar events, backlog, objectives, time tracking, and email threads from connected accounts (Gmail, Outlook).
  Use this skill when users want to interact with Sunsama for task management, daily planning, and email thread operations.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Sunsama MCP

Access Sunsama via MCP (Model Context Protocol) with managed authentication.

## Quick Start

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'searchTerm': 'meeting'}).encode()
req = urllib.request.Request('https://api.maton.ai/sunsama/search_tasks', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/sunsama/{tool-name}
```

Maton proxies requests to Sunsama's MCP server and automatically injects your credentials. The `{tool-name}` corresponds to the MCP tool name (e.g., `search_tasks`).

## Authentication

All requests require the Maton API key:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Sunsama MCP connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=sunsama&method=MCP&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'sunsama', 'method': 'MCP'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "PENDING",
    "creation_time": "2026-03-03T10:44:23.480898Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "sunsama",
    "method": "MCP",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Security & Permissions

- Access is scoped to tasks, channels, timers, scheduling data, and email threads within the connected Sunsama account.
- **Email thread access spans connected email accounts.** Sunsama can list, read, mark as read, delete, and create follow-up tasks from email threads in linked Gmail or Outlook accounts. Always confirm with the user before performing any email operation, as these actions affect the connected email account directly.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call — including email deletions and calendar event changes — confirm the target resource and intended effect with the user.

## MCP Reference

All MCP tools use `POST` method:

### Task Management

| Tool | Description | Schema |
|------|-------------|--------|
| `search_tasks` | Search tasks by term | [schema](schemas/search_tasks.json) |
| `create_task` | Create a new task | [schema](schemas/create_task.json) |
| `edit_task_title` | Update task title | [schema](schemas/edit_task_title.json) |
| `delete_task` | Delete a task | [schema](schemas/delete_task.json) |
| `mark_task_as_completed` | Mark task complete | [schema](schemas/mark_task_as_completed.json) |
| `mark_task_as_incomplete` | Mark task incomplete | [schema](schemas/mark_task_as_incomplete.json) |
| `append_task_notes` | Add notes to task | [schema](schemas/append_task_notes.json) |
| `edit_task_time_estimate` | Set time estimate | [schema](schemas/edit_task_time_estimate.json) |
| `edit_task_recurrence_rule` | Set recurrence | [schema](schemas/edit_task_recurrence_rule.json) |
| `get_task_time_estimate` | Get AI time estimate | [schema](schemas/get_task_time_estimate.json) |
| `restore_task` | Restore deleted task | [schema](schemas/restore_task.json) |

### Subtasks

| Tool | Description | Schema |
|------|-------------|--------|
| `add_subtasks_to_task` | Add subtasks | [schema](schemas/add_subtasks_to_task.json) |
| `edit_subtask_title` | Update subtask title | [schema](schemas/edit_subtask_title.json) |
| `mark_subtask_as_completed` | Mark subtask complete | [schema](schemas/mark_subtask_as_completed.json) |
| `mark_subtask_as_incomplete` | Mark subtask incomplete | [schema](schemas/mark_subtask_as_incomplete.json) |

### Backlog

| Tool | Description | Schema |
|------|-------------|--------|
| `get_backlog_tasks` | List backlog tasks | [schema](schemas/get_backlog_tasks.json) |
| `move_task_to_backlog` | Move task to backlog | [schema](schemas/move_task_to_backlog.json) |
| `move_task_from_backlog` | Move from backlog to day | [schema](schemas/move_task_from_backlog.json) |
| `reposition_task_in_backlog` | Reorder backlog task | [schema](schemas/reposition_task_in_backlog.json) |
| `change_backlog_folder` | Change task folder | [schema](schemas/change_backlog_folder.json) |
| `create_braindump_task` | Create backlog task | [schema](schemas/create_braindump_task.json) |

### Scheduling

| Tool | Description | Schema |
|------|-------------|--------|
| `move_task_to_day` | Reschedule task | [schema](schemas/move_task_to_day.json) |
| `reorder_tasks` | Reorder day's tasks | [schema](schemas/reorder_tasks.json) |
| `timebox_a_task_to_calendar` | Block time for task | [schema](schemas/timebox_a_task_to_calendar.json) |
| `set_shutdown_time` | Set daily end time | [schema](schemas/set_shutdown_time.json) |

### Calendar Events

| Tool | Description | Schema |
|------|-------------|--------|
| `create_calendar_event` | Create calendar event | [schema](schemas/create_calendar_event.json) |
| `delete_calendar_event` | Delete calendar event | [schema](schemas/delete_calendar_event.json) |
| `move_calendar_event` | Reschedule event | [schema](schemas/move_calendar_event.json) |
| `import_task_from_calendar_event` | Import event as task | [schema](schemas/import_task_from_calendar_event.json) |
| `set_calendar_event_allow_task_projections` | Toggle task overlap | [schema](schemas/set_calendar_event_allow_task_projections.json) |
| `accept_meeting_invite` | Accept meeting | [schema](schemas/accept_meeting_invite.json) |
| `decline_meeting_invite` | Decline meeting | [schema](schemas/decline_meeting_invite.json) |

### Time Tracking

| Tool | Description | Schema |
|------|-------------|--------|
| `start_task_timer` | Start timer | [schema](schemas/start_task_timer.json) |
| `stop_task_timer` | Stop timer | [schema](schemas/stop_task_timer.json) |

### Channels & Objectives

| Tool | Description | Schema |
|------|-------------|--------|
| `create_channel` | Create channel/context | [schema](schemas/create_channel.json) |
| `add_task_to_channel` | Assign task to channel | [schema](schemas/add_task_to_channel.json) |
| `create_weekly_objective` | Create weekly goal | [schema](schemas/create_weekly_objective.json) |
| `align_task_with_objective` | Link task to objective | [schema](schemas/align_task_with_objective.json) |

### Archive

| Tool | Description | Schema |
|------|-------------|--------|
| `get_archived_tasks` | List archived tasks | [schema](schemas/get_archived_tasks.json) |
| `unarchive_task` | Restore archived task | [schema](schemas/unarchive_task.json) |

### Email Integration

| Tool | Description | Schema |
|------|-------------|--------|
| `list_email_threads` | List email threads | [schema](schemas/list_email_threads.json) |
| `create_follow_up_task_from_email` | Create task from email | [schema](schemas/create_follow_up_task_from_email.json) |
| `delete_email_thread` | Delete email thread | [schema](schemas/delete_email_thread.json) |
| `mark_email_thread_as_read` | Mark email as read | [schema](schemas/mark_email_thread_as_read.json) |

### Recurring Tasks

| Tool | Description | Schema |
|------|-------------|--------|
| `delete_all_incomplete_recurring_task_instances` | Delete future recurrences | [schema](schemas/delete_all_incomplete_recurring_task_instances.json) |
| `update_all_incomplete_recurring_task_instances` | Update future recurrences | [schema](schemas/update_all_incomplete_recurring_task_instances.json) |

### Settings & Preferences

| Tool | Description | Schema |
|------|-------------|--------|
| `toggle_auto_import_events` | Toggle event auto-import | [schema](schemas/toggle_auto_import_events.json) |
| `update_calendar_preferences` | Update calendar settings | [schema](schemas/update_calendar_preferences.json) |
| `update_import_event_filters` | Set event filters | [schema](schemas/update_import_event_filters.json) |
| `log_user_feedback` | Submit feedback | [schema](schemas/log_user_feedback.json) |

---

## Common Endpoints

### Search Tasks

Search for tasks by keyword:
```bash
POST /sunsama/search_tasks
Content-Type: application/json

{
  "searchTerm": "meeting"
}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"tasks\":[{\"_id\":\"69a6bf3a04d3cd0001595308\",\"title\":\"Team meeting prep\",\"scheduledDate\":\"2026-03-03\",\"completed\":false}]}"
    }
  ],
  "isError": false
}
```

### Create Task

Create a new task scheduled for a specific day:
```bash
POST /sunsama/create_task
Content-Type: application/json

{
  "title": "Review quarterly report",
  "day": "2026-03-03",
  "alreadyInTaskList": false
}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"success\":true,\"task\":{\"_id\":\"69a6bf3a04d3cd0001595308\",\"title\":\"Review quarterly report\",\"notes\":\"\",\"timeEstimate\":\"20 minutes\",\"sortOrder\":-1772535610535,\"isPersonal\":false,\"isWork\":true,\"isPrivate\":false,\"isArchived\":false,\"completed\":false,\"isBacklogged\":false,\"scheduledDate\":\"2026-03-03\",\"subtasks\":[],\"channel\":\"work\",\"folder\":null,\"timeboxEventIds\":[]}}"
    }
  ],
  "isError": false
}
```

### Get Backlog Tasks

List all tasks in the backlog:
```bash
POST /sunsama/get_backlog_tasks
Content-Type: application/json

{}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"tasks\":[],\"queryId\":\"bb7d004a-0b29-49d9-8345-6d9037786fbb\",\"totalPages\":1}"
    }
  ],
  "isError": false
}
```

### Mark Task as Completed

```bash
POST /sunsama/mark_task_as_completed
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308",
  "finishedDay": "2026-03-03"
}
```

### Add Subtasks to Task

```bash
POST /sunsama/add_subtasks_to_task
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308",
  "subtasks": [
    {"title": "Step 1: Research"},
    {"title": "Step 2: Draft outline"},
    {"title": "Step 3: Review"}
  ]
}
```

### Create Calendar Event

```bash
POST /sunsama/create_calendar_event
Content-Type: application/json

{
  "title": "Team standup",
  "startDate": "2026-03-03T09:00:00"
}
```

### Move Task to Day

Reschedule a task to a different day:
```bash
POST /sunsama/move_task_to_day
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308",
  "calendarDay": "2026-03-04"
}
```

### Timebox Task to Calendar

Block time for a task on your calendar:
```bash
POST /sunsama/timebox_a_task_to_calendar
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308",
  "startDate": "2026-03-03",
  "startTime": "14:00"
}
```

### Create Weekly Objective

```bash
POST /sunsama/create_weekly_objective
Content-Type: application/json

{
  "title": "Complete Q1 planning",
  "weekStartDay": "2026-03-03"
}
```

### Create Braindump Task (Backlog)

Add a task to backlog with time bucket:
```bash
POST /sunsama/create_braindump_task
Content-Type: application/json

{
  "title": "Research new tools",
  "timeBucket": "in the next month"
}
```

**Time bucket options:**
- `"in the next two weeks"`
- `"in the next month"`
- `"in the next quarter"`
- `"in the next year"`
- `"someday"`
- `"never"`

### Start/Stop Task Timer

```bash
POST /sunsama/start_task_timer
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308"
}
```

```bash
POST /sunsama/stop_task_timer
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308"
}
```

### Set Shutdown Time

Set when your workday ends:
```bash
POST /sunsama/set_shutdown_time
Content-Type: application/json

{
  "calendarDay": "2026-03-03",
  "hour": 18,
  "minute": 0
}
```

## Code Examples

### JavaScript

```javascript
const response = await fetch('https://api.maton.ai/sunsama/search_tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  },
  body: JSON.stringify({
    searchTerm: 'meeting'
  })
});
const data = await response.json();
console.log(data);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://api.maton.ai/sunsama/search_tasks',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'searchTerm': 'meeting'
    }
)
print(response.json())
```

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing MCP connection or invalid tool name |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited |

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Notes

- All task IDs are MongoDB ObjectIds (24-character hex strings)
- Date format: `YYYY-MM-DD` for days, ISO 8601 for datetimes
- MCP tool responses wrap content in `{"content": [{"type": "text", "text": "..."}], "isError": false}` format
- The `text` field contains JSON-stringified data that should be parsed
- Time estimates are returned as human-readable strings (e.g., "20 minutes")

## Resources

- [Sunsama](https://sunsama.com)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
