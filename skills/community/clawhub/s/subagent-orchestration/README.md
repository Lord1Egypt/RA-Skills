# Subagent Orchestration

An OpenClaw skill for effective subagent delegation, spawning, and debugging.

## Why This Exists

OpenClaw subagents have sandbox constraints that aren't obvious until you hit them. Agents time out, can't browse the web, can't run inline Python — and you only learn this after watching them fail. This skill captures those lessons so you don't have to re-learn them.

## Agent Types

| Type | Tools | Use For |
|------|-------|---------|
| **Worker** | Default (no web) | File ops, script execution, git, code changes |
| **Researcher** | `ollama_web_search`, `ollama_web_fetch` | Web research, API lookups, live data |
| **Council** | Multi-model, no web | Analysis, review, decision-making with diverse perspectives |

## Key Constraints

Default subagents **cannot**:
- Use `ollama_web_fetch` or `ollama_web_search`
- Run `python3 -c "..."` inline commands
- Access the main session's conversation history

They **can**:
- Read/write files
- Run scripts from `.py` files
- Execute simple shell commands

## Quick Start

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

> **Use the [Council of LLMs](https://github.com/wahajahmed010/council-of-llms) skill for proper multi-model councils.**
> Single-model "councils" (one subagent roleplaying 3 experts) cause context overflow and produce shallow analysis.

Spawn 3 parallel subagents with different models and perspectives:

```
# Strategos — strategy & business impact
sessions_spawn(
  model: "ollama/kimi-k2.6:cloud",
  label: "Council-Strategos",
  runtime: "subagent", mode: "run", lightContext: true,
  runTimeoutSeconds: 900,
  task: "You are Strategos. [context]. Analyze from a STRATEGIC perspective."
)

# Analyticos — data quality & edge cases
sessions_spawn(
  model: "ollama/deepseek-v4-pro:cloud",
  label: "Council-Analyticos",
  runtime: "subagent", mode: "run", lightContext: true,
  runTimeoutSeconds: 900,
  task: "You are Analyticos. [context]. Analyze from an ANALYTICAL perspective."
)

# Creativos — UX & novel approaches
sessions_spawn(
  model: "ollama/gemma4:31b-cloud",
  label: "Council-Creativos",
  runtime: "subagent", mode: "run", lightContext: true,
  runTimeoutSeconds: 900,
  task: "You are Creativos. [context]. Analyze from a CREATIVE perspective."
)
```

Then synthesize all 3 outputs into a unified verdict. See the [Council of LLMs skill](https://github.com/wahajahmed010/council-of-llms) for full details.

## Timeout Strategy

| Task Type | Min Timeout | Recommended |
|-----------|------------|-------------|
| Simple file ops | 120s | 180s |
| Research (web) | 300s | 600s |
| Council/review | 300s | 600s |
| Complex multi-step | 600s | 900s |

**Never rush agents.** Quality > speed.

## Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Agent times out | Can't access web tools | Use `toolsAllow` or pre-fetch content |
| Agent times out | Can't run inline Python | Write `.py` file, pass path |
| Agent times out | `runTimeoutSeconds` too low | Set `runTimeoutSeconds: 900` |
| Agent times out | Gateway under load (10s spawn timeout) | Kill zombie subagents, wait, retry |
| Agent returns nothing | Missing context | Paste data in `task` parameter |
| Agent stuck in loop | Vague task | Add explicit "return X" instruction |
| Gateway crashes | Context overflow on spawn | Use `lightContext: true` |
| Council returns shallow analysis | Single-model roleplay | Use [Council of LLMs](https://github.com/wahajahmed010/council-of-llms) multi-model pattern |
| Council context overflow | Too much data in task | Keep task descriptions under 2000 words |
| Spawn fails (10s gateway timeout) | Gateway CPU overload | Kill stale subagents first, then retry |

## Configuration

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

Set council models in `~/.openclaw/council-config.json`:

```json
{
  "council_models": [
    "ollama/kimi-k2.6:cloud",
    "ollama/deepseek-v4-pro:cloud",
    "ollama/gemma4:31b-cloud"
  ],
  "default_timeout": 900,
  "max_tokens": 8192
}
```

## Companion Skills

- **[Council of LLMs](https://github.com/wahajahmed010/council-of-llms)** — Multi-model deliberation pattern. Spawn 3 subagents with different models and perspectives, synthesize into a unified verdict. Essential for high-stakes decisions that need diverse viewpoints.

## Install

```bash
# Install both skills together
openclaw skills install wahajahmed010/subagent-orchestration
openclaw skills install wahajahmed010/council-of-llms

# Or via ClawHub
clawhub install subagent-orchestration
clawhub install council-of-llms
```

## License

MIT-0