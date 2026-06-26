# Release Notes: wip-ldm-os v0.4.33

**Fix registry version tracking + add ldm worktree command.**

## What changed

### Registry fix (#139)
After `ldm install` updates a toolbox-style package (like wip-ai-devops-toolbox with 12 sub-tools), the registry now updates the version for ALL sub-tools, not just the parent entry. Previously, sub-tools kept their old version in the registry, causing `ldm install --dry-run` to show them as needing updates again.

### ldm worktree command (#130)
New command for centralized worktree management:

```bash
ldm worktree add cc-mini/fix-bug    # creates _worktrees/<repo>--cc-mini--fix-bug/
ldm worktree list                    # shows all active worktrees
ldm worktree remove <path>           # removes a worktree
ldm worktree clean                   # prunes stale worktrees
```

Auto-detects the repo from CWD. Creates worktrees in a sibling `_worktrees/` directory so they don't get mixed in with real repos.

## Why

Registry versions weren't updated for sub-tools, causing phantom re-updates. Worktrees created as repo siblings caused confusion with iCloud sync and directory listings.

## Issues closed

- #139
- #130

## How to verify

```bash
ldm install
ldm install --dry-run
# Should show "Everything is up to date" (no phantom updates)
```
