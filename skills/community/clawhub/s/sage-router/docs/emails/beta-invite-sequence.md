# Sage Router hosted beta invite email sequence

**Status: drafts for launch. Personalize before sending. Replace {{first_name}}, {{link}}, etc.**

## Email 1 — Invite (send on beta admit)

Subject: You're in — Sage Router hosted beta access

Hi {{first_name}},

You're on the Sage Router hosted beta list, and access is open now.

Sage Router is the open-source, local-first AI model router. Hosted Sage Router adds generated keys, quotas, analytics, provider health monitoring, dashboards, and reliability routing — without bundled model resale.

What you get in beta:
- Hosted routing analytics dashboard
- Provider health + uptime checks
- Team config sync
- Early pricing (lite/pro/max) before public launch

Get started: {{link}}

Your provider credentials stay on your machine by default. We don't resell model access.

Reply with what you're routing and which harness (Codex, Claude Code, Cursor, OpenClaw, etc.) — it shapes the roadmap.

— Earl

## Email 2 — Day 2: quick win

Subject: A 30-second Sage Router win

Hi {{first_name}},

If you haven't pointed a tool at Sage Router yet, the fastest win is Codex:

    python3 router.py --port 8790
    export OPENAI_BASE_URL=http://localhost:8790/v1
    export OPENAI_API_KEY=local-router
    codex --model openai/gpt-4.1

Now every request is policy-routed across your providers with automatic fallback. Watch the route log when a provider hiccups — that's the differentiator.

Full guide: {{codex_guide_link}}

— Earl

## Email 3 — Day 5: vs OpenRouter

Subject: Why local-first, not a marketplace

Hi {{first_name}},

A common question: how is this different from OpenRouter?

OpenRouter is a hosted model marketplace/proxy with documented BYOK paths. Sage Router is local-first routing for access you already control: your keys, your subscriptions, your local Ollama models, and your private endpoints, with policy-based failover and telemetry you own.

Full comparison: {{comparison_link}}

If you're already on OpenRouter, you can still wire it in as one BYOK upstream.

— Earl

## Email 4 — Day 10: feedback + pricing

Subject: Two quick questions + beta pricing

Hi {{first_name}},

Beta pricing is live: Lite $6/mo, Pro $30/mo, and Max $72/mo. The local core stays free.

Two questions that shape launch:
1. Which plan fits how you'd actually use it?
2. What's the one feature that would make you pay?

Reply directly — I read every response.

— Earl

## Email 5 — Day 21: launch + share

Subject: Sage Router is launching publicly

Hi {{first_name}},

We're going public this week. If Sage Router has saved you a provider outage or a rewiring job, the most helpful thing you can do is share it where your community lives (HN, Reddit, X, a team Slack).

Launch post + assets: {{launch_link}}
Repo: https://github.com/earlvanze/sage-router

Thank you for being in the beta.

— Earl
