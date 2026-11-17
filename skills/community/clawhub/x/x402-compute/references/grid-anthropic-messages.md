# Grid: Anthropic-compatible API (`/v1/messages`)

The Grid speaks the Anthropic Messages API next to the OpenAI one. Claude Code, the official
Anthropic SDKs and any Anthropic-format client can point their base URL at the Grid and run on
Grid models. Same auth, same credits, same x402 payment, same node routing and encryption as
`/v1/chat/completions`.

- **Base URL:** `https://grid.x402compute.cc` (no `/v1` suffix: Anthropic clients add it)
- **Auth:** `x-api-key: x402c_...` or `Authorization: Bearer x402c_...` (credits of the key
  owner), a signed-in session token, or pay per request with `X-Payment` (x402)
- **Model ids:** Grid model ids such as `qwen-2.5-32b`, never Claude ids

## Endpoints

| Method | Path | Notes |
|---|---|---|
| `POST` | `/v1/messages` | Streaming and non-streaming |
| `POST` | `/v1/messages/count_tokens` | Returns `{"input_tokens": N}`. An estimate, free, no auth, rate-limited per IP |
| `GET` | `/v1/models` | Anthropic shape when the request has an `anthropic-version` header, OpenAI shape otherwise. Supports `limit`, `after_id`, `before_id` |
| `GET` | `/v1/models/{model_id}` | One model, Anthropic shape |

`?beta=true` is accepted. `anthropic-version` and `anthropic-beta` headers are accepted and not
enforced.

## Quick start

```bash
# Which models fit? Look at max_input_tokens.
curl -s https://grid.x402compute.cc/v1/models -H "anthropic-version: 2023-06-01"

curl -s https://grid.x402compute.cc/v1/messages \
  -H "x-api-key: $COMPUTE_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"qwen-2.5-32b","max_tokens":512,
       "messages":[{"role":"user","content":"Hello"}]}'

curl -s https://grid.x402compute.cc/v1/messages/count_tokens \
  -H "content-type: application/json" \
  -d '{"model":"qwen-2.5-32b","messages":[{"role":"user","content":"Hello"}]}'
```

```python
import os, anthropic
client = anthropic.Anthropic(api_key=os.environ["COMPUTE_API_KEY"],
                             base_url="https://grid.x402compute.cc")
msg = client.messages.create(model="qwen-2.5-32b", max_tokens=512,
                             messages=[{"role": "user", "content": "Hello"}])
print(msg.content[0].text)
```

```ts
import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic({ apiKey: process.env.COMPUTE_API_KEY, baseURL: "https://grid.x402compute.cc" });
const msg = await client.messages.create({
  model: "qwen-2.5-32b", max_tokens: 512,
  messages: [{ role: "user", content: "Hello" }],
});
```

## Use Claude Code with the Grid

```bash
export ANTHROPIC_BASE_URL=https://grid.x402compute.cc
export ANTHROPIC_API_KEY=<YOUR_COMPUTE_API_KEY>   # an x402c_ compute API key
claude --model qwen-2.5-32b
```

**Pick a large-context model.** Claude Code's own system prompt and tools are about 13k tokens
before you type anything. Many Grid models run 4k to 16k context. Check `max_input_tokens` in
`GET /v1/models` (with the `anthropic-version` header) and choose one well above 13k. Today
`qwen-2.5-32b` (32k) fits; 4k models do not. A prompt that leaves no room for a reply gets a
400 that names the limit.

## What is supported

- `model`, `messages`, `max_tokens`, `system` (string or text blocks), `stop_sequences`,
  `stream`, `temperature`, `tools`, `tool_choice` (`auto`, `any`, `tool`, `none`)
- Content blocks: `text`; `image` with a base64 source (vision models only, one image per
  request, non-streaming only); `tool_use`; `tool_result` with text content and `is_error`
- Mid-conversation `role: "system"` messages (folded into the user turn they follow)
- Streaming events in Anthropic order: `message_start`, `content_block_start`,
  `content_block_delta` (`text_delta`, `input_json_delta`), `content_block_stop`,
  `message_delta`, `message_stop`, plus `ping` and an `error` event if a stream fails
- Stop reasons: `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `refusal`
- `usage.input_tokens` and `usage.output_tokens`; cache counts are always 0;
  `usage.cost_usd` is an extra field with the charge
- Errors in Anthropic shape with a `request-id` header

**Accepted but ignored:** `thinking` of type `adaptive`, `disabled` or `between_tools`,
`output_config.effort`, `metadata`, `service_tier`, `cache_control` (no prompt caching),
`context_management` edits of type `clear_thinking_*`. Earlier `thinking` blocks are dropped.
Tools with `defer_loading: true` are left out.

**Refused with a 400 `invalid_request_error`:** extended thinking with `budget_tokens`,
`output_config.format`, `strict` tools, server and Anthropic-defined tools (web search, web
fetch, code execution, bash, text editor, computer, memory, tool search),
`disable_parallel_tool_use`, `document` and `search_result` blocks, image URLs and Files API
images, images inside `tool_result`, `mcp_servers`, `container`, other `context_management`
edits, `top_p`, `top_k`, assistant prefill, `max_tokens: 0`, and any unknown top-level field.

## Behaviour to know

- **Output** is capped at 8192 tokens; `max_tokens` above the room left is clamped (the
  `x-sgl-max-tokens-*` headers say so).
- **Stop sequences** are cut by the Grid, but the node keeps generating until it stops, and
  those tokens are billed.
- **Tool input** arrives as one `input_json_delta` per tool call, after the call is complete.
- **Long non-streaming replies** can return `504 timeout_error` with a `job_id` and
  `x-should-retry: false`. Do not retry that (a retry is a second paid job). Use
  `"stream": true` for long replies; Claude Code always streams.
- **Retries:** 429 and 5xx are safe to retry. Payment errors carry `x-should-retry: false`.
- **x402:** without auth the 402 body is an Anthropic `billing_error` that also keeps the x402
  fields (`x402Version`, `accepts`, `price_usd`) at the top level, so x402 clients work unchanged.
- **Encryption:** the Grid seals the prompt to the node, like `/v1/chat/completions` from an
  SDK. There is no client-sealed (browser) version of `/v1/messages`.
