---
name: reivo
description: Track AI agent costs in real-time, set budget limits, and auto-detect runaway loops. Smart routing reduces costs 40-60%. Works with OpenAI, Anthropic, and Google models. Free to use — just route your API calls through the Reivo proxy.
homepage: https://reivo.dev
user-invocable: true
metadata: {"openclaw": {"emoji": "💰", "homepage": "https://reivo.dev", "requires": {"env": ["REIVO_API_KEY"], "bins": ["curl", "node"]}, "primaryEnv": "REIVO_API_KEY", "envVars": [{"name": "REIVO_API_KEY", "required": true, "description": "Reivo API key (starts with rv_). Get one free at https://reivo.dev"}], "os": ["darwin", "linux"], "author": "tazsat0512"}}
---

# Reivo — AI Agent Cost Optimizer

You are now equipped with Reivo, a cost optimization and protection layer for AI API calls.

## What Reivo Does

Reivo is a transparent proxy that sits between your agent and the LLM provider. It:
- **Routes to cheaper models** — analyzes each request and picks the cheapest model that delivers the same quality (40-60% cost reduction)
- **Tracks costs** per session, agent, and model in real-time
- **Enforces budget limits** — blocks requests when spending exceeds the limit
- **Detects runaway loops** — auto-stops agents stuck in infinite loops (hash match + TF-IDF cosine similarity)
- **Anomaly detection** — EWMA-based spike detection flags abnormal usage patterns
- **Graceful degradation** — 4-level progressive response (normal → aggressive routing → new sessions only → blocked)
- **Sends Slack alerts** — budget warnings, loop detection, and anomaly notifications

The guardrail engine is open source: [reivo-guard](https://github.com/tazsat0512/reivo-guard) (TypeScript + Python).

## Configuration

The user's Reivo API key is available as `$REIVO_API_KEY`.

**Proxy base URLs** (use these instead of direct provider URLs):
- OpenAI: `https://proxy.reivo.dev/openai/v1`
- Anthropic: `https://proxy.reivo.dev/anthropic/v1`
- Google: `https://proxy.reivo.dev/google/v1beta`

**Dashboard:** https://app.reivo.dev

## Available Commands

When the user asks about costs, budgets, or Reivo, use the following:

### Check Costs

When the user asks "how much am I spending?", "show costs", "cost report", or similar:

```bash
curl -s -H "Authorization: Bearer $REIVO_API_KEY" \
  "https://app.reivo.dev/api/v1/overview?days=7"
```

Present the response as:
- Total spend for the period
- Daily cost breakdown (as a simple text chart)
- Top models by cost
- Request count

### Check Defense Status

When the user asks "budget status", "am I safe?", "loop status", or similar:

```bash
curl -s -H "Authorization: Bearer $REIVO_API_KEY" \
  "https://app.reivo.dev/api/v1/defense-status"
```

Present as:
- Budget: $X.XX / $Y.YY (Z%) with visual progress bar
- Loops detected: N today, N this week
- Requests blocked: N today, N this week

### Get Optimization Tips

When the user asks "how can I save?", "optimization tips", "reduce costs", or similar:

```bash
curl -s -H "Authorization: Bearer $REIVO_API_KEY" \
  "https://app.reivo.dev/api/v1/optimization"
```

Present each tip with severity, description, and estimated savings. Tips include:
- **Prompt caching** — duplicate prompts that could use caching
- **Max tokens waste** — requests using <20% of their max_tokens budget
- **Unused tools** — tool definitions sent but never called

### Set Budget

When the user says "set budget to $50", "limit spending", or similar:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $REIVO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"budgetLimitUsd": 50}' \
  "https://app.reivo.dev/api/v1/settings"
```

Confirm the budget was set and explain that requests will be blocked once the limit is reached.

### Clear Budget

When the user says "remove budget", "clear limit", or similar:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $REIVO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"budgetLimitUsd": null}' \
  "https://app.reivo.dev/api/v1/settings"
```

### Set Routing Mode

When the user says "aggressive mode", "quality mode", or "change routing":

```bash
curl -s -X POST \
  -H "Authorization: Bearer $REIVO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"routingMode": "aggressive"}' \
  "https://app.reivo.dev/api/v1/settings"
```

Modes: `aggressive` (maximize savings), `balanced` (default), `quality` (prefer original model).

### Configure Slack Notifications

When the user says "set up Slack", "notify me on Slack", or similar:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $REIVO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slackWebhookUrl": "https://hooks.slack.com/services/..."}' \
  "https://app.reivo.dev/api/v1/settings"
```

### Manage Provider API Keys

Provider keys should be managed via the dashboard for security:

> **Add or rotate provider keys at:** https://app.reivo.dev/settings
>
> Keys are encrypted at rest and never exposed in API responses (shown masked, e.g. `sk-abc1...xyz9`).
> For maximum security, create limited-scope or project-scoped keys dedicated to Reivo.

To list currently configured keys:

```bash
curl -s -H "Authorization: Bearer $REIVO_API_KEY" \
  "https://app.reivo.dev/api/v1/provider-keys"
```

### View Agent Breakdown

When the user asks "which agent costs the most?", "cost by agent", or similar:

```bash
curl -s -H "Authorization: Bearer $REIVO_API_KEY" \
  "https://app.reivo.dev/api/v1/agents?days=30"
```

Present agent-by-agent and model-by-model cost breakdown.

### Monthly Report

When the user asks "monthly report", "this month's spending", or similar:

```bash
curl -s -H "Authorization: Bearer $REIVO_API_KEY" \
  "https://app.reivo.dev/api/v1/overview?days=30"
```

### Open Dashboard

When the user says "open dashboard", "show dashboard", or "I want more detail":

> **Reivo Dashboard:** https://app.reivo.dev
>
> Sign in to see interactive cost charts, session replays, loop detection history, and optimization recommendations.

## Setup Instructions

If the user hasn't set up Reivo yet, guide them:

1. **Sign up** at https://app.reivo.dev
2. **Generate an API key** in Settings (format: `rv_...`)
3. **Set the environment variable:**
   ```bash
   export REIVO_API_KEY="rv_your_key_here"
   ```
4. **Add provider keys** via the dashboard at https://app.reivo.dev/settings (recommended for security — keys are encrypted at rest)
5. **Route API calls through the proxy** by changing the base URL in your provider config.

For OpenClaw specifically, update the provider configuration:
```json
{
  "providers": [
    {
      "name": "openai",
      "apiKey": "${REIVO_API_KEY}",
      "baseUrl": "https://proxy.reivo.dev/openai/v1"
    },
    {
      "name": "anthropic",
      "apiKey": "${REIVO_API_KEY}",
      "baseUrl": "https://proxy.reivo.dev/anthropic/v1"
    }
  ]
}
```

The proxy forwards your requests to the real provider using the provider key you registered. Your original API keys never leave the Reivo server.

## Self-Hosted Guardrails

Want guardrails without the proxy? Use [reivo-guard](https://github.com/tazsat0512/reivo-guard) directly:

```bash
pip install reivo-guard    # Python
npm install reivo-guard    # TypeScript
```

reivo-guard provides budget enforcement, loop detection, anomaly detection, and more — all open source (MIT). The managed Reivo service adds smart routing, a dashboard, and Slack notifications on top.

## What Reivo does NOT store

- Prompt or completion content (forwarded and discarded)
- Conversation history
- Raw API keys in the database (encrypted at rest, decrypted only during proxying)

Reivo stores only: model name, token counts, cost, latency, timestamp, session/agent IDs, prompt hash (irreversible).

## Behavior Guidelines

- Always show costs in USD with 2 decimal places
- When budget is over 80%, proactively warn the user
- If an API call fails with 429 from Reivo proxy, explain it's a budget block (not rate limiting)
- Never expose the full API key in output — show only `rv_...xxxx` (last 4 chars)
- Suggest the dashboard for detailed analysis beyond what the API provides
