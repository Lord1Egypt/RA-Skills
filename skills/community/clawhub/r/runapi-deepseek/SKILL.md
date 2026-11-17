---
name: deepseek
description: Call the DeepSeek API (deepseek-flash, deepseek-v4-pro, deepseek-v4-flash, and deepseek-v4-flash-vision-exp) through RunAPI using OpenAI-compatible Chat Completions and Responses. Use deepseek-flash for the current V4.1 Flash 1017 model; the v4 names remain compatibility aliases.
documentation: https://runapi.ai/models/deepseek.md
provider_page: https://runapi.ai/providers/deepseek.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/deepseek
    primaryEnv: OPENAI_API_KEY
    requires:
      env: [OPENAI_API_KEY, OPENAI_BASE_URL]
    envVars:
    - {name: OPENAI_API_KEY, required: true, description: RunAPI API key used by OpenAI-compatible DeepSeek clients.}
    - {name: OPENAI_BASE_URL, required: true, description: Set to https://runapi.ai/v1 for DeepSeek on RunAPI.}
---

# DeepSeek on RunAPI

The current official revision is DeepSeek-V4.1-Flash-1017, updated on
2026-10-17. V4.1 Flash first launched on 2026-09-10. Use `deepseek-flash`;
`deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` remain compatibility
names. The official upgrade does not establish the revision of every RunAPI
service option. Third-party versions remain unconfirmed unless separately
verified. See the [current model reference](https://runapi.ai/models/deepseek/v4.1-flash.md).

Use OpenAI-compatible endpoints at `https://runapi.ai/v1` as the primary protocol.

## Primary protocol recipe

### Authenticate

Set `OPENAI_API_KEY` to a RunAPI API key and `OPENAI_BASE_URL` to `https://runapi.ai/v1`.

### Send request

```python
from openai import OpenAI
client = OpenAI(api_key="YOUR_RUNAPI_TOKEN", base_url="https://runapi.ai/v1")
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": "Explain this decision."}],
)
print(response.choices[0].message.content)
print(response.usage)
```

For long output, set `stream=True` and
`stream_options={"include_usage": True}`; consume through `[DONE]`.
`deepseek-v4-flash` additionally supports one custom function on Responses;
keep automatic tool selection and one serial call/result lifecycle.

For image input, use `deepseek-flash` only where the current model contract
permits it. DeepSeek documents image input, but RunAPI has not tested vision
on every service option. The retired `deepseek-v4-flash-vision-exp` name is
a historical compatibility alias, not a separate recommended vision model.

### Verify result

For Chat, require final assistant content, `finish_reason`, and `usage`. For
Responses, require final output, one usage-bearing `response.completed`, and
`[DONE]` when streaming.

### Stop boundaries

Correct a rejected shape once using the structured error. Retry transport once
only before any response or Usage and when replay is safe. Record a terminal
error and stop without changing model or protocol. Add tools, reasoning,
storage, cache controls, documents, or multimodal input only when the current
RunAPI contract verifies the exact model/protocol shape.

## Compatibility protocols

Load [compatibility protocols](references/compatibility-protocols.md) only when an existing client requires Anthropic Messages or Gemini contents.

## Supported models

| Model ID | Use when |
|---|---|
| `deepseek-flash` | Current V4.1 Flash 1017 official revision for fast text and reasoning |
| `deepseek-v4-flash-vision-exp` | Historical compatibility alias, not a separate vision model |
| `deepseek-v4-pro` | Higher-quality verified text workloads |
| `deepseek-v4-flash` | Compatibility alias for Flash |

## References

- <https://runapi.ai/models/deepseek.md>
- <https://runapi.ai/providers/deepseek.md>
- <https://runapi.ai/models.md>
