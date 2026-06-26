---
name: session-coordinator
version: 3.0.1
description: "Async Process Pattern for OpenClaw agents. Core rule: main process must never block. Use when: (1) agent should stay responsive to user dialog at all times, (2) long/uncertain operations must not block the main session, (3) multi-node coordination requires clear separation between dialog/dispatch (main) vs execution (subagent). Triggers on: async mode, main process blocking, spawn decision, long operation handling.
---

# Session Coordinator Skill v3.0.1 — Main Process Never Blocks

## Core Principle

**Main process = dialog + dispatch. Never block.**

The main goal is responsiveness — the main process must never be blocked, stalled, or made unresponsive. This is not "never execute." It is "never block."

A blocked main process shows as: typing indicator disappears, user cannot get a response, session appears frozen.

## Decision Framework

### Spawn when (blocks or uncertain):
- Remote operations (SSH, remote API calls)
- git push/pull/clone operations
- Any operation involving network I/O
- Operations with unknown duration
- Operations that need isolation (fail without affecting main session)
- **State-modifying operations**: file write, git commit, package publish, deploy, or any operation that changes persistent state on disk or remote
- Anything requiring waiting for external result
- **Spawn must always include a `label` parameter** (see Spawn Label Convention below)

### Execute directly when (fast, non-blocking AND same topic):
- Local scripts that run in <1 second
- Reading files, writing docs, writing code
- Dialog, judgment, approval, reasoning
- Quick system calls (RAM, disk, process status)
- Must NOT involve network I/O (SSH, HTTP, remote calls)
- Must be same topic as current conversation

### Self-check signal:

"If my typing indicator disappeared, am I being blocked right now?"

If a question or request is on a DIFFERENT topic, spawn it — do not handle it directly even if it seems fast. Different topic = different subagent.

---

## Spawn Mode v3 — Default: session thread

**Default spawn mode is `mode="session"` with `thread=true`.**

- Use `mode="session"`, `thread=true` for most tasks (interactive, multi-step, or uncertain duration)
- Use `mode="one-shot"` only when explicitly instructed or when the task is trivial and guaranteed single-turn
- Never assume `mode="run"` (run = detached, no result push = unreliable)

```python
# ✅ Default: session thread (most tasks)
spawn(task="task-description", mode="session", thread=true, label="task-label")

# ✅ Explicit one-shot: only when scope is trivially bounded
spawn(task="task-description", mode="one-shot", label="task-label")

# ❌ Don't use run unless you explicitly need detached/no-result
spawn(task="task-description", mode="run")
```

---

## Timeout Guidelines

Use these as a guide to set `runtime` when spawning:

| Tier | Duration | Examples |
|------|----------|----------|
| **fast** | ~5 min | file ops, single API call, config check, quick test |
| **medium** | ~15 min | git operations, moderate build, moderate data processing |
| **long** | 60 min+ | large clones, heavy builds, multi-step deployments, data migration |

```python
# Fast task — 5 min timeout
spawn(task="check service status", runtime="fast", label="service-status-check")

# Medium task — 15 min timeout
spawn(task="clone repository and run tests", runtime="medium", label="repo-test")

# Long task — 60 min timeout
spawn(task="full deployment pipeline", runtime="long", label="deploy-pipeline")
```

---

## Spawn Label Convention

When spawning a subagent, **always include a descriptive `label` parameter**:

- Use dashes, not spaces (e.g., `project-config-sync` not `project config sync`)
- Use generic, descriptive names only — never specific project names, IPs, hostnames, or user names
- Label should reflect the actual task category or action

**Generic placeholder examples:**
- `project-name` → `repo-name` or `project-alfa`
- `192.168.x.x` → `remote-host` or `node-alpha`
- `user@host` → `admin-user` or `service-account`

```python
# ✅ Good: generic, dashes, descriptive
spawn(task="sync config to remote node", label="config-sync")
spawn(task="run test suite for module", label="test-suite")
spawn(task="deploy service to environment", label="service-deploy")

# ❌ Bad: spaces, specific names, cryptic
spawn(task="...", label="proj1")           # too short, no dashes
spawn(task="...", label="192-168-1-1")     # specific IP — not allowed
spawn(task="...", label="johns-task")      # specific user name — not allowed
spawn(task="...", label="foo-bar-v2")      # specific project codename — not allowed
```

When the user says "stop that thing", look at `subagents list` and match the label to find the right subagent to stop.

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

## Result Writing

### Important results → MEMORY.md

After a subagent completes, if the result is **significant** (decision made, lesson learned, important output, state change), write it to `MEMORY.md` in the main session.

```markdown
## [Date] Task Result
- Task: task-description
- Outcome: what happened
- Key decision/learning: ...
```

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

user does not need to know the execution architecture. The subagent handles the work; you handle the conversation.

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
| Fast local operations | ✅ | ❌ |
| Blocking operations | ❌ | ✅ |

---

## Execution Model

### Blocked = Wrong

If the main process blocks, the pattern has failed — regardless of whether the task eventually completes.

### Spawn and Continue

```python
# ❌ Wrong — blocks main process, typing disappears
exec("ssh remote-host ...")
subprocess.run(...)

# ✅ Correct — non-blocking, typing stays active
spawn(task="remote operation description", runtime="medium", mode="session", thread=true, label="remote-task")
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

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct |
|-------------|---------|---------|
| "Let me check..." + exec in main | Blocks typing | Spawn subagent |
| Waiting for subagent result before responding | Blocks dialog | Continue, report later |
| Direct remote operations in main process | Blocks | Spawn |
| Spawning to avoid doing work (not to avoid blocking) | Misuse of pattern | Execute directly if fast |
| All work spawn, nothing direct | Over-interpretation | Fast ops = direct |
| Announcing the spawn to user | Noise, breaks flow | Spawn silently, continue |
| Using specific IPs/hostnames in labels | Privacy leak | Use generic names |

---

## Workflow Summary

1. **User request arrives**
2. **Assess: will this block?** (slow / uncertain / remote = spawn; fast / local / dialog = direct)
3. **If spawn → spawn with session thread + appropriate runtime + generic label**
4. **If direct → execute and respond now**
5. **Result arrives via push → report to user**
6. **If result is significant → write to MEMORY.md or daily log**
7. **Self-check: is typing indicator still showing?**

---

## Key Insight

"Never block" is the rule. "Never execute" is a misreading of the rule — fast operations should be direct because they do not block. The typing indicator is the visible signal: if it disappears, something is blocking.

---

## Privacy Notes

All examples in this skill use **generic placeholders only**. No specific project names, IPs, hostnames, user names, service names, or AI names appear in any example. This protects both operational security and privacy.
