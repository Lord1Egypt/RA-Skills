# Release Notes: wip-ai-devops-toolbox v1.9.52

**Fix branch guard false-blocking bash commands targeting worktree paths**

## What changed

- Branch guard now extracts absolute paths from any bash command (mkdir, cp, mv, touch, etc.) and resolves the git branch from the target path's repo, not the CWD
- `findRepoRoot()` improved to walk up to existing directories for paths that don't exist yet (handles mkdir for new directories)
- Added `.ldm/worktrees` to allowed worktree locations alongside `_worktrees/` and `.claude/worktrees`

## Why

When Claude Code launches from `~/wipcomputerinc/` (on main) and runs bash commands targeting files inside a worktree (e.g., `mkdir -p /path/to/_worktrees/repo--branch/new-dir/`), the guard only knew how to extract paths from `cd` and `git -C` patterns. Any other command fell back to CWD resolution, saw "main", and blocked incorrectly. This caused minutes of wasted time every session.

## Issues closed

- wipcomputer/wip-ldm-os#187

## How to verify

```bash
# From CWD on main, this should no longer be blocked:
# mkdir -p /path/to/_worktrees/repo--branch/new-directory/
# cp file.txt /path/to/_worktrees/repo--branch/
```
