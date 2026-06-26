# Plan: Daily Workspace Health Audit

**Date:** 2026-04-08
**Author:** cc-mini (with Parker)
**Status:** plan
**Where:** Add to `wip-healthcheck` or `ldm doctor`

## The Problem

Nobody watches the workspace. Commits land in wrong repos. Files accumulate in root. Worktrees have uncommitted work. System directories drift. Parker finds out days later.

## What the Audit Checks

Run daily (morning). Report to Parker via iMessage or TUI.

### 1. Workspace root cleanliness
- `~/wipcomputerinc/` should only contain: `repos/`, `library/`, `team/`, `settings/`, `_trash/`, `_transfer/`, `screenshots/`, `CLAUDE.md`
- Flag any unexpected files (*.png, *.html, *.md in root, new folders)

### 2. Repo status (all repos under repos/)
- Uncommitted changes
- Unpushed commits
- Branches that diverged from main
- Stale worktrees with uncommitted work

### 3. System directories
- `~/.ldm/` ... unexpected files, config drift
- `~/.openclaw/` ... config drift, stale sessions
- `~/.claude/` ... stale plans, orphaned session files

### 4. Worktree audit
- List all worktrees across all repos
- Flag worktrees with uncommitted changes
- Flag worktrees whose branches are already merged (should be cleaned up)
- Flag worktrees older than 7 days with no commits

### 5. Secret scan
- Grep all repos for hardcoded keys (same pattern as today's security audit)
- Flag any file containing `sk-ant-api`, `xai-[a-z0-9]{30}`, `ghp_`, `ops_`, `tvly-`

### 6. Doc sync check
- Compare `library/documentation/` timestamps with `~/.ldm/shared/docs/` (or `~/.ldm/library/` after rename)
- Flag if home docs are newer than OS docs (means installer didn't propagate)

## Output Format

```
Daily Workspace Audit (2026-04-09 06:00 PST)

CLEAN:
  - 14 repos, all clean
  - 0 stale worktrees
  - No hardcoded secrets

ISSUES:
  ! wipcomputerinc/ root: 2 unexpected files (screenshot.png, test.html)
  ! wip-ldm-os-private: 1 worktree with uncommitted work (cc-mini/templates)
  ! library/documentation/how-worktrees-work.md newer than deployed version
```

## Implementation Options

1. **Add to wip-healthcheck** ... runs every 3 min already, add a daily workspace scan
2. **Add to ldm doctor** ... `ldm doctor --workspace` flag
3. **New cron on Lesa** ... daily at 06:00, reports to Parker via iMessage
4. **CC SessionStart hook** ... runs on every CC session boot, reports issues

Option 1 or 3 is best. Runs without anyone remembering.

## Cross-references

- `repos/ldm-os/utilities/wip-healthcheck-private/` ... existing healthcheck
- `ai/product/plans-prds/current/ldmos-core/2026-04-08--cc-mini--shared-to-library-refactor.md` ... the library rename plan
