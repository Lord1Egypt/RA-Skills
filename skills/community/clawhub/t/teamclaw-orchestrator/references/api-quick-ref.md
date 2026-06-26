# TeamClaw API Quick Reference

## Controller URL

Default: `http://127.0.0.1:9527`

## Endpoints

### Health & Status

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Health check → `{"status":"ok"}` |
| GET | `/api/v1/team/status` | Full team snapshot (workers, tasks, runs, clarifications) |
| GET | `/api/v1/roles` | List all available roles |

### Controller Orchestration

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/controller/intake` | Submit requirement → auto-decompose into tasks |
| GET | `/api/v1/controller/runs` | List orchestration runs |

**Intake request:**
```json
{ "message": "Build a REST API for user management" }
```

**Intake response:**
```json
{
  "controllerRun": { "id": "run-abc", "status": "completed", "source": "intake" },
  "result": "Orchestration output text..."
}
```

### Tasks

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/tasks` | Create task |
| GET | `/api/v1/tasks` | List all tasks |
| GET | `/api/v1/tasks/:id` | Get task detail |
| GET | `/api/v1/tasks/:id/execution` | Get task with execution events |
| PATCH | `/api/v1/tasks/:id` | Update task (status, priority, progress) |
| POST | `/api/v1/tasks/:id/assign` | Assign to worker/role |
| POST | `/api/v1/tasks/:id/handoff` | Hand off to another role |
| POST | `/api/v1/tasks/:id/result` | Submit result |

**Create task:**
```json
{
  "title": "Implement login form",
  "description": "Email/password login with validation",
  "priority": "high",
  "assignedRole": "developer"
}
```

**Task statuses:** `pending` → `assigned` → `in-progress` → `completed` | `failed` | `blocked`

**Priorities:** `low`, `medium`, `high`

**Roles:** `pm`, `architect`, `developer`, `qa`, `release-engineer`, `infra-engineer`, `devops`, `security-engineer`, `designer`, `marketing`

### Workers

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/workers` | List workers |
| POST | `/api/v1/workers/register` | Register worker |
| POST | `/api/v1/workers/:id/heartbeat` | Heartbeat |
| DELETE | `/api/v1/workers/:id` | Remove worker |

**Worker statuses:** `idle`, `busy`, `offline`

**Transport types:** `http` (remote), `local` (child process), `in-process` (subagent)

### Messages

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/messages/direct` | Send to specific role |
| POST | `/api/v1/messages/broadcast` | Send to all workers |
| POST | `/api/v1/messages/review-request` | Request review from role |
| GET | `/api/v1/messages` | List messages (query: `limit`, `offset`) |

**Direct message:**
```json
{ "from": "user", "toRole": "developer", "content": "Add input validation" }
```

### Clarifications

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/clarifications` | List all (includes `pendingCount`) |
| POST | `/api/v1/clarifications` | Request clarification |
| POST | `/api/v1/clarifications/:id/answer` | Answer clarification |

**Answer:**
```json
{ "answer": "Use PostgreSQL for the database", "answeredBy": "user" }
```

### Workspace

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/workspace/tree` | Directory tree |
| GET | `/api/v1/workspace/file?path=<path>` | File content |

### Web UI

| Path | Description |
|------|-------------|
| `/ui` | TeamClaw dashboard |
