---
name: session-closeout
description: Run a read-only end-of-session audit of the current workspace and report what still needs attention. Checks for git repos with uncommitted changes, MASTER_TODO.md freshness, and optionally whether named project docs were updated today. Writes nothing and runs nothing it finds in the workspace. Use only when the user explicitly asks to run closeout, end the session, or invokes /closeout.
license: MIT
---

# Session Closeout

A read-only audit for the end of a work session. It reads the workspace, prints
what it found, and stops there. It creates no files, no directories, no commits,
and it never runs a builder, a hook, or any other script it discovers.

Recording the closeout is your job, not the script's. Take the values it prints
and write them wherever your notes live.

## Run it

From the workspace root:

```bash
bash skills/session-closeout/scripts/session-closeout.sh
```

Optional inputs:

| Variable | Effect |
|---|---|
| `CLOSEOUT_PROJECTS` | Pipe-delimited project slugs, e.g. `"alpha\|beta"`. Checks whether `STATUS.md`, `DECISIONS.md`, `PROJECT.md`, or `BACKLOG.md` under `projects/<slug>/` were touched today. Warn only. |
| `CLOSEOUT_TODO_STALE_HOURS` | Age at which `MASTER_TODO.md` counts as stale. Digits only, default 24. |

The workspace root is always the current directory. There is no environment
variable that moves it, and none that moves the projects directory either.

## What it checks

1. **Task hygiene.** Reports whether `MASTER_TODO.md` is fresh, stale, or missing.
   It never rebuilds the file. If it is stale and you keep a builder, run that
   builder yourself as a separate, reviewed step, then rerun this audit.
2. **Repo hygiene.** Finds git repos up to 4 levels below the workspace and lists
   the ones with uncommitted changes. It reads status only, with the repo's own
   fsmonitor and hooks pinned off, so scanning a repo cannot run that repo's code.
3. **Project-doc hygiene** (only with `CLOSEOUT_PROJECTS`). Flags projects whose
   core docs were not updated today. Slugs must be plain directory names: anything
   containing a separator, a `..`, or a leading dash is rejected and reported
   rather than looked up.
4. **Automation hygiene.** Always reports `not_verified`; check cron and
   automation health by hand.

## Read the output

The script prints `key=value` lines. Summarize these for the user, then record
the session outcome yourself if you keep session notes.

| Key | Values |
|---|---|
| `CLOSEOUT_STATUS` | `ok`, `warning` (dirty repos, stale todo, stale project docs, rejected slugs), `error` (`MASTER_TODO.md` missing) |
| `WORKSPACE_ROOT` | the directory that was audited |
| `MASTER_TODO_STATUS` | `fresh`, `stale`, `missing` |
| `DIRTY_REPO_COUNT`, `DIRTY_REPOS:` | repos to review; never auto-commit or discard |
| `PROJECT_DOC_WARNINGS` | count of projects with no core doc updated today |
| `REJECTED_SLUG_COUNT` | slugs that failed validation and were not looked up |
| `EXCEPTION_n` | `severity\|finding\|suggested action` |

## Boundaries

- Writes nothing. If you want a closeout block in a daily note, write it yourself
  from these values, as a separate and visible step.
- Runs nothing it discovers in the workspace: no builders, no `closeout-hooks.sh`,
  no plugins.
- Extra checks belong in a separate command you review and run yourself, not in
  this script.
- Do not invoke it on a timer or as a "wrap up" reflex; it is for explicit
  closeout requests.

## Requirements

Bash 4+ and git.
