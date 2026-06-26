---
name: teamclaw
description: >
  Orchestrate a virtual AI software team to build features, fix bugs, or complete any software task.
  Use when the user wants to delegate work to a multi-role team (developer, architect, QA, etc.),
  check team progress, review task results, or answer worker clarifications.
  Triggers: "build me ...", "create a ...", "team status", "assign to team", "teamclaw",
  "have the team ...", "delegate this to ...", "what are the workers doing".
version: 1.0.0
metadata:
  openclaw:
    author: TeamClaws
    homepage: https://github.com/topcheer/teamclaw
    links:
      homepage: https://github.com/topcheer/teamclaw
      repository: https://github.com/topcheer/teamclaw
      documentation: https://github.com/topcheer/teamclaw/blob/main/README.md
      changelog: https://github.com/topcheer/teamclaw/releases
---

# TeamClaw — AI Team Orchestration

Orchestrate a virtual software team through natural conversation. Submit requirements, monitor progress, review deliverables, and answer clarifications — all without leaving your chat.

## When to Use This Skill

Activate when the user:

- Wants to **build, create, or implement** something (e.g., "build me a todo app", "create an auth system")
- Asks to **delegate work** to a team (e.g., "have the team work on this", "assign this to the developer")
- Wants to check **team status** (e.g., "what are the workers doing?", "show me task progress")
- Needs to **review results** (e.g., "show me what the developer built", "check the QA report")
- Has **pending clarifications** to answer (e.g., "are there questions from the team?")
- Mentions **teamclaw** by name

## Prerequisites

TeamClaw must be running in controller mode. Detect the controller URL:

```bash
# Default controller URL
TEAMCLAW_URL="http://127.0.0.1:9527"

# Health check — verify the controller is running
curl -sf "$TEAMCLAW_URL/api/v1/health"
```

If the health check fails, tell the user to start TeamClaw first (install the `teamclaw-setup` skill for guidance).

## Core Workflow

### 1. Submit a Requirement

When the user describes what they want built, submit it to the controller intake:

```bash
curl -s -X POST "$TEAMCLAW_URL/api/v1/controller/intake" \
  -H "Content-Type: application/json" \
  -d '{"message": "<user requirement here>"}'
```

The controller will:
1. Analyze the requirement
2. Decompose it into tasks for appropriate roles (developer, architect, QA, etc.)
3. Assign tasks to available workers
4. Return a controller run with tracking info

**Response fields:**
- `controllerRun.id` — run identifier for tracking
- `controllerRun.status` — `running`, `completed`, `failed`
- `result` — the controller agent's orchestration output

**Important:** The intake call may take 30-180 seconds as the controller agent plans and decomposes the work. Use `--max-time 300` with curl for large requirements.

### 2. Monitor Progress

#### Check team overview
```bash
curl -s "$TEAMCLAW_URL/api/v1/team/status"
```

Key response fields:
- `workers` — map of all workers with their status (`idle`, `busy`, `offline`)
- `tasks` — map of all tasks with status (`pending`, `assigned`, `in-progress`, `completed`, `failed`)
- `pendingClarificationCount` — number of unanswered questions from workers
- `controllerRuns` — orchestration run history

#### List tasks
```bash
curl -s "$TEAMCLAW_URL/api/v1/tasks"
```

#### Get task details with execution history
```bash
curl -s "$TEAMCLAW_URL/api/v1/tasks/<taskId>/execution"
```

Returns the task with full execution log (lifecycle events, progress updates, errors).

#### List workers
```bash
curl -s "$TEAMCLAW_URL/api/v1/workers"
```

### 3. Review Results

When a task completes, its result contract contains structured deliverables:

```bash
# Get the task to see its resultContract
curl -s "$TEAMCLAW_URL/api/v1/tasks/<taskId>"
```

The `resultContract` includes:
- `summary` — what was accomplished
- `deliverables[]` — list of files, notes, or artifacts produced
- `discoveredPatterns[]` — patterns noticed during execution
- `suggestedNextSteps[]` — recommended follow-up actions

### 4. Handle Clarifications

Workers may need clarification to proceed. Check and answer them:

```bash
# List pending clarifications
curl -s "$TEAMCLAW_URL/api/v1/clarifications"

# Answer a clarification
curl -s -X POST "$TEAMCLAW_URL/api/v1/clarifications/<clarificationId>/answer" \
  -H "Content-Type: application/json" \
  -d '{"answer": "<your answer>", "answeredBy": "user"}'
```

### 5. Create Individual Tasks

For fine-grained control, create tasks directly:

```bash
curl -s -X POST "$TEAMCLAW_URL/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement user login",
    "description": "Create a login form with email/password auth",
    "priority": "high",
    "assignedRole": "developer"
  }'
```

Valid roles: `pm`, `architect`, `developer`, `qa`, `release-engineer`, `infra-engineer`, `devops`, `security-engineer`, `designer`, `marketing`.

Valid priorities: `low`, `medium`, `high`.

### 6. Send Messages to the Team

```bash
# Direct message to a role
curl -s -X POST "$TEAMCLAW_URL/api/v1/messages/direct" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "user",
    "toRole": "developer",
    "content": "Please also add input validation"
  }'

# Broadcast to all workers
curl -s -X POST "$TEAMCLAW_URL/api/v1/messages/broadcast" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "user",
    "content": "Deadline moved up — prioritize core features"
  }'
```

## Response Presentation

When presenting results to the user:

1. **After intake submission**: Summarize what the controller planned — how many tasks, which roles assigned, estimated workflow.

2. **For status checks**: Show a concise table of workers and tasks:
   ```
   Workers: 3 active (developer: busy, qa: idle, architect: idle)
   Tasks: 5 total (2 completed, 1 in-progress, 2 pending)
   Clarifications: 1 pending
   ```

3. **For completed tasks**: Highlight the deliverables, key files changed, and suggested next steps.

4. **For clarifications**: Present the question clearly and ask the user to provide an answer.

## Web UI

TeamClaw also provides a web dashboard for visual monitoring:

```
Open in browser: $TEAMCLAW_URL/ui
```

Mention this to users who prefer a visual overview.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Health check fails | Ensure TeamClaw plugin is enabled in controller mode: `openclaw plugins list` |
| No workers available | Check processModel config; single-process creates workers automatically |
| Intake times out | Increase `taskTimeoutMs` in TeamClaw config; ensure AI model is responsive |
| Task stuck in pending | No idle worker for the assigned role; check `GET /api/v1/workers` |
| Clarification blocking | Answer pending clarifications via `POST /api/v1/clarifications/:id/answer` |

## Read references for detailed API docs

Read `references/api-quick-ref.md` for the complete endpoint reference when you need exact request/response formats.
