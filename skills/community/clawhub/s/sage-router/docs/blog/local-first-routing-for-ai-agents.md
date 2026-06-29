# Local-first routing for AI agents

**Why the next layer of AI infra lives on your machine, not in a marketplace.**

Agent harnesses (Codex CLI, Claude Code, Cursor, Aider, Continue, OpenHands, OpenClaw) each ship their own model picker, and most of them still break the moment a provider rate-limits, goes down, or quietly reroutes your traffic to a cheaper model. Teams that run several providers and local models end up glueing fallback logic into every tool.

Sage Router takes a different bet: **routing is local-first infrastructure for access you already control.**

## The problem with "one bill, one marketplace"

Hosted model marketplaces are convenient, but they can trade away three things agentic teams care about:

1. **Custody.** Provider keys, BYOK policy, and traffic often move into a hosted control plane.
2. **Control.** You can't define routing policy, fallback order, or local-vs-cloud preference the way you can with your own providers.
3. **Local models.** Local Ollama and private Tailnet models are usually outside the natural path of a hosted marketplace, even though they are often the cheapest reliable fallback you have.

## What local-first routing actually means

Sage Router runs on your machine or server. It exposes one OpenAI-compatible and Anthropic-compatible endpoint. Your tools point at it. The router:

- Selects the best model per request by task type, capability, latency, context size, and policy.
- Fails over across your authorized providers when one is down, slow, or rate-limited, with no mid-stream model handoff.
- Discovers new models from Ollama, OpenAI, Anthropic, Gemini, NVIDIA NIM, and OpenClaw automatically.
- Keeps provider credentials local by default, so hosted Sage infrastructure physically cannot harvest them.
- Emits route-event telemetry (selected model, attempts, elapsed time, plan) so you can prove which route is best.

## A 30-second Codex example

```bash
python3 router.py --port 8790
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
codex --model openai/gpt-4.1
```

Now every Codex request is policy-routed across your providers and local models, with automatic fallback. You didn't rewiring Codex; you swapped the model layer underneath it.

## Free core, paid convenience

The local router is free and open source and works without an account. Hosted Sage Router monetizes routing convenience, not bundled model resale: generated keys, quotas, provider health monitoring, hosted dashboards, uptime checks, and reliability/failover routing. That keeps trust bottom-up (developers adopt the free local core) and revenue top-up (teams pay for operations and reliability).

## Try it

- Repo: https://github.com/earlvanze/sage-router
- Site: https://sagerouter.dev
- Codex guide: [docs/integrations/codex.md](../integrations/codex.md)
- vs OpenRouter: [docs/openrouter-comparison.md](../openrouter-comparison.md)
