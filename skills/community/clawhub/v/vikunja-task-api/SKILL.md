---
name: vikunja-task-api
version: 2.3.0
description: |
  Install: clawhub install ashanzzz-vikunja-task-api

  Full Vikunja v2 API integration — projects, tasks, labels, teams, views, comments, attachments, bulk operations, and more.
homepage: https://vikunja.io/
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["curl","jq"],"env":["VIKUNJA_URL"],"optionalEnv":["VIKUNJA_TOKEN","VIKUNJA_USERNAME","VIKUNJA_PASSWORD"]},"primaryEnv":"VIKUNJA_TOKEN"}}
---

# Vikunja Task API Skill

## Install

```bash
clawhub install ashanzzz-vikunja-task-api
```

Then set environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `VIKUNJA_URL` | Yes | Vikunja 实例地址，如 `http://192.168.8.11:3456` |
| `VIKUNJA_TOKEN` | Recommended | API Token（优先）或用户名/密码 |
| `VIKUNJA_USERNAME` | Alt | 用户名（TOKEN 未设置时使用） |
| `VIKUNJA_PASSWORD` | Alt | 密码（TOKEN 未设置时使用） |

> For detailed setup, see the **Setup After Install** section below.

## Quick Setup

In your OpenClaw workspace, add to `secure/api-fillin.env`:

```bash
VIKUNJA_URL=http://your-vikunja-instance:3456
VIKUNJA_TOKEN=tk_xxxxxxxxxxxxx   # Optional: API token (recommended)
# VIKUNJA_USERNAME=your_username  # Optional: for login-based auth
# VIKUNJA_PASSWORD=your_password  # Optional: for login-based auth
```

### 2. Verify Connectivity

```bash
curl -s $VIKUNJA_URL/api/v1/info | jq
```

### 3. Install via ClawHub (if available)

```bash
clawhub install vikunja-task-api
```

Or manually clone into your skills directory:

```bash
git clone https://github.com/ashanzzz/openclaw-person-skills.git
export CLAWHUB_WORKDIR=$(pwd)/openclaw-person-skills
```

---

## Installation (Human User)

### Prerequisites

- **Vikunja instance** (self-hosted or cloud) — get it at https://vikunja.io/download
- **API token** from Vikunja: Settings → API Tokens → Create new token
- **curl** and **jq** installed on your system

### Setup Steps

**Step 1: Get your Vikunja URL**

Note your Vikunja instance base URL, e.g.:
- Self-hosted: `http://192.168.1.100:3456`
- Cloud: `https://vikunja.example.com`

**Step 2: Generate an API Token**

1. Log in to Vikunja
2. Go to **Settings → API Tokens**
3. Click **Create new token**
4. Copy the token (starts with `tk_`)

**Step 3: Test the Connection**

```bash
export VIKUNJA_URL="http://your-vikunja-instance:3456"
export VIKUNJA_TOKEN="tk_your_token_here"

# Test (should return instance info)
curl -s "$VIKUNJA_URL/api/v1/info" | jq

# List your projects
curl -s "$VIKUNJA_URL/api/v1/projects" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq '.[] | {id,title}'
```

**Step 4: Optional — Install the Helper Script**

Save `vikunja.sh` to a directory in your PATH for convenient CLI access:

```bash
curl -sL https://raw.githubusercontent.com/ashanzzz/openclaw-person-skills/main/skills/vikunja-task-api/vikunja.sh \
  -o /usr/local/bin/vikunja && chmod +x /usr/local/bin/vikunja
```

Then configure:

```bash
echo 'export VIKUNJA_URL="http://your-vikunja-instance:3456"' >> ~/.bashrc
echo 'export VIKUNJA_TOKEN="tk_your_token"' >> ~/.bashrc
source ~/.bashrc
```

Usage examples:

```bash
vikunja list                    # List all open tasks
vikunja due-today               # Tasks due today
vikunja create 9 "New task"    # Create task in project 9
vikunja done 123                # Mark task 123 as done
vikunja show 123                # Show task details
```

---


Use Vikunja as the **source of truth** for all task management. This skill supersedes any internal working-buffer tracking for user-visible tasks.

## API Base

- **Base URL**: `$VIKUNJA_URL/api/v1` (auto-normalized, no trailing slash)
- **Auth**: `Authorization: Bearer <token>` (JWT or API token)
- **Token acquisition**: `POST /login` with `username` + `password`

## Authentication

### Login (get JWT)
```bash
curl -X POST "$VIKUNJA_URL/api/v1/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"USER","password":"PASS"}' | jq '.token'
```

### API Token (recommended for automation)
Create a token in Vikunja UI: Settings → API Tokens. Then use:
```bash
export VIKUNJA_TOKEN="tk_xxxx"
```

## Critical HTTP Method Rules (Must Remember!)

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create project | **PUT** | `/projects` |
| Update project | **POST** | `/projects/{id}` |
| Delete project | **DELETE** | `/projects/{id}` |
| Create task | **PUT** | `/projects/{id}/tasks` |
| Update task | **POST** | `/tasks/{id}` |
| Delete task | **DELETE** | `/tasks/{id}` |
| Bulk update tasks | **POST** | `/tasks/bulk` |
| Get all tasks | **GET** | `/tasks` |
| Move task to bucket | **POST** | `/projects/{project}/views/{view}/buckets/{bucket}/tasks` |
| Create label | **PUT** | `/labels` |
| Update label | **PUT** | `/labels/{id}` |
| Delete label | **DELETE** | `/labels/{id}` |

## Core Endpoints

### Projects

```bash
# List all projects
curl -s "$VIKUNJA_URL/api/v1/projects" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq '.[] | {id,title,owner}'

# Create project (PUT, not POST!)
curl -X PUT "$VIKUNJA_URL/api/v1/projects" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Project Name","description":"","identifier":"","hex_color":""}' | jq '{id,title}'

# Get project details
curl -s "$VIKUNJA_URL/api/v1/projects/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq

# Update project (POST)
curl -X POST "$VIKUNJA_URL/api/v1/projects/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Title","hex_color":"#ff0000"}' | jq '{id,title}'

# Delete project
curl -X DELETE "$VIKUNJA_URL/api/v1/projects/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"

# Duplicate project
curl -X PUT "$VIKUNJA_URL/api/v1/projects/{id}/duplicate" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq '{id,title}'
```

### Tasks

```bash
# Get all open tasks (filter: done = false)
curl -s "$VIKUNJA_URL/api/v1/tasks" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  | jq '.[] | select(.done == false) | {id,title,due_date,project_id}'

# Get tasks by project
curl -s "$VIKUNJA_URL/api/v1/projects/{id}/tasks" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  | jq '.[] | {id,title,done,due_date}'

# Create task in project (PUT, not POST!)
curl -X PUT "$VIKUNJA_URL/api/v1/projects/{project_id}/tasks" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Task Title","description":"","due_date":"2026-04-30T23:59:00Z"}' | jq '{id,title}'

# Get task details
curl -s "$VIKUNJA_URL/api/v1/tasks/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq

# Update task (POST) — including mark done
curl -X POST "$VIKUNJA_URL/api/v1/tasks/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"done":true,"title":"Updated Title"}' | jq '{id,done,done_at}'

# Delete task
curl -X DELETE "$VIKUNJA_URL/api/v1/tasks/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"

# Bulk update tasks
curl -X POST "$VIKUNJA_URL/api/v1/tasks/bulk" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tasks":[{"id":1,"done":true},{"id":2,"done":true}]}' | jq

# Update task position (for drag-and-drop reordering)
curl -X POST "$VIKUNJA_URL/api/v1/tasks/{id}/position" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"position":0,"bucket_id":5}' | jq

# Duplicate task
curl -X PUT "$VIKUNJA_URL/api/v1/tasks/{id}/duplicate" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"project_id":9}' | jq '{id,title}'
```

### Task Assignees

```bash
# Get assignees
curl -s "$VIKUNJA_URL/api/v1/tasks/{id}/assignees" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq

# Add assignee
curl -X PUT "$VIKUNJA_URL/api/v1/tasks/{id}/assignees" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":1}' | jq

# Bulk add assignees
curl -X POST "$VIKUNJA_URL/api/v1/tasks/{id}/assignees/bulk" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_ids":[1,2,3]}' | jq

# Remove assignee
curl -X DELETE "$VIKUNJA_URL/api/v1/tasks/{id}/assignees/{user_id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"
```

### Task Labels

```bash
# Get labels on a task
curl -s "$VIKUNJA_URL/api/v1/tasks/{id}/labels" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq

# Add label to task
curl -X PUT "$VIKUNJA_URL/api/v1/tasks/{id}/labels" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"label_id":5}' | jq

# Bulk update labels on task
curl -X POST "$VIKUNJA_URL/api/v1/tasks/{id}/labels/bulk" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"labels":[{"label_id":5},{"label_id":8}]}' | jq

# Remove label from task
curl -X DELETE "$VIKUNJA_URL/api/v1/tasks/{id}/labels/{label_id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"
```

### Task Comments

```bash
# Get comments
curl -s "$VIKUNJA_URL/api/v1/tasks/{id}/comments" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq

# Create comment
curl -X PUT "$VIKUNJA_URL/api/v1/tasks/{id}/comments" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"This is a comment"}' | jq '{id,comment}'

# Update comment
curl -X POST "$VIKUNJA_URL/api/v1/tasks/{id}/comments/{comment_id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"Updated comment"}' | jq

# Delete comment
curl -X DELETE "$VIKUNJA_URL/api/v1/tasks/{id}/comments/{comment_id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"
```

### Task Attachments

```bash
# List attachments
curl -s "$VIKUNJA_URL/api/v1/tasks/{id}/attachments" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq

# Upload attachment
curl -X PUT "$VIKUNJA_URL/api/v1/tasks/{id}/attachments" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -F "file=@/path/to/file.pdf" | jq

# Delete attachment
curl -X DELETE "$VIKUNJA_URL/api/v1/tasks/{id}/attachments/{attachment_id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"
```

### Task Relations

```bash
# Create relation between two tasks
curl -X PUT "$VIKUNJA_URL/api/v1/tasks/{id}/relations" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"other_task_id":10,"relation_kind":"subtask|blocks|depends_on|related"}' | jq

# Remove relation
curl -X DELETE "$VIKUNJA_URL/api/v1/tasks/{id}/relations/{relation_kind}/{other_task_id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"
```

### Labels (standalone)

```bash
# List all labels
curl -s "$VIKUNJA_URL/api/v1/labels" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq '.[] | {id,title,hex_color}'

# Create label
curl -X PUT "$VIKUNJA_URL/api/v1/labels" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Bug","hex_color":"#ff0000"}' | jq '{id,title}'

# Update label
curl -X PUT "$VIKUNJA_URL/api/v1/labels/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Feature","hex_color":"#00ff00"}' | jq

# Delete label
curl -X DELETE "$VIKUNJA_URL/api/v1/labels/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"
```

### Project Views & Kanban Buckets

```bash
# List project views
curl -s "$VIKUNJA_URL/api/v1/projects/{id}/views" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq '.[] | {id,title,kind}'

# List kanban buckets
curl -s "$VIKUNJA_URL/api/v1/projects/{id}/views/{view_id}/buckets" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq '.[] | {id,title}'

# Create bucket
curl -X PUT "$VIKUNJA_URL/api/v1/projects/{id}/views/{view_id}/buckets" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"To Do"}' | jq '{id,title}'

# Update bucket
curl -X POST "$VIKUNJA_URL/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket_id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"In Progress"}' | jq

# Delete bucket
curl -X DELETE "$VIKUNJA_URL/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket_id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"

# Move task to bucket (kanban drag-and-drop)
curl -X POST "$VIKUNJA_URL/api/v1/projects/{project}/views/{view}/buckets/{bucket}/tasks" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"task_id":123,"position":0}' | jq
```

### Project Members

```bash
# List project users
curl -s "$VIKUNJA_URL/api/v1/projects/{id}/users" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq

# Add user to project
curl -X PUT "$VIKUNJA_URL/api/v1/projects/{id}/users" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"rights":1}' | jq   # rights: 0=read, 1=write, 2=admin

# Update user rights
curl -X POST "$VIKUNJA_URL/api/v1/projects/{project_id}/users/{user_id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rights":2}' | jq

# Remove user from project
curl -X DELETE "$VIKUNJA_URL/api/v1/projects/{project_id}/users/{user_id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"
```

### Teams

```bash
# List all teams
curl -s "$VIKUNJA_URL/api/v1/teams" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq '.[] | {id,name}'

# Create team
curl -X PUT "$VIKUNJA_URL/api/v1/teams" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Engineering"}' | jq '{id,name}'

# Get team details
curl -s "$VIKUNJA_URL/api/v1/teams/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq

# Add member to team
curl -X PUT "$VIKUNJA_URL/api/v1/teams/{id}/members" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com"}' | jq
```

### Project Shares (link sharing)

```bash
# List shares
curl -s "$VIKUNJA_URL/api/v1/projects/{id}/shares" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq

# Create share link
curl -X PUT "$VIKUNJA_URL/api/v1/projects/{id}/shares" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"right":1}' | jq  # right: 0=read, 1=write

# Delete share
curl -X DELETE "$VIKUNJA_URL/api/v1/projects/{id}/shares/{share_id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"
```

### Saved Filters

```bash
# Create saved filter
curl -X PUT "$VIKUNJA_URL/api/v1/filters" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Filter","filter":"done = false","project_id":0}' | jq '{id,title}'

# Get saved filter
curl -s "$VIKUNJA_URL/api/v1/filters/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq

# Update saved filter
curl -X POST "$VIKUNJA_URL/api/v1/filters/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filter":"done = false && due_date < now"}' | jq

# Delete saved filter
curl -X DELETE "$VIKUNJA_URL/api/v1/filters/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"
```

### Notifications

```bash
# Get notifications
curl -s "$VIKUNJA_URL/api/v1/notifications" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq '.[] | {id,title,message}'

# Mark all as read
curl -X POST "$VIKUNJA_URL/api/v1/notifications" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"

# Mark one as (un)read
curl -X POST "$VIKUNJA_URL/api/v1/notifications/{id}" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_read":true}' | jq
```

### Reactions

```bash
# Add reaction to entity (task, comment, etc.)
curl -X PUT "$VIKUNJA_URL/api/v1/{kind}/{id}/reactions" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reaction":"👍"}' | jq

# Get reactions
curl -s "$VIKUNJA_URL/api/v1/{kind}/{id}/reactions" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq

# Remove reaction
curl -X POST "$VIKUNJA_URL/api/v1/{kind}/{id}/reactions/delete" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN"
```

### Service Info

```bash
# Get instance info (no auth required)
curl -s "$VIKUNJA_URL/api/v1/info" | jq
```

## Filtering Syntax

Vikunja uses a powerful filter language:

```
done = false
done = false && due_date < now
done = false && project_id = 9
done = false && due_date >= now/d && due_date < now/d + 1d
done = false && due_date < now + 1w
labels contains "Bug"
title contains "urgent"
priority > 0
assignee = <user_id>
```

Full docs: https://vikunja.io/docs/filters/

## Helper CLI (vikunja.sh)

```bash
# List open tasks
vikunja.sh list --filter 'done = false'

# Overdue tasks
vikunja.sh overdue

# Due today
vikunja.sh due-today

# Show task
vikunja.sh show 123

# Mark done
vikunja.sh done 123

# Create task
vikunja.sh create 9 "New Task"

# Delete task
vikunja.sh delete 123
```

## Task Display Format

Each task output:
```
<EMOJI> <DUE_DATE> - #<ID> <TASK>
```
- Emoji: first char of project title (first non-alphanumeric token for CJK/English)
- Default emoji: 🔨
- No due date: `(no due)`

## Task Model (Complete Field Reference)

```json
{
  "id": 123,
  "title": "Task Title",
  "description": "",
  "done": false,
  "done_at": null,
  "due_date": "2026-04-30T15:59:00Z",
  "project_id": 9,
  "repeat_after": 0,
  "priority": 0,
  "start_date": "0001-01-01T00:00:00Z",
  "end_date": "0001-01-01T00:00:00Z",
  "hex_color": "",
  "percent_done": 0,
  "created": "2026-03-31T12:00:00Z",
  "updated": "2026-03-31T12:00:00Z",
  "cover_image_url": null,
  "custom_fields": [],
  "缕": []
}
```

**Important:**
- `due_date = 0001-01-01T00:00:00Z` = no deadline
- `priority`: 0=none, 1=low, 2=medium, 3=high
- `repeat_after`: seconds until respawn (0 = not recurring)

## Pagination

Endpoints that return lists support pagination via `page` and `per_page` query params.

Headers returned:
- `x-pagination-total-pages`
- `x-pagination-result-count`

## Setup

```bash
# Recommended: write to secure/api-fillin.env
VIKUNJA_URL=http://192.168.8.11:3456
VIKUNJA_TOKEN=tk_xxxx
```

## Differences from Typical REST APIs

Vikunja uses non-standard methods for create operations:
- **PUT** for create (projects, tasks, labels, comments, filters)
- **POST** for update
- **DELETE** for delete

This is because Vikunja's create endpoints return the created object with an ID, allowing you to immediately work with it — similar to a POST but idempotent.

## Complete API Group Summary

| Group | Key Endpoints |
|-------|--------------|
| Auth | `POST /login` |
| Projects | CRUD: PUT/GET/POST/DELETE `/projects` |
| Tasks | CRUD: PUT(create in project), GET/POST/DELETE `/tasks` |
| Task Assignees | GET/PUT/POST/DELETE `/tasks/{id}/assignees` |
| Task Labels | GET/PUT/POST `/tasks/{id}/labels` |
| Task Comments | GET/PUT/POST/DELETE `/tasks/{id}/comments` |
| Task Attachments | GET/PUT/DELETE `/tasks/{id}/attachments` |
| Task Relations | PUT/DELETE `/tasks/{id}/relations` |
| Task Position | `POST /tasks/{id}/position` |
| Labels | CRUD: PUT/GET/PUT/DELETE `/labels` |
| Views & Buckets | GET `/projects/{id}/views`, CRUD `/buckets` |
| Project Members | GET/PUT/POST/DELETE `/projects/{id}/users` |
| Teams | CRUD: PUT/GET/POST/DELETE `/teams` |
| Project Shares | GET/PUT/DELETE `/projects/{id}/shares` |
| Saved Filters | CRUD: PUT/GET/POST/DELETE `/filters` |
| Notifications | GET/POST `/notifications` |
| Reactions | GET/PUT/POST `/reactions` |
| User Settings | Various `/user/settings/*` |
| Webhooks | CRUD `/webhooks` |
| Service | `GET /info` (no auth) |

Full OpenAPI spec: `$VIKUNJA_URL/api/v1/docs.json`
