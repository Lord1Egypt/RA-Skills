---
name: gemini
description: Call the Gemini API (gemini-2.5-flash, gemini-2.5-pro, gemini-3-flash-preview, gemini-3-pro-preview, gemini-3.1-pro-preview, gemini-3.5-flash) through RunAPI using the official OpenAI SDK or Gemini contents clients. Use when the user asks for Gemini chat, streaming completions, multimodal vision input, Google Search grounding, structured output, reasoning effort, or to point an existing OpenAI or Gemini client at RunAPI as the base URL.
documentation: https://runapi.ai/models/gemini.md
provider_page: https://runapi.ai/providers/google.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/gemini
    primaryEnv: RUNAPI_TOKEN
    requires:
      env:
      - RUNAPI_TOKEN
    envVars:
    - name: RUNAPI_TOKEN
      required: true
      description: RunAPI API key used for Gemini requests.
    - name: GOOGLE_API_KEY
      required: false
      description: Optional alias when using Gemini contents streaming examples.
    - name: GOOGLE_GENAI_BASE_URL
      required: false
      description: Optional Gemini client base URL override for RunAPI.
---

# Gemini on RunAPI

Gemini on RunAPI exposes **two request styles**:

| Request style | Endpoint | Use when |
|---|---|---|
| OpenAI-compatible | `POST /v1/chat/completions` | You already use the OpenAI SDK or any OpenAI client |
| Gemini contents | `POST /v1beta/models/<model>:generateContent` or `:streamGenerateContent` | You use a Gemini SDK/client with `contents` requests |

Both accept the same RunAPI API Key.

## Setup

```dotenv
RUNAPI_TOKEN=YOUR_RUNAPI_TOKEN
```

Get a RunAPI API Key at <https://runapi.ai/api_keys>.

### OpenAI-compatible setup

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_RUNAPI_TOKEN",
    base_url="https://runapi.ai/v1",
)
```

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "YOUR_RUNAPI_TOKEN",
  baseURL: "https://runapi.ai/v1",
});
```

### Gemini contents setup

```bash
export GOOGLE_API_KEY=YOUR_RUNAPI_TOKEN
export GOOGLE_GENAI_BASE_URL=https://runapi.ai
```

## Core recipe — OpenAI-compatible

```python
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[{"role": "user", "content": "Explain quantum computing simply."}],
    reasoning_effort="high",
)
print(response.choices[0].message.content)
print(response.usage)
```

```typescript
const response = await client.chat.completions.create({
  model: "gemini-2.5-flash",
  messages: [{ role: "user", content: "Explain quantum computing simply." }],
});
```

```bash
curl -X POST "https://runapi.ai/v1/chat/completions" \
  -H "x-api-key: YOUR_RUNAPI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash",
    "messages": [{"role": "user", "content": "Explain quantum computing simply."}]
  }'
```

## Core recipe — Gemini contents

```bash
curl -X POST \
  "https://runapi.ai/v1beta/models/gemini-3-flash-preview:streamGenerateContent" \
  -H "x-goog-api-key: YOUR_RUNAPI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      { "role": "user", "parts": [{ "text": "Hello!" }] }
    ]
  }'
```

For `gemini-3-flash-preview` and `gemini-3.5-flash`, RunAPI uses the native
Gemini `streamGenerateContent` route. For other callable Gemini models, RunAPI
accepts Gemini `contents` requests and bridges them to the OpenAI-compatible
chat request format. Use the official Gemini SDKs when an existing application
already sends `contents` requests; for new app code, prefer the
OpenAI-compatible setup.

## Streaming (OpenAI-compatible)

```python
stream = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[{"role": "user", "content": "Write a haiku about coding."}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
```

Streaming runs through a regional edge proxy so the request does not hold a
Rails/Puma thread. Long generations should always stream.

## Vision / multimodal

```json
{
  "model": "gemini-2.5-flash",
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

Standard OpenAI multimodal block for the OpenAI-compatible endpoint. For the
`contents` streaming endpoint, embed image data as `parts[].inlineData` or
`parts[].fileData`.

## Google Search grounding

```json
{
  "model": "gemini-2.5-pro",
  "messages": [
    { "role": "user", "content": "Latest news on Gemini 3." }
  ],
  "tools": [
    { "type": "function", "function": { "name": "googleSearch" } }
  ]
}
```

Available on `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-3.1-pro-preview`,
and `gemini-3-pro-preview`.

## Structured output

```json
{
  "model": "gemini-2.5-flash",
  "messages": [{ "role": "user", "content": "Give me one person object." }],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "person",
      "schema": {
        "type": "object",
        "properties": { "name": { "type": "string" }, "age": { "type": "integer" } },
        "required": ["name", "age"]
      }
    }
  }
}
```

## Reasoning effort

Supported on `gemini-2.5-pro`, `gemini-3.1-pro-preview`, `gemini-3-pro-preview`,
and `gemini-3-flash-preview` — pass `reasoning_effort: "low" | "medium" | "high"`.

## List models

```bash
curl https://runapi.ai/v1beta/models -H "x-api-key: YOUR_RUNAPI_TOKEN"
```

Or via the OpenAI-style path:

```bash
curl https://runapi.ai/v1/models \
  -H "Authorization: Bearer YOUR_RUNAPI_TOKEN"
```

## Supported models

| Model ID | OpenAI endpoint | Gemini contents endpoint | Capabilities |
|---|---|---|---|
| `gemini-2.5-flash` | yes | bridged `generateContent` / `streamGenerateContent` | Chat, multimodal, Google Search, structured output, thoughts |
| `gemini-2.5-pro` | yes | bridged `generateContent` / `streamGenerateContent` | + reasoning effort |
| `gemini-3.1-pro-preview` | yes | bridged `generateContent` / `streamGenerateContent` | + reasoning effort |
| `gemini-3-pro-preview` | yes | bridged `generateContent` / `streamGenerateContent` | + reasoning effort |
| `gemini-3-flash-preview` | yes | native `:streamGenerateContent` | Chat, multimodal, function calling, structured output, reasoning effort |
| `gemini-3.5-flash` | — | native `:streamGenerateContent` | Streaming `contents` requests, multimodal, function calling, thoughts |

`gemini-flash-latest` resolves to `gemini-3-flash-preview`.

## Connect Gemini CLI itself

```bash
export GOOGLE_API_KEY=YOUR_RUNAPI_TOKEN
export GOOGLE_GENAI_BASE_URL=https://runapi.ai
gemini
```

## Agent rules

- Use the OpenAI-compatible endpoint for new app code. Use Gemini `contents`
  paths when an existing client already sends `contents` requests.
- Native Gemini streaming is available for `gemini-3-flash-preview` and
  `gemini-3.5-flash`; other callable Gemini models accept `contents` requests
  through a RunAPI protocol bridge.
- Use streaming for any response longer than a few hundred tokens. Do not
  hold the agent on a long blocking request.
- Google Search grounding uses a `googleSearch` function tool.
- Pricing, rate limits, quotas — link to <https://runapi.ai/models/gemini.md>,
  not this skill file.

## Routing

- Model page: <https://runapi.ai/models/gemini.md>
- Provider page: <https://runapi.ai/providers/google.md>
- Catalog: <https://runapi.ai/models.md>
