# Task Recovery Guide

Use this when a long task was interrupted, the model ran out of room, a session died, or you need to continue work without restarting from zero.

## Natural-language recovery entrypoints

Good user intents include:

- "恢复上次任务"
- "列出未完成任务"
- "继续 task-xxx"
- "看下哪个任务卡住了"

## Recovery procedure

### 1. Find candidate tasks

Inspect `tasks/*.json` and prioritize tasks whose top-level status is:

- `running`
- `waiting`
- `blocked`
- `partial`

If the user provided a `taskId`, use that task first.

### 2. Read the task file and resume summary

Check at minimum:

- `executionMode`
- `status`
- `stage`
- `stages`
- `nextAction`
- `resumeHint`
- `process.sessionId`
- `subtask.sessionKey`
- `cron.jobId`
- `artifacts`
- `result` / `error`

Then run:

```bash
python3 ./scripts/task-resume-summary.py <taskId>
```

This is the preferred human-readable recovery entry point.

### 3. Verify reality before trusting the file

Task files are cached state, not ground truth.

Depending on execution mode, verify the real backing state:

#### background-process
- inspect `process.sessionId`
- check process logs/status
- confirm whether the command is still running, succeeded, or died

#### subsession
- inspect `subtask.sessionKey`
- read session history or latest messages
- determine whether the sub-session completed, failed, or stalled

#### cron
- inspect `cron.jobId`
- check whether the job still exists, has run, or is pending

#### external state / side effects
- verify service health
- verify target files exist
- verify docs were actually written
- verify outputs exist in `outputs/<taskId>/`

Record verification with:

```bash
python3 ./scripts/task-verify.py <taskId> "<what reality says>"
```

### 4. Correct the task file if reality disagrees

Examples:

- task file says `running`, but process is dead → change to `failed` or `blocked`
- task file says `restart_service` still running, but service is healthy → mark it `done` and continue to verification
- task file says `failed`, but the output already exists and validates → mark the task `partial` or continue to the next stage

Reality wins.

If you need to correct state while verifying:

```bash
python3 ./scripts/task-verify.py <taskId> "<summary>" --correct-status running --correct-stage verify
```

### 5. Resume only the remaining work

Do **not** restart the whole task by default.

Resume from:

- the first `running` or `todo` stage that is still genuinely unfinished, or
- the `nextAction` if it still matches reality

Always be careful around external side effects. Never repeat deploy/restart/send/write steps blindly.

### 6. Update checkpoint during recovery

As soon as recovery starts, update:

- `lastVerifiedAt`
- `updatedAt`
- `status`
- `stage`
- `nextAction`
- `error` / `result` if newly discovered

Then continue stage by stage and keep writing state after each completed stage.

### 7. Notify after recovery

If recovery or reconnection actually happened, proactively tell the user.

Recovery should not be silent.

## Safe recovery principle

Recovery is **not** “run everything again.”
Recovery is “identify the last trustworthy completion point, then continue from there.”
