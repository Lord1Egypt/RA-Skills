# Reddit r/selfhosted launch execution

- **Channel:** r/selfhosted
- **Campaign:** `sage-router-launch`
- **UTM link:** `https://sagerouter.dev/self-hosted-ai-model-router?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch`
- **Created:** 2026-06-27
- **Status:** ready to post (requires owner manual submission)
- **Success signal to watch:** `reddit` source clicks, self-hosted magic-link events, quickstart copies, GitHub stars

## Title

Sage Router — self-hosted AI model router with automatic provider failover

## Body

I built and open-sourced the model router I run for my own agents.

Sage Router sits between your agent tools and your model providers. It exposes one OpenAI-compatible endpoint, selects a route by task/model capability/provider health/policy, and fails over when a provider rate-limits or goes down.

The self-hosted angle: provider credentials can stay on your machine or private server by default. Hosted Sage Router adds generated keys, quotas, analytics, health checks, and reliability routing, but the local core remains useful without a hosted account.

What it supports today:

- OpenAI-compatible clients and Codex-style tools
- OpenAI, Anthropic, Gemini, NVIDIA NIM, Ollama, and Ollama Cloud through your authorized access
- Local-first and Tailnet deployments on port `8790`
- Capability-aware routing for text, image, audio, and video inputs
- Multiple API keys per provider with load balancing and 429 failover

30-second local start:

```bash
python3 router.py --port 8790
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
```

Repo: https://github.com/earlvanze/sage-router?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

Self-hosted overview: https://sagerouter.dev/self-hosted-ai-model-router?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

Quickstart: https://sagerouter.dev/quickstart?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

Sage Router vs OpenRouter: https://sagerouter.dev/compare/openrouter?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

What are you using for provider failover today? Are people here mostly wiring fallback into each app, using a gateway, or just letting individual clients fail?

## Posting instructions

1. Post only this copy; do not paste prompts, provider credentials, API keys, OAuth tokens, customer data, or raw provider responses.
2. After posting, copy the live Reddit post URL and timestamp below.
3. Watch the launch funnel at `https://app.sagerouter.dev/launch-funnel.html` for `reddit` attributed events within 24-48 hours.

## Live post URL

_Paste after posting:_

## Timestamp posted

_Paste after posting:_
