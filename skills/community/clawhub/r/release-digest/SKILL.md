---
name: release-digest
description: Generate a concise, reproducible release digest from a local git repository — grouped commits, subject/file stats, and a Markdown changelog — without any third-party API.
metadata:
  { "openclaw": { "emoji": "🗞️", "os": ["darwin", "linux"], "requires": { "bins": ["git"] } } }
---

# release-digest

Produce a plain-Markdown release digest for a git repo. The digest is deterministic
given the same `--since`/`--until` window, so the same inputs always yield the
same document (making outputs easy to review and diff).

## When to use it

- A user asks "what changed between v1.2.0 and v1.3.0" or "draft release notes".
- You need a changelog section for a PR, release issue, or weekly digest.

## When NOT to use it

- You need to publish to a hosted release system (GitHub Releases, npm publish...).
  This skill only writes a Markdown digest — it never pushes or publishes anything.
- The repository has no git history (e.g. a freshly initialized repo with no
  commits in the requested window).

## Prerequisites

- `git` available on PATH.
- Run from inside the target repository (or pass `--repo <path>`).

## Steps

1. Resolve the window. If `--since` is omitted, default to the latest tag
   reachable from HEAD, or 14 days ago if no tags exist.
2. Run the bundled script to emit a Markdown digest:
   ```bash
   bash scripts/release-digest.sh --repo . --since <ref-or-date> --until HEAD
   ```
3. Hand the printed Markdown back to the caller. Never paste secrets, tokens,
   or private filenames that the commit log may surface — redact before replying.

## Output

A Markdown document with: window, commit count, author count, grouped commit
list, and a one-line `stat --summary` of files changed.
