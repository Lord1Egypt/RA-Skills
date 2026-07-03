# Deep Coding Harness — Project Architecture

## Directory Structure

All paths are relative to your **project root directory** (where `projects-registry.json` and `server.py` live):

```
<project-root>/
├── projects-registry.json          ← All projects overview
├── server.py                       ← Dashboard HTTP server (port 8765)
├── dashboard.html                  ← Dashboard UI
├── requests/                        ← New project requests
│   └── done/                        ← Processed requests
├── logs/                            ← Orchestrator-level logs
├── <project-slug>/                  ← Project directory (e.g., slot-machine/)
│   ├── project-state.json           ← Module states, progress, review history
│   ├── logs/
│   │   ├── orchestrator.log         ← Orchestrator activity
│   │   ├── builder-<module>.log     ← Each Builder writes its own file
│   │   └── reviewer-<module>.log    ← Each Reviewer writes its own file
│   └── <source code>/               ← Generated project files
```

## Project State Format

```json
{
  "name": "Project Name",
  "status": "in_progress | completed | blocked",
  "statistics": {
    "completion_percentage": 0-100,
    "state_distribution": {
      "pending": 0,
      "in_progress": 0,
      "ready_for_review": 0,
      "in_review": 0,
      "needs_revision": 0,
      "accepted": 0
    }
  },
  "modules": [
    {
      "module_id": "module-name",
      "name": "Module Name",
      "description": "What this module does",
      "dependencies": ["dependency-module-id"],
      "state": "pending | in_progress | ready_for_review | in_review | needs_revision | accepted",
      "assigned_to": null,
      "agent_assignments": [],
      "review_history": [
        {
          "iteration": 1,
          "timestamp": "2026-04-07T17:00:00+08:00",
          "status": "passed | needs_revision",
          "summary": "Review summary",
          "checklist": [
            {"criterion": "Criterion name", "passed": true, "detail": "Details"}
          ]
        }
      ],
      "progress": {
        "started_at": null,
        "review_iterations": 0,
        "completed_at": null,
        "accepted_at": null
      }
    }
  ]
}
```

## Module Lifecycle

```
pending → in_progress → ready_for_review → in_review → accepted
                        ↑                    |
                        └── needs_revision ──┘
```

### State Transitions

| From State | Trigger | Action |
|------------|---------|--------|
| `pending` | All dependencies accepted | Set `in_progress` → spawn Builder |
| `in_progress` | Builder completes work | Set `ready_for_review` → spawn Reviewer |
| `ready_for_review` | - | **Immediately spawn Reviewer** → set `in_review` |
| `in_review` | Reviewer completes | Check result: `accepted` or `needs_revision` |
| `needs_revision` | Review feedback | Set `in_progress` → re-spawn Builder with feedback |
| `accepted` | - | No further action, check next module |

### Critical Rules

- **One action per heartbeat cycle**
- **Never leave `ready_for_review` more than one cycle** — spawn Reviewer immediately
- **Reviewer MUST write review result to `review_history` array**
- **E2E smoke test mandatory for bugfixes and new features**
- **DO NOT copy project-state.json to archive/**

## Builder Workflow

1. Spawn via your configured runtime (ACP or subagent)
2. Builder receives task prompt with:
   - Project path and module details
   - Success criteria
   - Files to create/modify
   - Log file path
3. Builder works independently, writes code, tests, docs
4. Builder sets module state to `ready_for_review`
5. Builder appends to `logs/builder-<module>.log`

## Reviewer Workflow

1. Spawn when module is `ready_for_review`
2. Reviewer MUST:
   - Read ALL modified files
   - Actually run/test the application (not just read code)
   - For web projects: serve via HTTP, verify in browser
   - Write detailed review results to `review_history`
3. If all criteria pass → set state to `accepted`
4. If any fail → set state to `needs_revision` with specific feedback
5. Reviewer appends to `logs/reviewer-<module>.log`

## E2E Smoke Test

**Mandatory for bugfixes and new features before delivery:**

1. After module accepted, spawn E2E Reviewer
2. E2E Reviewer:
   - Serves the application via HTTP
   - Opens in browser (Playwright for web projects, if available)
   - Tests the specific fix/feature
   - Confirms no regressions
3. Only after E2E passes → mark project completed

## Dashboard

Dashboard serves at `http://localhost:8765` via `server.py`.

Features:
- Lists all projects with completion status
- Shows per-module states with color coding
- Displays agent activity timeline (merged from per-agent logs)
- Links to project files for direct access
- Auto-refreshes project state

### Server Configuration

- Python 3 HTTP server
- Serves `dashboard.html` at root
- `/api/projects` endpoint returns project list
- `/api/projects/<id>` returns detailed state
- Static file serving for project directories
- PID tracking for graceful shutdown
- **Security**: Binds to `127.0.0.1` only, includes path traversal protection

### Dashboard Display

Projects shown as cards with:
- Project name and status badge
- Completion progress bar
- Module states (colored dots)
- Agent activity timeline
- Quick links to project files

## Agent Communication

- Orchestrator → Builder: via `sessions_spawn` with detailed task prompt
- Builder → Orchestrator: via completion event (push-based)
- Orchestrator → Reviewer: via `sessions_spawn` with review criteria
- Reviewer → Orchestrator: via completion event (push-based)
- Main Agent ↔ Orchestrator: via `sessions_send` to `agent:orchestrator:main`

## Logging Convention

Each agent writes to its own log file (APPEND mode only):

```
logs/orchestrator.log          ← Orchestrator decisions
logs/builder-game-engine.log   ← Builder progress
logs/reviewer-game-engine.log  ← Reviewer findings
```

Timestamp format: ISO 8601 with local timezone

Example: `[2026-04-07T17:00:00+08:00] Started work on module game-engine`
