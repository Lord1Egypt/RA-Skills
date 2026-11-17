---
name: claude
description: Call Claude models through RunAPI using the Anthropic Messages protocol. Use for Claude chat, streaming, vision, tools, reasoning, token counting, or an existing compatibility client that needs the conditional reference.
documentation: https://runapi.ai/models/claude.md
provider_page: https://runapi.ai/providers/anthropic.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/claude
    primaryEnv: ANTHROPIC_API_KEY
    requires:
      env: [ANTHROPIC_API_KEY, ANTHROPIC_BASE_URL]
    envVars:
    - {name: ANTHROPIC_API_KEY, required: true, description: RunAPI API key used by Anthropic-compatible clients.}
    - {name: ANTHROPIC_BASE_URL, required: true, description: Set to https://runapi.ai for Claude on RunAPI.}
---

# Claude on RunAPI

Use Anthropic Messages at `https://runapi.ai` with `POST /v1/messages` as the primary protocol.

## Primary protocol recipe

### Authenticate

Set `ANTHROPIC_API_KEY` to a RunAPI API key and `ANTHROPIC_BASE_URL` to
`https://runapi.ai`. The SDK sends `x-api-key`; Bearer authentication is also accepted.

### Send request

```python
import anthropic
client = anthropic.Anthropic(api_key="YOUR_RUNAPI_TOKEN", base_url="https://runapi.ai")
message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain this decision."}],
)
print(message.content[0].text)
print(message.usage)
```

`max_tokens` is required. For long output, use `client.messages.stream(...)`
and consume `stream.text_stream` through the terminal event. Add image blocks,
function tools, reasoning controls, or token counting only when the current
RunAPI contract verifies them for the selected exact model.

### Verify result

Require final text, `stop_reason`, and authoritative `usage`. A stream is
complete only after terminal Usage and `message_stop`. Token counting estimates
input only; actual response Usage remains authoritative.

### Stop boundaries

Correct a rejected shape once using the structured error. Retry transport once
only before any response or Usage and when replay is safe. Record a terminal
error and stop without changing model or protocol.

## Compatibility protocols

Load [compatibility protocols](references/compatibility-protocols.md) only when an existing client requires OpenAI Chat/Responses or Gemini contents.

## Supported models

| Model ID | Use when |
|---|---|
| `claude-fable-5-1` | — |
| `claude-fable-5` | Flagship state-of-the-art coding, reasoning, and vision |
| `claude-sonnet-5-5` | Sonnet 5 successor for everyday coding and agents |
| `claude-sonnet-5` | Near-Opus coding at Sonnet cost |
| `claude-opus-5` | Latest Opus frontier reasoning |
| `claude-opus-4-8` | Strongest general model |
| `claude-opus-4-7` | Previous Opus generation |
| `claude-opus-4-6` | High-end reasoning |
| `claude-sonnet-4-6` | Balanced reasoning and speed |
| `claude-opus-4-5-20251101` | Dated Opus 4.5 snapshot |
| `claude-sonnet-4-5-20250929` | Dated Sonnet 4.5 snapshot |
| `claude-haiku-5-5` | Lowest-cost Claude; higher rates above 100K-token prompts |
| `claude-haiku-4-5-20251001` | Fastest lightweight snapshot |
| `claude-opus-4-1-20250805` | Dated Opus 4.1 snapshot |
| `claude-opus-5-5` | Long-running agentic coding and knowledge work |

## References

- <https://runapi.ai/models/claude.md>
- <https://runapi.ai/providers/anthropic.md>
- <https://runapi.ai/models.md>
