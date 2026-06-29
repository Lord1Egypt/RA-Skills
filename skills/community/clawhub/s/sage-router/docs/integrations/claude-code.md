# Use Sage Router with Claude Code

Claude Code (and any Anthropic-compatible client) can point at Sage Router through
its Anthropic Messages endpoint. Sage Router then routes each request across your
own authorized providers — Anthropic, OpenAI-compatible, Gemini, NVIDIA NIM, Ollama,
and Ollama Cloud — with automatic failover when a provider is slow, down, or
rate-limited. Your provider credentials stay on your machine by default.

## Setup

Start Sage Router locally:

```bash
python3 router.py --port 8790
```

Point Claude Code at it:

```bash
export ANTHROPIC_BASE_URL=http://127.0.0.1:8790
export ANTHROPIC_API_KEY=local-router
```

Sage Router accepts `POST /v1/messages` and selects a model per request based on
intent, capability, latency, and policy, then fails over across your configured
providers with no mid-stream handoff.

## Model selection

Use `auto` for policy-based selection, or a provider-qualified model to pin a route:

```bash
# Let Sage Router pick by task/capability/health
claude --model auto

# Pin a specific provider/model
claude --model anthropic/claude-sonnet
claude --model openai/gpt-4.1
claude --model ollama/qwen2.5-coder:latest
```

## Route modes

Pass a route mode to bias selection. Sage Router normalizes aliases
(`deep`→`best`, `local-strict`→`local-first`):

- `fast` — cheapest/lowest-latency healthy model
- `balanced` — default; quality vs cost vs latency
- `best` — highest-quality healthy model, cost-insensitive
- `local-first` — local/Ollama first, cloud fallback only if local is unhealthy
- `realtime` — optimize for latency

## Recommended policy for coding agents

- Day-to-day coding/refactor/debug: `balanced` or `local-first` with a
  coding-strong local model first and a cloud coding model as fallback.
- Fragile repo-wide edits or deep reasoning: `best` with a frontier model first.
- Background maintenance / bulk calls: `local-first` to keep cost near zero.

## Failover and health

Sage Router tracks per-provider/per-model health and applies cooldowns after
repeated failures. If your Anthropic access is down or rate-limited, the request
falls through to the next healthy provider in the chain — Claude Code keeps
running on one stable endpoint instead of you re-pointing it at each provider.

## Notes

- BYOK/BYOS only: Sage Router routes access you already have. It does not resell
  model access, pool accounts, or share subscriptions.
- If you do not have an active Anthropic subscription, configure OpenAI/Gemini/
  Ollama routes and Sage Router will route Claude-style requests to those providers
  per policy.
