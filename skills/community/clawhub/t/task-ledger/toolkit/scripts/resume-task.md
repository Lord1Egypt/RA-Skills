# Resume Task Playbook

Use this when a user says:

- continue
- resume the last task
- resume `<taskId>`
- which task is stuck?

## Step 1: identify the task

- If the user names a `taskId`, use it.
- Otherwise run `./scripts/list-open-tasks.py` and pick the most relevant recent task.

## Step 2: read the checkpoint

Inspect:

- `tasks/<taskId>.json`
- `logs/<taskId>.log`
- `outputs/<taskId>/`

Look at:

- `status`
- `stage`
- `stages`
- `nextAction`
- `resumeHint`
- `process.sessionId`
- `subtask.sessionKey`
- `cron.jobId`
- `artifacts`

## Step 3: read the resume summary

Run:

```bash
python3 ./scripts/task-resume-summary.py <taskId>
```

Use this as the fast recovery briefing before touching task state.

## Step 4: verify reality

Do not trust the task file alone.

Depending on execution mode:

### background-process
- inspect the referenced process
- check logs
- decide whether it is still running, succeeded, or failed

### subsession
- inspect session history
- decide whether the sub-session finished, stalled, or needs steering

### cron
- inspect the cron job state / runs
- decide whether it is still pending or already fired

### external side effects
- verify the service / file / document / output directly

Record what you found:

```bash
python3 ./scripts/task-verify.py <taskId> "<summary of reality>"
```

## Step 5: correct the checkpoint if needed

If reality and JSON disagree, update the JSON.

Examples:
- `running` -> `failed` if the process died
- current stage -> `done` if the real side effect already happened
- `failed` -> next stage if the output already exists and validates

Use correction flags when needed:

```bash
python3 ./scripts/task-verify.py <taskId> "<summary>" --correct-status running --correct-stage verify
```

## Step 6: continue only unfinished work

Resume from the first truly unfinished stage.
Do not blindly rerun deploy/restart/send/write steps.

## Step 7: keep updating state

As recovery proceeds, keep the checkpoint current:

- update `updatedAt`
- update `lastVerifiedAt`
- update `status`
- update `stage`
- update `nextAction`
- write `result` or `error` as needed

## Step 8: notify after recovery

If the task actually resumed after interruption or reconnection, proactively tell the user.

## Principle

Recovery is not “start over.”
Recovery is “find the last trustworthy point and continue from there.”
