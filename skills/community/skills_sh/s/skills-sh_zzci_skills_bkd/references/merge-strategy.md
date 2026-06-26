# BKD Worktree Merge Strategy

Branch merging for worktree-mode subtasks. Simple-mode subtasks skip this entirely
since they work directly on the main branch.

## Table of Contents

- [Branch Architecture](#branch-architecture)
- [1. Handle Main Branch State Before Merge](#1-handle-main-branch-state-before-merge)
- [2. Merge Strategies](#2-merge-strategies)
- [3. Post-Merge Verification](#3-post-merge-verification)
- [4. Merge Failure Handling](#4-merge-failure-handling)
- [5. Worktree Cleanup](#5-worktree-cleanup)
- [Key Rules](#key-rules)


## Branch Architecture

The coordinator issue always runs on the main branch. Subtasks with `useWorktree: true`
work in isolated branches:

```
Main branch (main/master)          <- coordinator runs here
  +-- bkd/{subIssueId-1}          <- subtask 1 worktree branch
  +-- bkd/{subIssueId-2}          <- subtask 2 worktree branch
  +-- bkd/{subIssueId-3}          <- subtask 3 worktree branch
```

BKD auto-creates branch `bkd/{issueId}` for `useWorktree: true` issues.

Worktree path: `<WORKTREE_BASE>/<projectId>/<issueId>/`

Base branch priority: `origin/main` > `origin/master` > `main` > `master`

## 1. Handle Main Branch State Before Merge

The coordinator runs on the main branch, so there are usually uncommitted changes
(coordinator logic, config, docs, etc.) present at merge time.

```bash
cd {project_directory}
git status --porcelain
```

**When uncommitted changes exist:**

```bash
# Check file overlap between coordinator changes and subtask changes
curl -s "$BKD_URL/projects/{pid}/issues/$SUB_ID/changes" | jq '.data[].path'
git diff --name-only
git diff --cached --name-only
```

```bash
# Option A: No file overlap (common case)
# Commit coordinator changes first, then merge subtask
git add -A
git commit -m "feat: {coordinator work description}"
# Proceed to merge

# Option B: File overlap exists
# Stash coordinator changes, merge subtask, then restore
git stash push -m "coordinator work before merge bkd/{subIssueId}"
# Proceed to merge
# After merge:
git stash pop
# Resolve conflicts if any -> git add -> git commit
```

**Rule: Never merge with a dirty working tree.** Always commit or stash first.

## 2. Merge Strategies

Choose based on file overlap between subtasks:

### Strategy A: No Conflict, Sequential Merge (default)

When subtask changes do not overlap. Merge each subtask as soon as it passes review (pipeline-style):

```bash
cd {project_directory}
git fetch origin

# Merge each reviewed subtask one at a time
git merge bkd/{subIssueId} --no-ff -m "merge: {subtask title} (bkd/{subIssueId})"
```

### Strategy B: Overlap, Ordered Merge + Conflict Resolution

When subtasks touch overlapping files. Merge in dependency order, resolve conflicts after each:

```bash
# Merge base subtask first
git merge bkd/{baseSubIssueId} --no-ff -m "merge: {base subtask title}"

# Then merge dependent subtask, resolve conflicts
git merge bkd/{dependentSubIssueId} --no-ff
# If conflicts: resolve -> git add -> git commit
```

### Strategy C: Integration Branch

For many subtasks or complex dependencies. Create an integration branch first:

```bash
# Detect base branch
BASE_BRANCH=$(git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}')
BASE_BRANCH=${BASE_BRANCH:-main}

MERGE_BASE=$(git rev-parse HEAD)

git checkout -b integrate/{orchestratorId} $BASE_BRANCH

for SUB_BRANCH in bkd/{sub1} bkd/{sub2} bkd/{sub3}; do
  git merge $SUB_BRANCH --no-ff
  # Resolve conflicts if any
done

# After integration branch tests pass, merge back to base branch
git checkout $BASE_BRANCH
git merge integrate/{orchestratorId} --no-ff -m "merge: {dispatch task title}"
```

## 3. Post-Merge Verification

```bash
# Record MERGE_BASE before merging (do this before step 2)
MERGE_BASE=$(git rev-parse HEAD)

# After merge, check all changes introduced
git diff ${MERGE_BASE}..HEAD --stat

# Build verification
npm run build  # or project-appropriate build command

# Test verification
npm run test
```

## 4. Merge Failure Handling

### Unresolvable conflicts

```bash
git merge --abort
```

Follow-up coordinator with report, escalate to human.

### Build/test failure after merge

```bash
git revert -m 1 HEAD --no-edit
```

Follow-up the failing subtask with error details, move back to `working`
(Rule 10 — send the prompt via a temp file, not inline: `jq -n --rawfile prompt
/tmp/bkd-prompt.txt '{prompt:$prompt}' > /tmp/bkd-body.json`, then `curl
--data-binary @/tmp/bkd-body.json`; see `rest-api.md` →
[Sending Request Bodies Safely](rest-api.md#sending-request-bodies-safely)):

```bash
curl -s -X POST "$BKD_URL/projects/{pid}/issues/$SUB_ID/follow-up" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "Post-merge build failed, reverted.\nError: {build/test error details}\nRequired: fix issues based on latest main branch and resubmit."
  }' | jq

curl -s -X PATCH "$BKD_URL/projects/{pid}/issues/$SUB_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"working"}' | jq
```

Reworked subtasks re-enter the pipeline from the completion report step.

## 5. Worktree Cleanup

No manual cleanup needed. BKD auto-cleans worktrees 1 day after an issue enters `done`.

- Cleanup cycle: every 30 minutes
- Controlled by: `worktree:autoCleanup` application setting
- Early cleanup if needed:
  ```bash
  curl -s -X DELETE "$BKD_URL/projects/{pid}/worktrees/{subIssueId}" | jq
  ```

## Key Rules

1. **Always `--no-ff`** - preserve branch history for per-subtask traceability
2. **Record `MERGE_BASE` before merging** - `git rev-parse HEAD` before merge, used for post-merge diff
3. **Roll back before continuing** - conflicts: `merge --abort`; post-merge failures: `revert -m 1`; never operate on dirty merge state
4. **Simple mode serial constraint** - in simple mode, subtasks must run serially or have zero file overlap; switch to worktree mode if conflicts appear
5. **Branch naming is fixed** - subtask branches: `bkd/{issueId}`, integration branches: `integrate/{orchestratorId}`
6. **Do not manually clean worktrees** - BKD auto-cleans after `done` + 1 day unless early cleanup is needed
