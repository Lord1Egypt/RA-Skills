---
name: wisgate-models
description: Query Wisgate for model pricing, capabilities, and configuration details. Use when adding a model to OpenClaw, comparing Wisgate pricing, or checking if a model supports a specific API type (Anthropic/OpenAI/Google). Also use when a less capable model needs help with Wisgate tasks.
metadata:
  openclaw:
    emoji: "🧙"
---

# Wisgate Model Management

## Canonical Model Catalog

**Always check `MODELS.json` first** before using Firecrawl or the API:

```bash
python3 -c "
import json
with open('MODELS.json') as f:
    data = json.load(f)
# List all models
for k, v in data.items():
    print(k)
"
```

To look up a specific model:
```bash
python3 -c "
import json, pprint
with open('MODELS.json') as f:
    data = json.load(f)
pprint.pprint(data.get('MODEL_ID'))
"
```
`MODELS.json` contains what you need for setting up the model in `openclaw.json`: `openclaw_provider_key`, `api_type`, `context_window`, `max_output_tokens`, `notes` (your and Florian's notes on that model), and all pricing fields.

## Adding a Model to OpenClaw

**Step 1:** Look up the model in `MODELS.json` to get all fields.

**Step 2:** Add to `agents.defaults.models` in `openclaw.json`:
```json
"PROVIDER_KEY/MODEL_ID": {}
```
e.g. `"custom-api-wisgate-ai-openai/qwen3-max": {}`

**Step 3:** Add the full model definition to the provider's `models` array:
```json
{
  "id": "MODEL_ID",
  "name": "Display Name (Wisgate)",
  "contextWindow": 200000,
  "maxTokens": 33000,
  "input": ["text"],
  "cost": {
    "input": 0.50,
    "output": 2.00,
    "cacheRead": 0.10,
    "cacheWrite": 0.50
  },
  "reasoning": false
}
```

- `reasoning: true` only for models with `-thinking` in the name
- `input: ["text"]` for LLMs; `["text", "image"]` for multimodal

## When MODELS.json Is Missing a Model

Use Firecrawl to fetch from Wisgate:
```bash
FIRECRAWL_API_KEY=[see_below_for_where_to_find_the_key] \
python3 ~/.openclaw/workspace/skills/firecrawl-search/scripts/scrape.py \
"https://wisgate.ai/models/MODEL_ID"
```

Extract from output:
- CTX → `contextWindow`
- `Input: **$X.XX** per 1M tokens` → `cost.input`
- `Output: **$Y.YY** per 1M tokens` → `cost.output`
- `Cache Read:` / `Cache Write:` → `cost.cacheRead` / `cost.cacheWrite`

Then also **add the new model to `MODELS.json`** so future lookups work.

## API Type Mapping

| Endpoint Type | OpenClaw Provider | Base URL |
|---|---|---|
| Anthropic (Claude) | `custom-api-wisgate-ai` | `https://api.wisgate.ai/` |
| OpenAI compatible | `custom-api-wisgate-ai-openai` | `https://api.wisgate.ai/v1` |
| Google (Gemini) | `custom-api-wisgate-google` | `https://api.wisgate.ai/v1beta` |

## Firecrawl API Key

Stored in `TOOLS.md`


