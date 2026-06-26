# Phase 3: Post-Merge Cleanup — Subagent Instructions

Auto-approve all tool calls (yolo mode).

1. Verify sprint-status.yaml at the repo root has status `done` for all merged stories.
   Fix any that are missing.

2. Repo root branch safety check:
     git branch --show-current
   If not main:
     git restore .
     git switch main
     git reset --hard origin/main
   If switch fails because a worktree claims the branch:
     git worktree list
     git worktree remove --force <path>
     git switch main
     git reset --hard origin/main

3. Pull main:
     git pull --ff-only origin main

Report: done or any errors encountered.
