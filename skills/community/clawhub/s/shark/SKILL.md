---
name: shark
slug: shark
version: 0.3.1
summary: "The Shark Pattern — universal non-blocking execution for any AI coding agent. Spawn remoras for slow tools, keep the main agent swimming. Works with Claude Code, Codex, Gemini CLI, Cursor, Aider, OpenClaw."
tags: [async, performance, subagents, non-blocking, concurrency, patterns, claude-code, codex, gemini, cursor, aider]
homepage: https://github.com/keugenek/shark-pattern
author: keugenek
---

# 🦈 The Shark Pattern

> *A shark that stops swimming dies. An agent that waits for tools wastes compute.*

**Works with:** Claude Code · Codex · Gemini CLI · Cursor · Windsurf · Aider · OpenClaw · any LLM agent

## When to Use This Skill

Trigger this skill when the user says:
- "use the shark pattern"
- "non-blocking agent"
- "never wait for tools"
- "spawn background workers"
- "parallel subagents"
- "keep the main agent moving"
- or when you notice you're about to block on a slow tool (web fetch, SSH, build, test run, API call)

## The Rule

**Every LLM turn must complete in under 30 seconds.**

If any operation would take longer:
1. Spawn a remora (`sessions_spawn` with `mode: "run"`)
2. Continue reasoning immediately
3. Incorporate remora results when they arrive

You are **never** in I/O wait. You are **always** reasoning about something.

## Lifecycle

```
┌─────────────┐
│  DECOMPOSE  │  Break task into N independent subtasks
└──────┬──────┘
       │ spawn N remoras (+ 1 pilot fish when first completes early)
       ▼
┌─────────────┐
│    SPAWN    │  sessions_spawn × N, all parallel, record session IDs
└──────┬──────┘
       │ main agent keeps reasoning (never waits)
       ▼
┌─────────────┐     timeout/crash
│   MONITOR   │ ──────────────────► MARK ⏱/❌ (partial still useful)
└──────┬──────┘
       │ all done OR deadline hit
       ▼
┌─────────────┐
│  AGGREGATE  │  Collect results, note failures, merge pilot fish draft
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   REPORT    │  Single coherent response with failure count noted
└─────────────┘
```

**No nested remoras.** If a remora is running, it executes inline — remoras cannot spawn their own remoras. Only the main shark spawns.

## The Pattern

### Bad (Ralph-style blocking):
```
think → call slow tool → WAIT 60s → think → call slow tool → WAIT 45s → ...
```

### Good (Shark-style non-blocking):
```
think → spawn remora(slow tool) → think about something else
     → spawn remora(another tool) → synthesize partial results
     → receive remora result → incorporate → swim on
```

## Implementation

When applying the Shark Pattern, structure your work like this:

### 1. Identify blocking operations
Before calling any tool, ask: "Will this take more than 20-30 seconds?"

Slow tools (always spawn):
- Web searches / page fetches
- SSH commands on remote machines
- Build / test / CI runs
- File system scans over large directories
- API calls with unknown latency
- LLM inference calls (coding agents)

Fast tools (run inline, never spawn):
- Reading local files
- Simple calculations
- String manipulation
- Memory lookups

### 2. Spawn remoras

```
sessions_spawn({
  task: "Do the slow thing and return the result",
  mode: "run",
  runtime: "subagent",
  streamTo: "parent"  // optional: stream output back
})
```

Spawn multiple remoras in parallel when possible — don't serialize unless there's a data dependency.

### 3. Keep the main fin moving

After spawning, immediately continue:
- Plan the next step
- Work on a different part of the task
- Summarize what you know so far
- Prepare to incorporate results

### 4. Incorporate results

When remora results arrive, weave them in and continue. Never re-do work a remora already completed.

If your runtime keeps subagents alive after completion, close them once you've incorporated their result. In Codex that means: wait for the remora, use its output, then `close_agent(id)` unless you intentionally plan to reuse that same agent.

## Timing Budget

| Operation | Budget | Action |
|-----------|--------|--------|
| File read | < 2s | Inline |
| Web search | 5-30s | Spawn |
| SSH command | 10-120s | Spawn |
| Build/test | 30-300s | Spawn |
| Coding agent | 60-600s | Spawn |
| Memory search | < 3s | Inline |

## Example: Multi-Step Research Task

**Without Shark (blocking):**
```
1. Search web for X        [wait 15s]
2. Search web for Y        [wait 12s]  
3. Fetch page Z            [wait 8s]
4. SSH check server        [wait 30s]
Total: ~65 seconds blocked
```

**With Shark (non-blocking):**
```
1. Spawn: search X         [0s - spawned]
2. Spawn: search Y         [0s - spawned]
3. Spawn: fetch Z          [0s - spawned]
4. Spawn: SSH check        [0s - spawned]
5. Plan synthesis while waiting [15s of actual thinking]
6. All results arrive → synthesize
Total: ~15s of thinking + max(tool times) in parallel
```

## Output Format

### Announce on start
> 🦈 **Shark mode** — spawning [N] remoras for [tasks], continuing...

### Progress bar (chat-friendly, Unicode only — no images needed)

Use this format after each remora or pilot fish completes. Works in Telegram, Discord, Signal, iMessage — anywhere.

```
🦈 3 remoras · 1 pilot fish

◉ [A] task name here    ████████████ ✅ 9s
◉ [B] task name here    ████████████ ✅ 33s
○ [C] task name here    ░░░░░░░░░░░░ pending
◈ [P] Pilot fish        ██████░░░░░░ ~14s left

↳ continuing...
```

**Symbols:**
- `◉` = remora (completed)
- `○` = remora (pending)
- `⊙` = remora (running)
- `◈` = pilot fish (time-bounded)
- `████████████` = done bar (12 blocks)
- `██████░░░░░░` = partial (filled = elapsed / total budget)
- `░░░░░░░░░░░░` = not started

**Progress fill:** `filled = round(elapsed / timeout * 12)` blocks of `█`, remainder `░`

Only post an update when something changes (remora completes or pilot fish starts/ends). Don't spam — one update per event.

### Final synthesis
After all remoras done:
> 🦈 **All fins in** — synthesising [N] results + pilot draft

Then deliver the report.

## The Pilot Fish Sub-Pattern

> *Pilot fish swim alongside sharks doing prep work. When you have idle time, use it.*

When one remora returns early and others are still running:

1. **Spawn a pilot fish** — a time-bounded analysis sub-agent
2. **Give it only the partial results so far** + a hard timeout equal to the estimated remaining wait
3. **Let it pre-validate, pre-analyse, find patterns, draft conclusions**
4. **Kill it** (or it self-terminates) when the last primary remora completes
5. **Incorporate** whatever the pilot fish produced into the final synthesis

```
remora A ──────► result (early)
remora B ────────────────────────────► result
remora C ──────────────────────────────────► result

main:   spawn A, B, C
        A done → spawn pilot-fish(A's result, timeout=est_remaining)
        pilot-fish: pre-analyse A, draft partial report, validate data...
        B done → pilot-fish still running, feed B's result in (or kill+reuse)
        C done → kill pilot-fish, synthesise A+B+C+pilot-fish draft
```

### Pilot Fish Rules

- **Always time-bounded** — pass `runTimeoutSeconds` equal to estimated remaining wait
- **Never blocks** — spawned async, main agent continues
- **Opportunistic** — if it finishes early, bonus; if killed mid-run, partial output is still useful
- **One at a time** — don't stack pilot fish on pilot fish
- **Task:** pre-validate data, find gaps, draft structure, flag anomalies, prepare questions

### Example

```
// remoras A (fast) and B (slow) both spawned
// A finishes in 10s, B will take another 30s

// Spawn pilot fish with 25s budget:
sessions_spawn({
  task: "Pre-analyse these results from remora A. 
         Validate the data, note any gaps, draft the structure 
         of the final report. Stop after 25 seconds.",
  runTimeoutSeconds: 25,
  mode: "run"
})

// Main agent continues doing other work
// When B finishes → kill pilot fish → synthesise A + B + pilot draft
```

## Decision Tree — When to Spawn

Before every tool call, ask: **"Will this take more than 10 seconds?"**

```
Estimated time < 10s?  → run inline
Estimated time ≥ 10s?  → spawn remora
Unknown latency?        → spawn remora (assume slow)
Data dependency on another remora? → wait, then inline
Already at 8 remoras? → queue, don't stack
```

**Always spawn:** web search/fetch, SSH, build/test, coding agents, CI triggers, API calls with unknown latency
**Always inline:** file read, memory lookup, string ops, math, local config reads

---

## Error Handling

remoras **will** fail, timeout, or return garbage. Plan for it.

### remora timeout
```
◉ [A] task    ████████████ ⏱ 30s [timeout]
```
- Treat as partial result — use whatever was returned
- Do **not** re-spawn the same task (wastes time, likely to timeout again)
- Note the gap in synthesis: "A timed out — data may be incomplete"
- If A's result is critical, spawn a smaller-scoped follow-up shark

### remora crash / error
```
◉ [A] task    ████████████ ❌ [error: connection refused]
```
- Log the error inline in the progress bar
- Continue synthesis without that result
- Mention the failure in the final report
- Optionally file an issue / alert if it's infrastructure
- If the runtime still shows the remora as open after completion or error, clean it up immediately. In Codex, close completed remoras with `close_agent(id)` once their output is delivered.

### Partial results (most common)
- Most useful — a remora that timed out at 28s has 28s of work in it
- Always check if partial output is usable before discarding
- Progress bar: `⏱` = timeout with partial, `❌` = hard error with nothing

### >50% remoras failed
- Degrade gracefully — fall back to sequential for remaining work
- Note in report: "⚠️ degraded mode — N/M remoras failed"

### All remoras failed
- Fall back to sequential execution for the most critical task only
- Do not spawn another full fleet — you're likely hitting a systemic issue

### Forgetting to spawn the pilot fish (most common mistake)
- You finished a fast inline task, a remora is still running, and you just... wait
- **Symptom:** main agent idle, no pilot fish, time wasted
- **Fix:** always ask after any remora completes early — "what can I pre-draft right now?"
- Even if you have nothing obvious, draft the output structure, prepare questions, or outline the synthesis

### Pilot fish killed mid-run
- Normal and expected — whatever it produced is still useful
- Incorporate partial pilot fish output into synthesis
- Don't wait for it or re-spawn it

---

## Terminology

- **remora** = a `sessions_spawn` call with `mode: "run"`, `runtime: "subagent"`, and `runTimeoutSeconds` set. A remora is specifically a *timed* sub-agent — untimed subagents are not remoras.
- **Pilot fish** = a remora spawned *after* another remora completes, with a short timeout sized to the estimated remaining wait. Purpose: pre-analysis only, never primary work.
- **Fleet** = the full set of remoras spawned for one task
- **Fin moving** = the main agent is doing useful work (not waiting)
- **No nested remoras** = remoras always execute inline — only the main shark spawns

### `runTimeoutSeconds` — confirmed real
Verified against OpenClaw source: `runTimeoutSeconds: z.number().int().min(0).optional()` — maps to the subagent wait timeout. Use it. Hard-kills the sub-agent process after N seconds, partial output returned.

---

## Pilot Fish Sizing Formula

```
pilotFishTimeout = min(estimatedRemaining * 0.8, 25)
```

- `estimatedRemaining` = how long you think the slowest remaining remora will take
- Cap at 25s so pilot fish always finishes before the main synthesis turn
- If you don't know: use 20s as default

Example: slowest remaining remora estimated at 30s → pilot fish timeout = min(24, 25) = 24s

---

## Hard Limits

- **Never** use `yieldMs` > 30000 in exec calls — this holds the main turn hostage
- **Never** `process(action=poll, timeout > 20000)` in the main session — same reason
- **Never** add `sleep` or wait loops in the main thread
- **Always** set `runTimeoutSeconds` on remoras — unbound sub-agents are not sharks
- **Always** clean up completed remoras — if your runtime requires explicit teardown, do it right after incorporating the result
- **Max 8** concurrent remoras — beyond this, context overhead exceeds the gain
- **Never stack pilot fish** — one at a time, no pilot fish spawning pilot fish
- **Spawn tasks ≤ 3 sentences** — longer task descriptions need decomposition first

## Enforcing the 30-Second Timeout

The 30s cap isn't just a guideline — here's how to actually enforce it per runtime.

### OpenClaw subagents
```js
sessions_spawn({
  task: "...",
  mode: "run",
  runtime: "subagent",
  runTimeoutSeconds: 30   // hard kill after 30s — agent gets SIGTERM
})
```
`runTimeoutSeconds` is enforced by the OpenClaw runtime — the sub-agent process is killed if it exceeds it. Partial output is still returned.

### exec calls (shell, SSH, scripts)
```js
exec({
  command: "some-slow-command",
  timeout: 30,        // hard kill in seconds
  background: true,   // don't block the main agent turn
  yieldMs: 500        // poll back quickly to check
})
```
`timeout` kills the process. `background: true` means the main agent doesn't wait — it gets a session handle and can check back with `process(poll)`.

### Gemini CLI via exec
```bash
timeout 30 gemini -p "task here"
# or on Windows:
Start-Process gemini -ArgumentList '-p "task"' -Wait -Timeout 30
```
Wrap the CLI invocation with OS-level `timeout` / `Start-Process -Timeout`.

### Pilot fish — always use `runTimeoutSeconds`
```js
sessions_spawn({
  task: "pre-analyse partial results, draft structure, flag gaps",
  mode: "run",
  runTimeoutSeconds: estimatedRemainingMs / 1000,  // die before the last remora
})
```
Set it to *slightly less* than your estimated remaining wait — so the pilot fish always finishes before you need to synthesise.

### What happens when timeout fires
- Sub-agent/process is killed
- Whatever output was produced so far is returned
- Main agent treats it as a partial result — still useful for synthesis
- Log: `[timeout]` in the progress bar instead of `✅`

```
⊙ [A] slow task    ████████████ ⏱ 30s [timeout — partial result]
```

### The LLM turn itself
You can't hard-kill an LLM mid-turn, but you can:
1. **Keep prompts tight** — don't ask for exhaustive analysis in one turn
2. **Use `thinking: "none"`** for fast sub-tasks that don't need deep reasoning
3. **Break large tasks** into smaller shark-able chunks upfront

Rule of thumb: if a task description is >3 sentences, it probably needs to be split into remoras.

## Compatibility — Claude, Codex, Gemini CLI

The Shark Pattern is **runtime-agnostic**. remoras can be any agent type.

### OpenClaw (Claude / Sonnet / Opus)
```
sessions_spawn({
  task: "...",
  mode: "run",
  runtime: "subagent",
  runTimeoutSeconds: 30   // hard cap for pilot fish
})
```

### Codex
```
sessions_spawn({
  task: "...",
  runtime: "acp",
  agentId: "codex",
  mode: "run",
  runTimeoutSeconds: 30
})
```

Codex-specific lifecycle:
- Spawn with `spawn_agent(...)` or the runtime-equivalent remora launcher
- Check completion with `wait_agent(...)`
- If you want to reuse the same remora, send more work with `send_input(...)`
- Otherwise, once the remora has completed and you've incorporated its result, call `close_agent(id)` so the agent does not linger in the session

### Gemini CLI
Gemini CLI is a local process — spawn via exec with a timeout:
```
exec({
  command: "gemini -p \"task description here\"",
  timeout: 30,            // hard cap in seconds
  background: true,       // don't block main agent
  yieldMs: 500            // check back quickly
})
```
For Gemini sub-tasks, use `exec` with `timeout` + `background: true` rather than `sessions_spawn`. Treat the process handle the same way — continue working, collect output when it lands.

### Mixed fleets
You can mix runtimes in the same shark run:
```
spawn remora A → Codex (coding task)
spawn remora B → Gemini (web search / analysis)
spawn remora C → Claude subagent (reasoning)
spawn pilot fish  → Claude subagent (pre-analysis, time-bounded)
```

### Which to use when

| Task type | Best runtime |
|-----------|-------------|
| Code generation / editing | Codex |
| Web search / summarise | Gemini CLI |
| Multi-step reasoning | Claude subagent |
| File ops / SSH / shell | exec (background) |
| Pre-analysis / drafting | Claude subagent (pilot fish) |

## shark-exec Sub-Skill

For slow shell commands (>5s), use the **shark-exec** companion skill:
- Located at `shark-exec/SKILL.md` in this repo
- Wraps any `exec` call in background + cron poller
- Guarantees main turn completes in <30s even for 10-minute commands
- Use it instead of inline exec whenever the command might block

## Loop Enforcement (Ralph-style)

The 30-second rule is best enforced at the **shell level**, not inside a turn.

Use `shark.sh` (or `shark.ps1` on Windows) to run Claude in a bounded loop:

```sh
./shark.sh "find the latest ChatterPC version, check pve3, summarise GitHub issues"
```

Each iteration:
1. Builds a fresh prompt: skill context + task + current state
2. Runs `claude --print` with a hard `timeout 25s` shell wrapper
3. If Claude times out → loop continues (it's expected — shark pattern means short turns)
4. If Claude writes `.shark-done` → loop exits

This is identical to the Ralph Loop pattern, but with the Shark Pattern as the prompt — Claude spawns remoras for slow work, keeps each turn under 25s, and the shell loop enforces the hard cut.

### When to use the loop vs direct claude

| Use case | Approach |
|----------|----------|
| Single fast task (<30s total) | `claude --print "..."` directly |
| Multi-step task, slow tools | `./shark.sh "..."` loop |
| CI/build watching | shark-exec (background + cron) |
| Interactive chat | OpenClaw main session |

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SHARK_MAX_LOOPS` | `50` | Maximum iterations before giving up |
| `SHARK_LOOP_TIMEOUT` | `25` | Per-turn timeout in seconds (hard kill) |

### Completion protocol

When Claude determines the task is done, it writes to `.shark-done`:
```
TASK_COMPLETE
<brief summary of what was accomplished>
```
The loop detects this file and exits cleanly.

## Commands

When the user invokes these commands, follow the instructions for each.

### `/shark <task>`

Apply the Shark Pattern to the given task. Decompose, spawn remoras for slow ops, keep the main fin moving. Follow all rules in this SKILL.md.

### `/shark-loop <task> [--max-loops N] [--timeout S]`

Run the external shark loop enforcer. Execute:
```
$env:SHARK_MAX_LOOPS = "<N>"
$env:SHARK_LOOP_TIMEOUT = "<S>"
powershell.exe -ExecutionPolicy Bypass -File "<skill_dir>/shark.ps1" "<task>"
```
Defaults: `--max-loops 50`, `--timeout 25`. On Linux/Mac use `shark.sh` instead.

### `/shark-status`

Check current shark state:
1. Read `<skill_dir>/shark-exec/state/pending.json` — report active background jobs (label, command, elapsed time, whether overdue past maxSeconds)
2. If `.shark-done` exists, show its contents
3. If `SHARK_LOG.md` exists, show the last 10 lines
4. If nothing exists, report "No active shark jobs."

### `/shark-clean`

Remove shark state files: `.shark-done`, `SHARK_LOG.md`, `shark-exec/state/pending.json`. Report what was cleaned.

### `/shark-autotune`

Analyse timing history and recommend optimal settings.

1. Read `<skill_dir>/state/timings.jsonl` — each line is:
   ```json
   {"ts":1710000000,"loop":1,"elapsed_s":12.3,"timeout_s":25,"result":"ok|timeout|done","task_hash":"abc123"}
   ```

2. If no data, report "No timing data yet. Run tasks with /shark first."

3. Compute and report:
   - **Total runs** (unique task_hash values) and **total loops**
   - **Median turn time** (p50) and **p95 turn time**
   - **Timeout rate** — % of turns with result "timeout"
   - **Loops to completion** — median and max (count loops per task_hash that has a "done" entry)
   - **Wasted headroom** — sum of (timeout_s - elapsed_s) for result "ok" turns
   - **Optimal timeout** — p95 turn time + 3s buffer, rounded up to nearest 5s
   - **Optimal max_loops** — p95 loops-to-completion + 2

4. Show recommendations:
   ```
   Current:     SHARK_LOOP_TIMEOUT=25  SHARK_MAX_LOOPS=50
   Recommended: SHARK_LOOP_TIMEOUT=N   SHARK_MAX_LOOPS=M

   Rationale:
   - p95 turn time is Xs, so timeout of Ns covers 95% with buffer
   - p95 completion is N loops, so max_loops of M gives safe margin
   - Timeout rate is X% — [>15%: consider splitting tasks | healthy]
   - Wasted headroom: Xs total
   ```

5. If timeout rate > 30%: "Consider breaking tasks into smaller steps."
6. If median turn time < 5s: "Most turns complete fast. Consider lowering timeout."

## Timing Instrumentation

Both `shark.sh` and `shark.ps1` automatically record per-loop timings to `state/timings.jsonl`. Each entry includes:
- `ts` — Unix timestamp
- `loop` — loop iteration number
- `elapsed_s` — actual wall-clock seconds for this turn
- `timeout_s` — configured timeout for this run
- `result` — `"ok"` (completed), `"timeout"` (hit limit), `"done"` (task finished)
- `task_hash` — 8-char hash correlating loops within a single run

Use `/shark-autotune` to analyse this data and tune your settings.

---

## References

- Ralph Loop (sequential baseline): ghuntley.com/ralph/
- OpenClaw sessions_spawn docs: spawn with `mode: "run"`, `runtime: "subagent"`
- Gemini CLI: `npm install -g @google/gemini-cli`
- The name: sharks use ram ventilation — they literally die if they stop moving
