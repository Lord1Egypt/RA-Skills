# TickTick access policy

An access policy limits which endpoints TickTick connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/ticktick#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for TickTick: its 21 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create ticktick --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "open/v1/project/{id}/column"},
    {"method": "GET", "path": "open/v1/project/{id}/task/{id}/comments"},
    {"method": "GET", "path": "open/v1/countdown"},
    {"method": "GET", "path": "open/v1/focus"},
    {"method": "GET", "path": "open/v1/focus/{id}"},
    {"method": "GET", "path": "open/v1/habit"},
    {"method": "GET", "path": "open/v1/habit/checkins"},
    {"method": "GET", "path": "open/v1/habit/sections"},
    {"method": "GET", "path": "open/v1/habit/{id}"},
    {"method": "POST", "path": "open/v1/preference"},
    {"method": "GET", "path": "open/v1/project/group"},
    {"method": "GET", "path": "open/v1/project"},
    {"method": "GET", "path": "open/v1/project/{id}"},
    {"method": "GET", "path": "open/v1/project/{id}/data"},
    {"method": "GET", "path": "open/v1/project/{id}/members"},
    {"method": "GET", "path": "open/v1/tag"},
    {"method": "GET", "path": "open/v1/project/{id}/task/{id}"},
    {"method": "POST", "path": "open/v1/task/completed"},
    {"method": "POST", "path": "open/v1/task/filter"},
    {"method": "POST", "path": "open/v1/task/search"},
    {"method": "POST", "path": "open/v1/task/undone"}
  ],
  "deny": []
}
```

## Endpoints

The TickTick endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | open/v1/project/{id}/column | read | columns | Get project columns. |
| POST | open/v1/project/{id}/column | write | columns | Create a column. |
| POST | open/v1/project/{id}/column/{id} | write | columns | Update a column. |
| POST | open/v1/project/{id}/task/{id}/comment | write | comments | Add a task comment. |
| DELETE | open/v1/project/{id}/task/{id}/comment/{id} | write | comments | Delete a task comment. |
| GET | open/v1/project/{id}/task/{id}/comments | read | comments | Get task comments. |
| GET | open/v1/countdown | read | countdowns | Get countdowns. |
| GET | open/v1/focus | read | focus | Get focus records by time range. |
| POST | open/v1/focus | write | focus | Create a focus record. |
| GET | open/v1/focus/{id} | read | focus | Get a focus record by ID. |
| DELETE | open/v1/focus/{id} | write | focus | Delete a focus record. |
| GET | open/v1/habit | read | habits | Get all habits. |
| POST | open/v1/habit | write | habits | Create a habit. |
| GET | open/v1/habit/checkins | read | habits | Get habit check-ins. |
| GET | open/v1/habit/sections | read | habits | Get habit sections. |
| GET | open/v1/habit/{id} | read | habits | Get a habit by ID. |
| POST | open/v1/habit/{id} | write | habits | Update a habit. |
| POST | open/v1/habit/{id}/checkin | write | habits | Create or update a habit check-in. |
| POST | open/v1/preference | read | preferences | Get user preferences. |
| GET | open/v1/project/group | read | project-groups | Get project groups. |
| POST | open/v1/project/group | write | project-groups | Create a project group. |
| POST | open/v1/project/group/{id} | write | project-groups | Update a project group. |
| DELETE | open/v1/project/group/{id} | write | project-groups | Delete a project group. |
| GET | open/v1/project | read | projects | Get the user projects. |
| POST | open/v1/project | write | projects | Create a project. |
| GET | open/v1/project/{id} | read | projects | Get a project by ID. |
| POST | open/v1/project/{id} | write | projects | Update a project. |
| DELETE | open/v1/project/{id} | write | projects | Delete a project. |
| GET | open/v1/project/{id}/data | read | projects | Get a project with its tasks and columns. |
| GET | open/v1/project/{id}/members | read | projects | Get project members. |
| GET | open/v1/tag | read | tags | Get tags. |
| POST | open/v1/tag | write | tags | Create a tag. |
| GET | open/v1/project/{id}/task/{id} | read | tasks | Get a task by project ID and task ID. |
| DELETE | open/v1/project/{id}/task/{id} | write | tasks | Delete a task. |
| POST | open/v1/project/{id}/task/{id}/complete | write | tasks | Complete a task. |
| POST | open/v1/task | write | tasks | Create a task. |
| POST | open/v1/task/assign | write | tasks | Assign a task to a project member. |
| POST | open/v1/task/batch | write | tasks | Batch create or update tasks. |
| POST | open/v1/task/completeTasks | write | tasks | Complete multiple tasks. |
| POST | open/v1/task/completed | read | tasks | List completed tasks by project and time range. |
| POST | open/v1/task/filter | read | tasks | Filter tasks by project, dates, priority, tags, kind and status. |
| POST | open/v1/task/move | write | tasks | Move tasks between projects. |
| POST | open/v1/task/search | read | tasks | Search tasks by keywords and filters. |
| POST | open/v1/task/unassign | write | tasks | Unassign a task. |
| POST | open/v1/task/undone | read | tasks | List undone tasks within a date range. |
| POST | open/v1/task/{id} | write | tasks | Update a task. |
