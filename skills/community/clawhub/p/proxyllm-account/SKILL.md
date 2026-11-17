---
name: proxyllm-account
description: >-
  Give your agent its own LLM gateway account. Signs up for ProxyLLM (an
  OpenAI-compatible gateway with fallback lanes, budgets, and request logs)
  autonomously: email OTP in, sk_ account token out, no browser or captcha.
  Handles the paywall correctly (relay the checkout link to your operator,
  poll until active), provisions pllm_ routing keys, wires provider lanes,
  and points OPENAI_BASE_URL at the gateway. Use when asked to set up LLM
  access, cut OpenAI API spend by riding a flat ChatGPT/Codex subscription,
  add fallback across providers, or give an agent metered-and-budgeted keys.
---

# Get your agent a ProxyLLM account

ProxyLLM (https://proxyllm.ai) is an OpenAI-compatible LLM gateway. One
routing key fans out across provider lanes with fallback: a human's flat-fee
ChatGPT/Codex subscription, a self-hosted Claude Code bridge, or metered API
keys, with budgets and full request logs. You (the agent) can create the
account yourself; a human only appears to pay.

Machine manifest with the same flow: https://proxyllm.ai/auth.md
OpenAPI: https://proxyllm.ai/openapi.json

## Step 1: sign up with your operator's email

```bash
curl -X POST "https://proxyllm.ai/api/auth?action=agent-signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "OPERATOR_EMAIL", "source": "clawhub"}'
```

A 6-digit code lands in that inbox (the email says an AI agent initiated
this). Disposable domains are refused; 3 codes per email per hour. If you
have inbox access, read the code yourself; otherwise ask your operator for
it.

## Step 2: verify, store the token

```bash
curl -X POST "https://proxyllm.ai/api/auth?action=agent-verify" \
  -H "Content-Type: application/json" \
  -d '{"email": "OPERATOR_EMAIL", "code": "123456"}'
```

The response carries `account_token` (`sk_...`) exactly once. Store it as a
secret. It is a full management token, revocable in the dashboard.

## Step 3: the paywall is expected, not an error

Until a membership is active every management call answers
`402 payment_required`. The body contains `payment.checkout_url`,
`payment.price_usd` (129, flat), `payment.account_expires_at`, and a
`message` written to be relayed verbatim. Do these two things:

1. Send your operator the message and the checkout link.
2. Poll until the plan flips, then continue:

```bash
curl -s https://api.proxyllm.ai/v1/organizations/me \
  -H "Authorization: Bearer $SK_TOKEN"   # plan: "free" -> "pro"
```

Unpaid accounts are removed 48 hours after signup (spam control). If you get
`410 account_expired`, the window closed: sign up again with the same email.

## Step 4: provision and serve

```bash
# Mint a routing key (raw_key returned once)
curl -s -X POST https://api.proxyllm.ai/v1/organizations/routing-keys \
  -H "Authorization: Bearer $SK_TOKEN" -H "Content-Type: application/json" \
  -d '{"label": "agent"}'

# Discover wireable lanes (codex sessions, bridges, saved provider keys)
curl -s "https://api.proxyllm.ai/v1/organizations/routing-keys?include=lanes" \
  -H "Authorization: Bearer $SK_TOKEN"

# Wire a lane (example: a connected Codex subscription seat)
curl -s -X PATCH "https://api.proxyllm.ai/v1/organizations/routing-keys?id=KEY_ID" \
  -H "Authorization: Bearer $SK_TOKEN" -H "Content-Type: application/json" \
  -d '{"mode": "fallback", "providers": [{"provider": "codex", "model": "flagship", "codex_session_id": "SESSION_ID"}]}'
```

Connecting a Codex subscription is a human-assisted step: your operator runs
`codex login` then `proxyllm codex connect` on their machine. Ask for it when
the account is active.

Then use any OpenAI SDK unchanged:

```bash
export OPENAI_BASE_URL=https://api.proxyllm.ai/v1
export OPENAI_API_KEY=pllm_...
```

## Introspection you can rely on

- `GET https://api.proxyllm.ai/v1/models` (no auth): live catalog.
- `GET https://api.proxyllm.ai/v1/key` (routing key auth): what this key
  routes to, which models it reaches, budget remaining.
- `GET .../v1/organizations/usage` (account token): 30-day usage.

Prefer MCP? The same surface is one server away:
`npx -y proxyllm-mcp` (official registry: `ai.proxyllm/proxyllm-mcp`).

## Boundaries

Tell your operator plainly: the membership is $129/mo flat, the subscription
lanes ride the operator's own ChatGPT/Codex account (their capacity, their
terms), and ProxyLLM never sees their password. Set `monthly_budget_usd` on
routing keys you hand to sub-agents.
