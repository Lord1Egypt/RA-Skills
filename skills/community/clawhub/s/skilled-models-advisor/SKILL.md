---
name: skilled-models-advisor
description: >
  Consult the tool-models agent for model selection, cost estimation, capability
  queries, and provider comparisons. Use when choosing a model for any task,
  comparing costs, checking what's available, or answering "which model should I
  use for X?" — do not guess from training data, the database is always fresher.
---

# Skilled Models Advisor

Provides access to the `tool-models` agent and its query CLI for data-driven
model selection. All recommendations default to models we have active credentials
for. Pass `--all` to any command to see the full 2,700+ model universe.

---

## When to use this skill

Consult `tool-models` before:

- **Spawning a sub-agent** — pick the right model for the task at hand
- **User asks "which model for X"** — always query rather than guess
- **Estimating costs** — especially before high-volume or recurring workloads
- **Recommending a config change** — primary/fallback assignments
- **Comparing providers for the same model** — context limits and output caps differ
- **Checking if a model supports vision, PDF, reasoning, or function calling**

Do NOT guess model specs from training data. Prices change, new models appear,
and provider limits (output caps, context) vary from the model's stated maximum.

---

## Spawn syntax

```javascript
// Minimal — natural language question
sessions_spawn({
  agentId: "tool-models",
  runtime: "subagent",
  task: "Which model is best for processing long legal PDFs on a $50/month budget?"
})

// With structured context
sessions_spawn({
  agentId: "tool-models",
  runtime: "subagent",
  task: "Compare claude-sonnet-4-6 vs gemini-2.5-flash for a high-volume summarization pipeline. We process ~2M input tokens and ~200k output tokens per day."
})

// Model selection for a spawn
sessions_spawn({
  agentId: "tool-models",
  runtime: "subagent",
  task: "I'm about to spawn a coding sub-agent for refactoring a large CFML codebase. What's the best accessible model balancing code quality and cost?"
})
```

---

## Direct CLI (when running in tool-models workspace)

```bash
QUERY="python3 $HOME/.openclaw/workspace-tool-models/skills/model-advisor/scripts/query.py"

# Stats — what's in the database, what we have access to
$QUERY stats

# Task-based recommendation (accessible models only by default)
$QUERY recommend "summarize long PDFs cheaply"
$QUERY recommend "complex reasoning and code generation"
$QUERY recommend "real-time low-latency chat"
$QUERY recommend "process images and extract structured data"

# Structured filters
$QUERY filter --reasoning --available                       # reasoning models in OpenClaw
$QUERY filter --cost-max 0.5 --ctx-min 128000              # under $0.50/M, 128k+ context
$QUERY filter --vision --pdf --cost-max 1                  # vision+PDF under $1/M
$QUERY filter --cost-max 0                                 # free models only

# Side-by-side comparison
$QUERY compare gpt-4.1 claude-sonnet-4-6 gemini-2.5-flash
$QUERY compare mistral-medium-latest mistral-small-latest

# Cost estimation
$QUERY cost gemini-2.5-flash --input 1000000 --output 100000
$QUERY cost claude-sonnet-4-6 --input 50000 --output 5000 --monthly 1000

# Top models by metric
$QUERY top --by cost          # cheapest accessible models
$QUERY top --by ctx --count 5 # largest context windows

# Provider overview
$QUERY providers

# Full record for a model
$QUERY get gemini-2.5-flash
```

---

## Common scenarios

### "What model should I use for [task]?"
```javascript
sessions_spawn({
  agentId: "tool-models",
  runtime: "subagent",
  task: `recommend "${task}" — return top 3 with reasoning`
})
```

### "How much will this cost?"
```javascript
sessions_spawn({
  agentId: "tool-models",
  runtime: "subagent",
  task: `Estimate monthly cost for processing ${inputTokens} input + ${outputTokens} output tokens/day using ${model}. Also compare with the top 2 cheaper alternatives.`
})
```

### "Is [model] available and does it support [capability]?"
```javascript
sessions_spawn({
  agentId: "tool-models",
  runtime: "subagent",
  task: `get ${model} — check if it supports vision and PDF input, and what context/output limits apply on each provider`
})
```

### "What's the best free model for [task]?"
```javascript
sessions_spawn({
  agentId: "tool-models",
  runtime: "subagent",
  task: `recommend "${task}" --cost-max 0 — only free models`
})
```

---

## Notes

- **`accessible` = we have a working API key for that provider right now**
- **`piaiAvailable` = model is in OpenClaw's built-in catalog** (subset of accessible)
- Provider-reported limits always override generic specs (SambaNova caps many models at 3k output; Groq caps at 32k — these differ from the model's stated max)
- Database refreshed nightly by the `model-scanner` cron job
- Data sources: OpenClaw pi-ai catalog → LiteLLM → OpenRouter → live provider APIs
