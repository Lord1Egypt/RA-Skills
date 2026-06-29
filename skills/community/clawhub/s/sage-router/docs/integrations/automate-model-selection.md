# Automate AI model selection for agents

Sage Router automates model and provider selection for AI agents and developer
tools. Instead of hard-coding one model per agent, you point every agent at one
local endpoint and Sage Router picks the best model per request — then fails over
across your own authorized providers when one is slow, down, or rate-limited.

## Why automate model selection

Every agent harness (Codex, Claude Code, Cursor, Aider, Continue, OpenHands) ships
its own model picker and breaks the moment a provider rate-limits or goes down.
Hard-coding a model means you eat outages and overpay when a cheaper model would
do. Automating selection gives you:

- **Right model per task** — coding tasks to coding models, reasoning to frontier
  models, chat to fast models.
- **Automatic failover** — one provider dying doesn't kill the session.
- **Cost control** — local/Ollama first for cheap work, cloud only when needed.
- **One stable endpoint** — agents never re-point at individual providers.

## How Sage Router selects

For each request Sage Router classifies intent (CODE, ANALYSIS, CREATIVE,
REALTIME, GENERAL), estimates complexity and token load, then scores candidate
models by:

- Capability fit for the intent
- Per-provider/per-model health and cooldown state
- Latency and cost
- Route mode policy (`fast`, `balanced`, `best`, `local-first`, `realtime`)

It builds an ordered fallback chain and tries providers in order until one
succeeds — no mid-stream handoff, response shape preserved for the client.

## 30-second start

```bash
python3 router.py --port 8790
export OPENAI_BASE_URL=http://127.0.0.1:8790/v1
export OPENAI_API_KEY=local-router
codex --model auto
```

Use `auto` for policy-based selection, or pin a provider/model when you want an
explicit route: `openai/gpt-4.1`, `anthropic/claude-sonnet`,
`ollama/qwen2.5-coder:latest`.

## Route modes

- `fast` — cheapest/lowest-latency healthy model
- `balanced` — default trade-off
- `best` — highest-quality healthy model
- `local-first` — local/Ollama first, cloud fallback only if local unhealthy
- `realtime` — minimize latency

## BYOK / compliance

Sage Router routes access you already have. It does not resell model access, pool
accounts, share subscriptions, or bypass provider Terms of Service. Credentials
stay on your machine by default.

## Next

- [Codex CLI guide](codex.md)
- [Claude Code guide](claude-code.md)
- [OpenAI-compatible endpoint](openai-compatible.md)
- [Harness fallback policy](harness-fallback.md)
