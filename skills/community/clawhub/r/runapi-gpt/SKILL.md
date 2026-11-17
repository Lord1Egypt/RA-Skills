---
name: gpt
description: Call GPT generation and OpenAI text embedding models through RunAPI using OpenAI-compatible clients. Use for chat, Responses, embeddings, streaming, tools, vision, or an existing compatibility client that needs the conditional reference.
documentation: https://runapi.ai/models/gpt.md
provider_page: https://runapi.ai/providers/openai.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/gpt
    primaryEnv: OPENAI_API_KEY
    requires:
      env: [OPENAI_API_KEY, OPENAI_BASE_URL]
    envVars:
    - {name: OPENAI_API_KEY, required: true, description: RunAPI API key used by OpenAI-compatible clients.}
    - {name: OPENAI_BASE_URL, required: true, description: Set to https://runapi.ai/v1 for GPT on RunAPI.}
---

# GPT on RunAPI

Use OpenAI-compatible clients at `https://runapi.ai/v1` as the primary protocol.

## Primary protocol recipe

### Authenticate

Set `OPENAI_API_KEY` to a RunAPI API key and `OPENAI_BASE_URL` to `https://runapi.ai/v1`.

### Send request

```python
from openai import OpenAI
client = OpenAI(api_key="YOUR_RUNAPI_TOKEN", base_url="https://runapi.ai/v1")
response = client.responses.create(model="gpt-5.5", input="Summarize this review.")
print(response.output_text)
print(response.usage)
```

Use `client.chat.completions.create` for `gpt-5.2`, which does not accept
Responses. Use Responses for `gpt-5.*-pro`. Use `client.embeddings.create` only
with the three embedding model IDs below. For streaming Responses, set
`stream=True` and consume through one usage-bearing `response.completed`
followed by `[DONE]`.

For `gpt-5.6-luna`, `gpt-5.6-sol`, and `gpt-5.6-terra`, start with text input,
sync or SSE transport, parameterized custom functions, and automatic prompt
caching. Add reasoning controls, multimodal input, hosted tools, or
continuation state only when the current RunAPI contract verifies that shape.

### Verify result

Responses require final output, `response.completed`, and `usage`. Chat requires
final assistant content, `finish_reason`, and `usage`. Embeddings require one
numeric vector per input and response `usage`.

### Stop boundaries

Correct a rejected shape once using the current error and endpoint contract.
Retry transport once only before any response or Usage and when replay is safe.
Record a terminal error and stop without changing model, endpoint, or protocol.
Keep embedding models on `/v1/embeddings`.

## Compatibility protocols

Load [compatibility protocols](references/compatibility-protocols.md) only when an existing client requires Anthropic Messages or Gemini contents.

## Live audio

`gpt-live-1` is available only on the dedicated Live transport. Use WebRTC
with `POST /v1/live/webrtc` and a client SDP offer, or WebSocket with
`GET /v1/live/websocket` and a first `session.start` frame. Live sessions may
delegate backend work through `delegation.type: responses` or return function
work through `delegation.type: client`. Responses delegation accepts hosted
tools on both transports and `function` tools on WebSocket: delegated events
arrive wrapped in `response.event`, a function call arrives as a nested
`response.output_item.done`, and the client answers with `response.item.create`
(`function_call_output`) followed by `response.create`. Chat Completions and
Responses calls do not accept this model.

## Supported models

| Model ID | Use when |
|---|---|
| `gpt-5.5` | Latest general model |
| `gpt-5.4` | Production default |
| `gpt-5.4-mini` | Cost-optimized |
| `gpt-5.4-nano` | Smallest, fastest |
| `gpt-5.2` | Cost-effective |
| `gpt-4.1` | Non-reasoning chat; image input on Chat Completions only |
| `gpt-4.1-mini` | Lower-cost GPT-4.1; image input on Chat Completions only |
| `gpt-4o-mini` | — |
| `gpt-5.6-luna` | Text and parameterized functions in the consistently available Responses subset |
| `gpt-5.6-sol` | Text and parameterized functions in the consistently available Responses subset |
| `gpt-5.6-terra` | Text and parameterized functions in the consistently available Responses subset |
| `gpt-6-astra` | — |
| `codex-auto-review` | — |
| `gpt-5-pro` | Text-only analysis and coding with the Responses API; other input modalities await billing review |
| `gpt-6-sol` | — |
| `gpt-6.1-sol` | — |
| `gpt-6.1-terra` | — |
| `gpt-6-luna` | — |
| `text-embedding-3-large` | High-capacity vectors |
| `text-embedding-3-small` | Efficient vectors |
| `text-embedding-ada-002` | Legacy-compatible vectors |

## References

- <https://runapi.ai/models/gpt.md>
- <https://runapi.ai/providers/openai.md>
- <https://runapi.ai/models.md>
