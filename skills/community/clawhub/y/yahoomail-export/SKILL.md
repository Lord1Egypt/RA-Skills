---
name: yahoomail-export
description: Export large Yahoo Mail archives with the folder-rotation IMAP workflow, resumable downloads, and safe delete-after-verify handling.
metadata:
  short-description: Export large Yahoo Mail archives safely
---

# Yahoo Mail Export

Use this skill when working on large Yahoo Mail IMAP exports, especially when the mailbox is bigger than Yahoo's practical folder limits or the connection keeps dropping mid-run.

## Use This Skill For

- Draining Yahoo `INBOX` in bounded batches
- Downloading export folders to local `.eml` files
- Deleting only messages that have been verified locally
- Resuming after Yahoo IMAP disconnects, `SERVERBUG`s, or broken pipes
- Turning an existing export workflow into a repeatable, documented process

## Workflow

1. Check whether `INBOX` is already empty.
2. Pick the first export folder with room.
3. Move a bounded batch out of `INBOX`.
4. Download that export folder locally.
5. Delete only messages that were successfully written to disk.
6. Save state so the next run can resume cleanly.

## Practical Yahoo Limits Observed

These are operational observations from the completed migration, not official Yahoo documentation:

- `10,000` messages is the practical folder ceiling for normal IMAP selection.
- `8,999` messages is a safe move batch for the rotation step.
- `1,000`-message delete chunks worked reliably.
- `0.1s` between fetches was enough to keep the connection usable.
- Periodic reconnects were necessary during long fetch runs.
- Yahoo would sometimes drop the socket with:
  - `IMAP4rev1 Server logging out`
  - `Broken pipe`
  - `SERVERBUG`

## Preferred Implementation Pattern

Use a script that:

- writes `.eml` before metadata
- keeps per-folder progress
- reconnects after a fixed number of fetches
- deletes by UID, not by unstable sequence assumptions
- writes a state file and a lock file
- treats `INBOX empty` as a terminal success condition

## Core Files

- `export-scripts/purge_cycle.py` - main safe rotation cycle
- `export-scripts/move_to_exports.py` - move-only helper for testing
- `triage-pipeline/build_embeddings.py` - embedding generation
- `triage-pipeline/pre_filter.py` - rule-based filtering
- `triage-pipeline/triage_emails.py` - LLM triage
- `triage-pipeline/summary_report.py` - summary generation

## Important Guardrails

- Do not delete from Yahoo until the local `.eml` is written.
- Do not assume a stalled log means failure once `INBOX` is empty.
- Do not keep the watchdog running forever after completion; it will happily rediscover “stalls” in a finished job.
- Keep export folders under the practical limit so Yahoo does not become philosophical about your session.

## If You Need to Reuse This Skill

For a new mailbox migration, adapt the constants in the scripts first:

- account credentials
- base directory
- move batch size
- delete chunk size
- reconnect delay
- cooldown intervals

Then test on a tiny folder before touching the real inbox.

