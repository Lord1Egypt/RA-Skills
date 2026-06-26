# Vikunja API Reference (v2.3.0)

Full API spec extracted from the running instance's Swagger/OpenAPI definition.

## Authentication

| Step | Method | Endpoint | Body |
|------|--------|----------|------|
| Login | `POST` | `/api/v1/login` | `{"username": "...", "password": "..."}` |
| Token | Returns `{"token": "eyJ..."}` | — | — |
| Use | — | Header: `Authorization: Bearer <token>` | — |
| Logout | `POST` | `/api/v1/user/logout` | — |
| Token refresh | `POST` | `/api/v1/user/token/refresh` | — |

## Projects

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/v1/projects` | List all projects |
| `PUT` | `/api/v1/projects` | Create a project |
| `GET` | `/api/v1/projects/:id` | Get one project |
| `POST` | `/api/v1/projects/:id` | Update a project |
| `DELETE` | `/api/v1/projects/:id` | Delete a project |
| `GET` | `/api/v1/projects/:id/views` | Get project views |

### Project Schema

```json
{
  "id": 1,
  "title": "Inbox",
  "description": "",
  "identifier": "",
  "hex_color": "",
  "parent_project_id": 0,
  "is_archived": false,
  "is_favorite": false,
  "owner": { "id": 1, "username": "admin" },
  "created": "2026-05-18T17:02:41Z",
  "updated": "2026-05-18T17:02:41Z",
  "views": [ ... ]
}
```

## Tasks

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/v1/tasks` | List all tasks (user-wide) |
| `GET` | `/api/v1/projects/:id/tasks` | List tasks in project |
| `PUT` | `/api/v1/projects/:id/tasks` | **Create** a task |
| `GET` | `/api/v1/tasks/:id` | Get one task |
| `POST` | `/api/v1/tasks/:id` | **Update** a task |
| `DELETE` | `/api/v1/tasks/:id` | Delete a task |
| `POST` | `/api/v1/tasks/bulk` | Bulk update tasks |
| `POST` | `/api/v1/tasks/:id/read` | Mark as read |
| `POST` | `/api/v1/tasks/:id/position` | Update task position |

### Task Schema

```json
{
  "id": 1,
  "title": "Task title",
  "description": "Details here",
  "done": false,
  "done_at": "0001-01-01T00:00:00Z",
  "due_date": "2026-05-20T18:00:00Z",
  "start_date": "2026-05-19T09:00:00Z",
  "end_date": "2026-05-21T17:00:00Z",
  "priority": 2,
  "project_id": 1,
  "reminders": [{"reminder": "2026-05-20T17:00:00Z", "relative_to": "due_date", "relative_period": 0}],
  "repeat_after": 0,
  "repeat_mode": 0,
  "hex_color": "",
  "assignees": [],
  "labels": [],
  "identifier": "#1",
  "index": 1,
  "is_favorite": false,
  "is_unread": false,
  "bucket_id": 0,
  "position": 0,
  "percent_done": 0,
  "reactions": {},
  "created_by": { "id": 1, "username": "admin" },
  "created": "2026-05-18T17:10:25Z",
  "updated": "2026-05-18T17:10:25Z"
}
```

### Filter Syntax

Use the `filter` query parameter for task lists:

| Syntax | Example | Meaning |
|--------|---------|---------|
| `field=value` | `done=false` | Only undone tasks |
| `field>=value` | `priority>=3` | Priority 3 or higher |
| `field=value&field2=val2` | `done=false&priority=1` | AND filter |
| `title:keyword` | `title:fix` | Search title by keyword |

## Labels

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/v1/labels` | List all labels |
| `PUT` | `/api/v1/labels` | Create a label |
| `GET` | `/api/v1/labels/:id` | Get one label |
| `PUT` | `/api/v1/labels/:id` | Update a label |
| `DELETE` | `/api/v1/labels/:id` | Delete a label |
| `GET` | `/api/v1/tasks/:id/labels` | Get labels on a task |
| `PUT` | `/api/v1/tasks/:id/labels` | Replace all labels on a task |
| `POST` | `/api/v1/tasks/:id/labels/bulk` | Bulk add/remove labels |

### Label Schema

```json
{
  "id": 1,
  "title": "work",
  "description": "Work-related tasks",
  "hex_color": "#ff6600",
  "created": "2026-05-18T17:02:41Z",
  "updated": "2026-05-18T17:02:41Z"
}
```

## Bulk Operations

### Bulk Update Tasks

```
POST /api/v1/tasks/bulk
```

Body:

```json
{
  "task_ids": [1, 2, 3],
  "values": { "done": true }
}
```

Other bulk fields: `fields` (array of field names to update), `tasks` (array of full task objects for per-task updates).

## Task Relation Kinds

| Value | Meaning |
|-------|---------|
| `subtask` | This task is a subtask of the referenced task |
| `parenttask` | This task is the parent of the referenced task |
| `related` | Tasks are related |
| `duplicateof` | This task duplicates the referenced task |
| `duplicates` | This task is duplicated by the referenced task |
| `blocking` | This task blocks the referenced task |
| `blocked` | This task is blocked by the referenced task |
| `precedes` | This task precedes the referenced task |
| `follows` | This task follows the referenced task |
| `copiedfrom` | Copied from referenced task |
| `copiedto` | Copied to referenced task |

## Recurring Tasks

- `repeat_after` (integer): seconds between repetitions
- `repeat_mode` (integer):
  - `0` = default — repeats after the specified seconds
  - `1` = monthly — repeats all dates each month (ignores repeat_after)
  - `2` = from-current — repeats from the current date rather than the last set date

When a recurring task is marked as done, it:
1. Marks itself as undone
2. Increases all reminders and due_date by repeat_after seconds (or switches to the next month/day)

## Reminders

A reminder object:

```json
{
  "reminder": "2026-05-20T17:00:00Z",
  "relative_to": "due_date",
  "relative_period": 0
}
```

- `relative_to`: `due_date`, `start_date`, or `end_date`
- `relative_period`: seconds before/after the reference date. Negative = before.

## Views & Buckets

Each project can have multiple views:

| View Kind | Description |
|-----------|-------------|
| `list` | Simple list view |
| `gantt` | Timeline/Gantt chart |
| `table` | Spreadsheet-like view |
| `kanban` | Kanban board with buckets |

Buckets are used in kanban views. Tasks can be moved between buckets using the `bucket_id` field.

> **Version note:** Bucket API endpoints require Vikunja v2.4+. The v2.3.0 instance has bucket-related task fields but no bucket management API.

## Pagination & Sorting

Query parameters:

| Param | Description | Example |
|-------|-------------|---------|
| `s` | Search string | `s=milk` |
| `sort_by` | Fields to sort by | `sort_by=priority` |
| `order_by` | Ascending/descending | `order_by=desc` |
| `expand` | Expand sub-resources | `expand=buckets,comments` |
