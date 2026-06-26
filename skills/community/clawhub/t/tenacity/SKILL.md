---
name: tenacity
description: Autonomous goal completion with checkpoint, resume, and no intermediary confirmation handoffs. Use when a task is complex, long-running, or requires the agent to keep working without stopping for confirmation at every step. Triggers: "keep going", "don't stop until done", "run until complete", "autonomous", "tenacity", "never give up".
---

# Tenacity — Autonomous Goal Completion

This skill implements the **Tenacity execution pattern**: the agent keeps running until the stated goal is reached, only asking for human input when genuinely blocked.

## Core Principle

**Default behavior:** Ask for confirmation only when blocked, not at every step. If the path is clear, execute.

## When to Activate

Activate when Andrea says things like:
- "keep going until done"
- "don't stop to ask"
- "run this autonomously"
- "finish it completely"
- Any long-running multi-step task

## Architecture

Tenacity uses OpenClaw's existing primitives:

| Component | Role |
|-----------|------|
| **Standing Orders** | Grants permanent authority to execute within scope |
| **Task Flow** | Durable multi-step state across gateway restarts |
| **Lobster** | Deterministic steps with resume tokens |
| **Cron** | Scheduling and enforcement |
| **Checkpoint** | State saved after each milestone |

## Execution Pattern

### Step 1: Define Scope (Standing Order)

Before starting, establish:
- **What** the agent is authorized to do
- **When** to stop and ask (hard blockers only)
- **What** constitutes completion

```markdown
## Standing Order: [Task Name]

**Authority:** [exactly what the agent can do]
**Hard blockers:** [only conditions that require human input]
**Completion:** [how to know when done]
**Escalation:** [when to alert if something goes wrong]
```

### Step 2: Create Task Flow

Use a persistent session (`session:<id>`) for the task flow so state survives restarts:

```bash
openclaw tasks create "Tenacity: [task]" --session session:tenacity-task
```

Or use cron with a named session:

```bash
openclaw cron add \
  --name "[Task] tenacity run" \
  --session session:tenacity-task \
  --message "Execute [task] per standing orders. Check checkpoint before resuming." \
  --announce \
  --channel telegram \
  --to "834732674"
```

### Step 3: Checkpoint Protocol

After each milestone, save state:

```
CHECKPOINT: milestone_X_completed
STATE: {step: 3, last_file: "output.json", errors: []}
TIMESTAMP: 2026-05-14T10:30:00Z
```

On restart, resume from checkpoint:

```
RESUME from checkpoint: milestone_X_completed
Last state: {step: 3, last_file: "output.json"}
Continue from step 4...
```

### Step 4: Hard Blocker Conditions

**Ask only when:**
1. File/system permission denied and no alternative path
2. External dependency unavailable after all retries
3. Decision required that changes scope or direction
4. Andrea explicitly set a constraint

**Never ask when:**
- A step can be attempted with alternative tools
- A command failed but a retry or workaround exists
- The path is clear but requires multiple steps
- Output could be improved but is already acceptable

### Step 5: Completion

When goal is reached:
- Save final checkpoint with `STATUS: COMPLETE`
- Brief summary to Andrea
- Log to `memory/tenacity-log.md`

## Checkpoint Script

See `scripts/checkpoint.sh` — run after each milestone:

```bash
bash scripts/checkpoint.sh "step_3_done" '{"step": 3, "last": "file.csv"}'
```

## Resume Protocol

On session start, check for incomplete checkpoints:

```bash
bash scripts/checkpoint.sh --resume
```

If resume point exists, announce: "Resuming from [milestone]..."

## References

- Task Flow: `docs/automation/taskflow.md`
- Standing Orders: `docs/automation/standing-orders.md`
- Cron: `docs/automation/cron-jobs.md`
- Lobster: See `openclaw lobster --help`