---
tracker:
  kind: linear
  project_slug: your-project-slug
  api_key: $LINEAR_API_KEY
  active_states:
    - Todo
    - In Progress
    - Rework
  terminal_states:
    - Done
    - Closed
    - Cancelled
    - Duplicate
polling:
  interval_ms: 30000
workspace:
  root: ~/code/symphony-workspaces
hooks:
  after_create: |
    git clone --depth 1 "$SOURCE_REPO_URL" .
agent:
  max_concurrent_agents: 2
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
{% if issue.description %}
{{ issue.description }}
{% else %}
No description provided.
{% endif %}

Rules:
1. Work only inside the issue workspace.
2. Continue autonomously unless blocked by missing required auth, permissions, or secrets.
3. Report completed actions and blockers only.
