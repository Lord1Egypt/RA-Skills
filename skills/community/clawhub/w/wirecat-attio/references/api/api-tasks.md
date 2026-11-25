<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Tasks

## `attio api tasks-create [options]`

- What: Create a task
- Call: `POST /v2/tasks`, effect: write
- Sign-in: oauth2 (task:read-write, object\_configuration:read, record\_permission:read, user\_management:read)
- Body: `PostV2TasksRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api tasks-delete [options]`

- What: Delete a task
- Call: `DELETE /v2/tasks/{task_id}`, effect: destructive
- Sign-in: oauth2 (task:read-write)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--task-id <value>` | yes | task\_id |

## `attio api tasks-get [options]`

- What: Get a task
- Call: `GET /v2/tasks/{task_id}`, effect: read
- Sign-in: oauth2 (task:read, object\_configuration:read, record\_permission:read, user\_management:read)

| Flag | Required | What |
|---|---|---|
| `--task-id <value>` | yes | task\_id |

## `attio api tasks-list [options]`

- What: List tasks
- Call: `GET /v2/tasks`, effect: read
- Sign-in: oauth2 (task:read, object\_configuration:read, record\_permission:read, user\_management:read)
- Pages: offset: send `offset` (query), raised by the items read so far; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | limit |
| `--offset <value>` | no | offset |
| `--sort <value>` | no | sort |
| `--linked-object <value>` | no | linked\_object |
| `--linked-record-id <value>` | no | linked\_record\_id |
| `--assignee <value>` | no | assignee |
| `--is-completed <value>` | no | is\_completed |
| `--all` | no | read every page, as the API pages it |

## `attio api tasks-update [options]`

- What: Update a task
- Call: `PATCH /v2/tasks/{task_id}`, effect: write
- Sign-in: oauth2 (task:read-write, object\_configuration:read, record\_permission:read, user\_management:read)
- Body: `PatchV2TasksByTaskIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--task-id <value>` | yes | task\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
