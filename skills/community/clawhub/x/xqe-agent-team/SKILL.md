---
name: agent-team
description: >
  Orchestrate a dynamic multi-agent team where a lead agent (opus) plans and delegates tasks
  to specialized worker agents (sonnet) that communicate bidirectionally. Use when tasks
  benefit from parallelism or specialization — code review, market research, trading signal
  analysis, competitive analysis, or any complex task decomposable into parallel workstreams.
  Triggers on phrases like "agent team", "multi-agent", "spawn agents", "parallel agents",
  "team of agents", "让多个agent协作", "多智能体", "agent团队".
---

# Agent Team

Orchestrate a dynamic team of agents: one **Orchestrator** (opus) plans + delegates + synthesizes; multiple **Worker agents** (sonnet) execute specialized subtasks and communicate bidirectionally.

## Architecture

```
User
  └─► Orchestrator (opus)
        ├─ plans team composition dynamically
        ├─ spawns Worker A (sonnet) ──┐
        ├─ spawns Worker B (sonnet)   │ bidirectional
        ├─ spawns Worker C (sonnet) ◄─┘ via sessions_send
        └─ aggregates → final report to user
```

## Workflow

### Step 1 — Orchestrator Plans the Team

Analyze the task and define 2–4 worker roles. Each role needs:
- **Name**: short label (e.g. `researcher`, `coder`, `reviewer`)
- **Task**: specific, scoped instruction
- **Inputs needed from other workers**: what it needs to receive before finishing (for bidirectional flow)

See `references/role-patterns.md` for common role combinations per scenario.

### Step 2 — Spawn Workers

Spawn each worker as a persistent sub-agent session. **Always set `streamTo: "parent"`** so the user sees real-time output in their chat window:

```python
# Pseudocode — use sessions_spawn tool
sessions_spawn(
  task="You are the [ROLE] agent. [SPECIFIC TASK]. 
        When you need input from another agent, send a message to session [SESSION_KEY].
        Report your final result clearly structured.",
  runtime="subagent",
  mode="session",          # persistent — can receive follow-up messages
  model="sonnet",          # worker uses sonnet
  label="worker-[role]",
  streamTo="parent"        # stream output to user's chat in real time
)
```

Spawn all independent workers in **parallel** (single tool call block). Only spawn sequentially when a worker strictly depends on another's output.

### Step 3 — Bidirectional Communication

Workers can message each other via `sessions_send`. The orchestrator:
1. Gives each worker the session keys of peers it may need to consult
2. Monitors via `subagents(action=list)` — check on-demand, not in a loop
3. Can steer any worker mid-task: `subagents(action=steer, target=<label>, message=<redirect>)`

Direct worker-to-worker message pattern:
```
Worker A finishes partial result
  → sessions_send(sessionKey=worker-B-key, message="Here's my output: ...")
Worker B incorporates it, finishes
  → sessions_send(sessionKey=orchestrator-key, message="Done: ...")
```

### Step 3.5 — Relay Progress to User (Orchestrator Broadcast)

After each worker completes, send a status update to the user before moving on:

```
"[worker-researcher] 完成 ✅ — 找到 12 条相关数据，传给 worker-analyst"
"[worker-analyst] 处理中... 等待 worker-researcher 结果"
"[worker-reviewer] 完成 ✅ — 发现 3 个风险点"
```

This gives the user full visibility into the team's progress without needing to check logs manually.

### Step 4 — Aggregate Results

Once all workers report back, the orchestrator:
1. Synthesizes outputs into a coherent final answer
2. Resolves conflicts between workers' findings
3. Delivers structured report to the user

## Model Config

| Role | Model | Rationale |
|------|-------|-----------|
| Orchestrator | Current session model (Jarvis / Friday / Jupiter) | Complex planning + synthesis |
| Workers | `sonnet` | Cost-efficient execution |

**Orchestrator identities:**
- **Jarvis** — technical tasks (code, architecture, systems)
- **Jupiter** — trading strategy, quant analysis
- **Friday** — admin, research, daily tasks

Override worker model when a subtask needs deeper reasoning: pass `model="anthropic/claude-opus-4-6"` to that specific spawn.

## Common Scenarios

See `references/role-patterns.md` for ready-made role sets:
- **Code review**: `reader` + `security-reviewer` + `refactor-planner`
- **Market research**: `data-analyst` + `sentiment-analyst` + `risk-assessor`
- **Trading signals**: `technical-analyst` + `fundamental-analyst` + `macro-watcher`

## Key Rules

- **Spawn independent workers in one parallel block** — never sequential unless there's a hard dependency
- **No tight poll loops** — use `subagents(action=list)` only when checking status on-demand
- **Session cleanup**: after aggregation, kill idle workers with `subagents(action=kill, target=<label>)`
- **Scoped tasks**: each worker gets a single, well-defined responsibility — avoid overlap
- **Context isolation**: workers don't share the orchestrator's full context; pass only what's needed
