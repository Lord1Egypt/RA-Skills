---
name: qwen
description: Call the Qwen API (Qwen3.6, Qwen3.5, Qwen3-Coder-Next, and Qwen3-VL open-weight models) through RunAPI using OpenAI-compatible Chat Completions. Use for Qwen text chat, image understanding, streaming, or an existing compatibility client that needs the conditional reference.
documentation: https://runapi.ai/models/qwen.md
provider_page: https://runapi.ai/providers/alibaba.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/qwen
    primaryEnv: OPENAI_API_KEY
    requires:
      env: [OPENAI_API_KEY, OPENAI_BASE_URL]
    envVars:
    - {name: OPENAI_API_KEY, required: true, description: RunAPI API key used by OpenAI-compatible Qwen clients.}
    - {name: OPENAI_BASE_URL, required: true, description: Set to https://runapi.ai/v1 for Qwen on RunAPI.}
---

# Qwen on RunAPI

Use OpenAI-compatible Chat Completions at `https://runapi.ai/v1` as the primary protocol.

## Primary protocol recipe

### Authenticate

Set `OPENAI_API_KEY` to a RunAPI API key and `OPENAI_BASE_URL` to `https://runapi.ai/v1`.

### Send request

```python
from openai import OpenAI
client = OpenAI(api_key="YOUR_RUNAPI_TOKEN", base_url="https://runapi.ai/v1")
response = client.chat.completions.create(
    model="qwen3.6-27b",
    messages=[{"role": "user", "content": "Review this function for bugs."}],
)
print(response.choices[0].message.content)
print(response.usage)
```

For long output, call the same method with `stream=True` and
`stream_options={"include_usage": True}`; consume every chunk through `[DONE]`.

### Verify result

Require final assistant content, a terminal `finish_reason`, and authoritative
`usage`. Thinking models may also return `reasoning_content`; use the final
answer in `content`. A stream is complete only after its terminal usage chunk
and `[DONE]`.

### Stop boundaries

Correct a rejected shape once using the structured error. Retry transport once
only before any response or Usage and when replay is safe. Record a terminal
error and stop without changing model or protocol. Send image input only on
Chat Completions and only to a model whose row below lists image input. Keep
`qwen3-coder-next` requests to text.

## Compatibility protocols

Load [compatibility protocols](references/compatibility-protocols.md) only when an existing client requires OpenAI Responses, Anthropic Messages, or Gemini contents.

## Capability boundary

| Capability | Current behavior |
|---|---|
| Text history, sync, streaming | Supported through OpenAI-compatible Chat Completions |
| Image input | Chat Completions only, for the Qwen3.6, Qwen3.5, and Qwen3-VL models |
| Function tools | Chat Completions; verify each tool call before acting on it |
| OpenAI Responses, Anthropic Messages, Gemini contents | Text requests; image input is rejected |
| Usage | Preserve returned token fields; never infer missing details |

## Supported models

| Model ID | Use when |
|---|---|
| `qwen3.6-27b` | Dense agentic coding and reasoning with image input |
| `qwen3.6-35b-a3b` | Efficient MoE coding and reasoning with image input |
| `qwen3.5-397b-a17b` | Largest Qwen3.5 open-weight model with image input |
| `qwen3.5-122b-a10b` | Qwen3.5 MoE for text and image reasoning |
| `qwen3.5-27b` | Dense Qwen3.5 text and image workloads |
| `qwen3.5-35b-a3b` | Low-cost Qwen3.5 MoE workloads |
| `qwen3-coder-next` | Text-only coding agents and repository work |
| `qwen3-vl-235b-a22b-thinking` | Image reasoning with always-on thinking |
| `qwen3-vl-235b-a22b-instruct` | Image understanding and OCR without thinking |

## References

- <https://runapi.ai/models/qwen.md>
- <https://runapi.ai/providers/alibaba.md>
- <https://runapi.ai/models.md>
