---
name: workflow-checkpoint
version: 1.0.0
description: Workflow Checkpoint System - Save and recover from any point in multi-step AI workflows. Never lose progress mid-task.
emoji: 💾
tags: [workflow, checkpoint, recovery, reliability, productivity]
---

# Workflow Checkpoint System 💾

Save and recover from any point in multi-step AI workflows. Never lose progress mid-task.

## Why This Matters

AI Agents executing multi-step workflows often fail mid-way:
- Task 3 of 5 fails → all progress lost
- Session restarts → must start from scratch
- Token overflow → workflow interrupted
- Tool errors → uncertain where we left off

This skill eliminates that problem with automatic checkpointing.

## How It Works

### Core Protocol

```
For every multi-step workflow:

1. PLAN → Write steps to checkpoint file
2. EXECUTE → After each step, save:
   - Which step completed
   - What output was produced
   - What artifacts were created
   - Current state/data
3. VERIFY → Check step result
4. CHECKPOINT → Update progress file
5. RECOVER → On failure, resume from last checkpoint
```

### Checkpoint File Format

Save to `memory/checkpoints/<workflow-name>.json`:

```json
{
  "workflow": "deploy-website",
  "startedAt": "2026-04-21T07:30:00Z",
  "totalSteps": 5,
  "completedSteps": [1, 2, 3],
  "currentStep": 4,
  "status": "in_progress",
  "steps": {
    "1": {
      "name": "Clone repository",
      "status": "done",
      "output": "/tmp/myapp cloned successfully",
      "timestamp": "2026-04-21T07:31:00Z"
    },
    "2": {
      "name": "Install dependencies",
      "status": "done",
      "output": "npm install completed",
      "timestamp": "2026-04-21T07:33:00Z"
    },
    "3": {
      "name": "Build project",
      "status": "done",
      "output": "build/ directory created",
      "timestamp": "2026-04-21T07:35:00Z"
    },
    "4": {
      "name": "Deploy to server",
      "status": "failed",
      "error": "Connection timeout",
      "timestamp": "2026-04-21T07:38:00Z"
    },
    "5": {
      "name": "Verify deployment",
      "status": "pending"
    }
  },
  "artifacts": ["/tmp/myapp/build/", "/tmp/myapp/config/"],
  "lastCheckpoint": "2026-04-21T07:38:00Z"
}
```

### Recovery Protocol

When resuming a failed workflow:

1. Read checkpoint file
2. Identify last completed step
3. Skip completed steps (verify artifacts still exist)
4. Resume from failed/pending step
5. Update checkpoint

### Usage Examples

#### Before a complex task:
```
I'm about to execute a 5-step workflow: deploy-website.
Steps: 1) Clone repo 2) Install deps 3) Build 4) Deploy 5) Verify
Saving checkpoint to memory/checkpoints/deploy-website.json
```

#### After each step:
```
Step 2/5 complete: Install dependencies
Output: npm install completed, 142 packages
Checkpoint updated: completedSteps [1,2]
```

#### On failure:
```
Step 4/5 FAILED: Deploy to server
Error: Connection timeout to 192.168.1.100:22
Checkpoint saved. Can resume from step 4.
Retrying... (attempt 1/3)
```

#### On recovery:
```
Resuming workflow: deploy-website
Last checkpoint: Step 3 completed at 07:35
Skipping steps 1-3 (verified artifacts exist)
Resuming from step 4: Deploy to server
```

## Integration with Other Skills

Works great with:
- **EVR** - Verify each step before checkpointing
- **Error Recovery** - Auto-retry failed steps from checkpoint
- **Memory Guard** - Checkpoints persist across sessions

## Anti-Patterns

❌ Don't save checkpoints for single-step tasks
❌ Don't save sensitive data in checkpoint files
❌ Don't skip verification when resuming
❌ Don't forget to clean up old checkpoints

## License

MIT
