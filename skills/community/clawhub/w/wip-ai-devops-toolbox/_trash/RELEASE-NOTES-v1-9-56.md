# Release Notes: wip-ai-devops-toolbox v1.9.56

**Branch guard now blocks destructive git commands on all branches.**

## The story

The branch guard blocked commits and file writes on main, but allowed destructive git commands that destroy uncommitted work. Commands like `git clean -fd`, `git checkout --`, `git stash drop`, and `git reset --hard` slipped through because they were either in the allowed list or not in the blocked list. These commands destroyed Parker's Finder aliases, other agents' uncommitted edits, and user files multiple times on Mar 28-29.

The fix adds a new DESTRUCTIVE_PATTERNS list that fires on ALL branches, not just main. The guard also closes several bypass vectors: `node -e` removed from the allowed list, python/node file-write patterns detected, and `git checkout` narrowed to branch-switching only.

## What changed

- Added DESTRUCTIVE_PATTERNS: git clean -f, git checkout --, git stash drop/pop/clear, git reset --hard, git restore, python/node bypasses
- Removed `git checkout` blanket allow. Now only allows `git checkout <branch>` (switching)
- Removed `git stash drop` from allowed list
- Removed `node -e` from allowed bash patterns (bypass vector)
- Added `git stash show` and `git restore --staged` as safe read-only operations
- Deny message tells agent to use worktrees and safety checkpoints instead

## Issues closed

- #240 (branch guard + harness directories)
- #241 (python bypass detection)
- PR #284

## How to verify

```bash
# These should all be BLOCKED:
# git clean -fd
# git checkout -- somefile
# git stash drop
# git stash pop
# git reset --hard
# python3 -c "open('f','w').write('x')"

# These should still WORK:
# git checkout main (branch switching)
# git stash list (read-only)
# git status, git log, git diff
# Normal worktree workflow
```
