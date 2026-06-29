# Use Sage Router as an Anthropic-compatible endpoint

Sage Router exposes an Anthropic Messages-compatible endpoint at `POST /v1/messages`
for tools and SDKs that speak the Claude request format. It routes each request
across your own authorized providers (Anthropic, OpenAI-compatible, Gemini, NVIDIA
NIM, Ollama, Ollama Cloud) with policy-based model selection and automatic
failover. No resale, no pooling — BYOK/BYOS only.

## Endpoint

- Base URL: `http://127.0.0.1:8790`
- Path: `POST /v1/messages`
- Auth: `ANTHROPIC_API_KEY` (use `local-router` for the local token, or a generated
  `sk_sage_*` key when client auth is enabled)

```bash
export ANTHROPIC_BASE_URL=http://127.0.0.1:8790
export ANTHROPIC_API_KEY=local-router
```

## Python (Anthropic SDK)

```python
from anthropic import Anthropic
client = Anthropic(base_url="http://127.0.0.1:8790", api_key="local-router")
msg = client.messages.create(
    model="auto",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Refactor this function for readability."}],
)
print(msg.content[0].text)
```

## curl

```bash
curl http://127.0.0.1:8790/v1/messages \
  -H "x-api-key: local-router" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "auto",
    "max_tokens": 512,
    "messages": [{"role": "user", "content": "Summarize this PR."}]
  }'
```

## Model selection

- `auto` — Sage Router selects by intent, capability, latency, and health.
- Provider-qualified — pin a route: `anthropic/claude-sonnet`, `openai/gpt-4.1`,
  `ollama/qwen2.5-coder:latest`.

## Route modes

`fast`, `balanced` (default), `best`, `local-first`, `realtime`. Aliases
`deep`→`best` and `local-strict`→`local-first` are accepted.

## Failover

If the first-choice provider is unhealthy or rate-limited, Sage Router retries the
next healthy provider in the chain transparently — the Anthropic-format response
shape is preserved for the client.
