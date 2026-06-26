---
name: shark-exec
version: 0.2.1
summary: "Background shell execution pattern for any AI coding agent. Wraps slow commands in background process + poller so the main agent always replies within 30s."
tags: [async, shell, background, shark, non-blocking]
---

# shark-exec

**Never block the main turn.** This skill wraps any slow shell command in a background process + poller, so the agent always replies to the user within 30 seconds — even if the command takes 10 minutes.

---

## When to Use

Use this skill whenever you're about to call a shell command and the command is expected to take **more than ~5 seconds**. Examples:

- `gh run watch <run-id>` — waiting for CI
- `npm run build` / `pytest` / `cargo build`
- `docker build`, `docker pull`
- Long-running SSH remote commands
- Any command with a long blocking wait
- Any command that polls, watches, or tails output

**Do NOT use for:**
- Quick reads (`cat`, `ls`, `git status`) — inline is fine
- Commands you're confident finish in <5s

---

## Protocol (Step by Step)

### Step 1 — Send Immediate Acknowledgment

Before spawning the background job, send the user a reply:

```
⏳ [label] running in background (max Xs)...
```

Example: `⏳ CI: run #12345 — watching in background (max 120s)...`

This must be the **first thing you do** — before exec, before writing state. Silence = failure.

### Step 2 — Launch Background Process

Launch the command in the background using your agent's background execution primitive (see [Runtime Adapters](#runtime-adapters) below).

You'll get back a handle to identify the process (session ID, PID, etc.).

```
# Generic pseudocode
handle = background_exec("gh run watch 12345")
```

### Step 3 — Write State

Read `<workspace>/skills/shark/shark-exec/state/pending.json`. If it doesn't exist, start with `{"jobs": []}`.

Append your new job:

```json
{
  "jobs": [
    {
      "sessionId": "sess-abc-123",
      "label": "CI: run #12345",
      "command": "gh run watch 12345",
      "startedAt": 1710000000000,
      "maxSeconds": 120,
      "cronJobId": null
    }
  ]
}
```

**Critical:** `startedAt` must be the actual current timestamp in milliseconds (`Date.now()`), not a hardcoded placeholder.

Set `cronJobId: null` for now — you'll fill it in step 4.

### Step 4 — Schedule a Poller

Schedule a poller that fires every ~15 seconds. The poller reads `pending.json`, checks each job's status, delivers results, and cleans up completed jobs.

**Generic pseudocode:**
```
scheduler.every(15000, () => {
  jobs = read("pending.json").jobs
  for job in jobs:
    status = poll(job.handle)
    if status.done:
      notify_user(job.label, status.output)
      remove_job(job)
    elif now > job.startedAt + job.maxSeconds * 1000:
      kill(job.handle)
      notify_user(job.label, "killed after Xs", status.partial_output)
      remove_job(job)
  if jobs.empty:
    cancel_this_scheduler()
})
```

**OpenClaw-specific example:**
```json
{
  "schedule": {"kind": "every", "everyMs": 15000},
  "payload": {
    "kind": "agentTurn",
    "message": "Check <workspace>/skills/shark/shark-exec/state/pending.json for pending background jobs. For each entry: call process(action=poll, sessionId=X, timeout=3000). If completed, send the result to <your notification channel> and remove the entry from pending.json. If still running and startedAt + maxSeconds*1000 < Date.now(), kill it with process(action=kill, sessionId=X) and send partial output with '⏱ killed after Xs'. After processing all entries, if pending.json jobs array is empty, delete this cron job (cronJobId is stored in the state file under cronJobId field)."
  },
  "sessionTarget": "isolated",
  "delivery": {"mode": "none"}
}
```

Once you have the poller/cron ID, **immediately update the state file** to store it:

```json
{ "sessionId": "sess-abc-123", ..., "cronJobId": "the-cron-id-returned" }
```

This is required so the poller can self-delete when done.

> **Important:** Only create ONE poller per session, even if there are multiple concurrent background jobs. The single poller will check all entries in pending.json.

### Step 5 — Poller Fires (Every 15s)

The poller will:

1. Read `pending.json`
2. For each job, check its process status
3. If **completed**: send result to user, close the finished handle if your runtime requires explicit cleanup, remove from jobs array, save pending.json
4. If **still running** and **past maxSeconds**: kill the process, send partial output + timeout message
5. If **still running** and within maxSeconds: leave in place, poller will retry in 15s
6. If jobs array is empty after processing: cancel the poller

### Step 6 — Result Delivery Format

**Success:**
```
✅ CI: run #12345 completed (47s)

<output truncated to last 50 lines if long>
```

**Timeout/Kill:**
```
⏱ CI: run #12345 killed after 120s

Last output:
<last 20 lines of output>
```

**Process already exited before first poll** (common when the command finishes in <15s):
```
✅ CI: run #12345 — completed before first poll
Output: <last output from exec result in the system event>
```
In this case, the exec result may arrive as a system event in the main session. Read it from there and deliver it directly — no need for the poller at all.

If your runtime keeps completed agents around until you explicitly tear them down, close them at this point too. In Codex, a completed subagent should be `close_agent(id)`'d after its result has been delivered unless you are intentionally keeping it for reuse.

**Error (process not found / session lost):**
```
❌ CI: run #12345 — session not found (process may have exited before poll; check last system event for output)
```

---

## State File Format

**Path:** `<workspace>/skills/shark/shark-exec/state/pending.json`

```json
{
  "jobs": [
    {
      "sessionId": "sess-abc-123",
      "label": "CI: run #12345",
      "command": "gh run watch 12345",
      "startedAt": 1710000000000,
      "maxSeconds": 120,
      "cronJobId": "cron-xyz-456"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `sessionId` | string | From exec response (or PID for non-OpenClaw runtimes) |
| `label` | string | Human-readable name shown in ack/result |
| `command` | string | The shell command that was run |
| `startedAt` | number | `Date.now()` at launch time (ms) |
| `maxSeconds` | number | Kill threshold (default: 120) |
| `cronJobId` | string\|null | Poller/cron job ID for cleanup; null until created |

The state file format is **agent-agnostic** — any runtime adapter can read and write it.

---

## maxSeconds Defaults

| Command type | Suggested maxSeconds |
|---|---|
| `gh run watch` | 300 (CI can be slow) |
| `npm run build` | 180 |
| `docker build` | 600 |
| `pytest` / `cargo test` | 300 |
| Generic unknown | 120 |
| User-specified | Honor their request |

If the user says "wait up to 10 minutes", use `maxSeconds: 600`.

---

## Multiple Concurrent Jobs

If there's already a poller running (check `cronJobId` in any existing job in pending.json), **do not create a new poller**. Just add your new job to the array. The existing poller will pick it up on its next tick.

Algorithm:
1. Read pending.json
2. If `jobs.length > 0` and any job has a non-null `cronJobId` → reuse that cronJobId, just append new job
3. If `jobs.length === 0` or all `cronJobId` are null → create a new poller, then update state

---

## Runtime Adapters

### OpenClaw
- Background exec: `exec({background: true, yieldMs: 500})`
- Poll: `process({action: "poll", sessionId: X, timeout: 5000})`
- Schedule: `cron({action: "add", schedule: {kind: "every", everyMs: 15000}, ...})`
- Notify: `message({action: "send", target: "<your notification channel>", message: "..."})`

### Claude Code / claude --print
- Background exec: `Bash("command &")` + capture PID
- Poll: `Bash("kill -0 <pid> && cat /tmp/output-<pid>.txt")`
- Schedule: not native — use a wrapper script or OS cron
- Notify: write result to stdout (caller receives it)

### Codex (openai/gpt-5-codex)
- Background exec: `shell("command &")` + PID
- Poll: `shell("ps -p <pid>; cat /tmp/out-<pid>.txt")`
- Schedule: OS cron or a watcher script
- Agent remoras: `spawn_agent(...)` → `wait_agent(...)` → deliver result → `close_agent(id)` unless you are intentionally reusing that same agent

### Cursor / Windsurf / Aider
- Background exec: terminal background process (`&` or `Start-Job` on Windows)
- Poll: check process status + output file
- Schedule: OS-level cron or task scheduler

---

## Error Handling

### Poll throws "session not found"
→ Remove the job from pending.json, send:
`❌ [label] — session lost (process may have crashed or the exec session expired)`

### Completed agent still hanging around
→ If the work is done and the runtime still shows the subagent as open, close it as part of delivery cleanup. In Codex, use `close_agent(id)` after a completed `wait_agent(...)` unless you plan to reuse that agent.

### Output is very long
→ Truncate to last 50 lines. Always append truncation notice:
`[output truncated — showing last 50 lines of N total]`

### pending.json is corrupted/invalid JSON
→ Reset to `{"jobs": []}`, send:
`⚠️ shark-exec: pending.json was corrupted and has been reset. Background jobs may have been lost.`

### exec returns no handle/sessionId
→ Fall back to inline exec. Do not use shark-exec for that command.

---

## Full Example: Replacing `gh run watch`

### ❌ Old (blocking) way:
```
exec("gh run watch 12345")
// Agent blocks for 3 minutes, user gets no reply
```

### ✅ New (shark-exec) way:

**Turn 1 (main agent):**
1. Send: `⏳ CI: run #12345 — watching in background (max 300s)...`
2. Launch background: `exec("gh run watch 12345", background=true, yieldMs=500)` → `sessionId: "sess-9f3a"`
3. Write to pending.json:
   ```json
   {
     "jobs": [{
       "sessionId": "sess-9f3a",
       "label": "CI: run #12345",
       "command": "gh run watch 12345",
       "startedAt": 1710005200000,
       "maxSeconds": 300,
       "cronJobId": null
     }]
   }
   ```
4. Create poller (every 15s, using your agent's scheduler) → `cronJobId: "cron-8b2c"`
5. Update pending.json with `cronJobId: "cron-8b2c"`
6. **Main turn ends. User got their reply in <5s.**

**~47 seconds later (poller fires 3 times, 3rd time it's done):**
1. Poller reads pending.json → finds `sess-9f3a`
2. Poll process `sess-9f3a` → status: completed, output: "Run #12345 completed: success"
3. Sends result to user:
   ```
   ✅ CI: run #12345 completed (47s)

   Run #12345 (main / push) · Completed successfully
   Jobs: build ✓, test ✓, deploy ✓
   ```
4. Closes the finished handle if the runtime requires explicit cleanup
5. Removes job from pending.json → jobs array empty
6. Cancels poller `cron-8b2c`

---

## Quick Reference Checklist

Before every long-running command:
- [ ] Will this take >5s? → Use shark-exec
- [ ] Send ack message **first**
- [ ] Launch in background (see Runtime Adapters)
- [ ] Write to pending.json
- [ ] Create or reuse poller
- [ ] Update cronJobId in state
- [ ] Close completed agents/handles if the runtime requires explicit cleanup

---

## Helper Script

`scripts/poll-and-deliver.js` — run to inspect current pending jobs:

```bash
node <workspace>/skills/shark/shark-exec/scripts/poll-and-deliver.js
```

Prints a human-readable summary of all pending jobs, their ages, and whether they're past maxSeconds. Useful for debugging stuck jobs.

> **Note:** This script is the OpenClaw adapter. For other runtimes, implement equivalent polling using your platform's APIs (see Runtime Adapters above).
