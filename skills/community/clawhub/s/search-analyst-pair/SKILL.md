---
name: search-analyst-pair
description: Turn any research request into a structured, reviewable brief — fact collection, risk analysis, and recommendation in three deterministic steps.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - OPENCLAW_BASE_URL
        - OPENCLAW_TOKEN
      bins:
        - python3
        - curl
        - jq
    primaryEnv: OPENCLAW_TOKEN
    emoji: "🔍"
    homepage: "https://github.com/baobaodawang-creater/neo-agent-lab"
---

# Search Analyst Pair

This skill packages a deterministic `/hunt` workflow for OpenClaw.

When a user message starts with `/hunt`, the workflow follows a strict 3-hop chain:

1. **Search** (DeepSeek): gather facts and sources only.
2. **Analyst** (Gemini): analyze Search output and identify key points and risks.
3. **Main** (Kimi): synthesize Search + Analyst into final guidance.

## Why this skill

- Prevents ad-hoc routing for critical tasks.
- Separates **fact collection**, **analysis**, and **decision output**.
- Supports both native OpenClaw orchestration and a FastAPI fallback runner.

## Best-fit scenarios

- Time-sensitive research tasks that require reliable structure.
- Decision support where source traceability matters.
- Team workflows that need stable, reviewable output sections.

## Requirements

- OpenClaw gateway running and reachable.
- Agent IDs available: `main`, `search`, `analyst`.
- `tools.agentToAgent.enabled=true` in OpenClaw config.
- `subagents.allowAgents` configured:
  - `main` allows `search`, `analyst`
  - `search` allows `analyst`

## Behavior contract

- Trigger prefix: `/hunt`
- Fixed order: `Search -> Analyst -> Main`
- Fallback policy: if agent-to-agent spawn fails, the workflow must explicitly mark fallback output.

## Usage examples

```text
/hunt Review today's agent framework updates and give a practical migration plan.
```

```text
/hunt Collect top legal AI workflow changes this week and assess implementation risk.
```

## Output shape (recommended)

- `Search findings`
- `Analyst assessment`
- `Main conclusion`
