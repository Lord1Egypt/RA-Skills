# Release Notes: wip-ai-devops-toolbox v1.9.57

**deploy-public.sh now excludes .worktrees/ and _worktrees/ from public repo syncs.**

## The story

v1.9.56 accidentally deployed worktree directories (containing embedded git repos) to the public repo. The deploy script's rsync excluded ai/, .git/, _trash/, and other dev artifacts but didn't exclude worktree directories. Added both .worktrees/ (new convention) and _worktrees/ (old convention) to the exclude list.

## Issues closed

- #228 (deploy-public.sh leaks .worktrees/ to public repo)

## How to verify

```bash
# Run deploy-public.sh --dry-run and confirm .worktrees/ is not synced
grep -n "worktrees" scripts/deploy-public.sh
```
