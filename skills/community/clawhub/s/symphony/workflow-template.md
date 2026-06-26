# WORKFLOW.md Template for Symphony

Use this as a starting contract for repository-owned orchestration policy.

```md
---
tracker:
  kind: linear
  project_slug: your-project-slug
  api_key: $LINEAR_API_KEY
  active_states:
    - Todo
    - In Progress
  terminal_states:
    - Done
    - Closed
    - Cancelled
polling:
  interval_ms: 30000
workspace:
  root: ~/code/symphony-workspaces
hooks:
  after_create: |
    git clone --depth 1 "$SOURCE_REPO_URL" .
agent:
  max_concurrent_agents: 3
  max_retry_backoff_ms: 300000
codex:
  command: codex app-server
  approval_policy: on-request
  thread_sandbox: workspace-write
  turn_sandbox_policy:
    type: workspaceWrite
---

You are working on Linear issue {{ issue.identifier }}.

Title: {{ issue.title }}
State: {{ issue.state }}
Description:
{{ issue.description }}
```

## Template Rules

- Keep front matter as a top-level object with known keys (`tracker`, `polling`, `workspace`, `hooks`, `agent`, `codex`).
- Keep prompt variables strict and valid; unknown variables should fail rendering.
- Keep the prompt explicit about stop conditions, validation bar, and handoff state.
- Keep hook scripts short, deterministic, and workspace-scoped.

## Recommended Additions

- Add `codex.turn_timeout_ms` and `codex.stall_timeout_ms` for long-running tasks.
- Add `hooks.before_run` for dependency checks and fast-fail gating.
- Add `hooks.before_remove` if cleanup requires custom teardown.
- Add optional `server.port` if you need the HTTP dashboard and API endpoints.

## Validation Commands

```bash
# Confirm workflow file exists and has front matter
test -f WORKFLOW.md
grep -n "^tracker:\\|^agent:\\|^codex:" WORKFLOW.md

# Confirm Linear token is available
test -n "$LINEAR_API_KEY"

# Confirm Codex and Git credentials are available
test -n "$OPENAI_API_KEY" || codex auth whoami >/dev/null 2>&1
git ls-remote "$SOURCE_REPO_URL" >/dev/null
```
