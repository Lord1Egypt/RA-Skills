# Squad Control API Reference

**Base URL:** Set as `SC_API_URL` (e.g. `https://www.squadcontrol.ai`)  
**Auth:** `x-api-key: <SC_API_KEY>` header on all requests.

---

## API Key Scopes

**Workspace-scoped key** — bound to a single workspace. All endpoints return/operate on that workspace only.

**Account-scoped key** — spans all workspaces in your account.
- `/api/tasks/pending` returns tasks from **all workspaces**, each with an embedded `workspace` object
- `/api/tasks/list` returns tasks across all workspaces; use `?workspaceId=<id>` to scope
- All write endpoints work normally with either key type

---

## GET /api/tasks/pending

Returns tasks ready for pickup.

Optional params: `?agentId=<id>`, `?limit=<n>`

**Response (workspace-scoped key):**
```json
{
  "workspace": {
    "_id": "wsId",
    "name": "My Workspace",
    "repoUrl": "https://github.com/org/repo",
    "githubToken": "ghp_xxxx",
    "agentConcurrency": 2
  },
  "tasks": [{
    "_id": "taskId",
    "title": "Add dark mode toggle",
    "description": "...",
    "priority": "medium",
    "tags": ["frontend"],
    "agent": {
      "_id": "agentId",
      "name": "Cody",
      "role": "Developer",
      "model": "anthropic/claude-sonnet-4-6",
      "soulMd": "You are Cody..."
    }
  }]
}
```

**Response (account-scoped key):**
```json
{
  "tasks": [{
    "_id": "taskId",
    "title": "Add dark mode toggle",
    "description": "...",
    "workspace": {
      "_id": "wsId",
      "name": "My Workspace",
      "repoUrl": "https://github.com/org/repo",
      "githubToken": "ghp_xxxx",
      "agentConcurrency": 3
    },
    "agent": {
      "_id": "agentId",
      "name": "Cody",
      "role": "Developer",
      "model": "anthropic/claude-sonnet-4-6",
      "soulMd": "You are Cody..."
    }
  }]
}
```

---

## POST /api/tasks/pickup

Mark a task as in-progress. Call before starting work.

Body:
```json
{ "taskId": "...", "agentId": "...", "branch": "task/<taskId>" }
```

Response:
```json
{
  "success": true,
  "workspace": {
    "repoUrl": "https://github.com/org/repo",
    "githubToken": "ghp_xxxx"
  }
}
```

---

## POST /api/threads/send

Post a message to the task thread. Use for status updates, findings, errors.

Body:
```json
{ "taskId": "...", "agentId": "...", "content": "Starting work on the feature..." }
```

Optional: `?limit=N` and `&after=<lastMessageId>` when fetching thread history for incremental reads.

---

## POST /api/tasks/set-review

Move task to review queue. Use when a PR was created.

Body:
```json
{
  "taskId": "...",
  "agentId": "...",
  "result": "Summary of changes",
  "deliverables": [{ "type": "pr", "name": "PR #42", "url": "https://github.com/..." }]
}
```

---

## POST /api/tasks/complete

Mark task done. Only use when there is NO PR (research, docs-only tasks).

Body:
```json
{
  "taskId": "...",
  "agentId": "...",
  "result": "Summary of what was done",
  "status": "done",
  "deliverables": [{ "type": "file", "name": "report.md", "url": "..." }]
}
```

---

## POST /api/tasks/review

Submit review verdict after examining a PR.

Body:
```json
{
  "taskId": "...",
  "agentId": "...",
  "verdict": "approve",
  "comments": "Looks good. Clean implementation, types pass."
}
```

`verdict`: `"approve"` or `"request_changes"`

---

## POST /api/tasks/fail

Report a task failure. Always call this instead of silently stopping.

Body:
```json
{ "taskId": "...", "agentId": "...", "error": "tsc failed with 3 errors in billing.ts" }
```

---

## POST /api/tasks/create

Create a new task programmatically (useful for breaking down work into subtasks).

Body:
```json
{
  "title": "Fix login redirect bug",
  "description": "After OAuth, users land on /dashboard instead of /onboarding",
  "priority": "high",
  "tags": ["bug", "auth"],
  "assignedAgentId": "...",
  "workspaceId": "..."
}
```

---

## GET /api/agents

List all agents in the workspace.

Response:
```json
{
  "agents": [{
    "_id": "...",
    "name": "Cody",
    "role": "Developer",
    "model": "anthropic/claude-sonnet-4-6",
    "soulMd": "..."
  }]
}
```

Reviewer selection order:
1. `SC_REVIEWER_AGENT_ID` env var (explicit override)
2. Exact `role: "Code Reviewer"`
3. Role contains `Reviewer` or name `Hawk`

---

## GET /api/tasks/list

List tasks accessible to this API key.

Optional params:
- `?status=<status>` — filter by status (`pending`, `assigned`, `working`, `review`, `done`, `failed`)
- `?workspaceId=<id>` — scope to one workspace (useful with account-scoped keys)

Response: `{ "tasks": [...] }`

---

## GET /api/workspace

Get workspace details including repo URL.

---

## GET /api/health

Health check, no auth required. Returns `{ "status": "ok" }`.
