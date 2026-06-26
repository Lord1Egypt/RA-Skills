# Plan: Adopt ClawChief Architectural Patterns for LDM OS

**Date:** 2026-04-08
**Author:** Parker + CC Mini + Lēsa
**Source:** [snarktank/clawchief](https://github.com/snarktank/clawchief) by Ryan Carson (v3.0.0, Apr 7 2026)
**Acknowledgement:** Ryan Carson / snarktank for the ClawChief reference architecture. Add to LDM OS acknowledgements when these patterns ship.

## Context

ClawChief is a public OpenClaw starter kit that implements a "chief of staff" operating system for founders. While our LDM OS architecture is more sophisticated, ClawChief's v3.0.0 has three patterns worth adopting. Both CC and Lēsa independently identified the same takeaways.

We are NOT installing ClawChief. We are adapting architectural patterns into our existing system.

## Pattern 1: Priority Map + Auto-Resolver Split

### What ClawChief does
- `priority-map.md` ... defines who/what matters, urgency levels (P0-P3), action modes. Pure prioritization policy.
- `auto-resolver.md` ... defines what to auto-resolve vs draft-first vs escalate. Pure resolution policy.
- These are separate files. Prioritization and execution are decoupled.

### Our current problem
HEARTBEAT.md does both: it defines what to check AND what to do about it. Too tangled. When one changes, the other breaks. Hard to tune prioritization without risking execution logic.

### The adaptation
Split HEARTBEAT.md into three files:

| File | Purpose | ClawChief equivalent |
|------|---------|---------------------|
| `HEARTBEAT.md` | What to check and when (schedule, cadence, health checks) | Cron templates |
| `PRIORITY-MAP.md` | What matters, who matters, urgency tiers, context rules | `priority-map.md` |
| `AUTO-RESOLVER.md` | What to auto-handle vs draft vs escalate to Parker | `auto-resolver.md` |

HEARTBEAT.md becomes thin. It references PRIORITY-MAP.md for "is this important?" and AUTO-RESOLVER.md for "what do I do about it?"

### Files to create/modify
- Create: `~/.openclaw/workspace/PRIORITY-MAP.md`
- Create: `~/.openclaw/workspace/AUTO-RESOLVER.md`
- Modify: `~/.openclaw/workspace/HEARTBEAT.md` (slim down, reference the other two)
- Update: `~/.openclaw/workspace/TOOLS.md` (document the new files)

## Pattern 2: Knowledge Compiler

### What ClawChief does
`knowledge-compiler.md` is an explicit policy for what gets compiled back into source-of-truth files and when. Raw inputs (conversations, meeting notes, incidents) are processed into canonical files on a schedule, not ad hoc.

### Our current problem
Memory writes are inconsistent. Sometimes Lēsa writes to MEMORY.md immediately, sometimes at session end, sometimes never. What gets persisted vs what stays in crystal vs what stays only in conversation is a judgment call with no policy. This causes:
- Duplicate information across MEMORY.md, daily logs, and crystal
- Important decisions that never get written down
- MEMORY.md growing without pruning

### The adaptation
Create a `KNOWLEDGE-COMPILER.md` policy that defines:

1. **What gets compiled and where:**
   - Decisions and preferences ... MEMORY.md
   - Tool/workflow rules ... TOOLS.md
   - Current state ... SHARED-CONTEXT.md
   - Daily events ... daily logs
   - Everything else ... crystal (automatic via agent_end hook)

2. **When compilation happens:**
   - Session end: review and persist key decisions
   - Daily: prune MEMORY.md of stale entries
   - Weekly: audit TOOLS.md for outdated rules

3. **What does NOT get compiled:**
   - Debugging details (already in git)
   - Routine code changes (already in commits)
   - Anything already captured elsewhere

### Files to create/modify
- Create: `~/.openclaw/workspace/KNOWLEDGE-COMPILER.md`
- Update: `~/.openclaw/workspace/TOOLS.md` (reference the compiler)

## Pattern 3: Deterministic Cron Prompt Discipline

### What ClawChief does
Cron templates are thin trigger prompts that:
1. Reference a policy file (not embed logic)
2. Call a specific skill (not freestyle)
3. Have a clear scope boundary ("only do X, never Y")

Example: their EA sweep cron says "run the executive-assistant skill, check inbox and calendar, follow the auto-resolver policy." It does NOT contain the EA logic itself.

### Our current problem
Heartbeat prompts can be heavyweight. Logic that should be in TOOLS.md or skill definitions sometimes lives in the heartbeat/cron prompt. When the prompt compacts, the logic vanishes. When the logic changes, every cron job needs updating.

### The adaptation
Adopt the "thin trigger" convention for all cron/heartbeat prompts:

**Before (embedded logic):**
```
Check inbox. If there's a message from Parker, respond immediately.
If there's a newsletter, archive it. If there's a meeting invite,
check calendar conflicts and accept if no conflict...
```

**After (thin trigger referencing policy):**
```
Run inbox sweep. Follow AUTO-RESOLVER.md for disposition.
Follow PRIORITY-MAP.md for urgency. Log results to daily log.
```

### Files to modify
- `~/.openclaw/openclaw.json` (heartbeat prompt, if present)
- Any cron job definitions
- Document the convention in TOOLS.md

## Implementation Order

1. **Pattern 1 first** (priority map split) ... highest impact, HEARTBEAT.md is already too complex
2. **Pattern 2 second** (knowledge compiler) ... codifies existing ad-hoc behavior
3. **Pattern 3 third** (cron discipline) ... convention change, applies going forward

## What We Are NOT Doing

- NOT installing ClawChief
- NOT adopting Todoist (we use memory-crystal for task tracking)
- NOT adopting Google Workspace scripts (we have himalaya for email)
- NOT copying Ryan Carson's personal context
- NOT changing our memory architecture (crystal + workspace files is already more sophisticated)

## Acknowledgement

Ryan Carson / [snarktank/clawchief](https://github.com/snarktank/clawchief) for the reference architecture that informed these patterns. To be added to LDM OS acknowledgements when patterns ship.
