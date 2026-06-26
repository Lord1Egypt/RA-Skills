---
name: swarm-sprint
description: Parallel multi-agent coding sprints using git worktree isolation. Unlike naive parallel agents that silently overwrite each other's work, Swarm gives each agent its own private copy of the repo (a git worktree + branch) so they cannot touch each other's files. A mandatory conflict planner runs before any agent is spawned — it analyzes your task list, flags tasks that would touch the same files, and serializes them automatically. Coordinator reviews each diff before anything lands on main. Use when given 2+ coding tasks on a repository. Trigger phrases: "run a swarm sprint", "parallel sprint", "use swarm for these tasks". Inspired by Anthropic's COORDINATOR_MODE architecture.
---

# Swarm — Parallel Coding Sprints

Parallel multi-agent coding sprints using git worktree isolation.

## When to Use

- **2+ tasks** touching different parts of the codebase → use swarm
- **1 task** → do it directly, no swarm needed
- **2+ tasks ALL touching schema/auth** → serialize them (swarm handles this automatically)

Trigger phrases: "Run a swarm sprint", "Parallel sprint on [repo]", "Use swarm for these tasks"

## The Golden Rule — Always Plan First

**Before spawning any agents, run the conflict analyzer:**

```bash
node <skill-dir>/scripts/swarm.js --repo <repo_path> --tasks tasks.json --plan-only
```

Read the output:
- `✓ No conflicts` → all tasks run in parallel
- `⚠ HIGH conflict` → affected tasks auto-serialized into separate groups
- `LOW conflict` → runs parallel, watch the merge

**Never skip this step.** Two agents modifying the same file = merge conflict = wasted work.

## Workflow

### 1. Write tasks.json

```json
[
  {
    "id": "short-unique-id",
    "description": "Exactly what to build — be specific",
    "role": "coder",
    "successCriteria": ["Specific outcome", "TypeScript compiles clean"]
  }
]
```

### 2. Run conflict analysis (mandatory)

```bash
node <skill-dir>/scripts/swarm.js --repo <repo_path> --tasks tasks.json --plan-only
```

### 3. Create worktrees

```bash
node <skill-dir>/scripts/swarm.js --repo <repo_path> --tasks tasks.json
```

Creates isolated git worktree + branch per task. Writes `swarm-packages.json`.

### 4. Spawn subagents

Read `swarm-packages.json`. For each package, spawn a subagent with:
- Working directory = `worktreePath`
- Task prompt = `instructions` field
- Instruction to stay inside that directory only
- Instruction to `git add -A && git commit` before reporting back

### 5. Review each agent's output

```bash
git diff main..swarm/<branch-name>
```

### 6. Merge passing work

```bash
git merge swarm/<branch-name>
```

Merge one at a time. Verify TypeScript clean after each.

### 7. Cleanup (always, no exceptions)

```bash
node <skill-dir>/scripts/swarm.js --repo <repo_path> --cleanup swarm-packages.json
```

Deletes all worktrees and branches. Always run this.

## Agent Roles

| Role | Behavior |
|------|----------|
| `coder` | Implements task. No unrelated refactoring. Runs tsc when done. |
| `reviewer` | Reviews diff skeptically. Flags bugs, type errors, missing error handling. |
| `tester` | Writes tests following existing patterns. |

## High-Conflict Areas (Auto-Serialized)

- `schema.prisma`, migration SQL
- Auth/session middleware
- Main router or index registration
- Shared config/env files

## Rules

- Planning step is mandatory
- Worktrees always deleted after sprint
- Never push from a worktree — coordinator handles git
- Reviewer role should use cheaper model (Haiku); coder uses Sonnet
- Max 5 parallel agents
- Sprint log written to `memory/swarm-log.md`

## Dry Run

```bash
node <skill-dir>/scripts/swarm.js --repo <repo_path> --tasks tasks.json --dry-run
```
