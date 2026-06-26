# Reference

## Table of contents

- [Command families](#command-families)
- [Global flags](#global-flags)
- [Result envelope](#result-envelope)
- [Name-resolution commands](#name-resolution-commands)
- [Ensure commands](#ensure-commands)
- [Bulk commands](#bulk-commands)
- [Low-level wrappers](#low-level-wrappers)
- [Escape hatches](#escape-hatches)
- [Coverage notes](#coverage-notes)
- [Quick grep targets](#quick-grep-targets)

## Command families

### Read/list/search

- `get-projects`
- `get-archived-projects`
- `search-projects`
- `get-project`
- `get-project-collaborators`
- `get-project-full`
- `get-sections`
- `get-archived-sections`
- `search-sections`
- `get-section`
- `get-labels`
- `get-shared-labels`
- `search-labels`
- `get-label`
- `get-tasks`
- `get-tasks-by-filter`
- `get-task`
- `get-completed-tasks`
- `get-completed-stats`
- `get-comments`
- `get-comment`
- `get-activities`
- `ids-map`
- `get-backups`
- `template-export-url`

### Write one object

- `create-project`
- `update-project`
- `delete-project`
- `archive-project`
- `unarchive-project`
- `create-section`
- `update-section`
- `delete-section`
- `archive-section`
- `unarchive-section`
- `create-label`
- `update-label`
- `delete-label`
- `quick-add-task`
- `create-task`
- `update-task`
- `move-task`
- `close-task`
- `reopen-task`
- `delete-task`
- `create-comment`
- `update-comment`
- `delete-comment`
- `get-or-create-email`
- `disable-email`

### Agent-friendly helpers

- `resolve-project`
- `resolve-section`
- `resolve-label`
- `ensure-project`
- `ensure-section`
- `ensure-label`
- `bulk-close-tasks`
- `bulk-move-tasks`
- `bulk-comment-tasks`
- `report-completed`

### Escape hatches

- `sync`
- `raw`

## Global flags

Available on the main script:

- `--token` — explicit Todoist token
- `--base-url` — override API base URL
- `--timeout` — request timeout
- `--retry` — retries for 429/5xx/network failures
- `--retry-backoff` — initial backoff in seconds
- `--format json|summary`
- `--output FILE|-`
- `--verbose`

For paginated commands:

- `--limit`
- `--cursor`
- `--all`
- `--max-items`

For write commands:

- `--dry-run`
- `--confirm` for bulk and destructive operations

## Result envelope

Default output is a stable JSON envelope.

Typical read:

```json
{
  "ok": true,
  "action": "get-projects",
  "dry_run": false,
  "count": 3,
  "next_cursor": null,
  "data": {
    "results": [
      {"id": "abc", "name": "Inbox"},
      {"id": "def", "name": "Work"}
    ],
    "next_cursor": null
  }
}
```

Typical resolver:

```json
{
  "ok": true,
  "action": "resolve-section",
  "dry_run": false,
  "data": {
    "id": "6fFPHV272WWh3gpW",
    "project_id": "6XGgm6PHrGgMpCFX",
    "name": "Next Actions"
  }
}
```

Typical bulk preview:

```json
{
  "ok": true,
  "action": "bulk-move-tasks",
  "dry_run": true,
  "matched_count": 5,
  "changed_count": 4,
  "skipped_count": 1,
  "resolved": {
    "filter": "#Inbox & !recurring",
    "project_id": "6XGgm6PHrGgMpCFX",
    "section_id": "6fFPHV272WWh3gpW"
  },
  "data": [
    {
      "task_id": "6XGgmFVcrG5RRjVr",
      "from_project_id": "old-project",
      "to_project_id": "6XGgm6PHrGgMpCFX",
      "to_section_id": "6fFPHV272WWh3gpW"
    }
  ]
}
```

## Name-resolution commands

These commands are the safest way to bridge from user language to Todoist IDs.

### Resolve a project

```bash
python3 scripts/todoist_api.py resolve-project --name "Inbox"
python3 scripts/todoist_api.py resolve-project --name "Archive" --include-archived
python3 scripts/todoist_api.py resolve-project --name "Client Alpha" --strict
```

### Resolve a section within a project scope

```bash
python3 scripts/todoist_api.py resolve-section \
  --project-name "Client Alpha" \
  --name "Next Actions"
```

### Resolve a shared label too

```bash
python3 scripts/todoist_api.py resolve-label \
  --name "blocked" \
  --include-shared
```

Resolution rules:

1. exact case-insensitive name
2. if `--strict` is absent, unique prefix match
3. if still unresolved, unique substring match
4. otherwise fail loudly with candidate details

## Ensure commands

These commands are useful for idempotent agents.

### Ensure a project exists

```bash
python3 scripts/todoist_api.py ensure-project --name "Client Alpha"
```

### Ensure a project and patch a few fields if it already exists

```bash
python3 scripts/todoist_api.py ensure-project \
  --name "Client Alpha" \
  --description "Delivery work" \
  --color blue \
  --update-existing \
  --dry-run
```

### Ensure a section within a resolved project

```bash
python3 scripts/todoist_api.py ensure-section \
  --project-name "Client Alpha" \
  --name "Waiting" \
  --update-existing \
  --dry-run
```

### Ensure a label exists

```bash
python3 scripts/todoist_api.py ensure-label \
  --name "waiting-on" \
  --color berry_red
```

## Bulk commands

### Close all matching tasks

```bash
python3 scripts/todoist_api.py bulk-close-tasks \
  --filter "overdue & @errands" \
  --dry-run
```

### Move all matching tasks

```bash
python3 scripts/todoist_api.py bulk-move-tasks \
  --filter "#Inbox & !recurring" \
  --target-project-name "Work" \
  --target-section-name "Next Actions" \
  --dry-run
```

### Add the same comment to all matching tasks

```bash
python3 scripts/todoist_api.py bulk-comment-tasks \
  --filter "today & p1" \
  --content "Reviewed during morning triage." \
  --dry-run
```

Bulk commands are intentionally conservative:

- they always require `--dry-run` or `--confirm`
- they respect `--max-items`
- they return `matched_count`, `changed_count`, `skipped_count`
- they fail name resolution instead of guessing

## Low-level wrappers

### Projects

```bash
python3 scripts/todoist_api.py get-projects --all
python3 scripts/todoist_api.py get-project --project-id PROJECT_ID
python3 scripts/todoist_api.py get-project-full --project-id PROJECT_ID --output project-full.json
python3 scripts/todoist_api.py archive-project --project-id PROJECT_ID --dry-run
```

### Sections

```bash
python3 scripts/todoist_api.py get-sections --project-id PROJECT_ID --all
python3 scripts/todoist_api.py update-section --section-id SECTION_ID --name "Later" --dry-run
```

### Labels

```bash
python3 scripts/todoist_api.py get-labels --all
python3 scripts/todoist_api.py get-shared-labels
python3 scripts/todoist_api.py update-label --label-id LABEL_ID --color blue --dry-run
```

### Tasks

```bash
python3 scripts/todoist_api.py get-tasks --project-id PROJECT_ID --all
python3 scripts/todoist_api.py get-tasks-by-filter --query "today & !recurring" --lang en --all
python3 scripts/todoist_api.py quick-add-task --text "Email Jess tomorrow 09:00 #Personal"
python3 scripts/todoist_api.py update-task --task-id TASK_ID --priority 1 --dry-run
python3 scripts/todoist_api.py move-task --task-id TASK_ID --section-id SECTION_ID --dry-run
```

### Comments

```bash
python3 scripts/todoist_api.py get-comments --task-id TASK_ID --all
python3 scripts/todoist_api.py create-comment --task-id TASK_ID --content "Waiting on review" --dry-run
```

### Reporting and utilities

```bash
python3 scripts/todoist_api.py report-completed \
  --since "2026-03-01T00:00:00Z" \
  --until "2026-03-31T23:59:59Z"

python3 scripts/todoist_api.py get-activities --parent-project-id PROJECT_ID --all
python3 scripts/todoist_api.py ids-map --object-name tasks --ids 918273645,918273646
python3 scripts/todoist_api.py get-or-create-email --obj-type task --obj-id TASK_ID --dry-run
python3 scripts/todoist_api.py template-export-url --project-id PROJECT_ID
```

## Escape hatches

### `sync`

Use this when the work is inherently batched or when you need incremental sync:

```bash
python3 scripts/todoist_api.py sync \
  --sync-token '*' \
  --resource-types '["all"]'
```

Preview sync commands:

```bash
python3 scripts/todoist_api.py sync \
  --commands-file assets/sync/seed-project.json \
  --dry-run
```

### `raw`

Use this for niche endpoints or temporary gaps in the wrapper:

```bash
python3 scripts/todoist_api.py raw \
  --method GET \
  --path /projects/PROJECT_ID/full
```

```bash
python3 scripts/todoist_api.py raw \
  --method GET \
  --path /activities \
  --query parent_project_id=PROJECT_ID \
  --all
```

## Coverage notes

Wrapped directly in V2:

- projects, archived projects, collaborators, project full
- sections, archived sections
- labels and shared labels
- tasks, task filter, quick add, move, close, reopen, completed tasks, completed stats
- comments
- activities
- ID mapping
- backups list
- task/project email creation and disable
- template export URL
- sync/raw escape hatches
- name resolution, ensure, bulk close/move/comment, completed report

Still best handled with `raw` or `curl`:

- multipart uploads
- template import from file
- template export as file download
- attachment upload and comment attachment wiring
- any very new endpoint not yet exposed by the CLI

## Quick grep targets

Useful search terms for this reference set:

```bash
grep -n "bulk-" references/REFERENCE.md
grep -n "ensure-" references/REFERENCE.md
grep -n "completed" references/REFERENCE.md
grep -n "ids-map" references/REFERENCE.md
grep -n "template" references/REFERENCE.md
```
