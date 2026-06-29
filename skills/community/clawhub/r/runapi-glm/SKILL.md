---
name: glm
description: Call the GLM API (glm-5.1, glm-5-turbo, glm-5, glm-4.7, glm-4.6, glm-4.5, glm-4.5-air) through RunAPI using the official OpenAI SDK or compatible clients. Use when the user asks for GLM chat, streaming completions, Anthropic or Gemini protocol compatibility, or when they want to point an existing OpenAI SDK setup at RunAPI as the base URL.
documentation: https://runapi.ai/models/glm.md
provider_page: https://runapi.ai/providers/z-ai.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/glm
    primaryEnv: OPENAI_API_KEY
    requires:
      env:
      - OPENAI_API_KEY
      - OPENAI_BASE_URL
    envVars:
    - name: OPENAI_API_KEY
      required: true
      description: RunAPI API key used by OpenAI-compatible GLM clients.
    - name: OPENAI_BASE_URL
      required: true
      description: Set to https://runapi.ai/v1 for GLM on RunAPI.
---

# GLM on RunAPI

Use the official **OpenAI SDK** or any OpenAI-compatible HTTP client and switch
the base URL to `https://runapi.ai/v1`. The primary endpoint is Chat
Completions (`POST /v1/chat/completions`).

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
    model="glm-5.1",
    messages=[{"role": "user", "content": "Summarize this design review."}],
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
  model: "glm-5.1",
  messages: [{ role: "user", content: "Summarize this design review." }],
});
```

```bash
curl -X POST "https://runapi.ai/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_RUNAPI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5.1",
    "messages": [{"role": "user", "content": "Hello, GLM!"}]
  }'
```

## Streaming

```python
stream = client.chat.completions.create(
    model="glm-5-turbo",
    messages=[{"role": "user", "content": "Write a short implementation plan."}],
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

GLM models are also available through RunAPI's Anthropic-compatible and Gemini
`contents` client surfaces. RunAPI bridges those request and response shapes to
the OpenAI-compatible chat request format, so use these protocol paths only when an
existing agent runtime requires them:

```bash
curl -X POST "https://runapi.ai/v1/messages" \
  -H "x-api-key: YOUR_RUNAPI_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4.6",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Draft a concise answer."}]
  }'
```

```bash
curl -X POST \
  "https://runapi.ai/v1beta/models/glm-4.6:streamGenerateContent" \
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
| `glm-5.1` | Latest GLM chat workloads |
| `glm-5-turbo` | Faster GLM chat |
| `glm-5` | General GLM 5 requests |
| `glm-4.7` | GLM 4.7 compatibility |
| `glm-4.6` | Stable GLM 4.6 requests |
| `glm-4.5` | GLM 4.5 compatibility |
| `glm-4.5-air` | Lightweight GLM 4.5 requests |

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/glm.md
- Provider comparison: https://runapi.ai/providers/z-ai.md
- Catalog: https://runapi.ai/models.md

## Agent rules

- Keep API keys in `OPENAI_API_KEY`, `RUNAPI_TOKEN`, or a secret manager; never
  inline them in commits or shell history.
- Default new integrations to the OpenAI-compatible client at
  `https://runapi.ai/v1`.
- Use streaming for responses longer than a few hundred tokens.
- For pricing, rate-limit, and commercial-usage answers, link to
  https://runapi.ai/models/glm.md rather than copying values.
