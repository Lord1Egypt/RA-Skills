---
name: sync-data-notion
description: >
  Use when (1) user says 'Sync data to Notion database'. (2) user provides a CSV or JSON file and asks to sync it into a Notion database. (3) user wants to keep a Notion database in sync with an external data source on a recurring basis.
license: MIT
metadata:
  version: "1.0.1"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

## Core Position

This skill handles **bidirectional data synchronization** between external sources (CSV, JSON, REST API) and a target Notion database. It is NOT a one-shot import — it manages consistency, conflict detection, incremental updates, and partial failure handling.

Key responsibilities:
- Authenticate with Notion API using `NOTION_API_KEY` environment variable (never hardcode tokens)
- Map external field names to Notion database property names (title, rich_text, number, checkbox, select, multi_select, date, url, email, phone_number)
- Use Notion database schema (retrieved via `GET /databases/{id}`) to validate property types before writing
- Handle partial failures: sync what's possible, report what failed with per-record reasons
- Preserve the external record ID as a Notion property for traceability across syncs

## Modes

### `/sync-data-notion --full`
**Full sync mode.** Retrieves all records from the external source, compares with all existing Notion records (by ID or configured key field), and creates/updates as needed.

When to use: Initial sync, or when you suspect records have been modified outside the sync relationship.

### `/sync-data-notion --incremental`
**Incremental sync.** Only syncs records where `updated_at` (or configured timestamp field) is newer than the last sync timestamp stored in `~/.sync_notion_last_run/{database_id}.json`.

When to use: Recurring scheduled syncs. Requires `--last-run` to be set or a previous run timestamp to exist.

### `/sync-data-notion --dry-run`
**Preview mode.** Shows exactly what would change — new records, updated records, deleted records — without making any API calls that modify data.

When to use: Before a live sync, to let the user review and approve changes.

### `/sync-data-notion --reverse`
**Notion → External export.** Reads records from a Notion database and writes them to the external system. Requires `--target` to specify the destination format (CSV/JSON/REST endpoint).

When to use: When the external system is the primary store and Notion is used for review/editing.

## Execution Steps

1. **Parse and validate external input**

Read the provided data source:
- **CSV**: Use `csv.DictReader`, validate headers against the Notion database schema
- **JSON**: Parse to list of dicts; validate each record has required fields
- **REST API**: Call the endpoint with auth header from env, paginate if response has `next_cursor`

If malformed, stop and report:
```
Sync input is malformed at row {N}: missing required field "{field}".
Expected: {field_type} (from Notion database schema).
Received: {actual_value} (type {actual_type}).
```

2. **Retrieve Notion database schema**

```
GET https://api.notion.com/v1/databases/{database_id}
Authorization: Bearer {NOTION_API_KEY}
Notion-Version: 2022-06-28
```

Parse `properties` to build a schema map:
- `title` → write via `title` array (required)
- `rich_text` → write via `rich_text` array of text objects
- `number` → write via `number` (must be float or null, not string)
- `checkbox` → write via `boolean`
- `select` → write via `select` object `{name: value}`
- `multi_select` → write via `multi_select` array of `{name: value}` objects
- `date` → write via `date` object `{start: ISO8601}`
- `url` → write via `url` string
- `email` → write via `email` string
- `phone_number` → write via `phone_number` string

If a Notion property type is not supported (e.g., `formula`, `relation`, `rollup`), skip that property and log a warning.

3. **Build field mapping table**

Map source fields to Notion properties. Show the user a table before proceeding:

```
Source field      →  Notion property     →  Type
─────────────────────────────────────────────────
email             →  Email               →  email
name              →  Title               →  title
status            →  Status               →  select
tags              →  Tags                 →  multi_select
created_at        →  Created Date         →  date
```

If a required Notion property has no mapping:
- If `title`: stop — "Missing required title field in source data"
- If other required: log warning and set to `null`

4. **Query existing Notion records**

```
POST https://api.notion.com/v1/databases/{database_id}/query
{
  "page_size": 100,
  "start_cursor": "..."  // paginate through all pages
}
```

Build a lookup map: `{external_id or configured key field → Notion page_id}` for change detection.

5. **Create or update records**

**Create new record:**
```
POST https://api.notion.com/v1/pages
{
  "parent": {"database_id": "{database_id}"},
  "properties": { /* mapped properties */ }
}
```

**Update existing record:**
```
PATCH https://api.notion.com/v1/pages/{page_id}
{
  "properties": { /* mapped properties */ }
}
```

Use bulk endpoints where available (up to 10 pages per batch for creates via `POST /v1/pages` with individual objects in `children` — actually Notion API only supports 1 page per request, so serialize writes).

Track per-record outcomes:
- `created_count`: pages successfully created
- `updated_count`: pages successfully updated
- `failed_count`: records that failed with reason
- `skipped_count`: records skipped (no changes detected in incremental sync)

On 429 (rate limit): Wait `Retry-After` header seconds, retry up to 3 times.
On 400 (validation error): Log the specific property error, skip the record.
On 401/403: Stop immediately — "Authentication failed — check NOTION_API_KEY environment variable."

6. **Verify and report**

After sync completes, query a sample of created/updated records to confirm they exist:
```
GET https://api.notion.com/v1/pages/{page_id}
```

If records missing after write, retry up to 2 times, then flag for manual review.

Return structured summary:
```json
{
  "created": 47,
  "updated": 12,
  "failed": 3,
  "skipped": 5,
  "field_mapping": {"email": "Email", "name": "Title", ...},
  "failures": [
    {"record_id": "abc123", "reason": "Invalid email format"},
    {"record_id": "def456", "reason": "Notion property 'Status' does not have option 'Pending'"}
  ]
}
```

## Mandatory Rules

### Do not

- Do not hardcode the Notion API key — read from `os.getenv("NOTION_API_KEY")`
- Do not sync records without first validating the external data schema matches the Notion database properties
- Do not skip records silently — every skip must be reported with a reason in the summary
- Do not perform full sync without a dry-run option — always offer `--dry-run` to preview changes
- Do not overwrite existing records unless the field values have actually changed (compare all fields)
- Do not sync to a production Notion database without confirming with the user first (unless `--auto-approve` is set)
- Do not assume all Notion property types are writable — `formula`, `relation`, `rollup`, `file`, `verified` are read-only in Notion API

### Do

- Log every sync operation with timestamp, record counts, and outcome
- Show the field mapping table (Step 3) before making any changes
- Handle rate limiting (429) with exponential backoff — pause 1s, 2s, 4s between retries, up to 3 attempts
- State clearly when a sync is partial (some records failed) vs complete (0 failures)
- Preserve the external record ID in a Notion property (e.g., `external_id`) for traceability
- Store the last successful sync timestamp in `~/.sync_notion_last_run/{database_id}.json` for incremental syncs
- On validation errors, report the specific Notion property name and the invalid value

## Quality Bar

| Criterion | Minimum | Ideal |
|-----------|---------|-------|
| Records synced | 100% of valid input records | 100% including edge cases (nulls, special chars, multi-line text) |
| Field mapping coverage | 100% — every source field mapped | Documented + user-confirmed mapping before sync |
| Failures reported | 100% with per-record reason | Root cause + suggested fix per failure |
| Dry-run accuracy | Preview shows exact creates/updates | Zero unexpected changes in live sync |
| Authentication | Uses env vars, no tokens in code | Token auto-refresh on 401 with re-auth flow |
| Rate limit handling | 429 caught, 3 retries with backoff | Adaptive backoff based on Retry-After header |
| Property type validation | Validates before write | Schema validated at sync start, not per-record |

Every sync execution must return a structured JSON summary. A good output is one where all fields are mapped, every failure has a reason, and the field mapping table was shown before changes were made.

## Good vs. Bad Examples

| Scenario | Bad | Good |
|---------|-----|------|
| Missing field | Silently skips row, reports "Sync complete" | Reports "Skipped row 47: required field 'email' missing — Notion title cannot be empty" |
| Auth failure | Retries with same token, fails silently | Stops immediately with "Authentication failed — check NOTION_API_KEY env var is set and valid" |
| Rate limited | Ignores 429, continues, misses records | Pauses 30s (Retry-After), retries 3x, reports "Rate limited at batch 5 — paused 30s, retrying" |
| Partial failure | Reports "Sync complete" with all success | Reports "Sync partial: 47 created, 2 failed (see failures array for details)" |
| Dry-run vs live | No distinction in output format | Dry-run returns same JSON structure with `preview: true` and no page IDs assigned |
| Field mapping | Defaults silently to "field not mapped" | Shows full mapping table with arrow notation `email -> Email (email type)` before sync |
| Multi-select | Converts array to string, stores "tag1,tag2" in select | Maps to `multi_select` array: `[{"name": "tag1"}, {"name": "tag2"}]` |
| Date field | Stores date string as `rich_text` | Sends as `{"date": {"start": "2024-01-15"}}` — ISO8601 format |
| Null handling | Skips field entirely | Sends `null` for optional fields; skips only if field absent from source |