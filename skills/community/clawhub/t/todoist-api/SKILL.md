---
name: todoist
description: |
  Todoist API integration with managed OAuth. Manage tasks, projects, sections, labels, and comments. Use this skill when users want to create, update, complete, or organize tasks and projects in Todoist. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Todoist

Access the Todoist API v1 with managed OAuth authentication. Manage tasks, projects, sections, labels, and comments.

## Quick Start

```bash
# List all tasks
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/todoist/api/v1/tasks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/todoist/api/v1/{resource}
```

Maton proxies requests to `api.todoist.com/api/v1` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

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

Manage your Todoist OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=todoist&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'todoist'}).encode()
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
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "todoist",
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

### Specifying Connection

If you have multiple Todoist connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/todoist/api/v1/tasks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to tasks, projects, sections, labels, and comments within the connected Todoist account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### Projects

#### List Projects

```bash
GET /todoist/api/v1/projects
```

**Response:**
```json
{
  "results": [
    {
      "id": "6fwFRqmVCFvWVX5R",
      "name": "Inbox",
      "color": "charcoal",
      "parent_id": null,
      "child_order": 0,
      "is_shared": false,
      "is_favorite": false,
      "inbox_project": true,
      "view_style": "list",
      "description": "",
      "is_archived": false
    }
  ],
  "next_cursor": null
}
```

#### Get Project

```bash
GET /todoist/api/v1/projects/{id}
```

#### Create Project

```bash
POST /todoist/api/v1/projects
Content-Type: application/json

{
  "name": "My Project",
  "color": "blue",
  "is_favorite": true,
  "view_style": "board"
}
```

**Parameters:**
- `name` (required) - Project name
- `parent_id` - Parent project ID for nesting
- `color` - Project color (e.g., "red", "blue", "green")
- `is_favorite` - Boolean favorite status
- `view_style` - "list" or "board" (default: list)

**Example:**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'name': 'My New Project', 'color': 'blue'}).encode()
req = urllib.request.Request('https://api.maton.ai/todoist/api/v1/projects', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### Update Project

```bash
POST /todoist/api/v1/projects/{id}
Content-Type: application/json

{
  "name": "Updated Project Name",
  "color": "red"
}
```

#### Delete Project

```bash
DELETE /todoist/api/v1/projects/{id}
```

Returns 204 No Content on success.

#### Get Project Collaborators

```bash
GET /todoist/api/v1/projects/{id}/collaborators
```

### Tasks

#### List Tasks

```bash
GET /todoist/api/v1/tasks
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `project_id` | string | Filter by project |
| `section_id` | string | Filter by section |
| `label` | string | Filter by label name |
| `filter` | string | Todoist filter expression |
| `ids` | string | Comma-separated task IDs |

**Response:**
```json
{
  "results": [
    {
      "id": "6fwhG9wMHr4wxgpR",
      "content": "Buy groceries",
      "description": "",
      "project_id": "6fwFRqmVCFvWVX5R",
      "section_id": null,
      "parent_id": null,
      "child_order": 1,
      "priority": 2,
      "checked": false,
      "labels": [],
      "due": {
        "date": "2026-02-07T10:00:00",
        "string": "tomorrow at 10am",
        "lang": "en",
        "is_recurring": false
      },
      "added_at": "2026-02-06T20:41:08.449320Z"
    }
  ],
  "next_cursor": null
}
```

#### Get Task

```bash
GET /todoist/api/v1/tasks/{id}
```

#### Create Task

```bash
POST /todoist/api/v1/tasks
Content-Type: application/json

{
  "content": "Buy groceries",
  "project_id": "2366834771",
  "priority": 2,
  "due_string": "tomorrow at 10am",
  "labels": ["shopping", "errands"]
}
```

**Required Fields:**
- `content` - Task content/title

**Optional Fields:**
- `description` - Task description
- `project_id` - Project to add task to (defaults to Inbox)
- `section_id` - Section within project
- `parent_id` - Parent task ID for subtasks
- `labels` - Array of label names
- `priority` - 1 (normal) to 4 (urgent)
- `due_string` - Natural language due date ("tomorrow", "next Monday 3pm")
- `due_date` - ISO format YYYY-MM-DD
- `due_datetime` - RFC3339 format with timezone
- `assignee_id` - User ID to assign task
- `duration` - Task duration (integer)
- `duration_unit` - "minute" or "day"

**Example:**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    'content': 'Complete project report',
    'priority': 4,
    'due_string': 'tomorrow at 5pm',
    'labels': ['work', 'urgent']
}).encode()
req = urllib.request.Request('https://api.maton.ai/todoist/api/v1/tasks', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### Update Task

```bash
POST /todoist/api/v1/tasks/{id}
Content-Type: application/json

{
  "content": "Updated task content",
  "priority": 3
}
```

#### Close Task (Complete)

```bash
POST /todoist/api/v1/tasks/{id}/close
```

Returns 204 No Content. For recurring tasks, this schedules the next occurrence.

#### Reopen Task

```bash
POST /todoist/api/v1/tasks/{id}/reopen
```

Returns 204 No Content.

#### Delete Task

```bash
DELETE /todoist/api/v1/tasks/{id}
```

Returns 204 No Content.

### Sections

#### List Sections

```bash
GET /todoist/api/v1/sections
GET /todoist/api/v1/sections?project_id={project_id}
```

**Response:**
```json
{
  "results": [
    {
      "id": "6g424m6CQm47v7mm",
      "project_id": "6g424jv8X52hP7qF",
      "section_order": 1,
      "name": "To Do",
      "added_at": "2026-02-20T22:25:04.203675Z",
      "is_archived": false,
      "is_collapsed": false
    }
  ],
  "next_cursor": null
}
```

#### Get Section

```bash
GET /todoist/api/v1/sections/{id}
```

#### Create Section

```bash
POST /todoist/api/v1/sections
Content-Type: application/json

{
  "name": "In Progress",
  "project_id": "2366834771",
  "order": 2
}
```

**Required Fields:**
- `name` - Section name
- `project_id` - Parent project ID

#### Update Section

```bash
POST /todoist/api/v1/sections/{id}
Content-Type: application/json

{
  "name": "Updated Section Name"
}
```

#### Delete Section

```bash
DELETE /todoist/api/v1/sections/{id}
```

Returns 204 No Content.

### Labels

#### List Labels

```bash
GET /todoist/api/v1/labels
```

**Response:**
```json
{
  "results": [
    {
      "id": "2182980313",
      "name": "urgent",
      "color": "red",
      "order": 1,
      "is_favorite": false
    }
  ],
  "next_cursor": null
}
```

#### Get Label

```bash
GET /todoist/api/v1/labels/{id}
```

#### Create Label

```bash
POST /todoist/api/v1/labels
Content-Type: application/json

{
  "name": "work",
  "color": "blue",
  "is_favorite": true
}
```

**Parameters:**
- `name` (required) - Label name
- `color` - Label color
- `order` - Sort order
- `is_favorite` - Boolean favorite status

#### Update Label

```bash
POST /todoist/api/v1/labels/{id}
Content-Type: application/json

{
  "name": "updated-label",
  "color": "green"
}
```

#### Delete Label

```bash
DELETE /todoist/api/v1/labels/{id}
```

Returns 204 No Content.

### Comments

#### List Comments

```bash
GET /todoist/api/v1/comments?task_id={task_id}
GET /todoist/api/v1/comments?project_id={project_id}
```

**Note:** Either `task_id` or `project_id` is required.

**Response:**
```json
{
  "results": [
    {
      "id": "6g424pWVXPpwW7hR",
      "item_id": "6g424pQr2xfCcFr2",
      "content": "This is a comment",
      "posted_at": "2026-02-20T22:25:20.045703Z",
      "posted_uid": "57402826",
      "file_attachment": null,
      "reactions": null
    }
  ],
  "next_cursor": null
}
```

#### Get Comment

```bash
GET /todoist/api/v1/comments/{id}
```

#### Create Comment

```bash
POST /todoist/api/v1/comments
Content-Type: application/json

{
  "task_id": "9993408170",
  "content": "Don't forget to check the budget"
}
```

**Required Fields:**
- `content` - Comment text
- `task_id` OR `project_id` - Where to attach the comment

#### Update Comment

```bash
POST /todoist/api/v1/comments/{id}
Content-Type: application/json

{
  "content": "Updated comment text"
}
```

#### Delete Comment

```bash
DELETE /todoist/api/v1/comments/{id}
```

Returns 204 No Content.

## Priority Values

| Priority | Meaning |
|----------|---------|
| 1 | Normal (default) |
| 2 | Medium |
| 3 | High |
| 4 | Urgent |

## Due Date Formats

Use ONE of these formats per request:

- `due_string` - Natural language: "tomorrow", "next Monday at 3pm", "every week"
- `due_date` - Date only: "2026-02-15"
- `due_datetime` - Full datetime: "2026-02-15T14:00:00Z"

## Code Examples

### JavaScript

```javascript
// Create a task
const response = await fetch('https://api.maton.ai/todoist/api/v1/tasks', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    content: 'Review pull request',
    priority: 3,
    due_string: 'today at 5pm'
  })
});
const task = await response.json();
```

### Python

```python
import os
import requests

# Create a task
response = requests.post(
    'https://api.maton.ai/todoist/api/v1/tasks',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'content': 'Review pull request',
        'priority': 3,
        'due_string': 'today at 5pm'
    }
)
task = response.json()
```

## Notes

- Task IDs and Project IDs are strings, not integers
- Priority 4 is the highest (urgent), priority 1 is normal
- Use only one due date format per request (due_string, due_date, or due_datetime)
- Closing a recurring task schedules the next occurrence
- The Inbox project cannot be deleted
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 204 | Success (no content) - for close, reopen, delete operations |
| 400 | Invalid request or missing Todoist connection |
| 401 | Invalid or missing Maton API key |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Todoist API |

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

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `todoist`. For example:

- Correct: `https://api.maton.ai/todoist/api/v1/tasks`
- Incorrect: `https://api.maton.ai/api/v1/tasks`

## Resources

- [Todoist API v1 Documentation](https://developer.todoist.com/api/v1)
- [Todoist Filter Syntax](https://todoist.com/help/articles/introduction-to-filters)
- [Todoist OAuth Documentation](https://developer.todoist.com/guides/#oauth)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
