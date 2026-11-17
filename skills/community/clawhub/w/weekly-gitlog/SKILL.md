---
name: weekly-gitlog
description: Generate a compact weekly changelog from a git repository, grouped by author and day, without any dependencies. Use when you need a one-page summary of the last 7 days (or custom window) of commits for a report, standup, or release notes.
metadata: { "openclaw": { "emoji": "🗓️", "requires": { "bins": ["git"] } } }
---

# weekly-gitlog

Produce a compact weekly changelog from the current git repository. The output is plain text: one section per author, commits grouped by day, each commit on one line with short hash and subject.

## When to use

- Standup / weekly report prep
- Release-note drafting
- Quickly seeing "what did everyone touch in the last week"

## When NOT to use

- You need full diffs — use `git log -p` directly
- The repo has no commits in the window (script exits non-zero with a clear message)

## Prerequisites

- `git` on PATH
- Run from inside a git work tree (or pass `--repo <path>`)

## Steps

```bash
# last 7 days, grouped by author then day
node scripts/weekly-gitlog.mjs

# custom window (e.g. last 14 days) and repo path
node scripts/weekly-gitlog.mjs --days 14 --repo /path/to/repo

# machine-readable JSON instead of formatted text
node scripts/weekly-gitlog.mjs --json
```

## Output shape (text)

```
## alice@example.com
### 2026-08-28
  abc1234 fix: off-by-one in retry loop
### 2026-08-26
  def5678 feat: add weekly changelog script

## bob@example.com
### 2026-08-27
  9c0ffee docs: update README
```

## Notes

- The script only reads history; it never writes to the repository.
- Merge commits are skipped by default to keep the summary clean.
