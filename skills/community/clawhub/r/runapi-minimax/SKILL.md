---
name: minimax
description: Call the MiniMax text API (MiniMax-M3 through MiniMax-M2) through RunAPI using OpenAI-compatible Chat Completions. Use for MiniMax text chat, streaming, or an existing compatibility client that needs the conditional reference.
documentation: https://runapi.ai/models/minimax.md
provider_page: https://runapi.ai/providers/minimax.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/minimax
    primaryEnv: OPENAI_API_KEY
    requires:
      env: [OPENAI_API_KEY, OPENAI_BASE_URL]
    envVars:
    - {name: OPENAI_API_KEY, required: true, description: RunAPI API key used by OpenAI-compatible MiniMax clients.}
    - {name: OPENAI_BASE_URL, required: true, description: Set to https://runapi.ai/v1 for MiniMax on RunAPI.}
---

# MiniMax on RunAPI

Use OpenAI-compatible Chat Completions at `https://runapi.ai/v1` as the primary protocol. Use the separate Hailuo skill for video generation.

## Primary protocol recipe

### Authenticate

Set `OPENAI_API_KEY` to a RunAPI API key and `OPENAI_BASE_URL` to `https://runapi.ai/v1`.

### Send request

```python
from openai import OpenAI
client = OpenAI(api_key="YOUR_RUNAPI_TOKEN", base_url="https://runapi.ai/v1")
response = client.chat.completions.create(
    model="MiniMax-M3",
    messages=[{"role": "user", "content": "Draft a support response."}],
)
print(response.choices[0].message.content)
print(response.usage)
```

For long output, set `stream=True` and
`stream_options={"include_usage": True}`; consume through `[DONE]`.

### Verify result

Require final assistant content, `finish_reason`, and authoritative `usage`.
A stream is complete only after its terminal usage chunk and `[DONE]`.

### Stop boundaries

Correct a rejected shape once using the structured error. Retry transport once
only before any response or Usage and when replay is safe. Record a terminal
error and stop without changing model or protocol.

## Compatibility protocols

Load [compatibility protocols](references/compatibility-protocols.md) only when an existing client requires Anthropic Messages or Gemini contents.

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

- <https://runapi.ai/models/minimax.md>
- <https://runapi.ai/providers/minimax.md>
- <https://runapi.ai/models.md>
