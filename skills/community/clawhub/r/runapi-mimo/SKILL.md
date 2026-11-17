---
name: mimo
description: Call the MiMo API (mimo-v2.5-pro and mimo-v2.5) through RunAPI using OpenAI-compatible Chat Completions. Use for MiMo text generation, function calling, Claude Code, the verified MiMo image subset, streaming, or an existing compatibility client that needs the conditional reference.
documentation: https://runapi.ai/models/mimo.md
provider_page: https://runapi.ai/providers/xiaomi.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/mimo
    primaryEnv: OPENAI_API_KEY
    requires:
      env:
      - OPENAI_API_KEY
      - OPENAI_BASE_URL
    envVars:
    - name: OPENAI_API_KEY
      required: true
      description: RunAPI API key used by OpenAI-compatible MiMo clients.
    - name: OPENAI_BASE_URL
      required: true
      description: Set to https://runapi.ai/v1 for MiMo on RunAPI.
---

# MiMo on RunAPI

Use OpenAI-compatible Chat Completions at `https://runapi.ai/v1` as the primary
protocol. Keep the exact public model identity throughout the request.

## Primary protocol recipe

### Authenticate

Set `OPENAI_API_KEY` to a RunAPI API key and `OPENAI_BASE_URL` to
`https://runapi.ai/v1`. Keep the key in the environment or a secret manager.

### Send request

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_RUNAPI_TOKEN", base_url="https://runapi.ai/v1")
response = client.chat.completions.create(
    model="mimo-v2.5-pro",
    messages=[{"role": "user", "content": "Summarize this decision."}],
)
print(response.choices[0].message.content)
```

For longer output, request terminal usage while streaming:

```python
stream = client.chat.completions.create(
    model="mimo-v2.5",
    messages=[{"role": "user", "content": "Write a status update."}],
    stream=True,
    stream_options={"include_usage": True},
)
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
    if chunk.usage:
        print(chunk.usage)
```

### Verify result

For a synchronous call, require one response choice with a final assistant
message and read `usage` from that response. For SSE, consume through `[DONE]`
and require the terminal usage chunk requested by `include_usage`. An HTTP 2xx
without the expected final content and Usage is incomplete.

### Stop boundaries

Correct a rejected request shape at most once, using the structured error and
this verified allowlist. Retry a transport failure once only when no response
or Usage was returned and replay is safe. On a terminal RunAPI failure, retain
the request ID and error, then stop without changing model or protocol.

## Positive verified request allowlist

Start with only this verified request shape:

- `mimo-v2.5-pro`: a text-only `messages` history with system, user, and
  assistant roles.
- `mimo-v2.5`: the same text shape, plus synchronous Chat Completions content
  parts containing `text` and public HTTP(S) `image_url.url` values.
- Both models: synchronous calls or SSE with `stream_options.include_usage`.
- `mimo-v2.5` Chat Completions: an optional `metadata` object with string values,
  for example `{"user_id": "customer-123"}`, on synchronous or streaming requests.
  Do not rely on metadata being echoed in the response or available for stored-completion lookup.
- `mimo-v2.5` Chat Completions supports custom function `tools`, `tool_choice`
  (`auto`, `none`, `required`, or a named function), and `parallel_tool_calls`.
  Preserve assistant `tool_calls`, their IDs, and `reasoning_content` when supplied;
  return each result as a `tool` message with the matching `tool_call_id`.
  Continue until the model returns final text. Both sync and SSE are supported.
- For Claude Code with `mimo-v2.5`, use native Anthropic Messages as described
  in the compatibility reference. Tool calling is not enabled for Pro or Responses.

Add an optional control only when the current RunAPI contract or a successful
validation result explicitly verifies it for the selected model and mode.

## Compatibility protocols

Load [compatibility protocols](references/compatibility-protocols.md) only when an existing client requires Responses or Anthropic Messages. Keep the primary recipe in this file for new integrations.

## Supported models

| Model ID | Use when |
|---|---|
| `mimo-v2.5-pro` | Higher-quality verified text generation |
| `mimo-v2.5` | Text, custom tool calling, Claude Code, and synchronous Chat image requests |

## References

- Model overview and pricing: <https://runapi.ai/models/mimo.md>
- Provider page: <https://runapi.ai/providers/xiaomi.md>
- Catalog: <https://runapi.ai/models.md>
