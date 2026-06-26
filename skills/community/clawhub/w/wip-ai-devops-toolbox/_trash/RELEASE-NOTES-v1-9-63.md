# Release Notes: wip-ai-devops-toolbox v1.9.63

**Fix all wip-release errors: branch cleanup crashes, shell injection, stale remote refs.**

## The story

Every wip-release run produced errors: "fatal: Not a valid object name +", "remote ref does not exist", and shell injection risks from branch names passed through execSync template strings. These were dismissed as "non-blocking" but they cluttered every release output and masked real problems.

Root cause: branch cleanup code (sections 10 and 11) used `execSync` with template strings, which breaks on branch names with special characters and allows shell injection. Also tried to delete remote branches that GitHub already deleted during PR merge.

Fix: replaced all `execSync` template strings with `execFileSync` array args (safe from injection). Added character validation to skip branches with special chars. Wrapped remote delete in try/catch since GitHub PR merge already handles deletion.

## Issues closed

- #231 (continued: release pipeline reliability)

## How to verify

```bash
wip-release patch --dry-run
# Should show no "fatal" or "Not a valid object name" errors
# Guard tests: cd tools/wip-branch-guard && bash test.sh
```
