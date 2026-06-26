---
name: pura
description: Cut your OpenClaw agent's LLM costs 40-60%. Automatic model selection routes simple tasks to cheap providers, complex tasks to premium ones. Free for 5,000 requests.
metadata: {"openclaw": {"requires": {"env": ["PURA_API_KEY"]}, "optional_env": ["PURA_GATEWAY_URL"], "primaryEnv": "PURA_API_KEY", "emoji": "⚡", "homepage": "https://pura.xyz", "tags": ["llm", "routing", "cost-optimization", "ai-agent", "openclaw"]}}
---

# Pura — cut your agent's LLM costs 40-60%

Your OpenClaw agent probably sends every request to GPT-4o. Most of those requests are simple enough for a model that costs 10x less. Pura sits between your agent and the LLM providers, scores each request's complexity, and routes it to the cheapest model that can handle it.

Cascade routing: tries Groq first ($0.00059/1K tokens). If the response looks weak (too short, hedging language, refusal), it escalates to Gemini, then OpenAI, then Anthropic. Your agent gets a good answer. You pay the minimum.

Drop-in OpenAI-compatible. One env var change.

## What you get

- 4 providers (Groq, Gemini, OpenAI, Anthropic) behind one endpoint
- Automatic complexity scoring — no manual model selection
- Cascade routing — cheapest sufficient tier per request
- Per-request cost headers so your agent tracks spend
- Daily cost reports and income statements
- Free tier: 5,000 requests, no credit card

## Setup

Get an API key:

```bash
curl -s -X POST https://api.pura.xyz/api/keys \
  -H "Content-Type: application/json" \
  -d '{"label":"my-agent"}' | python3 -m json.tool
```

Save the returned key (starts with `pura_`):

```bash
export PURA_API_KEY="pura_your_key_here"
```

## Sending requests

Pura is OpenAI SDK-compatible. Change your base URL and you're done:

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://api.pura.xyz/v1",
    api_key=os.environ["PURA_API_KEY"]
)

response = client.chat.completions.create(
    model="auto",  # Pura picks the cheapest capable model
    messages=[{"role": "user", "content": "Hello"}]
)
```

Or with curl:

```bash
curl -s -X POST https://api.pura.xyz/v1/chat/completions \
  -H "Authorization: Bearer $PURA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}], "stream": false}'
```

## Response headers

Every response includes routing metadata:

| Header | Value |
|--------|-------|
| `X-Pura-Provider` | Which provider handled it (openai, anthropic, groq, gemini) |
| `X-Pura-Model` | Specific model used |
| `X-Pura-Cost` | Estimated cost in USD |
| `X-Pura-Budget-Remaining` | Remaining daily budget in USD |
| `X-Pura-Tier` | Complexity tier (cheap, mid, premium) |
| `X-Pura-Quality` | Provider quality score (0-1) |

## Cost reports

```bash
# 24h spend breakdown
curl -s https://api.pura.xyz/api/report \
  -H "Authorization: Bearer $PURA_API_KEY" | python3 -m json.tool

# Formatted income statement
curl -s https://api.pura.xyz/api/income \
  -H "Authorization: Bearer $PURA_API_KEY" | python3 -m json.tool
```

## Lightning wallet

5,000 free requests included. After that, fund a Lightning wallet:

```bash
# Get a funding invoice
curl -s -X POST https://api.pura.xyz/api/wallet/fund \
  -H "Authorization: Bearer $PURA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10000}' | python3 -m json.tool

# Check balance
curl -s https://api.pura.xyz/api/wallet/balance \
  -H "Authorization: Bearer $PURA_API_KEY" | python3 -m json.tool
```

## Model behavior

Set `model="auto"` or omit the model field entirely — both trigger cascade routing, where Pura scores your request's complexity and picks the cheapest provider that can handle it.

If you specify a model name directly (e.g. `gpt-4o`, `claude-sonnet-4-20250514`), Pura skips the cascade and routes straight to that provider.

## Explicit model routing

Override auto-routing by specifying a model:

```bash
# Force GPT-4o
curl -s -X POST https://api.pura.xyz/v1/chat/completions \
  -H "Authorization: Bearer $PURA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o", "messages": [{"role":"user","content":"Hello"}], "stream": false}'
```

Supported models: `gpt-4o`, `claude-sonnet-4-20250514`, `llama-3.3-70b-versatile`, `gemini-2.0-flash`.

## Routing hints

Influence provider selection without forcing a specific model:

```json
{
  "messages": [{"role": "user", "content": "..."}],
  "routing": {
    "quality": "high",
    "prefer": "anthropic",
    "maxCost": 0.01,
    "maxLatency": 5000
  }
}
```

## How routing works

Pura scores each request's complexity based on message length, code blocks, reasoning triggers, and conversation depth. Simple tasks go to Groq or Gemini. Complex reasoning goes to Anthropic or OpenAI. Quality scores (derived from recent success rate and latency) weight the selection so underperforming providers get fewer requests until they recover.

Cascade routing adds a second layer: if the cheapest provider's response looks bad (too short, hedging, refusal, incomplete), Pura automatically retries at the next tier up. You only pay premium prices when the cheap answer was genuinely insufficient.

## Typical cost savings

| Request type | Direct GPT-4o cost | Pura cascade cost | Savings |
|---|---|---|---|
| Simple Q&A ("What is X?") | $0.005 | $0.00059 (Groq) | 88% |
| Code explanation | $0.005 | $0.00125 (Gemini) | 75% |
| Complex reasoning | $0.005 | $0.005 (GPT-4o) | 0% |
| Long-context analysis | $0.005 | $0.003 (Claude) | 40% |

In practice, 70-80% of agent requests are simple enough for the cheapest tier.

## Security note

Your API keys for OpenAI, Anthropic, Groq, and Gemini stay on the Pura server. They never touch your agent or the OpenClaw runtime. If you are running an OpenClaw agent with plugins from untrusted sources, routing through Pura means those plugins cannot access your provider API keys.

## Links

- Gateway: <https://api.pura.xyz>
- Website: <https://pura.xyz>
- Compare cascade routing: <https://pura.xyz/compare>
- Docs: <https://pura.xyz/docs>
- GitHub: <https://github.com/puraxyz/puraxyz>
