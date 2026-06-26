---
name: responsive-agent
version: 1.8.0
description: "Responsive Agent Pattern for OpenClaw agents. Two-layer architecture: (1) main process never blocks — always spawn subagent for any blocking/remote/long operation, (2) subagent handles execution via exec+yieldMs for long local commands. Origin: based on session-coordinator v3, merged with async-command patterns. Core rule: main process must never block. Use when: (1) agent should stay responsive at all times, (2) long/uncertain operations must not block the main session, (3) multi-node coordination requires clear separation between dialog/dispatch (main) vs execution (subagent). Triggers on: async mode, main process blocking, spawn decision, long operation handling.
---

# Responsive Agent Skill v1.8.0 — Two-Layer Async Architecture

> Origin: Based on session-coordinator v3, merged with async-command patterns.

---

## Quick Reference

### Spawn Decision (binary — exec OR spawn, nothing else)

```
Is it fast (<1s) AND local AND same topic AND no network I/O AND read-only?
  → YES: exec directly in main process, respond
  → NO:  spawn subagent immediately
```

### yieldMs vs timeout (for subagent exec calls)

| Command duration | yieldMs | exec timeout |
|-----------------|---------|-------------|
| < 5s, need sync result | none (exec directly) | 10 |
| 5–30s | 5000 | 60 |
| > 30s, async ok | 10000 | 300 |
| Unknown duration | 30000 | 600 |

- **yieldMs** = wait-before-background threshold. If command exceeds yieldMs, it gets backgrounded automatically.
- **timeout** = hard kill after N seconds. Must be > yieldMs.
- To run sync: set timeout large, yieldMs = timeout (or omit yieldMs).
- To run async: set yieldMs small, timeout = estimated + buffer.

### Subagent Error Strategy

On exec failure: log → write `workspace/tasks/{task-id}/error.md` → reply to parent. No retry. Fail-fast.

---

## Two-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: MAIN PROCESS (never blocks)                   │
│  dialog + dispatch only — spawn everything else         │
└─────────────────────────────────────────────────────────┘
                         │
                    spawn ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 2: SUBAGENT (executes tasks)                     │
│  exec + yieldMs for long local commands                 │
└─────────────────────────────────────────────────────────┘
```

**Rule: Main process never blocks. Subagent never hangs.**

---

## Core Principle

**Main process = dialog + dispatch. Never block.**

The main goal is responsiveness — the main process must never be blocked, stalled, or made unresponsive. This is not "never execute." It is "never block."

A blocked main process shows as: typing indicator disappears, user cannot get a response, session appears frozen.

---

## Resource Limits

**Max concurrent subagents per main process: 5**

### Tracking and Queueing

- When user fires rapid requests: spawn a new subagent for each
- Track concurrent count internally
- **If count > 5**: reply "任务已加入队列，等前一个完成后自动开始" and queue the task

### Nested Spawn — Subagent Spawning Subagent

- The 5 concurrent subagent limit applies to **top-level subagents only** (direct children of the main process)
- **Nested subagents** (subagent's children) do **not** count toward the 5-slot limit
- **Rationale**: recursive task decomposition forms a DAG, not a tree — counting all levels would artificially limit deep task decomposition
- **Warning**: nested spawn should still be used sparingly — too many levels makes debugging hard

### Queue Processing

- Queue is FIFO (first in, first out)
- When a running subagent completes, start the next queued task
- Main process manages the queue — no user action needed

### Queue Priority

**Detailed priority queue implementation:**

- Main process maintains a queue dict with fields:
  - `{label, task, priority: "high"|"normal", timestamp}`
- On new spawn request:
  - If priority=high AND queue has no existing high-priority: insert at position 0, shift others back
  - If queue already has 1 high-priority: add after it (slot taken)
  - If priority=normal: add to end (FIFO)
- On subagent completion: start next in queue (high-priority first, then oldest normal)
- Reply to user: "已加入高优先级队列" or "已加入队列（第 N 位）"

**Concurrent high-priority conflict:**
When two high-priority tasks arrive simultaneously:
1. Both are marked high-priority
2. They are ordered by arrival timestamp (first-come, first-served within priority)
3. The earlier one gets slot 1, the later one waits
4. Reply to second user: "已有1个高优先级任务在排队，已加入队列（第2位）"
- Queue insertion is atomic per arrival — no race condition
- If same timestamp (very rare): use lexicographic label order as tiebreaker

**High-priority flag:** If user says "紧急" or "priority":
  - Mark task as high-priority
  - Reply: "已加入高优先级队列"
- High-priority queue slot is limited: max 1 high-priority task ahead of normal queue at a time

### Memory/CPU

- Subagent inherits main process limits — no extra quotas needed for OpenClaw context
- OS-level resource management handles overall system load

---

## When Is a Command "Long"? — Practical Thresholds

Use this to decide whether to exec directly or spawn:

| Duration | Type | Action |
|----------|------|--------|
| < 3s, known fast | local read, simple computation | exec directly in main process |
| 3–10s | local with uncertain load | exec with `yieldMs=3000`, `timeout=15` |
| > 10s or unknown | any remote, any build, any unknown | spawn subagent |

**Rule: "When in doubt, spawn."**

Specifically:
- **Any remote operation** (SSH, API call, HTTP) = long → spawn
- **Any operation with uncertain duration** = long → spawn
- **Any state-modifying operation** (write, commit, deploy) = long → spawn

**Quick decision tree:**
```
Is it < 3s AND local AND known-fast AND read-only?
  → YES: exec directly
  → NO:  spawn subagent
```

---

## Decision Framework

### Layer 1 — Main Process Spawn Decision Tree (mechanical)

When a request arrives at the main process, answer these questions in order:

```
Q1: Is it a FAST local read (<1s)?
    - No read I/O, no network, same topic, read-only?
    → YES: exec directly in main process, respond now
    → NO:  proceed to Q2

Q2: Is it ANY of the following?
    - Remote / network / SSH / HTTP
    - git push / pull / clone
    - Unknown duration
    - Different topic from current conversation
    - State-modifying (write, commit, deploy, publish)
    → YES: spawn subagent immediately
    → NO:  still spawn (conservative — when in doubt, spawn)
```

**Binary rule: if you hesitated on any Q, spawn.**

### Context Passing ("Continue from Above")

When user says "接着上面的" or "continue from above":

**Implementation method:**
1. Main process uses exec to read the previous task.md:
   ```
   exec(command="cat workspace/tasks/{task-id}/task.md", timeout=5)
   ```
2. Alternative for quick lookup: `memory_search` on the task-id
3. Main process copies the relevant context into the new spawn task description
4. New subagent receives a complete task description including the prior context

**Result:** New subagent can continue from where it left off.

- The task.md file at `workspace/tasks/{task-id}/task.md` is the continuity mechanism
- Main process is responsible for maintaining context, not the subagent

**Always spawn (never exec in main process):**
- Remote operations (SSH, remote API calls, HTTP)
- git push/pull/clone
- Any network I/O
- Unknown duration
- Different topic from current conversation
- State-modifying operations (file write, git commit, package publish, deploy)
- Anything requiring waiting for external result

**Main process never executes long commands. It only spawns.**

### Layer 2 — Subagent Execution Pattern

Inside a subagent, use `exec + yieldMs` for commands that may take time:

```json
// Short local command (<1s): exec directly, no yield needed
exec(command="ls /tmp")

// Long local command (5-30s): exec + yieldMs
exec(command="some-long-operation.sh", yieldMs=5000, timeout=60)

// Long command (>30s, async ok): exec + yieldMs
exec(command="moderate-build.sh", yieldMs=10000, timeout=300)

// Unknown duration: exec + yieldMs + large timeout
exec(command="unknown-task.sh", yieldMs=30000, timeout=600)

// Very long command: exec + background + poll
exec(command="very-long-build.sh", background=true, yieldMs=60000, timeout=3600)
```

**yieldMs = how long to wait before backgrounding.** If the command finishes within yieldMs, result is returned directly. If not, it is backgrounded and result arrives via push.

### ⚠️ yieldMs WARNING — Result Loss Risk

**If you need the result, yieldMs must be LARGER than estimated command duration.**

| Scenario | Problem | Correct |
|----------|---------|---------|
| yieldMs=5000, command takes 8s | Command bg'd BEFORE completing, result may be lost | Set yieldMs >= 8000 |
| yieldMs=10000, command takes 45s | Command completes normally, result returned | ✅ correct |
| yieldMs=5000, command takes 4s | Command completes normally, result returned | ✅ correct |

**Rule:**
- **Need the result?** → yieldMs >= estimated_duration
- **Fire-and-forget (don't need result)?** → yieldMs can be small (5000–10000ms)

---

## background=true vs yieldMs — What's the Difference?

These are two different mechanisms for handling long commands. They are **not** the same.

| | `yieldMs` | `background=true` |
|--|-----------|--------------------|
| **What it does** | Waits N ms before backgrounding, but process is still *attached* — result will eventually come back via push | Truly detaches the process — runs independently, no result returned unless you poll |
| **Result delivery** | ✅ Result arrives via push when done | ❌ No automatic result — detached |
| **Use when** | You need the result eventually | You explicitly need NO result (pure fire-and-forget) |

### If BOTH are set

If you set both `background=true` AND `yieldMs`:

1. `yieldMs` takes precedence initially — the command waits up to yieldMs milliseconds before being backgrounded
2. After yieldMs elapses, `background=true` kicks in — the process is truly detached
3. Result will **not** come back via push (background=true overrides the attached behavior)

### Decision Rule

| Scenario | Use |
|----------|-----|
| Need the result | `yieldMs` (set >= estimated duration) |
| Explicitly need NO result (pure fire-and-forget) | `background=true` |
| Most cases | `yieldMs` (not `background=true`) |

```json
// ✅ Need result — use yieldMs
// Inside subagent:
exec(command="analysis-script.sh", yieldMs=30000, timeout=120)

// ✅ Explicitly need NO result — use background=true
// Inside subagent:
exec(command="ping -c 100 remote-host", background=true)
// Result: none, process runs independently
```

**Rule of thumb:** Default to `yieldMs`. Use `background=true` only when you explicitly need the process to be truly detached with no result expected.

---

## yieldMs and exec timeout — Complete Reference

### The relationship

- **`yieldMs`**: wait time before backgrounding. If command takes longer than yieldMs, it goes to background automatically.
- **`timeout`**: hard kill after N seconds. Command is killed if it exceeds this.
- **Rule**: `yieldMs < timeout` always. yieldMs is the backgrounding threshold; timeout is the hard limit.

### When to use each

| Command duration | yieldMs | timeout | Strategy |
|-----------------|---------|---------|----------|
| < 5s, sync result needed | none (exec directly) | 10 | No yieldMs needed — exec direct |
| 5–30s | 5000 | 60 | yieldMs = wait-before-bg, timeout = hard limit |
| > 30s, async ok | 10000 | 300 | yieldMs small → bg quickly, timeout allows completion |
| Unknown duration | 30000 | 600 | Conservative — bg after 30s, kill at 10min |
| Very long (>10min) | 10000 | 3600 | yieldMs=10s for responsiveness, long timeout for completion |

### Sync vs async decisions

**Want result synchronously (wait in subagent until done)?**
- Set `yieldMs = timeout` (or omit yieldMs, use timeout only)
- Example: `exec("short-task.sh", timeout=30)` — waits up to 30s, returns result

**Async is fine (background immediately)?**
- Set `yieldMs` small (e.g., 5000–10000ms)
- Example: `exec("long-task.sh", yieldMs=5000, timeout=300)` — bg after 5s, result via push

---

## Subagent Error Strategy

When an exec call fails inside a subagent:

1. **Log the error** — capture stdout, stderr, exit code
2. **Create directory** — `mkdir -p workspace/tasks/{task-id}` (subagent's responsibility)
3. **Write error file** — `workspace/tasks/{task-id}/error.md`
4. **Reply to parent** — always report back to main process, even on failure

**Error file format** (`workspace/tasks/{task-id}/error.md`):
```markdown
# Subagent Error Report

- Task: [task description]
- Timestamp: [ISO timestamp]
- Exit code: [N or "signal"]
- Command: [what was run]

## stdout
[output]

## stderr
[error output]

## Analysis
[brief root cause if known]
```

**Key principles:**
- No automatic retry (fail-fast per ClawFlow principle)
- Subagent never silently dies — always replies to parent
- Main process decides whether to respawn or report failure to user

**error.md cleanup strategy:**

- error.md files are persistent audit trail — do NOT auto-delete
- They serve as historical record of what went wrong
- **Trigger:** during weekly memory maintenance (HEARTBEAT.md check)
- **Who:** main process runs the scan during HEARTBEAT
- **Script:**
  1. Scan `workspace/tasks/*/error.md`
  2. If file age > 30 days AND task is resolved: move to `workspace/tasks/archive/{year}/{task-id}/error.md`
  3. If total tasks/ directory > 1GB: report to user "tasks/ 目录超过 1GB，建议手动清理"
- **This is NOT automatic deletion — archive only, never delete**

**Directory creation:** Before writing any files (error.md or temp results), the subagent **must** create the directory:
```bash
mkdir -p workspace/tasks/{task-id}   # for error files
mkdir -p workspace/temp/{task-id}    # for large results
```
This is the subagent's responsibility, not the main process's.

---

## Subagent Reply to Parent

When a subagent completes (success or failure), it must reply to its parent session — it does **not** use `sessions_yield`. The subagent session key is known at spawn time; use it to send the final result directly.

**Result format:** brief summary of what was done, file paths if any (not raw large data).

```json
// Subagent sends result back to parent via message tool (channel send)
message(action="send", target="{parent_session_key}", message="Task complete. Files written: workspace/temp/{task-id}/result.txt")
// Subagent then terminates normally — no sessions_yield needed
```

**When to reply:**
- Always — success, failure, or error. Parent must hear back.
- Keep the message brief. If large data was produced, reply with the **file path**, not the raw content.

**Key point:** Subagent does NOT use `sessions_yield` — it terminates normally after sending the result via `sessions_send`.

### Spawn Failure Fallback

If spawning a subagent fails (system error):

1. **Reply to user**: "系统繁忙，请稍后再试"
2. **Log the failure**: create dir `mkdir -p workspace/mailbox/errors/` then write to `workspace/mailbox/errors/{timestamp}-spawn-fail.md`
3. **Do NOT retry** within the same session (fail-fast to prevent loop)

**Error log format**:
```markdown
# Spawn Failure Report
- Timestamp: [ISO timestamp]
- Task: [task description]
- Reason: [system error message if known]
```

---

## Spawn Mode v3 — Default: session thread

**Default spawn mode is `mode="session"` with `thread=true`.**

### thread=true vs thread=false vs mode="run"

| Mode | thread | Behavior | Use When |
|------|--------|----------|----------|
| `mode="session"` | `thread=true` | **Persistent conversation** — context is preserved across messages, multi-turn dialog possible | Multi-step tasks, tasks where user may ask follow-up questions, uncertain scope |
| `mode="session"` | `thread=false` | **New session each time** — context is NOT preserved, each spawn starts fresh. Subagent sends ONE final result push when done, then the session is closed. Cannot receive additional messages in the same thread. | Fire-and-forget tasks with bounded scope, no follow-up expected |
| `mode="run"` | N/A | **Detached, no session** — truly fire-and-forget, no result push | Rare; avoid unless you explicitly need detached execution |
| `mode="one-shot"` | N/A | **Does not exist in OpenClaw.** Was considered but removed. | Use `mode="session"` + `thread=false` for bounded fire-and-forget. |

**Both `thread=true` and `thread=false` receive the result via push mechanism.** The difference is whether the session stays open afterward:
- `thread=false`: session created but closed after final result push — one-shot, no follow-up
- `thread=true`: session stays alive, can receive multiple messages across turns

### Decision Guide

**"Is this a multi-step task or does the user expect follow-up?"**
- YES → `mode="session"` + `thread=true`
- NO, just do this one thing → `mode="session"` + `thread=false` (fire-and-forget)
- NO, but I explicitly need detached → `mode="run"`

```json
// ✅ Multi-step task — context preserved, user may ask follow-up
sessions_spawn(task="debug service issue, may need to run multiple commands", 
               runtime="medium", label="service-debug")

// ✅ Fire-and-forget — bounded scope, no follow-up expected
sessions_spawn(task="restart the backup service on remote node", 
               runtime="fast", label="backup-restart")

// ⚠️ Run mode — only when you explicitly need detached, no result push
sessions_spawn(task="background health check", runtime="fast", label="health-bg", mode="run")
```

**Note:** `thread=false` still creates a session (unlike `mode="run"`), so you get result push — but the subagent starts with a fresh context, no history from previous related spawns.

- Use `mode="session"`, `thread=true` for most tasks (interactive, multi-step, or uncertain duration)
- Use `mode="session"`, `thread=false` for fire-and-forget tasks with bounded scope
- Avoid `mode="run"` unless you explicitly need detached/no-result (it provides no result push)

```json
// ✅ Default: session thread (most tasks)
sessions_spawn(task="task-description", runtime="medium", label="task-label")

// ✅ Fire-and-forget: bounded scope, fresh context each time
sessions_spawn(task="task-description", runtime="fast", label="task-label")

// ⚠️ Avoid: run mode provides no result push — use only when detached is explicitly needed
sessions_spawn(task="task-description", runtime="fast", label="task-label", mode="run")
```

---

## Timeout Guidelines

### runtime vs exec timeout — Clarification

- **runtime** (fast/medium/long) and **exec timeout** are independent
- **runtime** = spawn-level timeout — how long the entire subagent session is allowed to run
- **exec timeout** = command-level timeout — how long a specific exec call waits
- If runtime=medium (15min) but exec timeout=3600s:
  - The exec will be killed if it runs longer than 3600s
  - The subagent itself will be killed if ALL its work exceeds 15min
  - They don't conflict — runtime is the outer limit, exec timeout is inner protection
- **Rule**: exec timeout should always be <= runtime, otherwise exec will be killed by runtime first
- **runtime=fast (5min) + large exec timeout (3600s)**: exec will be killed when the subagent's runtime timeout fires at 5 minutes, regardless of exec timeout. The outer runtime limit always wins. To avoid confusion: set exec timeout significantly smaller than runtime (e.g., runtime=fast, exec timeout=60–300)

### runtime Tiers

Use these as a guide to set `runtime` when spawning:

| Tier | Duration | Examples |
|------|----------|----------|
| **fast** | ~5 min | file ops, single API call, config check, quick test |
| **medium** | ~15 min | git operations, moderate build, moderate data processing |
| **long** | 60 min+ | large clones, heavy builds, multi-step deployments, data migration |

```json
// Fast task — 5 min timeout
sessions_spawn(task="check service status", runtime="fast", label="service-status-check")

// Medium task — 15 min timeout
sessions_spawn(task="clone repository and run tests", runtime="medium", label="repo-test")

// Long task — 60 min timeout
sessions_spawn(task="full deployment pipeline", runtime="long", label="deploy-pipeline")
```

---

## Spawn Label Convention

When spawning a subagent, **always include a descriptive `label` parameter**:

- Use dashes, not spaces (e.g., `project-config-sync` not `project config sync`)
- Use generic, descriptive names only — never specific project names, IPs, hostnames, or user names
- Label should reflect the actual task category or action
- **Rule: Does this label reveal anything about the user's private data?** If yes, change it.

### Label Examples

**GOOD labels (functional, generic):**
```python
label="config-sync"           # what it does, not which project
label="log-review"             # functional category
label="deploy-check"           # what it checks, not which environment
label="service-health"         # generic health check
label="backup-status"         # generic backup check
label="build-verify"           # what it verifies
```

**BAD labels (specific identifiers, reveal private data):**
```python
label="192.168.1.1"             # ❌ specific IP — privacy leak
label="ken-task"               # ❌ specific user name — privacy leak
label="fix-123"                # ❌ specific bug number — reveals internal tracking
label="proj-zeta"              # ❌ specific project codename
label="john-doe-deploy"        # ❌ specific person + action
label="acme-corp-sync"         # ❌ specific company name
```

**Generic placeholder rewrites:**
- `192.168.x.x` → `remote-host` or `node-alpha`
- `user@host` → `admin-user` or `service-account`
- `project-name` → `repo-name` or `project-alpha`
- `bug-123` → `bugfix-verify` or `issue-check`

```json
// ✅ Good: generic, dashes, descriptive
sessions_spawn(task="sync config to remote node", label="config-sync")
sessions_spawn(task="run test suite for module", label="test-suite")
sessions_spawn(task="deploy service to environment", label="service-deploy")

// ❌ Bad: spaces, specific names, cryptic
sessions_spawn(task="...", label="proj1")           // too short, no dashes
sessions_spawn(task="...", label="192-168-1-1")     // specific IP — not allowed
sessions_spawn(task="...", label="johns-task")      // specific user name — not allowed
sessions_spawn(task="...", label="foo-bar-v2")      // specific project codename — not allowed
```

When the user says "stop that thing", look at `subagents list` and match the label to find the right subagent to stop.

---

## Parallel Subagent Pattern

When a task requires multiple independent subagents running simultaneously:

1. Main process spawns all subagents at once (they run in parallel)
2. Each subagent runs independently, sends result to parent via sessions_send
3. Main process collects results as they arrive (push-based)
4. When all results are in, main process synthesizes and replies to user

**Data sharing**: each subagent writes its result to its own subdirectory `workspace/tasks/{parent-task-id}/{subagent-label}/result.txt`

**Result gathering**: results are collected after ALL subagents complete (not streaming). Main process reads all result files and synthesizes.

**This is fan-out pattern, not DAG dependency pattern** — all subagents are independent and start at the same time.

### Parallel Completion Detection (Join/Barrier Mechanism)

Main process needs a way to know when ALL parallel subagents are done:

**Mechanism: counter-based tracking**
- Main process maintains a counter: `remaining = N` (number of parallel subagents)
- Each subagent result arrival via push decrements counter
- When `remaining == 0`: all done, synthesize and report to user

**Implementation:**
- Main process tracks results in a dict keyed by subagent label
- Each push event: check if all results received, if yes → synthesize

**Example:**
```
parallel subtasks: [agent-a, agent-b, agent-c]
remaining = 3
→ agent-a pushes result: remaining = 2
→ agent-c pushes result: remaining = 1  
→ agent-b pushes result: remaining = 0 → all done, synthesize
```

### Concurrent Write Warning

**⚠️ Warning:** multiple subagents writing to the same parent directory is safe IF they write to DIFFERENT subdirectories (each subagent has its own `{subagent-id}/`).

**Rule:** each subagent writes ONLY to its own `workspace/tasks/{parent-task-id}/{subagent-label}/`
- Subdirectory is created per subagent, no shared files
- If two subagents try to write the same file: this is an error — use unique subdirectory names

### Parallel Subagent Labels

Use a common prefix for parallel subagent labels so they can be cancelled together:

```json
// Good: prefix-based naming for parallel tasks
sessions_spawn(task="check weather for location", runtime="fast", label="parallel-check-1")
sessions_spawn(task="check email inbox for urgent messages", runtime="fast", label="parallel-check-2")
sessions_spawn(task="check calendar for upcoming events", runtime="fast", label="parallel-check-3")
```

```json
// Example: user asks "check weather + email + calendar"
// Main process spawns 3 subagents in parallel:
sessions_spawn(task="check weather for location", runtime="fast", label="parallel-check-1")
sessions_spawn(task="check email inbox for urgent messages", runtime="fast", label="parallel-check-2")
sessions_spawn(task="check calendar for upcoming events", runtime="fast", label="parallel-check-3")

// Each subagent writes its result to:
// workspace/temp/{task-id}/parallel-check-1.txt
// workspace/temp/{task-id}/parallel-check-2.txt
// workspace/temp/{task-id}/parallel-check-3.txt

// Main process waits for all 3 results, then synthesizes and replies
```

### Parallel Subagent Failure Handling

**Rule: partial results are better than no results — never waste succeeded work.**

If one or more parallel subagents fail:

1. **Mark as failed** — the failed subagent writes its error to `workspace/tasks/{task-id}/error.md` and replies to parent
2. **Continue waiting** — do NOT cancel remaining subagents when one fails; wait for all to complete
3. **Synthesize partial results** — after all done, main process reads available result files and synthesizes
4. **Report to user** — "[X] failed, [Y] succeeded. Partial results: ..." with whatever succeeded
5. **If ALL failed** — report total failure with error summary from all failed subagents

**Example:**
```
User: check weather + email + calendar
→ 3 subagents spawned (parallel-check-1, parallel-check-2, parallel-check-3)
→ parallel-check-1 (weather): succeeded → weather-check.txt
→ parallel-check-2 (email): failed → error.md written, reply sent
→ parallel-check-3 (calendar): succeeded → calendar-check.txt

Main process synthesizes: 1 failed, 2 succeeded.
Reply: "2/3 succeeded. Weather: sunny, 22°C. Calendar: meeting at 3pm. Email check failed — see error log."
```

---

## Large Results

**If subagent produces > 1MB of data**, write to file instead of returning raw:

1. **Write result to**: `workspace/temp/{task-id}/result.txt`
2. **Reply to parent**: pass the **file path** (not the raw content)
3. **Main process**: reads the file path and reports to user

**Example:**
```json
// Large output scenario
exec(command="git diff --name-only", yieldMs=10000, timeout=60)
// Result: 50MB of file names → write to file instead

// Correct approach:
// 1. subagent writes to workspace/temp/{task-id}/result.txt
// 2. subagent replies with file path
// 3. main process reads path, reports to user
```

**Cleanup:** temp files are ephemeral — OS handles cleanup on reboot. No manual cleanup needed.

---

## Subagent Lifecycle

**Normal duration:** seconds to minutes depending on task complexity.

### Duration Guidelines

| Task Type | Expected Duration | Action |
|-----------|------------------|--------|
| Fast local reads | < 1s | exec direct in main |
| Simple operations | seconds | subagent |
| Multi-step tasks | minutes | subagent |
| Build/clone/deploy | minutes to hours | subagent with appropriate timeout |

### Long-Running Subagent Monitoring

- Subagent running **> 10 minutes** without update: check status via `subagents list`
- No automatic kill — let it finish unless user cancels
- If subagent appears stalled after > 10min without result, report to user

### Subagent Completion

- Subagent completion: **auto-replies to parent** when done (via push mechanism)
- Parent receives result and reports to user
- No polling needed — completion is push-based

### Long Task Progress Reporting

- For very long tasks (>5 min), subagent can optionally send interim progress to parent
- Progress format: brief message like "Step 2/5 complete, moving to step 3"
- Subagent sends progress via sessions_send to parent (same as final result, just multiple pushes)
- Main process relays progress to user if user asks "how's it going?"
- **Rule**: do NOT proactively push progress to user — only send to parent, relay on demand
- This adds complexity, only implement if the task explicitly supports it

---

## Lifecycle Management

### Auto-Timeout

- Subagents run with a defined `runtime` timeout (fast/medium/long)
- If the subagent exceeds its timeout without a result, it is considered stalled
- Do NOT manually extend timeouts unless user explicitly asks

### Done Signals

A subagent can be safely let timeout (or can terminate early) when:

1. **user says "done"** — user has indicated the task is complete or no longer needed
2. **Context switches** — user has moved to a different topic or task; the previous subagent is no longer relevant
3. **Explicit cancel** — user says "stop", "cancel", "forget it"

### What to do when done signal fires:
- Do NOT try to salvage a timed-out subagent
- Do NOT restart the same task unless user explicitly asks
- Acknowledge the signal and move on

---

## Memory Updates

**After subagent completes:** if the task resulted in a **decision, config change, or state change**, update `MEMORY.md`.

### When to Update MEMORY.md

| Result Type | Update MEMORY.md? | Example |
|-------------|------------------|---------|
| Trivial/ephemeral | ❌ No | "checked service status", "file exists" |
| Decision made | ✅ Yes | "decided to use strategy X over Y because..." |
| Config changed | ✅ Yes | "updated timeout from 30s to 60s" |
| State change | ✅ Yes | "moved from manual to automated backup" |
| Lesson learned | ✅ Yes | "found that approach A fails in scenario X" |
| Important output | ✅ Yes | "discovered key info about..." |

### Update Format

```markdown
## [Date] Task Result
- Task: [brief description]
- Outcome: [what happened]
- Key decision/learning: [why this matters]
```

**Main process handles MEMORY.md writes** — subagent reports the result, main process decides whether to write it down.

---

## Result Writing

### Daily logs → memory/YYYY-MM-DD.md

Routine subagent work should be logged in the daily memory file:

```bash
# Create/update daily log
memory/2026-04-06.md
```

Include: task label, what was done, key result. Keep it concise.

---

## Spawn Is Transparent

**Do not announce to user when you are spawning a subagent.**

- Do NOT say "I'm spawning a subagent to handle this..."
- Do NOT say "Let me dispatch this to a background agent..."
- Just spawn it and continue the dialog naturally

User does not need to know the execution architecture. The subagent handles the work; you handle the conversation.

---

## Role Definition

| Responsibility | Main Process | Subagent |
|----------------|-------------|----------|
| User dialog | ✅ | ❌ |
| Task dispatch | ✅ | ❌ |
| Result production | ❌ | ✅ |
| Result delivery to user | ✅ | ❌ |
| Decision making | ✅ | ❌ |
| Status coordination | ✅ | ❌ |
| Fast local operations (<1s) | ✅ | ❌ |
| Blocking / remote / long operations | ❌ | ✅ |
| exec + yieldMs for long local commands | ❌ | ✅ |

---

## Execution Model

### Blocked = Wrong

If the main process blocks, the pattern has failed — regardless of whether the task eventually completes.

### Two-Layer Flow

```json
// Layer 1: Main process — always spawn for non-trivial work
// ❌ Wrong — blocks main process, typing disappears
exec(command="ssh remote-host ...")

// ✅ Correct — non-blocking, typing stays active
sessions_spawn(task="remote operation description", runtime="medium", label="remote-task")

// Inside the spawned subagent (Layer 2):
// ✅ exec + yieldMs for long local command
exec(command="some-long-local-script.sh", yieldMs=10000, timeout=300)

// ✅ exec + background for very long commands
exec(command="very-long-build.sh", background=true, yieldMs=60000, timeout=3600)
```

After spawning: continue dialog with user. Do NOT wait. Results arrive via push event.

### Fire-and-Forget

- Spawn with full task description and runtime estimate
- Do NOT estimate how long it takes
- Do NOT poll for status
- Continue dialog
- Report result when delivered

---

## Multi-Node Coordination

Each node runs its own subagents. Nodes do not delegate to each other's subagents. Coordination between nodes goes through whatever inter-node protocol is configured for that setup.

---

## User Cancellation Protocol

When the user says **"停" / "stop" / "取消"**:

1. **Check `subagents list`** — find all active subagents
2. **Match label** — if parallel subagents share a common prefix (e.g., `parallel-check-1`, `parallel-check-2`, `parallel-check-3`), match by prefix to catch ALL of them
3. **Send SIGTERM** — graceful termination to all matched subagents (max 5 seconds)
4. **Wait up to 5 seconds** — if still running, send SIGKILL (hard kill)
5. **Reply to user** — "已停止全部 {n} 个并行子任务" (for parallel) or "已停止 `{label}`" (for single)
6. **Log cancellation** — write to workspace:
   ```markdown
   # Subagent Cancellation Log
   - Label: {label}
   - Cancelled by: user
   - Timestamp: {ISO timestamp}
   - Result: SIGTERM → SIGKILL (or SIGTERM only if clean exit)
   ```

**Example flow (single subagent):**
```
User: 停！
Agent: (subagents list) → finds label="config-sync"
       (kill config-sync subagent)
       "已停止 config-sync"
```

**Example flow (parallel subagents):**
```
User: 停！
Agent: (subagents list) → finds parallel-check-1, parallel-check-2, parallel-check-3
       (kill all 3 subagents with prefix "parallel-check")
       "已停止全部 3 个并行子任务"
```

**Do NOT return partial results when user cancels** — assume clean stop is wanted.

**Rule:** Always reply confirming which subagent was stopped. Never silently ignore a cancellation request.

### Done Signals (Graceful Termination)

| Signal | Meaning | Behavior |
|--------|---------|----------|
| **SIGTERM** | Graceful termination | Finish current step, then exit (max 5 seconds) |
| **SIGKILL** | Forced termination | Exit immediately, no cleanup |

**When to use SIGKILL:** Only when user explicitly says "强制停止" or "kill" (kill, not stop/cancel).

---

## Real-World Templates

### Template: ClawHub Rate-Limit Wait
When ClawHub returns 429 Too Many Requests:

```json
sessions_spawn(
  task="Install or publish skill to ClawHub, handling rate limits. If 429 received, wait Retry-After seconds then retry. Max 3 attempts.",
  label="clawhub-ops"
)
```

Inside the subagent:
1. First attempt: run clawhub command
2. If 429: extract Retry-After header (e.g., 60 seconds)
3. exec(command="sleep {Retry-After}", yieldMs={Retry-After * 1000 + 1000}, timeout={Retry-After + 10})
4. Second attempt: retry the clawhub command
5. If still 429 after 3 attempts: write error.md, reply to parent with failure

### Template: GitHub Rate-Limit Wait
When GitHub API returns 403 with "rate limit exceeded":

```json
sessions_spawn(
  task="GitHub API operation, handle rate limits. If 403 received, wait suggested reset time then retry. Max 3 attempts.",
  label="github-ops"
)
```

Inside the subagent:
1. Check for X-RateLimit-Reset header
2. Calculate wait time: (reset_timestamp - now) + 5 seconds buffer
3. exec(command="sleep {wait_seconds}", yieldMs={wait_seconds * 1000 + 1000}, timeout={wait_seconds + 30})
4. Retry with Authorization header using token from TOOLS.md

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct |
|-------------|---------|---------|
| exec long command in main process | Blocks typing | Main process spawns; subagent uses exec+yieldMs |
| "Let me check..." + exec in main | Blocks typing | Spawn subagent |
| Waiting for subagent result before responding | Blocks dialog | Continue, report later |
| Direct remote operations in main process | Blocks | Spawn subagent |
| Spawning to avoid doing work (not to avoid blocking) | Misuse of pattern | Fast ops = direct in main process |
| All work spawn, nothing direct | Over-interpretation | Fast local ops = direct exec in main |
| Announcing the spawn to user | Noise, breaks flow | Spawn silently, continue |
| Subagent uses blocking exec without yieldMs | Subagent hangs | Subagent uses exec+yieldMs |
| Using specific IPs/hostnames in labels | Privacy leak | Use generic names |
| yieldMs >= timeout | Background threshold >= hard kill — illogical | yieldMs must always be < timeout |
| Subagent silently failing without reporting | Parent never knows | Always reply to parent, write error.md |
| Using thread=false when multi-step needed | Loses context mid-task, user follow-up fails | Use thread=true for multi-step or uncertain scope |
| Using thread=true for fire-and-forget | Wastes context window on single-use task | Use thread=false for bounded fire-and-forget tasks |
| `mode="one-shot"` (deprecated) | Not a valid mode — anti-pattern residue | Use `mode="run"` for detached or `mode="session"` with `thread=false` for fire-and-forget |
| User says "stop" but nothing happens | Subagent keeps running | Implement cancellation protocol: list → match label → SIGTERM → SIGKILL → reply |
| Subagent cancelled but no reply to user | User doesn't know it stopped | Always reply confirming which subagent was stopped |

---

## Workflow Summary

```
User request arrives
        │
        ▼
┌───────────────────────────────────┐
│ LAYER 1: MAIN PROCESS             │
│ Q1: fast + local + same topic?    │
│   YES → exec direct, respond      │
│ Q2: any spawn condition met?      │
│   YES → spawn subagent, continue  │
└───────────────────────────────────┘
        │
   spawn ↓
┌───────────────────────────────────┐
│ LAYER 2: SUBAGENT                 │
│ exec + yieldMs for long commands  │
│ background for very long          │
│ On error: log + error.md + reply  │
│ Return result via push            │
└───────────────────────────────────┘
        │
        ▼
Result arrives at main process
Report to user
If significant → write to MEMORY.md
```

---

## Key Insight

"Never block" is the rule. "Never execute" is a misreading of the rule — fast operations should be direct in the main process because they do not block.

The two-layer architecture makes this clean:
- **Main process**: dispatches everything, blocks nothing
- **Subagent**: executes with exec+yieldMs, never hangs without yield

The typing indicator is the visible signal: if it disappears, something is blocking.

---

## Privacy Notes

All examples in this skill use **generic placeholders only**. No specific project names, IPs, hostnames, user names, service names, or AI names appear in any example. This protects both operational security and privacy.
