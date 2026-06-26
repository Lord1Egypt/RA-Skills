# Checkpoint Patterns for Agent Systems

## Why Checkpoint?

Agent tasks can fail mid-execution (idle timeout, API throttling, OOM). Without checkpoints, all progress is lost.

## Three Strategies

### 1. File-Level Checkpoint (Simplest, Recommended)

Write output to file after each subtask completes.

```
Task: Write 5 chapters
→ Complete Ch1 → write ch1.md ✅ (checkpoint 1)
→ Complete Ch2 → write ch2.md ✅ (checkpoint 2)
→ Ch3 crashes → Restart: Ch1, Ch2 exist, only redo Ch3
```

Best for: Subagent orchestration. Each subagent writes to its own file. If one fails, only re-dispatch that one.

### 2. State Machine Checkpoint (Medium Complexity)

Model the task as a state machine. Persist state on each transition.

```json
{
  "taskId": "rebuild-v8",
  "currentStep": 9,
  "totalSteps": 14,
  "completedFiles": ["ch1.md", ..., "ch8.md"],
  "lastCheckpoint": "2026-04-08T15:30:00Z"
}
```

Recovery: Read state file, skip completed steps.

Best for: Sequential multi-step pipelines where order matters.

### 3. Event Sourcing (Most Powerful, Most Complex)

Store all state-change events instead of current state. Recovery = replay events.

Best for: Critical business workflows where you need full auditability and replay capability.

## Practical Rules

1. **Write to file after each step** — Don't accumulate in context memory
2. **Design idempotent tasks** — Re-running a step = same result (write to same file = overwrite = safe)
3. **Only retry the failed step** — Not the whole pipeline
4. **Observable progress** — `ls` shows what's done; don't rely on model's "memory"

## Why Not Just Use Context?

Three ways context fails as a checkpoint:
1. **Idle timeout** — Session killed, context gone
2. **Compaction** — Mid-task details may be summarized away
3. **Hallucination** — Model "remembers" doing step 5, but the file was never written

**File system is the only reliable persistence layer.** `ls` doesn't lie.
