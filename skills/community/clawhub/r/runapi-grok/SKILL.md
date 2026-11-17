---
name: grok
description: Call Grok 4.7 for text through RunAPI Chat Completions, Responses, Anthropic Messages, or Gemini contents. Use Grok 4.6 through Chat Completions or Responses; use Grok 4.5 or Grok 4.20 non-reasoning through their documented interfaces.
documentation: https://runapi.ai/models/grok.md
provider_page: https://runapi.ai/providers/xai.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/grok
    primaryEnv: OPENAI_API_KEY
    requires:
      env: [OPENAI_API_KEY, OPENAI_BASE_URL]
    envVars:
    - {name: OPENAI_API_KEY, required: true, description: RunAPI API key used by OpenAI-compatible Grok clients.}
    - {name: OPENAI_BASE_URL, required: true, description: Set to https://runapi.ai/v1 for Grok on RunAPI.}
---

# Grok on RunAPI

Use OpenAI-compatible endpoints at `https://runapi.ai/v1` as the primary protocol.

## Primary protocol recipe

### Authenticate

Set `OPENAI_API_KEY` to a RunAPI API key and `OPENAI_BASE_URL` to `https://runapi.ai/v1`.

### Send request

```python
from openai import OpenAI
client = OpenAI(api_key="YOUR_RUNAPI_TOKEN", base_url="https://runapi.ai/v1")
response = client.responses.create(
    model="grok-4.7",
    input=[{
        "role": "user",
        "content": [{"type": "input_text", "text": "Review this rollout plan."}],
    }],
    stream=False,
)
print(response.output_text)
print(response.usage)
```

Use Chat Completions for `grok-4.5`, `grok-4.6`, or `grok-4.7` chat workflows.
Grok 4.6 Chat accepts `reasoning_effort="high"`, `max_completion_tokens=64000`,
function tools and streaming with `stream_options={"include_usage": True}`.
Grok 4.7 Chat accepts text messages only. For tool continuation, retain the assistant's `tool_calls`
and return each result as a `role="tool"` message with the matching
`tool_call_id`.

Use Responses for `grok-4.5`, `grok-4.6`, or `grok-4.7`; Grok 4.6 does not
expose Anthropic Messages or Gemini contents. Grok 4.6 accepts function tools
and image input; add an `input_image` part with a public `image_url` alongside
`input_text` for image understanding. Grok 4.6 Responses also accepts hosted
`web_search` (billed per call on top of tokens), so Codex CLI works with it.
Do not send `input_file` or state fields such as `previous_response_id` for
Grok 4.6 or 4.7.

`grok-4.7` accepts text through Chat Completions, Responses, Anthropic
Messages, and Gemini `contents`. Reasoning controls, function tools, tool
history, structured output, image or file input, hosted tools, and cache
controls are not yet verified for `grok-4.7`; send plain text requests only.

For streaming Responses, set `stream=True`
and consume through `response.completed`, terminal `usage`, and `[DONE]`.

### Verify result

Responses require final output, one usage-bearing `response.completed`, and
`[DONE]`. Chat requires final assistant content, `finish_reason`, and terminal
`usage`.

### Stop boundaries

Correct a rejected shape once using the structured error. Retry transport once
only before any response or Usage and when replay is safe. Record a terminal
error and stop without changing model or protocol. Keep
`grok-4.20-0309-non-reasoning` text-only and stateless; add advanced controls
only when the current RunAPI contract verifies them for the exact model.

## Compatibility protocols

Load [compatibility protocols](references/compatibility-protocols.md) only when an existing client requires Grok 4.5 or 4.7 through Anthropic Messages or Gemini contents.

## Supported models

| Model ID | Use when |
|---|---|
| `grok-4.20-0309-non-reasoning` | Verified text workloads without reasoning controls |
| `grok-4.7` | Text through Chat Completions, Responses, Anthropic Messages, or Gemini contents; no reasoning controls, tools, structured output, or media input yet |
| `grok-4.6` | Chat Completions and Responses, streaming function tools, tool history, and low through xhigh reasoning; Responses also supports image input and structured output |
| `grok-4.5` | Current Grok chat and reasoning workloads |

## References

- <https://runapi.ai/models/grok.md>
- <https://runapi.ai/providers/xai.md>
- <https://runapi.ai/models.md>
