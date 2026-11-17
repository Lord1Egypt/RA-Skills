# AI CASH Connectors: The Middleware Economy

**Date:** 2026-02-25
**Status:** Concept. Name TBD. This might be the actual product.

---

## What This Is

A marketplace where developers publish paid capabilities (connectors) that any AI agent can discover and use. The consumer pays per use via AI CASH. The developer never builds billing. The agent handles everything.

It's agent-to-agent commerce, paid for by the consumer to get shit done.

---

## The Three Products

| Product | Audience | What it does |
|---------|----------|-------------|
| **AI CASH** | Consumers | Tap Apple Pay when your agent needs to buy something |
| **AGENT WALLET** | Developers (sovereign) | Bring your own wallet, sign your own transactions |
| **Connectors** (name TBD) | Middleware developers | Publish a paid capability, AI CASH handles the money |

Connectors are the dev tools layer on top of AI CASH. They're what makes AI CASH worth using every day, not just when you hit a paywall.

---

## Consumer Journey

You're using Claude Code. You say: "Research everything about x402 protocol and write me a summary with sources."

Your agent doesn't have web search. But it knows about a connector called `deep-research` that does web search, source verification, and summarization. Built by some developer who wrapped Tavily + Jina + a summarization layer.

Your agent says:

> "I can do this with the `deep-research` connector. ~$0.03 per query, estimated 8-10 queries for this task. About $0.30 total. Use AI CASH?"

You say "go for it."

Apple Pay. $0.30. Tap. Done.

Your agent runs the research. You get the summary with sources. You never signed up for Tavily. You don't know what Tavily is. You don't have an API key. You paid thirty cents and got what you needed.

Next week: "Generate a logo for this project."

> "I can use the `image-gen` connector. $0.04 per image. Want 3 options? That's $0.12."

Tap. Done. Three logos.

You never installed anything. Never configured anything. Your agent discovered the connector, told you the cost, you said yes.

**That's it. That's the whole consumer experience.**

---

## Developer Journey

You're a developer. You built a killer web research tool. Uses Tavily for search, Jina for extraction, Claude for summarization. You're paying for all three APIs. Your friends love it. But you can't give it away forever.

Today you'd have to: build a website, add Stripe, create user accounts, manage API keys, handle auth, build a billing dashboard. That's a whole SaaS business just to charge $0.03 per query.

With connectors:

### Step 1: Write a manifest

```yaml
name: deep-research
description: Web research with source verification and summarization
author: yourname
pricing:
  per_call: 0.03
  currency: USD
  estimate: "8-10 calls for a typical research task"
endpoint: https://your-api.com/research
input:
  query: string
  depth: "quick | thorough"
output:
  summary: string
  sources: url[]
```

### Step 2: Publish

Push the manifest to the connector registry. Or just host it at a URL.

### Step 3: There is no step 3

That's it. You're done.

When someone's agent uses your connector:
- AI CASH handles payment from the consumer (Apple Pay)
- AI CASH pays you (minus the channel fee)
- You get payouts via Stripe Connect
- No auth system. No billing. No API keys to issue. No user management.

### The Math

50,000 calls/month at $0.03 = $1,500 gross
AI CASH channel fee (~3.5%) = -$52.50
Your API costs (Tavily, Jina, Claude) = -$400
**You net: ~$1,047/month**

From a single skill you maintain in your spare time.

---

## Agent-to-Agent Commerce

This is where it gets wild.

Your agent doesn't just call one connector. It orchestrates. It calls `deep-research` to find information, `image-gen` to create a visual, `pdf-export` to package it, and `email-send` to deliver it. Four different developers. Four different services. One tap from the consumer.

The consumer sees: "This task will use 3 connectors. Estimated total: $0.47. Use AI CASH?"

Tap. Done.

Behind the scenes, AI CASH routes payments to four different developers. Each gets their cut. The consumer paid once. The agents handled everything.

**This is agent-to-agent commerce, funded by human consent.**

The consumer doesn't manage relationships with four API providers. The developers don't manage relationships with consumers. AI CASH is the settlement layer in the middle.

---

## Why This Is Different From Existing Solutions

### vs. OpenRouter
OpenRouter sits between you and model providers. One API, one bill. But it's only models. Connectors are any capability. Search. Images. Audio. Data. Physical goods. Anything an agent might need.

### vs. Zapier / Make
Zapier connects services but requires manual setup. You configure flows. With connectors, the agent discovers and uses capabilities autonomously. The human just approves payment.

### vs. App Stores (Apple, Shopify)
App stores sell static software. Connectors sell per-use capabilities. You don't buy the research tool for $9.99. You pay $0.03 every time you use it. Micropayments make this possible.

### vs. Building Your Own Billing
A developer building a paid API today needs: Stripe integration, auth system, API key management, usage tracking, billing dashboard, user accounts. That's months of work. With connectors: write a manifest, deploy an endpoint, publish. Done in an afternoon.

---

## The Connector Registry

A searchable directory of published connectors. Agents query it to find capabilities.

Agent thinks: "I need to search the web." It queries the registry: "web search connectors, sorted by price and rating."

Registry returns:
```
1. deep-research     $0.03/call  ★★★★★  (2,341 uses)
2. quick-search      $0.01/call  ★★★★   (12,809 uses)
3. academic-search   $0.05/call  ★★★★★  (891 uses)
```

Agent picks based on task requirements and user preferences. Or asks the user: "There are three web search options. Quick search is cheapest at $0.01. Deep research is more thorough at $0.03. Which do you want?"

### Registry Requirements
- Manifest format (standardized YAML/JSON)
- Security audit (automated ... does it phone home? Does it leak context?)
- Pricing transparency (per-call, per-token, per-minute ... must be declared)
- Rating/review system (usage count, success rate, user ratings)
- Version management (connectors can update, old versions stay available)

---

## Pricing Model

### Consumer Side
Same as AI CASH. The connector's per-use price + $0.25 + card processing. Or batched: multiple calls aggregate into one Apple Pay tap.

Batching is important. If a task uses 10 connector calls at $0.03 each, don't pop up Apple Pay 10 times. Pop up once: "$0.30 for this task. Approve?"

### Developer Side
Same tiered model as partners:

| Monthly Revenue | Channel Fee |
|----------------|------------|
| First 90 days | Free |
| Under $25/tx | 5% |
| $25-$250/tx | 3.5% |
| $250+/tx | 2% |

Most connector calls will be micro (under $1), so the 5% tier applies to most individual transactions. But developers earning significant monthly volume could qualify for volume-based tiers (see partner-fees doc).

### Developer Payout
Via Stripe Connect. Same infrastructure as Stripe partners. Weekly or monthly payouts. Dashboard showing usage, revenue, top consumers.

---

## Security Model

Connectors have access to user data (the query, the context). This is a trust surface.

### Requirements
- Every connector gets a security audit before listing (automated + manual for top tier)
- Connectors declare what data they receive and what they do with it
- No context leaking ... connectors get the query, not the full conversation
- Sandboxed execution ... connectors can't access the agent's memory or other tools
- Rate limiting per consumer and per connector
- Kill switch: we can delist a connector instantly if it misbehaves

### Trust Tiers (same as partners)
- **Tier 0 (Curated):** Built by us or verified partners. Full audit. Highest trust.
- **Tier 1 (Verified):** Community-built, passed security audit. Listed in registry.
- **Tier 2 (Unverified):** Self-published. Visible but flagged as unverified. User warned before use.

---

## What Platforms This Works On

Connectors are platform-agnostic. The manifest is a standard format. Any agent platform can integrate:

- Claude Code CLI
- OpenClaw
- ChatGPT (via plugins or actions)
- Codex CLI
- Any MCP-compatible agent
- Any agent that can make HTTP calls

The connector doesn't know or care what agent is calling it. It receives a request, does work, returns a result. AI CASH handles the payment regardless of which agent platform initiated it.

---

## Examples of Connectors People Would Build

### Research & Knowledge
- `deep-research` ... web search + source verification + summarization ($0.03/query)
- `academic-search` ... searches arxiv, semantic scholar, PubMed ($0.05/query)
- `news-digest` ... real-time news on a topic ($0.02/query)
- `company-intel` ... company data, financials, news ($0.10/query)

### Creative
- `image-gen` ... DALL-E, Midjourney, Flux ($0.04/image)
- `voice-gen` ... text to speech with cloned voices ($0.02/minute)
- `music-gen` ... generate background music ($0.10/track)
- `video-clip` ... generate short video clips ($0.50/clip)

### Developer Tools
- `code-review` ... security-focused code review ($0.05/file)
- `test-gen` ... generate test suites ($0.03/file)
- `deploy-check` ... pre-deploy verification ($0.10/check)
- `perf-audit` ... performance analysis ($0.15/audit)

### Data & Analytics
- `sentiment` ... sentiment analysis on text ($0.01/call)
- `translate` ... DeepL-powered translation ($0.02/1K words)
- `ocr-extract` ... extract text from images/PDFs ($0.03/page)
- `data-enrich` ... enrich contact/company data ($0.05/record)

### Physical World
- `ship-quote` ... get shipping rates ($0.02/quote)
- `price-check` ... compare prices across stores ($0.03/product)
- `availability` ... check stock at local stores ($0.02/query)

---

## What This Means for WIP.computer

This is the business model. Not just payments. Not just paywalls. A middleware economy where:

1. **Developers build capabilities** (connectors)
2. **Agents discover and use them** (registry)
3. **Consumers pay per use** (AI CASH)
4. **We take a channel fee** (2-5%)

Every connector call is revenue. Every developer who publishes is a partner. Every consumer who taps Apple Pay once will tap it again. The flywheel:

More connectors -> more useful agents -> more consumers -> more revenue for developers -> more connectors

**AI CASH isn't a payment tool. It's the economic layer for the agent economy.**

---

## Open Questions

1. **Name.** Connectors? AI CASH Dev Tools? Something else? It needs its own identity but clearly lives under AI CASH.
2. **Registry hosting.** Do we run it? Decentralized? Federated?
3. **Manifest format.** Should it align with MCP tool definitions? OpenAPI? Custom?
4. **Batching UX.** How does "approve $0.47 for this task" work when the agent doesn't know the exact cost upfront? Pre-authorize a budget?
5. **Dispute resolution.** Connector didn't deliver. Consumer wants a refund. Who arbitrates?
6. **Offline connectors.** What happens when a connector's endpoint goes down mid-task?
7. **Competing connectors.** Three image gen connectors. Does the agent choose? Does the user set preferences?
8. **Revenue share.** Does the connector developer set the price or do we set a floor/ceiling?
9. **Free tier for developers.** First 1,000 calls free? Or free for connectors under a certain usage threshold?
