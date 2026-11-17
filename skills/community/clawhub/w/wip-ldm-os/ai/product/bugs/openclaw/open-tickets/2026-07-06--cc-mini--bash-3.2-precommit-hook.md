# OpenClaw pre-commit hook assumes bash 4 (`mapfile`); macOS ships bash 3.2

- **Date:** 2026-07-06 (filed; problem observed 2026-07-03)
- **Author:** cc-mini
- **Status:** open
- **Severity:** P2 (tooling; blocks commits, has a safe workaround)
- **Parent:** `2026-07-04--cc-mini--lesa-noreply-loop-recovery-and-upgrade-plan.md` (owed-items list)

## Problem

OpenClaw's pre-commit hook uses bash 4 syntax (`mapfile`/`readarray`). macOS ships bash 3.2 (`/bin/bash`), so the hook fails on Parker's machine. In the 2026-07-03 coder session this surfaced as a commit that could not complete, and the WRONG reaction was to reach for `--no-verify` (which the branch-guard correctly blocked).

Codex's ruling (2026-07-03), reaffirmed here: **do NOT bypass the guard.** The fault is the hook's bash assumption, not the guard.

## Fix direction

- Run the hook under Homebrew bash 4+ (`/opt/homebrew/bin/bash`) ahead of system bash, OR rewrite the `mapfile` usage in POSIX/bash-3.2-compatible form.
- File the corresponding OpenClaw upstream tooling issue if the hook ships from upstream.

## Acceptance criteria

- [ ] Pre-commit hook runs clean on macOS bash 3.2 (either via Homebrew-bash shebang/PATH or a 3.2-compatible rewrite).
- [ ] No `--no-verify` in the workflow; the guard stays authoritative.
- [ ] Upstream tooling issue filed if the hook is upstream-sourced.

## References

- Guard master: `../../guard/guard-master-ticket.md`
- Source session: `wip-tracking-private-only/sesssions/openclaw/kay-mini--OC-work--partner/Terminal Saved Output 3.txt` (Codex diagnosis)

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
