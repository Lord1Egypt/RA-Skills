# Release Notes: wip-ai-devops-toolbox v1.9.46

**Centralized worktree management: guard rule, wip-release prune, Dev Guide convention.**

## What changed

### Guard: worktree path warning (#212)
Branch guard now warns when `git worktree add` creates a worktree outside `_worktrees/`. Shows the convention and suggests `ldm worktree add`. Warning only, not a hard block.

### wip-release: worktree prune (#212)
New step 12 in the release pipeline. After branch cleanup, prunes stale worktrees from `_worktrees/` whose branches are merged into main. Automatic cleanup after every release.

### Dev Guide: _worktrees/ convention (#212)
Documents the centralized worktree convention:
- All worktrees go in `_worktrees/<repo-name>--<branch-suffix>/`
- Use `ldm worktree add` (auto-detects repo, creates in the right place)
- Guard warns about worktrees outside the convention
- `wip-release` auto-prunes merged worktrees

## Why

Worktrees created as repo siblings confused iCloud sync, looked like real repos in directory listings, and were never cleaned up. This session alone created 10+ stale worktrees. The convention keeps them organized and the release pipeline cleans them automatically.

## Issues closed

- #212
- #213

## How to verify

```bash
# Guard warning:
cd /path/to/repo
git worktree add ../my-worktree -b test   # should warn about _worktrees/

# Correct path:
ldm worktree add cc-mini/test             # creates _worktrees/<repo>--cc-mini--test/
```
