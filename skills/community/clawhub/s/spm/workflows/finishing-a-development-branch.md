# Finishing a Development Branch

## Overview

Guide completion of development work: verify → present options → execute → cleanup.

## Step 1: Verify Tests

```bash
npm test   # or project's test command
```

If tests fail: Stop. Must fix before completing.

## Step 2: Present Options

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

## Step 3: Execute Choice

**Option 1: Merge Locally**
```bash
git checkout <base-branch> && git pull
git merge <feature-branch>
npm test   # verify on merged result
git branch -d <feature-branch>
```

**Option 2: Push and PR**
```bash
git push -u origin <feature-branch>
gh pr create --title "..." --body "..."
```

**Option 3: Keep** — Report branch name and path. Don't cleanup.

**Option 4: Discard** — Require typed "discard" confirmation. Then:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

## Step 4: Cleanup Worktree

For options 1, 2, 4:
```bash
git worktree remove <worktree-path>
```

## Step 5: Update WBS Ledger — Delivery Summary

Write the Delivery Summary section:
- Completed work mapped to original assignment
- Evidence package (test results, file diffs)
- Remaining blockers/skipped items
- Residual risks
