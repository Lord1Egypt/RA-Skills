# Todoist Orbit API notes

## Scope

This skill intentionally avoids the official Python SDK.
It also uses only the Todoist REST API.

Reasons:
- stdlib-only distribution keeps the skill portable
- the required surface is small enough to implement directly
- async orchestration is still possible with `asyncio.to_thread(...)`

## Endpoint map

### Tasks
- `GET /api/v1/tasks`
- `GET /api/v1/tasks/{id}`
- `POST /api/v1/tasks`
- `POST /api/v1/tasks/{id}`
- `POST /api/v1/tasks/{id}/move`
- `POST /api/v1/tasks/{id}/close`
- `POST /api/v1/tasks/{id}/reopen`
- `DELETE /api/v1/tasks/{id}`

### Projects
- `GET /api/v1/projects`
- `GET /api/v1/projects/{id}`
- `POST /api/v1/projects`
- `POST /api/v1/projects/{id}`
- `POST /api/v1/projects/{id}/archive`
- `POST /api/v1/projects/{id}/unarchive`
- `DELETE /api/v1/projects/{id}`
- `GET /api/v1/projects/search`
- project search: `projects search` now calls the dedicated Todoist project search endpoint; `--exact` still performs a local exact-name pass over the returned results for compatibility

### Sections
- `GET /api/v1/sections`
- `GET /api/v1/sections/{id}`
- `POST /api/v1/sections`
- `POST /api/v1/sections/{id}`
- `POST /api/v1/sections/{id}/archive`
- `POST /api/v1/sections/{id}/unarchive`
- `DELETE /api/v1/sections/{id}`
- section move: no REST endpoint exists; the CLI keeps `sections move` only as a compatibility stub that returns an error

### Labels
- `GET /api/v1/labels`
- `GET /api/v1/labels/{id}`
- `POST /api/v1/labels`
- `POST /api/v1/labels/{id}`
- `DELETE /api/v1/labels/{id}`
- `GET /api/v1/labels/search`
- label search: `labels search` now calls the dedicated Todoist label search endpoint; `--exact` still performs a local exact-name pass over the returned results for compatibility

### Comments and attachments
- `GET /api/v1/comments`
- `POST /api/v1/comments`
- `POST /api/v1/uploads`

## Attachment behavior

Todoist file attachments are represented as attachment objects linked from comments.

Practical pattern:
1. upload the file with `uploads add`
2. create a task comment with `comments add --task-id ... --attachment ./file`

The comment payload uses the attachment object returned by `POST /uploads`.

## CLI behavior

- Output is always JSON
- Errors are emitted as JSON on stderr
- `--pretty` enables indentation
- `resolve` fans out multiple requests concurrently with `asyncio.gather`
- `projects search` and `labels search` call Todoist's search endpoints; add `--exact` to keep only exact-name matches from the API results
- Use `comments add` for short inline text only
- Use `comments add-file` or `comments add-stdin` for long, structured, or multi-line comment bodies

## Caution

- Some Todoist features vary by user plan
- Upload/comment features may fail if the account or workspace plan does not allow them
- Prefer explicit IDs for write operations
- Section moves are not available through Todoist REST, so cross-project section reorganization must be done outside this CLI
- Project and label search commands are server-backed Todoist searches; `--exact` adds a local exact-name filter after the API call
- Keep task content and descriptions short; use comments for logs, transcripts, templates, or other structured notes
- Todoist comments are plain text, so use file/stdin-based comment creation when exact multi-line formatting matters
