---
name: spendex-ai-router
description: Smart AI router — automatically picks the best & cheapest LLM for every prompt. BYOK, tracks costs, enforces budgets. Supports 25+ providers.
requires:
  env:
    - SPENDEX_API_KEY
  bins:
    - curl
    - jq
---

# Spendex AI Router

Stop overpaying for AI. Spendex analyzes every prompt and routes it to the best model at the lowest cost — automatically.

**Bring Your Own Keys** — connect your existing OpenAI, Anthropic, Google, Mistral, DeepSeek, Groq, Together, Fireworks, Cohere keys in the Spendex dashboard. Spendex routes between them intelligently.

## Setup

1. Create a free account at https://spendex.ai
2. Connect your provider API keys in the dashboard (OpenAI, Anthropic, Google, etc.)
3. Copy your Spendex API key (`spx_...`) from the dashboard
4. Set it as an environment variable: `export SPENDEX_API_KEY="spx_your_key_here"`

## Chat Completion

When the user asks you to generate text, answer questions, write code, or any task that requires an LLM — route the request through Spendex instead of calling providers directly.

Spendex automatically classifies prompt complexity (simple/medium/complex) and picks the best model+provider combo for cost and quality.

```bash
curl -s -X POST "https://app.spendexai.com/v1/chat/completions" \
  -H "Authorization: Bearer $SPENDEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"messages\": [{\"role\": \"user\", \"content\": \"USER_PROMPT_HERE\"}],
    \"stream\": false
  }" | jq '{
    content: .choices[0].message.content,
    model: .model,
    cost: .usage.cost,
    saved: .usage.saved,
    classification: .usage.classification,
    provider: .usage.provider
  }'
```

Replace `USER_PROMPT_HERE` with the actual user message.

The response includes:
- `content` — the AI response
- `model` — which model was selected by the router
- `cost` — exact cost in USD
- `saved` — money saved vs. using the most expensive model
- `classification` — prompt complexity (simple / medium / complex)
- `provider` — which provider served the request

## Check Credit Balance

Show the user how much credit they have left.

```bash
curl -s "https://app.spendexai.com/api/credits/balance" \
  -H "Authorization: Bearer $SPENDEX_API_KEY" | jq '.'
```

## Check Budgets

Show active budgets and how much has been spent vs. the limit.

```bash
curl -s "https://app.spendexai.com/api/budgets" \
  -H "Authorization: Bearer $SPENDEX_API_KEY" | jq '.'
```

## Check Usage Stats

Show recent usage broken down by model and provider.

```bash
curl -s "https://app.spendexai.com/api/usage/realtime?stats=true" \
  -H "Authorization: Bearer $SPENDEX_API_KEY" | jq '.'
```

## Check Cost Savings

Show how much money Spendex has saved compared to always using the most expensive model.

```bash
curl -s "https://app.spendexai.com/api/analytics/savings" \
  -H "Authorization: Bearer $SPENDEX_API_KEY" | jq '.'
```

## Tips

- You can add a `"model"` field to force a specific model (e.g. `"model": "gpt-4o"`), but leaving it empty lets Spendex pick the optimal one.
- For conversations with history, include the full message array in `"messages"`.
- Spendex deduplicates identical requests to avoid double-billing.
- If the user asks "how much am I spending?", use the balance + usage + savings endpoints to give a full picture.
