# Block --no-verify and --force in branch guard

**Date:** 2026-03-16
**Closes:** #197, #143

## What changed

wip-branch-guard now blocks dangerous git flags on ANY branch, not just main:

- `--no-verify` ... always blocked. Agents were using this to bypass the pre-commit hook that blocks commits on main. The hook exists for a reason.
- `git push --force` ... blocked. Can destroy remote history. `--force-with-lease` is still allowed as the safer alternative.

These checks run early in the guard, before branch/worktree logic, so they can't be circumvented.

## Why

Agents were bypassing safety hooks with `--no-verify`. The pre-commit hook blocks commits on main, but `--no-verify` skips it entirely. This defeats the whole branch guard system. Same issue with `--force`: an agent could force-push and destroy work on the remote.

## Also closed

- #143: ClawHub scanning stuck (duplicate, resolved by SKILL.md republishing across v1.9.34-v1.9.36)
