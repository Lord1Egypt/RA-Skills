---
name: subagent-orchestration
description: "Orchestrate OpenClaw subagents effectively. Covers all three agent types (Worker, Researcher, Council) with correct spawning patterns, sandbox constraints, timeout strategies, and failure mode fixes. Includes multi-model council pattern via the council-of-llms companion skill. Prevents common failures: context overflow, gateway timeouts, web tool access, inline Python restrictions. Triggers on: spawn, delegate, subagent, agent timeout, agent failure, orchestration, multi-agent, council."
tags:
  - subagent
  - orchestration
  - delegation
  - spawning
  - timeout
  - council
  - multi-agent
  - parallel
  - worker
  - researcher
---

# Subagent Orchestration

## Agent Types

| Type | Tools | Use For |
|------|-------|---------|
| **Worker** | Default (no web) | File ops, script execution, git, code changes |
| **Researcher** | `ollama_web_search`, `ollama_web_fetch` | Web research, API lookups, live data |
| **Council** | Default (no web) | Analysis, review, decision-making with passed context |

## Sandbox Constraints

Default subagents (Worker/Council) **cannot**:
- Use `ollama_web_fetch` or `ollama_web_search`
- Run `python3 -c "..."` inline commands
- Access the main session's conversation history

They **can**:
- Read/write files
- Run scripts from `.py` files (`python3 /path/to/script.py`)
- Execute simple shell commands
- Use `exec`, `read`, `write`, `edit` tools

## Spawning Patterns

### Researcher (Web-Enabled)
```
sessions_spawn(
  toolsAllow: ["ollama_web_fetch", "ollama_web_search"],
  runtime: "subagent",
  mode: "run",
  lightContext: true,
  runTimeoutSeconds: 600,
  task: "Research X. Return: findings, sources, key metrics."
)
```

### Worker (File/Code Ops)
```
sessions_spawn(
  runtime: "subagent",
  mode: "run",
  lightContext: true,
  runTimeoutSeconds: 300,
  task: "Run python3 /path/to/script.py. Report output."
)
```

### Council (Multi-Model Deliberation)
```
# Spawn 3 parallel subagents with different models and perspectives
# See skills/council-of-llms/SKILL.md for full details
sessions_spawn(model: "ollama/kimi-k2.6:cloud", label: "Council-Strategos", ...)
sessions_spawn(model: "ollama/deepseek-v4-pro:cloud", label: "Council-Analyticos", ...)
sessions_spawn(model: "ollama/gemma4:31b-cloud", label: "Council-Creativos", ...)
# Then synthesize all 3 outputs into a unified verdict
```

### Single-Model Council (Legacy — Avoid)
```
# WARNING: Single-model councils cause context overflow and produce shallow analysis
# Use multi-model pattern above instead
sessions_spawn(
  runtime: "subagent",
  mode: "run",
  lightContext: true,
  runTimeoutSeconds: 900,
  task: "Review this data and decide: [data pasted inline]. Return: verdict, conditions, risks."
)
```

## Timeout Strategy

| Task Type | Min Timeout | Recommended |
|-----------|------------|-------------|
| Simple file ops | 120s | 180s |
| Research (web) | 300s | 600s |
| Council/review | 300s | 600s |
| Complex multi-step | 600s | 900s |

**Never rush agents.** Quality > speed. If an agent takes >60s, give the user a brief status update.

## Delegation Rules

1. **Never run long scripts yourself.** Write the script, hand the file path to a subagent.
2. **Pre-fetch web content yourself** for Worker/Council agents — they can't browse.
3. **Use Researcher agents** when you need web data that subagents can't access.
4. **Write `.py` files first** — don't pass inline Python to subagents.
5. **Paste context inline** — Council agents don't have your conversation history.

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Agent times out | Can't access web tools | Use `toolsAllow` or pre-fetch content |
| Agent times out | Can't run inline Python | Write `.py` file, pass path |
| Agent times out | `runTimeoutSeconds` too low | Set `runTimeoutSeconds: 900` in spawn call |
| Agent times out | Gateway under load (10s spawn timeout) | Kill zombie subagents, wait, retry |
| Agent returns nothing | Missing context | Paste data in `task` parameter |
| Agent stuck in loop | Vague task | Add explicit "return X" instruction |
| Gateway crashes | Context overflow on spawn | Use `lightContext: true` |
| Spawn fails (10s gateway timeout) | Gateway CPU overload | Kill stale subagents first, then retry |

## Anti-Patterns

- ❌ Doing research yourself when a Researcher agent could handle it
- ❌ Running `python3 -c` inline in task descriptions
- ❌ Setting 120s timeouts on research tasks
- ❌ Re-spawning an agent that's still running (>60s = be patient)
- ❌ Not passing context because "the agent should know"

## Config (openclaw.json)

Set subagent defaults in `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "runTimeoutSeconds": 900,
        "maxConcurrent": 5
      }
    }
  }
}
```

Also set in `~/.openclaw/council-config.json`:

```json
{
  "default_timeout": 900,
  "max_tokens": 8192
}
```