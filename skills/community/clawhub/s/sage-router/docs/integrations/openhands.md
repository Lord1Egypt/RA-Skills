# Use Sage Router with OpenHands

OpenHands can route every agent action through Sage Router by configuring it with
the OpenAI-compatible endpoint. Sage Router keeps OpenHands on one stable endpoint
while routing between local models, Ollama Cloud, NVIDIA NIM, and cloud APIs
according to policy and provider health — with automatic failover when a provider
dies.

## Setup

Start Sage Router:

```bash
python3 router.py --port 8790
```

Point OpenHands at it via environment:

```bash
export OPENAI_BASE_URL=http://127.0.0.1:8790/v1
export OPENAI_API_KEY=local-router
```

Or in `config.toml`:

```toml
[llm]
model = "auto"
api_base = "http://127.0.0.1:8790/v1"
api_key = "local-router"
```

## Model selection

- `auto` — Sage Router selects per task, capability, latency, and health.
- Pin a route with a provider-qualified model: `openai/gpt-4.1`,
  `anthropic/claude-sonnet`, `ollama/qwen2.5-coder:latest`.

## Recommended route modes

- `balanced` — general agent tasks (default)
- `best` — fragile repo-wide changes where quality matters most
- `local-first` — low-risk background work; local/Ollama first, cloud fallback
  only if local is unhealthy

## Failover

OpenHands keeps running on one endpoint even when a provider rate-limits or goes
down — Sage Router retries the next healthy provider in the chain transparently.

## Compliance

BYOK/BYOS only. Sage Router routes access you already have; it does not resell
model access, pool accounts, or bypass provider Terms of Service.
