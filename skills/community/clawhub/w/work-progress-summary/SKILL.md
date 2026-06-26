---
name: work_report_summary
description: Record daily work items in a local SQLite database, replace a day's report when the user wants to correct it, edit or delete one logged task by entry id, track entry history, inspect the historical changes for a specific report date, and retrieve daily or weekly progress summaries. Use when the user asks Codex to log completed work for a day, modify an existing daily report, update or delete a single logged task, inspect version history, inspect date-level history, look up what they worked on on a specific date, or summarize progress for the current or requested week.
---

# Work Report Summary

## Overview

Persist work logs in SQLite instead of ad hoc notes so the same history can be
queried later for exact daily or weekly summaries.

## Workflow

1. Resolve the date as an explicit `YYYY-MM-DD` value before writing or reading.
2. Resolve the database target.
   Use `default` unless the user asks for a separate database.
   Persist to `~/.work_report_summary/<db_name>.db` unless the user explicitly
   asks for another path.
3. Convert each work item into one JSON array element.
   Use `task` as required.
   Use `status` only when the user indicates `done`, `in_progress`, or
   `blocked`.
   Use `details` for brief outcome or blocker context.
4. Run the runtime script:
   - `record` to append entries for a day
   - `replace-day` to overwrite one day's report with the corrected full set
   - `update-entry` to revise one existing task by `entry id`
   - `delete-entry` to remove one existing task by `entry id`
   - `entry-history` to inspect all saved versions for one `entry id`
   - `day-history` to inspect all saved changes associated with one work date
   - `day-report` to inspect one day
   - `week-report` to inspect the Monday-Sunday week for an anchor date
5. Read the JSON output and answer in the user's language.
6. Stop and surface the error if the command fails. Do not invent missing data.

## Recording Rules

- Split multiple tasks into separate items before calling `record`.
- Default `status` to `done` when the user simply says they finished something.
- Preserve short evidence in `details` when the user mentions outcome, link, or
  blocker context.
- Run one `record` command per date when the user gives updates for multiple
  days.
- Use `replace-day` when the user says they want to revise, correct, overwrite,
  or redo an existing daily report.
- Treat `replace-day` as a full replacement for that date, not a partial merge.
- Use `update-entry` when the user wants to correct just one logged task while
  leaving the rest of the day unchanged.
- Resolve the target `entry id` from `day-report` or `week-report` before
  calling `update-entry`.
- Use `delete-entry` when the user wants to remove one mistaken task while
  leaving the rest of the day unchanged.
- Use `entry-history` when the user asks what changed, wants an audit trail, or
  needs to inspect versions after an update or deletion.
- Use `day-history` when the user asks how a day's report changed over time, or
  wants to review all historical edits related to one report date.

## Reporting Rules

- Use `day-report` for one explicit date.
- Use `week-report` for "this week" or any request anchored to a date inside the
  requested week.
- When the user writes in Chinese, prefer the response shapes in
  `{baseDir}/references/chinese_output.md`.
- Mention the exact date or week range in the final answer.
- State that a day has no recorded entries when the database is empty for that
  day.

## References

- Read `{baseDir}/references/commands.md` for CLI arguments, payload shape,
  environment variables, and output fields.
- Read `{baseDir}/references/chat_reference.md` for example user prompts and
  command selection patterns.
- Read `{baseDir}/references/chinese_output.md` for concise Chinese response
  templates for record confirmations, single-entry updates, deletions, history
  queries, date-history queries, report corrections, daily queries, and weekly
  summaries.
