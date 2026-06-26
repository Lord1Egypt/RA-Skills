---
name: status
description: Project status dashboard — open issues, recent commits, active branches/worktrees, memory state, and scratchpad. Use when the user asks for a status report, project overview, "what's going on", "where are we", or wants to catch up on project state without the full /catchup reconstruction.
---

# Project Status Report

Generate a concise project status dashboard. This is a read-only snapshot — it doesn't modify anything.

## Data Collection

Gather these in parallel where possible:

### 1. Git State
```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
git -C "$REPO_ROOT" log --oneline -10
git -C "$REPO_ROOT" branch -a --sort=-committerdate | head -15
git -C "$REPO_ROOT" worktree list
git -C "$REPO_ROOT" status --short
```

### 2. GitHub Issues
```bash
# Open issues, sorted by most recent
gh issue list --state open --json number,title,labels,updatedAt --limit 20
# Recently closed (last 7 days)
gh issue list --state closed --json number,title,closedAt --limit 10 | jq '[.[] | select(.closedAt > (now - 604800 | todate))]'
```

If `gh` is not authenticated, skip this section and note "GitHub CLI not authenticated — issue data unavailable."

### 3. Active Plans
Check `"$(git rev-parse --show-toplevel)/ai-workspace/plans/"` for any non-`.done.md` plan files. Read their Status field.

### 4. Memory State
- Read `"$(git rev-parse --show-toplevel)/ai-workspace/MEMORY.md"` — note line count vs 200-line limit
- Check `"$(git rev-parse --show-toplevel)/ai-workspace/.last-reflect-ts"` — how long since last /reflect
- Check `"$(git rev-parse --show-toplevel)/.branch-context.md"` — any uncommitted learnings

### 5. Scratchpad
Read `"$(git rev-parse --show-toplevel)/ai-workspace/scratchpad.md"` — count `- [ ]` items awaiting elevation.

## Output Format

Present as a compact dashboard. Adapt the sections based on what data is available — skip sections with no content rather than showing empty tables.

```
## Project Status: <repo-name>
### <date>

**Branch**: <current branch> | **Mode**: <autonomous/copilot> | **Last reflect**: <relative time>

### Open Issues (<count>)
| # | Title | Labels | Updated |
|---|-------|--------|---------|
(most recent 10, sorted by updated)

### Recently Closed (<count>, last 7d)
- #N title (closed <date>)

### Active Work
- Branches: <list active non-main branches>
- Worktrees: <list linked worktrees>
- Plans in progress: <list non-.done.md plans>

### Health
- MEMORY.md: <line count>/200 lines
- Scratchpad: <N> items flagged for elevation
- Last reflect: <timestamp or "never">
- .branch-context.md: <exists with N lines / not found>

### Suggested Next
(Pick 2-3 based on what you see — e.g., stale issues, scratchpad items to elevate, overdue reflect, MEMORY.md near limit)
```

The "Suggested Next" section is the most valuable part — it turns a passive report into actionable guidance. Base suggestions on:
- Issues with no recent activity
- `- [ ]` scratchpad items that should become issues
- MEMORY.md approaching 200 lines (needs pruning)
- Long time since last /reflect
- Branches with no recent commits (stale work)
- Open issues that match recently completed work (may be closeable)
