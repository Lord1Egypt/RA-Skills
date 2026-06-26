# Using Git Worktrees

## Overview

Create isolated git worktrees for each feature branch. Systematic directory selection + safety verification = reliable isolation.

## Directory Selection

Priority: `.worktrees/` (hidden) > `worktrees/` > Ask user

## Safety Verification

For project-local directories, MUST verify gitignore:

```bash
git check-ignore -q .worktrees || git check-ignore -q worktrees
```

If NOT ignored: add to `.gitignore` and commit.

## Creation Steps

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
path=".worktrees/$BRANCH_NAME"
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

## Run Project Setup

Auto-detect: `package.json` → `npm install`, `Cargo.toml` → `cargo build`, etc.

## Verify Clean Baseline

```bash
npm test   # or cargo test / pytest / go test
```

Tests must pass before proceeding. If they fail, report and ask.

## Report

```
Worktree ready at <path>
Tests passing (<N> tests, 0 failures)
```

## Cleanup

```bash
git worktree remove <path>
```
