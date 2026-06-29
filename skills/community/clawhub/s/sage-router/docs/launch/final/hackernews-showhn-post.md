# Hacker News Show HN launch post

Status: ready after owner approval. Use this after the initial Reddit sequence
or when an operator wants technical feedback on the local-first routing
architecture. Success means referral traffic from `hackernews`, GitHub stars,
quickstart copies, account activation clicks, and substantive comments about
routing policy, custody, or provider failover.

## Title

Show HN: Sage Router – open-source, local-first AI model router for agents

## Body

Hi HN, I built Sage Router because every agent harness I use has its own model
picker and breaks differently when a provider rate-limits or goes down.

Sage Router is a local-first routing layer: one OpenAI-compatible endpoint that
selects the best model per request by task type, model capability, provider
health, latency, and policy, then fails over across your own authorized
providers and local models.

The important product boundary: it is routing infrastructure for access you
already control, not a hosted marketplace. Provider credentials can stay on
your machine or private server by default. The hosted service adds generated
keys, quotas, analytics, health monitoring, dashboards, and reliability routing,
but it does not bundle model resale.

What it supports today:

- OpenAI-compatible clients, Codex, Cursor, Aider, Continue, and OpenHands
- local Ollama and Ollama Cloud through your authorized local Ollama runtime
- OpenAI, Anthropic-compatible routes, Gemini, NVIDIA NIM, OpenRouter BYOK, and
  private endpoints when configured
- multiple API keys per provider with load balancing and 429 failover
- capability-aware routing for text, image, audio, video, documents, tools, and
  long-context requests

30-second local start:

```bash
python3 router.py --port 8790
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
```

Repo:
https://github.com/earlvanze/sage-router?utm_source=hackernews&utm_medium=community&utm_campaign=sage-router-launch

Site:
https://sagerouter.dev/?utm_source=hackernews&utm_medium=community&utm_campaign=sage-router-launch

Quickstart:
https://sagerouter.dev/quickstart?utm_source=hackernews&utm_medium=community&utm_campaign=sage-router-launch

Comparison:
https://sagerouter.dev/compare/openrouter?utm_source=hackernews&utm_medium=community&utm_campaign=sage-router-launch

I would be interested in feedback on the routing/custody model: should this
stay primarily a self-hosted local layer, or is the hosted generated-key edge
the more useful default for teams?
