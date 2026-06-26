---
name: vibe-kanban-mcp
description: Operate the local Vibe Kanban (vibe-kanban) instance through the `vibe_kanban` MCP server using `mcporter`: list orgs/projects/issues/workspaces, create/update issues (e.g., bulk “5 tasks in To do”), and start/link workspace sessions to issues. Also troubleshoot the local dashboard by finding the current listening port(s) on macOS (lsof/netstat) and verifying HTTP responses.
---

# Vibe Kanban MCP

Source repo: https://github.com/DevBD1/openclaw-skill-vibe-kanban-mcp

## Prereqs / setup check

You need all three:

1) **mcporter** installed and on PATH
2) **vibe-kanban** installed and running locally (dashboard + MCP)
3) An mcporter config entry named **`vibe_kanban`** (so `mcporter call vibe_kanban.*` works)

Quick checks:

```bash
command -v mcporter
mcporter config get vibe_kanban --json
mcporter list vibe_kanban --schema
```

If `vibe_kanban` is missing, add it as a stdio server (example):

```bash
mcporter config add vibe_kanban --command npx --arg -y --arg vibe-kanban@latest --arg --mcp
```

If the dashboard is running but you don’t know the port(s):

```bash
ps aux | rg -i 'vibe[- ]kanban'
/usr/sbin/lsof -nP -p <pid> -a -iTCP -sTCP:LISTEN
```

Notes:
- `jq` is helpful for scripting (`jq -r .issue_id`) but not required.

## Quick start (mcporter)

```bash
mcporter config get vibe_kanban --json
mcporter list vibe_kanban --schema
mcporter call vibe_kanban.list_organizations --args '{}' --output json
```

Notes:
- `vibe_kanban` is typically **stdio** (e.g., `npx -y vibe-kanban@latest --mcp`). The **web dashboard** listens on separate local ports.
- Prefer `--output json` for calls you will parse.

## Common workflows

### List orgs → projects → issues

```bash
# orgs
mcporter call vibe_kanban.list_organizations --args '{}' --output json

# projects in an org
mcporter call vibe_kanban.list_projects --args '{"organization_id":"<org_uuid>"}' --output json

# issues in a project
mcporter call vibe_kanban.list_issues --args '{"project_id":"<project_uuid>","limit":50,"offset":0}' --output json
```

### Create an issue and put it in “To do”

`create_issue` returns `issue_id`. Then set the workflow state with `update_issue`.

```bash
ISSUE_ID=$(mcporter call vibe_kanban.create_issue \
  --args '{"project_id":"<project_uuid>","title":"My task","description":"Details","priority":"high"}' \
  --output json | jq -r .issue_id)

mcporter call vibe_kanban.update_issue \
  --args "{\"issue_id\":\"$ISSUE_ID\",\"status\":\"To do\"}" \
  --output json
```

Bulk-create 5 tasks quickly:

```bash
for t in "Task 1" "Task 2" "Task 3" "Task 4" "Task 5"; do
  ISSUE_ID=$(mcporter call vibe_kanban.create_issue \
    --args "{\"project_id\":\"<project_uuid>\",\"title\":\"$t\"}" \
    --output json | jq -r .issue_id)
  mcporter call vibe_kanban.update_issue \
    --args "{\"issue_id\":\"$ISSUE_ID\",\"status\":\"To do\"}" \
    --output json >/dev/null
done
```

### Start a workspace session linked to an issue

Get repo IDs (for `repos: [{repo_id, base_branch}]`):

```bash
mcporter call vibe_kanban.list_repos --args '{}' --output json
```

Start a workspace session and link it at creation using `issue_id`:

```bash
mcporter call vibe_kanban.start_workspace_session --args '{
  "title": "ISS-123 My task",
  "executor": "CODEX",
  "repos": [{"repo_id":"<repo_uuid>","base_branch":"main"}],
  "issue_id": "<issue_uuid>"
}' --output json
```

If you already have both IDs, link later:

```bash
mcporter call vibe_kanban.link_workspace \
  --args '{"workspace_id":"<workspace_uuid>","issue_id":"<issue_uuid>"}' \
  --output json
```

### Find the local vibe-kanban dashboard port (macOS)

The port is ephemeral. Find it from the process:

```bash
ps aux | rg -i 'vibe[- ]kanban'
# then
/usr/sbin/lsof -nP -p <pid> -a -iTCP -sTCP:LISTEN
```

Verify which port is the actual UI:

```bash
curl -sS -D - http://127.0.0.1:<port>/ -o /dev/null | head
```

Pitfall:
- You may see **two** listening ports; one can return `502 Bad Gateway` with a “Dev server unreachable …” message.
- `lsof`/`netstat` might not be on PATH; use `/usr/sbin/lsof` and `/usr/sbin/netstat`.
