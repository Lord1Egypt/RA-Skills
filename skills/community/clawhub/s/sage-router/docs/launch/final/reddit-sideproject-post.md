# Reddit r/SideProject launch post

Status: ready after owner approval. Use this as the third Reddit post after
r/selfhosted and r/Ollama. The goal is buyer-intent traffic: pricing views,
account activation clicks, generated hosted keys, and founder-sales replies.

## Title

I built Sage Router: one endpoint that routes AI agents across your own models

## Body

I built Sage Router because every agent tool I use has its own model config,
fallback behavior, and rate-limit failure mode.

The side project became a product: one OpenAI-compatible endpoint for Codex,
Cursor, Aider, Continue, OpenHands, OpenAI SDKs, Anthropic-compatible clients,
local Ollama, Ollama Cloud through authorized local runtime access, and other
BYOK providers.

What it does:

- chooses routes by task, provider health, model capability, latency, and
  policy;
- fails over on 429s and provider outages;
- load-balances multiple API keys per provider;
- routes image/audio/video inputs only to capable models;
- keeps provider credentials local by default when self-hosted;
- offers hosted generated `sk_sage_*` keys, quotas, analytics, and reliability
  routing for teams that want a public edge.

Commercial boundary: Sage Router sells routing infrastructure, not bundled
model resale. You still bring authorized provider access unless a future
managed-provider beta explicitly satisfies provider terms and unit economics.

Hosted plans are live:

- Lite: $6/month
- Pro: $30/month
- Max: $72/month

Pricing:
https://sagerouter.dev/pricing?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

Create a hosted key:
https://app.sagerouter.dev/account.html?plan=pro&start=checkout&utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

Quickstart:
https://sagerouter.dev/quickstart?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

Repo:
https://github.com/earlvanze/sage-router?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

For people launching AI infrastructure side projects: would you lead with the
hosted key workflow, the local-first open-source core, or the OpenRouter
comparison?
