# God Mode — True Autonomous AI Agent Loop

## What This Does
Turns any OpenClaw agent into a continuously executing autonomous worker. No more "wait for user message." The agent wakes on a heartbeat cycle, reads its task queue, picks the highest-priority task, executes it, audits the result, logs everything, and sleeps until next cycle.

## How It Works
1. **Heartbeat triggers** → OpenClaw sends heartbeat message to agent session
2. **Agent reads TASKS.md** → ordered priority queue of work items
3. **Agent picks top task** → executes it using available tools
4. **Agent writes result** → logs to `memory/YYYY-MM-DD.md` + updates TASKS.md
5. **Agent self-audits** → was the result good? What to improve?
6. **Agent sleeps** → waits for next heartbeat

## Architecture

```
HEARTBEAT.md          → What to check/do on each heartbeat
TASKS.md              → Priority queue of autonomous work items
memory/YYYY-MM-DD.md  → Execution log (append-only)
memory/god-mode-state.json → State tracking (last task, cycle count, errors)
```

## Files

### TASKS.md Format
```markdown
# Task Queue — Priority Order

## Priority 1 (Critical)
- [ ] Task description here | context/goals

## Priority 2 (High)
- [ ] Task description | context

## Priority 3 (Medium)
- [ ] Task description | context

## Completed
- [x] Done task | result summary | completed YYYY-MM-DD HH:MM
```

### god-mode-state.json Format
```json
{
  "lastCycle": "2026-04-16T07:00:00Z",
  "cycleCount": 42,
  "lastTask": "Check Moltbook engagement",
  "lastResult": "success",
  "errors": 0,
  "consecutiveErrors": 0,
  "totalTasksCompleted": 15
}
```

## Heartbeat Behavior

On every heartbeat, the agent:

1. **Read state** — load `god-mode-state.json`
2. **Error check** — if 3+ consecutive errors, pause and log warning
3. **Read TASKS.md** — pick first uncompleted task
4. **Execute task** — do the work
5. **Log result** — append to daily memory
6. **Update state** — increment cycle, record result
7. **Update TASKS.md** — mark task done, add any new tasks discovered
8. **Self-audit** — one line: was this cycle productive?

## Self-Cleaning (Auto-Hygiene)

Every 12th cycle (roughly hourly at 5-min intervals), the agent runs a hygiene sweep:

### Workspace Hygiene
- Scan workspace root for files > 7 days old and not in core set (AGENTS.md, SOUL.md, USER.md, IDENTITY.md, MEMORY.md, HEARTBEAT.md, TASKS.md, TOOLS.md, STATE.md)
- Move stale files to `memory/archive/`
- Delete empty directories
- Remove stale pending flags (`.audit-pending`, `.work-pending`, etc.)
- Clean `node_modules/` if present and not actively used

### Memory Hygiene
- Archive daily logs older than 7 days to `memory/archive/`
- Archive research/reference files not accessed in last 7 days
- Compress `memory/archive/` if > 10MB
- If TASKS.md > 100 lines → archive completed section

### Log Hygiene
- Truncate log files (`*.log`) > 1MB → keep last 100 lines
- Delete stale state files (test JSON, temp files)
- Clean `__pycache__` directories

### Hygiene Rules
- NEVER delete: AGENTS.md, SOUL.md, USER.md, IDENTITY.md, MEMORY.md, HEARTBEAT.md, TASKS.md, TOOLS.md, STATE.md
- NEVER delete: `memory/YYYY-MM-DD.md` for today and yesterday
- NEVER delete: `scripts/` directory
- NEVER delete: `.secrets/`, `.git/`
- ALWAYS move to archive before deleting — nothing is truly deleted
- Log every hygiene action in daily notes

## Guardrails

- **Never execute red-line tasks** (money, contracts, irreversible actions) without human approval
- **Max 1 task per heartbeat cycle** — prevents runaway execution
- **Error circuit breaker** — 3 consecutive errors = pause + alert human
- **Quiet hours** — respect configured quiet hours (no work, only monitoring)
- **Audit every cycle** — no silent work, every action logged
- **Self-cleaning** — hygiene sweep every 12th cycle keeps workspace lean

## Installation

1. Copy this skill to `~/.openclaw/workspace/skills/god-mode/`
2. Create `TASKS.md` in workspace root
3. Create `memory/god-mode-state.json` with initial state
4. Add heartbeat schedule to OpenClaw config (every 30 min recommended)
5. Update `HEARTBEAT.md` to reference God Mode protocol

## Pricing
- ClawHub: $49 one-time
- Includes: task queue, state tracking, audit log, guardrails, documentation
- Target: OpenClaw users who want their agents truly autonomous

## Why This Is Different
- Not a prompt hack — infrastructure-based autonomy
- Built on OpenClaw's heartbeat system (250K+ star platform)
- Memory persists across sessions
- Audit trail for every action
- Guardrails prevent runaway behavior
- Actually works (we use it ourselves)
