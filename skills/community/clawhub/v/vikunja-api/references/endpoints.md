# Vikunja API Endpoint Reference

Base: `${VIKUNJA_BASE_URL}/api/v1`
Auth: `Authorization: Bearer ${VIKUNJA_API_TOKEN}`

> Reminder: `PUT` = create, `POST` = update (Vikunja convention)

---

## Current user

```
GET /user
```
Returns the authenticated user object. Useful to resolve "me" to a user ID
when adding assignees.

Response fields: `id`, `username`, `email`, `name`

---

## Projects

### List all projects
```
GET /projects?page=1&per_page=50
```

Response: array of project objects.
Key fields: `id`, `title`, `description`, `identifier`, `is_archived`

### Get a single project
```
GET /projects/{projectID}
```

### Create a project
```
PUT /projects
```
Body:
```json
{
  "title": "My Project",
  "description": "Optional description",
  "color": "#ff0000"
}
```
Response: created project object with `id`.

---

## Tasks

### List all tasks (across all projects)
```
GET /tasks/all?page=1&per_page=50&sort_by=due_date&order_by=asc
```
Optional filter params: `filter=due_date<2025-12-31` (filter DSL).
Useful sort values: `due_date`, `priority`, `created`, `updated`.

### List tasks in a project
```
GET /projects/{projectID}/tasks?page=1&per_page=50
```

### Get a single task
```
GET /tasks/{taskID}
```
Returns full task object including labels, assignees, reminders.

### Create a task
```
PUT /projects/{projectID}/tasks
```
Body (all fields except `title` are optional):
```json
{
  "title": "Task title",
  "description": "Markdown description",
  "due_date": "2025-12-31T23:59:59Z",
  "start_date": "2025-12-01T09:00:00Z",
  "priority": 3,
  "percent_done": 0,
  "hex_color": "#ff0000",
  "reminders": [
    {
      "reminder": "2025-12-31T10:00:00Z",
      "relative_to": "",
      "relative_period": 0
    }
  ],
  "related_tasks": {
      "precedes": [{"id": 42}],
      "blocked_by": [{"id": 7}]
  }
}
```
Priority scale: `0` = none, `1` = low, `2` = medium, `3` = high, `4` = urgent, `5` = DO NOW.

`related_tasks` is optional. Keys are relation kinds; values are arrays of `{"id": taskID}`. 
Relations are created inline in a single request - no separate call needed.

Response: created task object with `id` and `index`.

### Update a task
```
POST /tasks/{taskID}
```
Body: same shape as create — only include fields you want to change.

To mark done:
```json
{ "done": true }
```

To update due date:
```json
{ "due_date": "2025-12-31T23:59:59Z" }
```

To update title + priority:
```json
{ "title": "New title", "priority": 5 }
```

### Delete a task
```
DELETE /tasks/{taskID}
```

---

## Reminders

Reminders live inside the task object. To add/change them, use the task update
endpoint with a `reminders` array. Each reminder is one of:

**Absolute datetime:**
```json
{
  "reminder": "2025-12-31T10:00:00Z"
}
```

**Relative to a task date field:**
```json
{
  "relative_to": "due_date",
  "relative_period": -3600
}
```
`relative_period` is in seconds. Negative = before the reference date.
`relative_to` options: `"due_date"`, `"start_date"`, `"end_date"`

To remove all reminders: `"reminders": []`

To add a reminder without touching others: GET the task first, append to the
existing `reminders` array, then POST the update.

---

## Labels

### List all labels
```
GET /labels?page=1&per_page=50&s=<search>
```
Key fields: `id`, `title`, `hex_color`

### Create a label
```
PUT /labels
```
Body:
```json
{
  "title": "urgent",
  "hex_color": "#ff0000"
}
```

### Add a label to a task
```
PUT /tasks/{taskID}/labels
```
Body:
```json
{ "label_id": 42 }
```

### Remove a label from a task
```
DELETE /tasks/{taskID}/labels/{labelID}
```

---

## Assignees

### List task assignees
```
GET /tasks/{taskID}/assignees
```

### Add an assignee
```
PUT /tasks/{taskID}/assignees
```
Body:
```json
{ "user_id": 7 }
```
To assign the current user: call `GET /user` first to get their `id`.

### Remove an assignee
```
DELETE /tasks/{taskID}/assignees/{userID}
```

---

## Task Relations

### Create a relation
PUT /tasks/{taskID}/relations

Body:
{
  "other_task_id": 456,
  "relation_kind": "precedes"
}

relation_kind values:
- "precedes" — esta tarea va antes que la otra
- "follows" — esta tarea va después que la otra  
- "related" — relación genérica sin orden
- "duplicates" / "duplicated_by"
- "blocked_by" / "blocking"
- "caused_by"
- "copied_from" / "copied_to"
- "parent_task" / "subtask"

Response: objeto con task_id, other_task_id, relation_kind, created_by, created.

### Delete a relation
DELETE /tasks/{taskID}/relations/{otherTaskID}/{relationKind}


## Error responses

All errors return JSON:
```json
{
  "code": 4001,
  "message": "The task does not exist."
}
```

Common codes:
| HTTP | Code | Meaning |
|---|---|---|
| 401 | 1000 | Invalid or missing token |
| 403 | 3001 | No permission on resource |
| 404 | 4001 | Resource not found |
| 400 | 1001 | Invalid input |
| 429 | — | Rate limited (default: 100 req/60s) |

On 401: ask the user to verify `VIKUNJA_API_TOKEN` and that the token has the
required scopes for the operation being attempted.
