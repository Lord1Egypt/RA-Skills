---
name: kimi
description: Call the Kimi API (kimi-k3, kimi-k2.7-code, kimi-k2.6, kimi-k2.5) through RunAPI using OpenAI-compatible Chat Completions. Use for Kimi text chat, streaming, or an existing compatibility client that needs the conditional reference.
documentation: https://runapi.ai/models/kimi.md
provider_page: https://runapi.ai/providers/moonshot-ai.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/kimi
    primaryEnv: OPENAI_API_KEY
    requires:
      env: [OPENAI_API_KEY, OPENAI_BASE_URL]
    envVars:
    - {name: OPENAI_API_KEY, required: true, description: RunAPI API key used by OpenAI-compatible Kimi clients.}
    - {name: OPENAI_BASE_URL, required: true, description: Set to https://runapi.ai/v1 for Kimi on RunAPI.}
---

# Kimi on RunAPI

Use OpenAI-compatible Chat Completions at `https://runapi.ai/v1` as the primary protocol.

## Primary protocol recipe

### Authenticate

Set `OPENAI_API_KEY` to a RunAPI API key and `OPENAI_BASE_URL` to `https://runapi.ai/v1`.

### Send request

```python
from openai import OpenAI
client = OpenAI(api_key="YOUR_RUNAPI_TOKEN", base_url="https://runapi.ai/v1")
response = client.chat.completions.create(
    model="kimi-k3",
    messages=[{"role": "user", "content": "Explain this finding."}],
)
print(response.choices[0].message.content)
print(response.usage)
```

For long output, set `stream=True` and
`stream_options={"include_usage": True}`; consume through `[DONE]`.

### Verify result

Require final assistant content, `finish_reason`, and authoritative `usage`.
Use the returned final answer rather than raw reasoning content.

### Stop boundaries

Correct a rejected shape once using the structured error. Retry transport once
only before any response or Usage and when replay is safe. Record a terminal
error and stop without changing model or protocol. For `kimi-k3` and
`kimi-k2.7-code`, start with text history and final answers; add tools,
multimodal input, reasoning controls, cache controls, or continuation only when
the current RunAPI contract explicitly verifies the exact shape.

## Compatibility protocols

Load [compatibility protocols](references/compatibility-protocols.md) only when an existing client requires Anthropic Messages or Gemini contents.

## Supported models

| Model ID | Use when |
|---|---|
| `kimi-k3` | Current flagship basic text requests |
| `kimi-k2.7-code` | Dedicated coding requests |
| `kimi-k2.6` | Recent Kimi K2 chat workloads |
| `kimi-k2.5` | Kimi K2.5 compatibility |

## References

- <https://runapi.ai/models/kimi.md>
- <https://runapi.ai/providers/moonshot-ai.md>
- <https://runapi.ai/models.md>
