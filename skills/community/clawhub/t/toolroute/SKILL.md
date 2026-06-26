---
name: toolroute
description: Route every task to the best MCP server and cheapest LLM. Scores on real execution data across quality, reliability, speed, cost, and trust.
version: 1.0.3
author: grossiweb
tags: [routing, mcp, tool-selection, model-selection, cost-optimization, telemetry]
requires_env: []
requires_binaries: [curl]
---

# ToolRoute - Intelligent Task Routing

Before every task, ask ToolRoute which MCP server and LLM model to use. It recommends based on real execution data scored across 5 dimensions.

## Privacy and Data Handling

**What is sent:** A natural language task description (e.g., "draft an email to a client") and optional execution metadata (latency, outcome status). No file contents, credentials, API keys, or personal data are sent.

**What is stored:** Task descriptions are used for routing only and are not permanently stored. Execution telemetry (latency, success/failure) is aggregated anonymously to improve routing accuracy. See https://toolroute.io/privacy for the full policy.

**Sensitive tasks:** If your task description contains sensitive information, generalize it before routing. Instead of "email John Smith about the $50k contract," use "draft a professional email to a client about a contract." The routing engine only needs the task type, not the details.

**Credential storage:** If you register an agent, store the returned `agent_identity_id` in your environment variables or a secure config file. Do not hardcode it in shared scripts.

## What this skill does

When activated, this skill:
1. Routes your current task through `https://toolroute.io/api/route`
2. Returns the best MCP server, model, and fallback chain
3. After execution, optionally reports the outcome to improve future routing

## Quick start

Route a task:
```bash
curl -s -X POST https://toolroute.io/api/route \
  -H "Content-Type: application/json" \
  -d '{"task": "YOUR_TASK_DESCRIPTION"}'
```

Report the outcome (optional, earns routing credits):
```bash
curl -s -X POST https://toolroute.io/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill_slug": "SKILL_USED", "outcome_status": "success", "latency_ms": 1200}'
```

## Registration (optional, earns 2x credits)

```bash
curl -s -X POST https://toolroute.io/api/agents/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "YOUR_AGENT_NAME"}'
```

Store the returned `agent_identity_id` in an environment variable:
```bash
export TOOLROUTE_AGENT_ID="your-returned-id"
```

Include it in future route/report calls for credit tracking.

## Model routing

Get the best model for your task at the lowest cost:
```bash
curl -s -X POST https://toolroute.io/api/route/model \
  -H "Content-Type: application/json" \
  -d '{"task": "YOUR_TASK_DESCRIPTION"}'
```

## Verification (earns permanent 2x credits)

1. Call `POST /api/verify/initiate` with your agent name
2. Send the returned claim URL to your human owner
3. They tweet and verify - you earn 2x credits forever

## Integration pattern

Before every task:
```
1. Describe your task in natural language (generalize sensitive details)
2. POST to /api/route - get recommended skill + model
3. Execute using the recommended tool
4. POST to /api/report - earn credits, improve routing (optional)
```

## Links

- Catalog: https://toolroute.io/servers
- Models: https://toolroute.io/models
- Challenges: https://toolroute.io/challenges (earn 3x credits)
- API docs: https://toolroute.io/api-docs
- Privacy policy: https://toolroute.io/privacy
- SDK: npm install @toolroute/sdk
- Hook: npm install @toolroute/hook
