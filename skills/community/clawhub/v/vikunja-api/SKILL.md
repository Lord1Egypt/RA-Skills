---
name: vikunja
description: >
  Interact with a Vikunja task management instance via its REST API. Use this
  skill whenever the user wants to manage tasks, projects, labels, assignees,
  or reminders in Vikunja — including creating tasks, listing what's due,
  marking things done, adding labels, assigning users, or organizing projects.
  Trigger on phrases like "add a task", "what's due today", "create a project
  in Vikunja", "assign this to me", "set a reminder", or any mention of
  Vikunja task management.
metadata:
  openclaw:
    requires:
      env:
        - VIKUNJA_BASE_URL
        - VIKUNJA_API_TOKEN
    primaryEnv: VIKUNJA_API_TOKEN
    homepage: https://github.com/seergs/vikunja-skill
---

# Vikunja Skill

Connects an OpenClaw agent to any Vikunja instance via its REST API (`/api/v1`).
Uses an API token for authentication — no session management needed.

## Configuration (required env vars)

| Variable | Description |
|---|---|
| `VIKUNJA_BASE_URL` | Base URL of the instance, e.g. `https://vikunja.example.com` |
| `VIKUNJA_API_TOKEN` | API token created under Settings → API Tokens |

The agent must confirm both vars are set before making any request.
If missing, tell the user exactly which var is absent and where to create the token
(Settings → API Tokens in the Vikunja web UI).

## Important API conventions

> **Vikunja uses non-standard HTTP verbs:**
> - `PUT` = **create** a new resource
> - `POST` = **update** an existing resource
> - `GET` = read / list
> - `DELETE` = delete

All requests:
- Header: `Authorization: Bearer <VIKUNJA_API_TOKEN>`
- Header: `Content-Type: application/json`
- Base: `${VIKUNJA_BASE_URL}/api/v1`

Paginated list endpoints accept `?page=N&per_page=50&s=<search>`.
Response headers `x-pagination-total-pages` and `x-pagination-result-count`
tell you if more pages exist.

## Supported operations

See `references/endpoints.md` for the full endpoint reference.

### Projects

- List all projects the user has access to
- Create a new project
- Get a single project by ID

### Tasks

- List tasks (all, or filtered by project)
- Get a single task by ID
- Create a task in a project
- Update a task (title, description, priority, due date, percent done)
- Mark a task as done (`"done": true`)
- Delete a task

### Labels

- List all available labels
- Create a label
- Add a label to a task
- Remove a label from a task

### Assignees

- Add a user as assignee to a task
- Remove an assignee from a task
- List task assignees

### Reminders

- Add a reminder to a task (absolute datetime or relative offset)
- Remove a reminder from a task
- Reminders are part of the task object — use the task update flow

### Task Relations
- Create a relation between two tasks (precedes, follows, blocked_by, subtask, etc.)
- Delete a relation
- When creating a new task with a known relation, use `related_tasks` inline in the body — no separate call needed
- When adding relations to already-existing tasks, use `PUT /tasks/{id}/relations`

## Workflow guidelines

1. **Resolve names to IDs first.** If the user says "add a task to my Work
   project", list projects and find the ID for "Work" before creating the task.
2. **Confirm destructive actions.** Before deleting a task or project, confirm
   with the user.
3. **Show structured output.** When listing tasks, present title, due date,
   priority, labels, and done status. Format dates in a human-readable way.
4. **Handle pagination.** If `x-pagination-total-pages > 1`, fetch subsequent
   pages or inform the user that results are truncated.
5. **Error handling.** On HTTP 4xx/5xx, surface the `message` field from the
   JSON response to the user. On 401, remind them to check `VIKUNJA_API_TOKEN`.

## Example interactions

- "What tasks are due this week?" → GET /tasks/all with filter, format results
- "Create a task 'Deploy new release' in my Homelab project due Friday" → resolve
  project ID, then PUT /projects/{id}/tasks
- "Mark task 42 as done" → POST /tasks/42 with `{"done": true}`
- "Add the 'urgent' label to task 17" → resolve label ID, PUT /tasks/17/labels
- "Assign me to task 5" → look up current user via GET /user, PUT /tasks/5/assignees
- "Set a reminder for task 8 in 2 hours" → compute absolute datetime, POST /tasks/8

Read `references/endpoints.md` for exact request/response shapes.
