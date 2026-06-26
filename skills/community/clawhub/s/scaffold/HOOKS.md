<!--
HOOKS.md - Scaffold Lifecycle Hook Protocol

WHAT THIS IS: Formal trigger-response procedures for the moments that matter most.
Hooks are what separates agents that degrade over a long session from ones that stay sharp.
Every hook here addresses a real failure mode that happens without it.

HOW TO CUSTOMIZE:
  - The hooks are ready to use as-is. Start there.
  - Add custom steps to OnTaskComplete if you want auto-testing, notifications, etc.
  - Add domain-specific recovery steps to OnError as you encounter failure patterns.
  - OnSessionStart: add any files your agent should load at startup.

UPGRADE: The Full version of Scaffold includes additional hooks:
  - OnContextHigh + OnCompactionRecovery (survive context resets cleanly)
  - PreExternalAction (confirmation gate before any external action)
  - /start and /end session boundary commands
  - WAL Protocol (write-ahead log for active working memory)
-->

# HOOKS.md - Lifecycle Hook Protocols

*These are not suggestions. When the trigger fires, run the procedure. No skipping.*

---

## Why Hooks?

Without explicit lifecycle hooks, agents:
- Start sessions without loading their own memory (and make decisions without context)
- Finish tasks without updating the task queue (so work silently disappears)
- Encounter errors and improvise (wasting turns and sometimes making things worse)

Hooks are the fix. Each one is a named trigger with a defined response. The agent always knows what to do when that moment arrives.

---

## OnSessionStart

**Trigger:** Any new session begins.

**Steps (in order, no skipping):**
1. Read `memory/active-tasks.md` — what's in progress? If something is 🔵 In Progress, pick it back up.
2. Read `SOUL.md` — recalibrate tone and operating principles.
3. Read `USER.md` — who am I working with and what do they care about?
4. Read today's and yesterday's daily log (`memory/YYYY-MM-DD.md`) — recent raw context.
5. **Main session only** (direct chat with [YOUR_HUMAN]): also read `MEMORY.md` for long-term context.

**Do not ask permission. Do not announce you're running the startup sequence. Just do it, then respond.**

> **Why:** Agents that don't load memory at startup make decisions without context. They repeat solved problems, forget what was agreed, and ask questions that were already answered.

---

## OnTaskComplete

**Trigger:** Any task, sub-task, or meaningful unit of work is finished.

**Steps:**
1. Run **OnStop** (the verification checklist below) before proceeding.
2. Update `memory/active-tasks.md` — move task to ✅ Completed with today's date and a 1-line summary.
3. Log what was done to today's daily file (`memory/YYYY-MM-DD.md`) — 1–3 lines, just the facts.
4. Git commit all workspace changes:
   ```
   git add -A && git commit -m "feat: <short description>"
   ```
5. If [YOUR_HUMAN] is in the session and waiting: announce what was done and how to verify it.

> **Why:** Without this hook, completed work disappears into context. The task queue goes stale. Future sessions have no idea what was done or where things stand.

---

## OnStop — Verification Before Done

**Trigger:** About to mark a task complete, send a "done" message, or add a ✅.

**Checklist (must pass all before calling it done):**
- [ ] Did I check the actual output, file, or result — not just that the command ran?
- [ ] If a file was created: does it exist and have the right content?
- [ ] If something was fixed: does the fix hold under the same conditions that caused the problem?
- [ ] If something was built: does it function as described?
- [ ] Ask: *"Would [YOUR_HUMAN] be satisfied if they checked this right now?"*

**If any check fails:** fix it first, then re-run the checklist.

> **Why:** "The command ran without errors" is not the same as "it works."

---

## OnError

**Trigger:** A tool call fails. A command returns unexpected results. Something breaks mid-task.

**Steps:**
1. Log the error to today's daily file — what failed, the error message, current task state.
2. Check: is a retry safe?
   - **Safe to retry (idempotent):** read a file, run a search, generate text → retry once with an adjustment. If it fails again, escalate.
   - **Not safe to retry:** send a message, modify a database, make a payment → do NOT retry. Surface to [YOUR_HUMAN] immediately.
3. When escalating:
   - (a) What failed and what the error was
   - (b) Current state of the task
   - (c) Your recommended next step
4. **Never silently swallow errors.**

> **Why:** Agents that improvise around errors waste turns and sometimes make things worse. Surface clearly, recover fast.

---

*HOOKS.md — Scaffold Lite. Upgrade to Full for compaction recovery, external action gates, WAL memory protocol, and /start /end session commands.*
