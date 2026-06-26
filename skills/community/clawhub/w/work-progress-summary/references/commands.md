# Commands

## Storage Resolution

Resolve the database path in this order:

1. Use `--db-path` when it is provided.
2. Otherwise resolve the base directory from `WORK_REPORT_SUMMARY_HOME`.
3. Fall back to `~/.work_report_summary`.
4. Resolve the file name from `--db-name`, then
   `WORK_REPORT_SUMMARY_DB_NAME`, then `default`.
5. Append `.db` if the chosen database name does not already end with `.db`.

Accept database names that match `[A-Za-z0-9._-]+`.
Do not pass path separators inside `--db-name`.

## Item JSON Shape

Pass a JSON array to `--items-json`.

Accept either shorthand strings:

```json
[
  "Finished incident follow-up",
  "Reviewed API contract"
]
```

Or structured objects:

```json
[
  {
    "task": "Reviewed PR 42",
    "status": "blocked",
    "details": "Waiting for QA sign-off"
  },
  {
    "task": "Updated runbook",
    "status": "done"
  }
]
```

Supported statuses:

- `done`
- `in_progress`
- `blocked`

For `record`, the array must be non-empty.
For `replace-day`, the array may be empty when the user wants to clear that
date's report entirely.

## Entry Identification

`day-report` and `week-report` entries include an `id` field.
Use that `id` as `--entry-id` when calling `update-entry`, `delete-entry`, or
`entry-history`.

## Command Shapes

Record work items:

```bash
python {baseDir}/scripts/work_report_summary.py record \
  --date 2026-03-31 \
  --db-name team_alpha \
  --items-json '[{"task":"Closed onboarding checklist"},{"task":"Reviewed PR 42","status":"blocked","details":"Waiting for QA"}]'
```

Replace one day's report:

```bash
python {baseDir}/scripts/work_report_summary.py replace-day \
  --date 2026-03-31 \
  --db-name team_alpha \
  --items-json '[{"task":"Rewrote release notes"},{"task":"Retested login flow","status":"in_progress"}]'
```

Update one specific entry:

```bash
python {baseDir}/scripts/work_report_summary.py update-entry \
  --db-name team_alpha \
  --entry-id 42 \
  --status done \
  --details 'QA sign-off completed'
```

Move one entry to another date:

```bash
python {baseDir}/scripts/work_report_summary.py update-entry \
  --db-name team_alpha \
  --entry-id 42 \
  --new-date 2026-04-01
```

Delete one specific entry:

```bash
python {baseDir}/scripts/work_report_summary.py delete-entry \
  --db-name team_alpha \
  --entry-id 42
```

Read version history for one entry:

```bash
python {baseDir}/scripts/work_report_summary.py entry-history \
  --db-name team_alpha \
  --entry-id 42
```

Read history for one work date:

```bash
python {baseDir}/scripts/work_report_summary.py day-history \
  --db-name team_alpha \
  --date 2026-03-31
```

Clear one day's report by replacing it with an empty list:

```bash
python {baseDir}/scripts/work_report_summary.py replace-day \
  --date 2026-03-31 \
  --db-name team_alpha \
  --items-json '[]'
```

Read one day:

```bash
python {baseDir}/scripts/work_report_summary.py day-report \
  --date 2026-03-31 \
  --db-name team_alpha
```

Read one week:

```bash
python {baseDir}/scripts/work_report_summary.py week-report \
  --date 2026-03-31 \
  --db-name team_alpha
```

Override the full database path:

```bash
python {baseDir}/scripts/work_report_summary.py record \
  --db-path ~/tmp/work/team_alpha.db \
  --items-json '["Closed release checklist"]'
```

## Output Fields

`record` returns:

- `db_path`
- `date`
- `recorded`
- `items`

`replace-day` returns:

- `db_path`
- `date`
- `previous_entry_count`
- `recorded`
- `items`

`update-entry` returns:

- `db_path`
- `entry_id`
- `previous_entry`
- `entry`
- `history_version`

`delete-entry` returns:

- `db_path`
- `entry_id`
- `deleted_entry`
- `history_version`

`entry-history` returns:

- `db_path`
- `entry_id`
- `current_exists`
- `version_count`
- `versions`

`day-history` returns:

- `db_path`
- `date`
- `entry_count`
- `version_count`
- `action_counts`
- `entries`

`day-report` returns:

- `db_path`
- `date`
- `entry_count`
- `status_counts`
- `entries`

Each object in `entries` includes:

- `id`
- `date`
- `task`
- `status`
- `details`
- `created_at`

`week-report` returns:

- `db_path`
- `anchor_date`
- `week_start`
- `week_end`
- `entry_count`
- `status_counts`
- `days`

Each object in `versions` includes:

- `history_id`
- `entry_id`
- `version`
- `action`
- `source_command`
- `date`
- `task`
- `status`
- `details`
- `created_at`
- `changed_at`

Each object in `entries` from `day-history` includes:

- `entry_id`
- `current_exists`
- `current_entry`
- `version_count`
- `action_counts`
- `versions`

## Agent Notes

- Prefer explicit dates over relative words when constructing commands.
- Treat JSON output as the source of truth.
- Report empty results directly instead of guessing unrecorded work.
- When a user asks to fix an already logged day, prefer `replace-day` over
  appending more `record` items.
- When a user asks to fix only one task, prefer `update-entry` after resolving
  the target `entry id`.
- When a user asks to remove only one task, use `delete-entry`.
- When a user asks what changed over time, use `entry-history`.
- When a user asks how one date's report evolved, use `day-history`.
