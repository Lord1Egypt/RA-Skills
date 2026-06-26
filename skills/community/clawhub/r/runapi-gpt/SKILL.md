---
name: gpt
description: Call the GPT API (gpt-5.2, gpt-5.4, gpt-5.4-mini, gpt-5.5, gpt-5.3-codex) and OpenAI text embeddings through RunAPI using the official OpenAI SDK, Anthropic SDK, Gemini contents clients, or compatible clients. Use when the user asks for OpenAI / GPT chat, streaming completions, vision input, tool use / function calling, reasoning effort, the Responses API, embeddings, semantic search vectors, Codex coding tasks, Anthropic or Gemini protocol compatibility, or when they want to point an existing LLM SDK setup at RunAPI as the base URL.
documentation: https://runapi.ai/models/gpt.md
provider_page: https://runapi.ai/providers/openai.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/gpt
    primaryEnv: OPENAI_API_KEY
    requires:
      env:
      - OPENAI_API_KEY
      - OPENAI_BASE_URL
    envVars:
    - name: OPENAI_API_KEY
      required: true
      description: RunAPI API key used by OpenAI-compatible SDKs.
    - name: OPENAI_BASE_URL
      required: true
      description: Set to https://runapi.ai/v1 for GPT on RunAPI.
---

# GPT on RunAPI

Use the official **OpenAI SDK** (Python, TypeScript, Ruby) -- or any
OpenAI-compatible HTTP client -- and switch the base URL to
`https://runapi.ai/v1`. The endpoints speak the standard OpenAI protocol:
**Chat Completions** (`POST /v1/chat/completions`), the **Responses API**
(`POST /v1/responses`), and **Embeddings** (`POST /v1/embeddings`). No client
code changes beyond `base_url` and `api_key`.

## Setup

```dotenv
OPENAI_API_KEY=YOUR_RUNAPI_TOKEN
OPENAI_BASE_URL=https://runapi.ai/v1
```

Get a RunAPI API Key at <https://runapi.ai/api_keys>.

| Language | Init |
|---|---|
| Python | `OpenAI(api_key=..., base_url="https://runapi.ai/v1")` |
| TypeScript | `new OpenAI({ apiKey: ..., baseURL: "https://runapi.ai/v1" })` |
| Ruby | `OpenAI::Client.new(access_token: ..., uri_base: "https://runapi.ai/v1")` |
| curl | `POST https://runapi.ai/v1/chat/completions` (or `/v1/responses`, `/v1/embeddings`) |

## Pick the right endpoint

| Model | Endpoint to use |
|---|---|
| `gpt-5.2`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-5.5`, `gpt-5.3-codex`, `gpt-5.3-codex-spark` | Chat Completions **or** Responses |
| `gpt-5.2-pro`, `gpt-5.4-pro`, `gpt-5.5-pro` | Responses **only** |
| `text-embedding-3-large`, `text-embedding-3-small`, `text-embedding-ada-002` | Embeddings **only** |

## Core recipe — Chat Completions

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_RUNAPI_TOKEN", base_url="https://runapi.ai/v1")

response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[{"role": "user", "content": "Explain quantum computing simply."}],
    reasoning_effort="high",
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
  model: "gpt-5.4",
  messages: [{ role: "user", content: "Explain quantum computing simply." }],
});
```

## Core recipe — Responses API

```python
import httpx

response = httpx.post(
    "https://runapi.ai/v1/responses",
    headers={"x-api-key": "YOUR_RUNAPI_TOKEN"},
    json={
        "model": "gpt-5.4",
        "input": "Explain the theory of relativity.",
        "reasoning": {"effort": "medium"},
    },
)
print(response.json())
```

The Responses API takes `input` (string or structured), `reasoning.effort`
(`"low"` / `"medium"` / `"high"`), and optional `include` for thinking blocks.

## Core recipe — Embeddings

```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=["search document", "query text"],
    encoding_format="float",
)
print(response.data[0].embedding)
print(response.usage)
```

```typescript
const response = await client.embeddings.create({
  model: "text-embedding-3-small",
  input: ["search document", "query text"],
  encoding_format: "float",
});
console.log(response.data[0].embedding);
```

## Streaming

```python
stream = client.chat.completions.create(
    model="gpt-5.4",
    messages=[{"role": "user", "content": "Write a haiku about coding."}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
```

```typescript
const stream = await client.chat.completions.create({
  model: "gpt-5.4",
  messages: [{ role: "user", content: "Write a haiku about coding." }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0].delta.content ?? "");
}
```

Streaming runs through a regional edge proxy so the request does not hold a
Rails/Puma thread. Long generations should always stream.

## Vision / multimodal

```json
{
  "model": "gpt-5.4",
  "messages": [
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "What is in this image?" },
        { "type": "image_url", "image_url": { "url": "https://example.com/img.jpg" } }
      ]
    }
  ]
}
```

Standard OpenAI multimodal block — works on both Chat Completions and
Responses (Responses also accepts structured `input` items).

## Tool use / function calling / web search

```json
{
  "model": "gpt-5.4",
  "messages": [
    { "role": "user", "content": "Find the latest news on RunAPI." }
  ],
  "tools": [
    { "type": "function", "function": { "name": "web_search" } }
  ]
}
```

`web_search` is supported across the GPT models above. Custom function tools
use the standard OpenAI `tools` schema.

## List models

```bash
curl https://runapi.ai/v1/models -H "Authorization: Bearer YOUR_RUNAPI_TOKEN"
```

Returns OpenAI-compatible model objects. If the API Key has
`allowed_models` restrictions, only permitted models are returned.

## Protocol compatibility

GPT generation models are also available through RunAPI's
Anthropic-compatible `/v1/messages` and Gemini `contents` client surfaces. Use
these protocol paths when an existing agent runtime already expects that
request shape; for new GPT app code, prefer the OpenAI-compatible setup above.

```bash
curl -X POST "https://runapi.ai/v1/messages" \
  -H "x-api-key: YOUR_RUNAPI_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.4",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Draft a concise answer."}]
  }'
```

```bash
curl -X POST \
  "https://runapi.ai/v1beta/models/gpt-5.4:streamGenerateContent" \
  -H "x-goog-api-key: YOUR_RUNAPI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"role":"user","parts":[{"text":"Hello, GPT!"}]}]}'
```

Embeddings remain available only on `/v1/embeddings`; do not send embedding
models to generation endpoints or compatibility surfaces.

## Supported models

| Model ID | API | Use when |
|---|---|---|
| `gpt-5.5` | Chat, Responses | Latest general model |
| `gpt-5.5-pro` | Responses only | Reasoning-heavy |
| `gpt-5.4` | Chat, Responses | Production default |
| `gpt-5.4-mini` | Chat, Responses | Cost-optimized |
| `gpt-5.4-nano` | Chat, Responses | Smallest, fastest |
| `gpt-5.4-pro` | Responses only | Reasoning |
| `gpt-5.3-codex` | Chat, Responses | Code generation |
| `gpt-5.3-codex-spark` | Chat, Responses | Faster Codex variant |
| `gpt-5.2` | Chat, Responses | Cost-effective |
| `gpt-5.2-pro` | Responses only | Reasoning |
| `text-embedding-3-large` | Embeddings | High-capacity vectors |
| `text-embedding-3-small` | Embeddings | Efficient vectors |
| `text-embedding-ada-002` | Embeddings | Legacy-compatible vectors |

## Connect Codex CLI itself

```bash
export OPENAI_BASE_URL=https://runapi.ai/v1
export OPENAI_API_KEY=YOUR_RUNAPI_TOKEN
codex
```

## Agent rules

- Pro models (`gpt-5.*-pro`) reject Chat Completions — always use Responses
  for them. Other models accept either endpoint.
- Embedding models only work on `/v1/embeddings`; do not send them to Chat
  Completions or Responses.
- Default GPT-native integrations to OpenAI-compatible endpoints. Use
  Anthropic-compatible or Gemini `contents` paths only for existing clients
  that require those request shapes.
- Use streaming for any response longer than a few hundred tokens. Do not
  hold the agent on a long blocking request.
- `reasoning_effort` is supported on every GPT model above; default is
  usually `"high"` for non-Pro models.
- Pricing, rate limits, quotas — link to <https://runapi.ai/models/gpt.md>,
  not this skill file.

## Routing

- Model page: <https://runapi.ai/models/gpt.md>
- Provider page: <https://runapi.ai/providers/openai.md>
- Catalog: <https://runapi.ai/models.md>
