# Gotchas

## Table of contents

- [Opaque IDs](#opaque-ids)
- [Search first, then write](#search-first-then-write)
- [Archived objects](#archived-objects)
- [Pagination and bounded output](#pagination-and-bounded-output)
- [Retry behaviour](#retry-behaviour)
- [Bulk safety](#bulk-safety)
- [Legacy naming in sync](#legacy-naming-in-sync)
- [Template and upload gaps](#template-and-upload-gaps)
- [Task and project deep links](#task-and-project-deep-links)
- [Plan-gated features](#plan-gated-features)

## Opaque IDs

Todoist IDs are opaque strings in API v1. Do not assume integers or sortable sequences.

What to do:

- keep IDs as strings
- do not coerce to integers
- use `ids-map` when migrating from older stored IDs
- prefer `resolve-*` commands when starting from names

## Search first, then write

Names are not stable IDs.

Safe pattern:

1. resolve or search the object
2. inspect the current object
3. preview the change
4. execute the change
5. verify

This matters most for:

- shared projects
- sections with repeated names across projects
- labels that may exist as personal or shared labels

## Archived objects

Archived projects and sections usually need explicit inclusion during resolution.

Examples:

```bash
python3 scripts/todoist_api.py resolve-project --name "Archive" --include-archived
python3 scripts/todoist_api.py resolve-section --project-name "Old Client" --name "Done" --include-archived
```

## Pagination and bounded output

Many Todoist endpoints are cursor-paginated.

Use:

- `--limit` for page size
- `--cursor` for the next page
- `--all` to drain the cursor chain
- `--max-items` to stop early
- `--output FILE` for very large payloads

If you only need a quick answer, prefer a small first page before loading everything.

## Retry behaviour

The CLI retries transient failures by default.

Built-in defaults:

- retry on `429`, `500`, `502`, `503`, `504`
- honour `Retry-After` / `error_extra.retry_after` when available
- exponential backoff from `--retry-backoff`

Tune when needed:

```bash
python3 scripts/todoist_api.py get-projects --retry 4 --retry-backoff 2
```

## Bulk safety

Bulk commands are designed for agents, not manual shell heroics.

Rules:

- `bulk-close-tasks`, `bulk-move-tasks`, and `bulk-comment-tasks` require `--dry-run` or `--confirm`
- they return counts and explicit change lists
- they skip tasks already at the destination in `bulk-move-tasks`
- they do not guess ambiguous names

## Legacy naming in sync

Todoist API v1 uses current names in top-level REST endpoints, but `/sync` still carries some legacy object names.

Examples you will still see in sync payloads:

- `items` where REST uses `tasks`
- `notes` where REST uses `comments`

If a task is small and single-purpose, prefer the modern REST wrapper. Use `sync` only when batching or incremental sync is the real goal.

## Template and upload gaps

The main wrapper intentionally avoids full multipart upload support.

Use `raw` or `curl` for:

- file uploads
- attachment workflows
- template import from file
- template export as file download

This keeps the main agent surface deterministic and non-fragile.

## Task and project deep links

The script adds `todoist://task?id=...` links to task objects where practical and `todoist://project?id=...` links to project objects where practical. These are useful when the next step is “open this object in Todoist”.

## Plan-gated features

Some Todoist API capabilities depend on the authenticated user’s plan or token scopes.

Watch for this especially around:

- reminders and other premium features
- backups
- uploads and upload limits
- template import/export availability in the user plan
