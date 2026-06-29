---
name: minimax
description: Call the MiniMax API (MiniMax-M3, MiniMax-M2.7, MiniMax-M2.7-highspeed, MiniMax-M2.5, MiniMax-M2.5-highspeed, MiniMax-M2.1, MiniMax-M2) through RunAPI using the official OpenAI SDK or compatible clients. Use when the user asks for MiniMax text chat, streaming completions, Anthropic or Gemini protocol compatibility, or when they want to point an existing OpenAI SDK setup at RunAPI as the base URL.
documentation: https://runapi.ai/models/minimax.md
provider_page: https://runapi.ai/providers/minimax.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/minimax
    primaryEnv: OPENAI_API_KEY
    requires:
      env:
      - OPENAI_API_KEY
      - OPENAI_BASE_URL
    envVars:
    - name: OPENAI_API_KEY
      required: true
      description: RunAPI API key used by OpenAI-compatible MiniMax clients.
    - name: OPENAI_BASE_URL
      required: true
      description: Set to https://runapi.ai/v1 for MiniMax on RunAPI.
---

# MiniMax on RunAPI

Use the official **OpenAI SDK** or any OpenAI-compatible HTTP client and switch
the base URL to `https://runapi.ai/v1`. This skill covers MiniMax **text**
models. For Hailuo video generation, install the separate Hailuo skill.

## Setup

```dotenv
OPENAI_API_KEY=YOUR_RUNAPI_TOKEN
OPENAI_BASE_URL=https://runapi.ai/v1
```

Get a RunAPI API Key at <https://runapi.ai/api_keys>.

## Core recipe - Chat Completions

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_RUNAPI_TOKEN",
    base_url="https://runapi.ai/v1",
)

response = client.chat.completions.create(
    model="MiniMax-M3",
    messages=[{"role": "user", "content": "Draft a support response."}],
)
print(response.choices[0].message.content)
print(response.usage)
```

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "YOUR_RUNAPI_TOKEN",
  baseURL: "https://runapi.ai/v1",
});

const response = await client.chat.completions.create({
  model: "MiniMax-M3",
  messages: [{ role: "user", content: "Draft a support response." }],
});
```

## Streaming

```python
stream = client.chat.completions.create(
    model="MiniMax-M2.7-highspeed",
    messages=[{"role": "user", "content": "Write a short status update."}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
```

Streaming runs through a regional edge proxy so the request does not hold a
Rails/Puma thread. Long generations should always stream.

## Protocol compatibility

MiniMax text models are also available through RunAPI's Anthropic-compatible
and Gemini `contents` client surfaces. RunAPI bridges those request and
response shapes to the OpenAI-compatible chat request format, so use these protocol
paths only when an existing tool expects those formats:

```bash
curl -X POST "https://runapi.ai/v1/messages" \
  -H "x-api-key: YOUR_RUNAPI_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiniMax-M2",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Draft a concise answer."}]
  }'
```

```bash
curl -X POST \
  "https://runapi.ai/v1beta/models/MiniMax-M2:streamGenerateContent" \
  -H "x-goog-api-key: YOUR_RUNAPI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"role":"user","parts":[{"text":"Hello!"}]}]}'
```

For new app code, prefer the OpenAI-compatible setup.

## List models

```bash
curl https://runapi.ai/v1/models \
  -H "Authorization: Bearer YOUR_RUNAPI_TOKEN"
```

## Supported models

| Model ID | Use when |
|---|---|
| `MiniMax-M3` | Latest MiniMax text chat |
| `MiniMax-M2.7` | MiniMax M2.7 compatibility |
| `MiniMax-M2.7-highspeed` | Faster MiniMax M2.7 requests |
| `MiniMax-M2.5` | MiniMax M2.5 compatibility |
| `MiniMax-M2.5-highspeed` | Faster MiniMax M2.5 requests |
| `MiniMax-M2.1` | MiniMax M2.1 compatibility |
| `MiniMax-M2` | MiniMax M2 compatibility |

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/minimax.md
- Provider comparison: https://runapi.ai/providers/minimax.md
- Catalog: https://runapi.ai/models.md

## Agent rules

- Keep API keys in `OPENAI_API_KEY`, `RUNAPI_TOKEN`, or a secret manager; never
  inline them in commits or shell history.
- Default new integrations to the OpenAI-compatible client at
  `https://runapi.ai/v1`.
- Use streaming for responses longer than a few hundred tokens.
- For Hailuo video generation, use the Hailuo model skill instead of this text
  LLM skill.
- For pricing, rate-limit, and commercial-usage answers, link to
  https://runapi.ai/models/minimax.md rather than copying values.
