---
name: groove-daily-end
description: "End the workday: write memory, analyse tasks, run end hook. Use when wrapping up the day."
license: MIT
allowed-tools: Bash(git:*) Bash(find:*) Read Write Edit Glob AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-daily-end

## Outcome

The workday is wrapped up: git changes are analysed, memory files are written in order, tasks are analysed, and the end hook is executed if present.

## Acceptance Criteria

- Git memory file written at `.groove/memory/git/YYYY-MM-DD-GIT-N.md`
- Daily memory file written at `.groove/memory/daily/YYYY-MM-DD.md`
- Weekly memory file written if today is the last weekday of the week
- Monthly memory file written if today is the last weekday of the month
- Tasks are analysed and summary is included in daily memory

## Constraints

- Read `.groove/index.md` for `tasks.backend` and `git.*` config; memory path is always `.groove/memory/`
- Call `/groove-utilities-task-analyse` to get task summary for daily memory population
- Memory population order (must follow this sequence):
  1. `/groove-utilities-memory-log-git`
  2. `/groove-utilities-memory-log-daily`
  3. `/groove-utilities-memory-log-weekly` (only if last weekday of week, or explicit request)
  4. `/groove-utilities-memory-log-monthly` (only if last weekday of month, or explicit request)
- Last weekday detection: use local calendar date; handle gracefully if run on weekend
- Do NOT modify tasks during end
- **Spec health check**: after all memory steps and before the end hook, check the specs directory at `.groove/memory/specs/`:
  - Glob all `*.md` files in the specs directory (including subdirectories)
  - For each spec file, check if it has been modified in the last 30 days: run `find .groove/memory/specs/ -name "*.md" -mtime +30` — any files returned are stale candidates
  - If stale specs found: report as a brief advisory (do not block):
    ```
    ⚠ Stale spec(s) — not modified in 30+ days:
      - <filename> (last modified: <date>)
      ...
    Consider archiving, updating, or deleting specs that are no longer active.
    ```
  - If no stale specs or specs directory is empty: skip silently
- After the spec health check, prompt for a session rating (optional):
  - Ask: "Rate today's session (1–5) — how well did the compound loop serve you? (press enter to skip)"
  - If the user provides a rating (1–5): append a line to `.groove/memory/learned/signals.md` in format:
    ```
    | YYYY-MM-DD | <rating>/5 | <one-sentence note if user adds one, otherwise blank> |
    ```
    If `signals.md` does not exist, create it first:
    ```markdown
    # Session Signals

    | Date | Rating | Note |
    |---|---|---|
    ```
  - If the user presses enter or provides no rating: skip silently
- After the session rating, prompt for workflow insights (optional):
  - Ask: "Any workflow insights from today to capture in learned memory? Name a topic (e.g. `patterns`, `tools`) or press enter to skip."
  - If the user provides a topic and content: append to `.groove/memory/learned/<topic>.md` under a `## YYYY-MM-DD` heading; create the file with a `# <Topic>` heading if it does not exist; create the dated heading if not already present
  - If the user presses enter or provides no content: skip silently — do not nag
- If today is Friday (last working day of week) or the last weekday of the month: after the workflow insights prompt, print a one-line suggestion (do not block or prompt further):
  ```
  💡 End of week — consider running /groove-utilities-memory-retrospective week for a trend summary.
  ```
  (Substitute `month` and "End of month" on the last weekday of the month.)
- After all standard steps: check if `.groove/hooks/end.md` exists
  - If it exists: read the `## Actions` section and execute each item in order; report completion per item
  - If it does not exist: skip silently
