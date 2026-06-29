# Dev.to launch post

Status: ready after owner approval. Use this when developer-tooling traffic is
the priority. Success means quickstart copies, GitHub traffic, generated-key
activation clicks, and replies about local-first provider failover.

## Title

Showoff Saturday: Sage Router — open-source local-first AI model router with automatic provider failover

## Tags

`#ai`, `#opensource`, `#routing`, `#ollama`, `#selfhosted`, `#agents`

## Body

I open-sourced Sage Router, the model router I run between my agent tools and
my providers.

Sage Router is a local-first routing layer: one OpenAI/Anthropic-compatible
endpoint that selects the best model per request by task type, capability,
latency, and policy, then fails over across your own providers with no
mid-stream handoff.

The bet: routing is local-first infrastructure for access you already control,
not a hosted marketplace. Your provider keys stay on your machine by default.
The core is free and open source (MIT). Hosted Sage Router plans add generated
keys, quotas, analytics, health monitoring, dashboards, and reliability routing
— still without bundled model resale.

- Repo: https://github.com/earlvanze/sage-router?utm_source=devto&utm_medium=community&utm_campaign=sage-router-launch
- Site: https://sagerouter.dev/?utm_source=devto&utm_medium=community&utm_campaign=sage-router-launch
- vs OpenRouter: https://sagerouter.dev/compare/openrouter?utm_source=devto&utm_medium=community&utm_campaign=sage-router-launch

30-second start:

```bash
python3 router.py --port 8790
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
codex --model openai/gpt-4.1
```

What's your current provider-failover setup? Genuinely curious what people
cobbled together.
