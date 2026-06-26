---
name: todoist-api
description: >-
  Manages Todoist tasks, projects, sections, labels, comments, completed-task reports,
  activity logs, ID migration, project templates, and sync workflows through Todoist API v1.
  Use when the user asks to capture tasks, quick-add work, triage an inbox, resolve Todoist
  names to IDs, bulk-close or move tasks, add repeated comments, review completed work,
  manage project structure, export templates, or automate Todoist workflows.
license: MIT. See LICENSE.txt
compatibility: Requires HTTPS access to api.todoist.com plus Python 3.9+ or curl. Write operations require a Todoist API token or OAuth access token.
metadata:
  author: OpenAI
  version: "2.0.0"
  todoist_api: "v1"
  last_reviewed: "2026-03-05"
---

# Todoist API

## When to use this skill

Use this skill when work involves **Todoist data or automation**, especially:

- capture or quick-add new tasks
- inspect, filter, move, complete, reopen, or delete tasks
- manage projects, sections, labels, or comments
- resolve human names to Todoist IDs before writing
- perform safer bulk edits with dry-runs
- review completed work or recent activity
- build Todoist scripts, agents, or integrations around the public API

## When not to use this skill

Do **not** use this skill for:

- editing the user’s local Todoist app UI directly
- calendar-specific workflows that belong in a calendar skill
- attachment upload flows that require multipart handling unless you are prepared to use `curl` or the `raw` escape hatch
- non-Todoist task systems

## Safety defaults

- Start **read-only** if the user’s intent is ambiguous.
- Resolve names to IDs before any write.
- Prefer **close** over **delete** unless the user explicitly wants permanent removal.
- Run `--dry-run` first for bulk or destructive work.
- Use `--confirm` for bulk closes, moves, repeated comments, and deletes.
- If a command may return a large payload, set `--output FILE` so stdout stays small and predictable.

## Pick the smallest capable surface

- **One object, one endpoint** → use a low-level REST wrapper such as `get-task`, `update-project`, or `get-comment`.
- **Natural-language capture** → use `quick-add-task`.
- **Resolve names safely** → use `resolve-project`, `resolve-section`, `resolve-label`.
- **Create if missing** → use `ensure-project`, `ensure-section`, `ensure-label`.
- **Many matching tasks** → use `bulk-close-tasks`, `bulk-move-tasks`, `bulk-comment-tasks`.
- **Completed-work review** → use `report-completed` or `get-completed-tasks`.
- **Full or incremental sync / batched writes** → use `sync`.
- **Unwrapped or niche endpoint** → use `raw`.

## Output contract

The main script prints structured output to stdout by default.

- `--format json` returns a stable JSON envelope with fields like `action`, `ok`, `count`, `next_cursor`, `matched_count`, `changed_count`, and `resolved`.
- `--format summary` returns a smaller human-readable summary.
- `--output FILE` writes the full output to a file and prints a small JSON notice to stdout.

This is designed for agent pipelines: stdout stays parseable, stderr carries diagnostics, and retries are built in for transient failures.

## Scripts

- **`scripts/todoist_api.py`** — main non-interactive Todoist CLI
- **`scripts/smoke_test.py`** — read-only connectivity check

Inspect help first:

```bash
python3 scripts/todoist_api.py --help
python3 scripts/todoist_api.py get-tasks-by-filter --help
python3 scripts/todoist_api.py bulk-move-tasks --help
python3 scripts/smoke_test.py --help
```

## Quick start

Set a token:

```bash
export TODOIST_API_TOKEN="YOUR_TODOIST_TOKEN"
```

Read-only smoke test:

```bash
python3 scripts/smoke_test.py
```

Sanity-check access:

```bash
python3 scripts/todoist_api.py get-projects --limit 5
python3 scripts/todoist_api.py get-labels --limit 10
```

Resolve names before writes:

```bash
python3 scripts/todoist_api.py resolve-project --name "Inbox"
python3 scripts/todoist_api.py resolve-section --project-name "Client Alpha" --name "Next Actions"
python3 scripts/todoist_api.py resolve-label --name "waiting-on"
```

## High-value agent workflows

### Quick add

```bash
python3 scripts/todoist_api.py quick-add-task \
  --text "Email Chris tomorrow at 09:00 #Work @follow-up p2"
```

### Create-if-missing section

```bash
python3 scripts/todoist_api.py ensure-section \
  --project-name "Client Alpha" \
  --name "Next Actions"
```

### Preview a bulk close

```bash
python3 scripts/todoist_api.py bulk-close-tasks \
  --filter "overdue & @errands" \
  --dry-run
```

### Execute the same bulk close

```bash
python3 scripts/todoist_api.py bulk-close-tasks \
  --filter "overdue & @errands" \
  --confirm
```

### Move matching tasks into a resolved section

```bash
python3 scripts/todoist_api.py bulk-move-tasks \
  --filter "#Inbox & !recurring" \
  --target-project-name "Work" \
  --target-section-name "Next Actions" \
  --dry-run
```

### Report completed work

```bash
python3 scripts/todoist_api.py report-completed \
  --since "2026-03-01T00:00:00Z" \
  --until "2026-03-31T23:59:59Z" \
  --by completion \
  --output reports/march-completed.json
```

## Recommended operating pattern

1. **Resolve or list** the target object.
2. **Read current state** with a low-level getter.
3. **Preview** the write with `--dry-run`.
4. **Execute** with `--confirm` when needed.
5. **Verify** by re-reading or by running a report command.

## Feature index

- **Command catalogue and endpoint coverage** → [references/REFERENCE.md](references/REFERENCE.md)
- **Task-first recipes** → [references/RECIPES.md](references/RECIPES.md)
- **Todoist-specific caveats** → [references/GOTCHAS.md](references/GOTCHAS.md)

## Escape hatches

Use `raw` when the public CLI surface does not yet wrap a needed endpoint:

```bash
python3 scripts/todoist_api.py raw \
  --method GET \
  --path /projects/PROJECT_ID/full
```

Use `sync` when you need incremental sync or batched commands:

```bash
python3 scripts/todoist_api.py sync \
  --sync-token '*' \
  --resource-types '["all"]'
```
