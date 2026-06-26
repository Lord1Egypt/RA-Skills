---
name: swarm-workflow-protocol
description: Multi-agent orchestration protocol for the 0x-wzw swarm. Defines spawn logic, relay communication, task routing, and information flow. Agents drive decisions; humans spar.
---

# Swarm Workflow Protocol

The operating system for multi-agent collaboration in the 0x-wzw swarm. Defines how agents spawn, communicate, challenge, and hand off work.

## Core Principle

**Optimal human-agent collaboration: humans spar, agents drive.** No approval bottlenecks. Continuous information flow. Goal: full autonomy through continuous improvement.

## The Human Role: Sparring Partner

Z is not a bottleneck — Z is a thinking partner who sharpens agents.

- Agents drive decisions and execution
- Z challenges assumptions when they see gaps
- Z's pushback improves outcomes
- Over time, the gap between agent decisions and Z's expectations narrows

**Sparring, not approving:**
- ❌ "Should I do X?" (approval-seeking)
- ✅ "I'm doing X because [reasoning]. You see any gaps?" (sparring)

## Pre-Task Spawn Analysis

Before any task, answer these 3 questions in 10 seconds.

### Q1: Complexity?
- **Simple** (one-shot, clear) → Don't spawn
- **Semi-complex** (multi-step) → Q2
- **Ultra-complex** (many decisions) → Q2

### Q2: Parallel Seams?
- Are there genuinely independent subspaces?
- Can two agents work simultaneously without needing each other's output?
- **No** → Don't spawn (serial dependency = compounding latency)
- **Yes** → Q3

### Q3: Token Math
- Spawn cost: ~500–1500 tokens overhead
- Only spawn if expected output is **3–5x that** (~2000–7500 tokens)
- **No** → Don't spawn (overhead exceeds savings)

## Decision Matrix

| Task | Complexity | Parallel? | Token Budget | Decision |
|------|------------|-----------|-------------|----------|
| Simple | — | — | — | Main session |
| Semi-complex | serial | No | — | Main session |
| Semi-complex | parallel | Yes | Sufficient | **Spawn** |
| Ultra-complex | parallel | Yes, 2-3 seams | Sufficient | **Spawn 2-3 leads** |
| Ultra-complex | many seams | — | — | Resist swarm urge |

## Task Lifecycle

1. **Intake** → Task arrives from Z, Moltbook, cron, or webhook
2. **Classify + Pre-Spawn** → Route to correct agent type, run 3-question gate
3. **Challenge Round** → Specialists validate viability via relay
4. **Synthesis** → October synthesizes, assigns work
5. **Execution** → Sub-agents or direct execution
6. **Continuous Updates** → Z gets progress throughout
7. **Handoff & Close** → Summary, file log, next steps

## Relay Communication

### Endpoints
- **Send:** `POST http://localhost:18790/message`
- **Fetch:** `GET http://localhost:18790/messages?agent=<YourName>`
- **Health:** `GET http://localhost:18790/status`
- **Auth header:** `x-auth-token: agent-relay-secret-2026`

### Message Types

| Type | When | Expectation |
|------|------|-------------|
| `urgent` | Z needs now | Immediate relay |
| `status_update` | Progress info | Log only |
| `task_delegation` | Work assigned | Log + await |
| `question` | Need agent input | Expect response |
| `data_pass` | Sharing results | Log + process |

### Standard Handoff Format

```
TO: <AgentName>
TYPE: <type>
CONTENT: [task description]
APPROACH: [agreed approach]
REPORT_TO: October
```

## File Locations

| What | Where |
|------|-------|
| Daily logs | `memory/daily-logs/YYYY-MM-DD.md` |
| Agent comm audit | `memory/agent-comm-logs/YYYY-MM-DD.jsonl` |
| This protocol | `skills/swarm-workflow-protocol/SKILL.md` |

## Anti-Patterns

- ❌ Waiting on Z for approval
- ❌ Executing before specialists validate
- ❌ Silent completions
- ❌ Spawning when serial dependency exists
- ❌ Forgetting to log audit trail
- ❌ Spawning to escape thinking (vs. leveraging parallel seams)
