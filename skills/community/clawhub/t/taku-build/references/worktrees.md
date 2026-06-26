---
name: taku-worktree
description: >
  Use when starting feature work that needs isolation from the current workspace —
  creates isolated git worktrees with auto-detected project setup and baseline test
  verification. Triggers on "create a worktree", "new branch workspace", "isolated
  environment", "start a feature branch", or when build-phase work needs a clean
  sandbox before making changes.
---

# taku-worktree — Git Worktree Isolation

Git worktrees let you work on multiple branches simultaneously without switching. One workspace per feature. No context pollution. No stash juggling. No "wait, I was in the middle of something."

## Why This Matters

Branch switching kills flow. You have uncommitted work, dependencies installed, test state cached. Switching branches means redoing all of that. Worktrees give each feature its own directory, its own node_modules, its own lockfile state. Switch instantly. Never lose context.

## Directory Selection

Follow this priority:

1. **Existing directory:** Check for `.worktrees/` or `worktrees/`. If both exist, `.worktrees/` wins.
2. **CLAUDE.md preference:** `grep -i "worktree" CLAUDE.md` — if specified, use it.
3. **Ask the user:** If neither exists, offer `.worktrees/` (project-local, hidden) or a global location.

## Safety: Verify gitignore

Before creating a project-local worktree, verify the directory is ignored:

```bash
git check-ignore -q .worktrees 2>/dev/null
```

If NOT ignored, fix it immediately:

```bash
echo ".worktrees/" >> .gitignore
git add .gitignore && git commit -m "chore: add .worktrees/ to gitignore"
```

Why: Unignored worktree contents get tracked by git. That pollutes `git status` and risks committing worktree artifacts. Fix it now or regret it later.

## Creation Steps

### 1. Detect project type

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create the worktree

```bash
git worktree add ".worktrees/$BRANCH_NAME" -b "$BRANCH_NAME"
cd ".worktrees/$BRANCH_NAME"
```

### 3. Auto-detect and install dependencies

```bash
[ -f package.json ] && npm install
[ -f Cargo.toml ] && cargo build
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f pyproject.toml ] && poetry install
[ -f go.mod ] && go mod download
```

Don't hardcode. Detect from project files. If none match, skip dependency install.

**Why auto-detect:** Hardcoded setup commands break on different projects and become stale. Auto-detection from project files means the worktree setup works for any project without modification.

### 4. Run baseline tests

Run the project's test suite. If tests fail before you've changed anything, that's a pre-existing problem. Report it and ask whether to proceed.

**Why baseline tests:** Without a baseline, you can't distinguish bugs you introduced from bugs that already existed. The baseline establishes what "passing" looks like in this worktree's environment. If tests fail here, any work you do will be built on a broken foundation.

```bash
npm test        # or cargo test, pytest, go test ./...
```

If tests pass: report the count. "Worktree ready. 47 tests, 0 failures."

If tests fail: show the output. Ask the user. Don't silently proceed with a broken baseline.

### 5. Report

```
Worktree: .worktrees/<branch-name>
Tests: <N> passing, <M> failing
Ready to implement: <feature-name>
```

## Cleanup

When the feature is done and merged:

```bash
git worktree remove ".worktrees/$BRANCH_NAME"
git branch -d "$BRANCH_NAME"
```

If the branch isn't merged yet and you want to keep it, just remove the worktree:

```bash
git worktree remove ".worktrees/$BRANCH_NAME"
```

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|------------|-----|
| Skip gitignore check | Worktree contents tracked by git | Always `git check-ignore` before creating |
| Proceed with failing tests | Can't tell new bugs from old | Report failures, get permission |
| Hardcode setup commands | Breaks on different projects | Auto-detect from project files |
| Never clean up worktrees | Disk usage grows, stale branches | Remove worktree after merge |

## Known Pitfalls

**Creating worktree without checking gitignore.** A worktree was created in `.worktrees/my-feature`. After implementing the feature, `git status` showed 2,000+ untracked files — the worktree's `node_modules/` and build artifacts. The entire worktree contents were about to be committed.

*What went wrong:* The gitignore check was skipped because "it usually works." The `.worktrees/` directory wasn't in `.gitignore`, so git saw everything inside it as untracked files.

*Prevention:* The Safety step is first for a reason: `git check-ignore -q .worktrees`. If it's not ignored, fix it BEFORE creating the worktree. This is a 10-second check that prevents a very messy cleanup.

**Baseline tests failing but proceeding anyway.** The worktree was created, `npm install` ran, `npm test` showed 3 failures. The developer proceeded with implementation assuming the failures were pre-existing. After 2 hours of work, the tests still failed — 2 were pre-existing but 1 was caused by a dependency version mismatch in the worktree's fresh install.

*What went wrong:* Failing baseline tests were assumed to be someone else's problem. The worktree's isolated environment had a different dependency resolution than the main workspace.

*Prevention:* If baseline tests fail, report the output and ask whether to proceed. Don't assume failures are pre-existing. In isolated worktrees, dependency versions may differ. Verifying the baseline protects you from debugging your own changes against a broken foundation.

**Stale worktrees accumulating.** Over 3 months, 12 worktrees were created for various features. 10 were merged, but the worktrees were never cleaned up. Each had its own `node_modules/` (500MB each). Six gigabytes of disk space consumed by dead worktrees.

*What went wrong:* The Cleanup step was never executed. After merging, developers moved on without removing worktrees.

*Prevention:* Add worktree cleanup to the post-merge routine. After merging or discarding a branch, remove the worktree immediately. List stale worktrees with `git worktree list` periodically.

## Completion

Status: DONE when worktree is created, dependencies installed, and baseline tests pass. DONE_WITH_CONCERNS if baseline tests fail but user chose to proceed. BLOCKED if git worktree setup fails.
