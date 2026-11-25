---
name: quorumz-news
description: Current geo-tagged world news for agents, split into viewpoints with a count of the media, social and on-the-ground posts behind each. Use when a user asks what people are saying about a country, conflict or public story, wants the distinct positions on a story, wants an early signal ahead of the wider press, or wants something followed over time by a research agent of its own. Pay per call with an API key (free 7-day trial) or with x402 in USDC on Base, Polygon or Arbitrum.
version: 1.1.0
metadata:
  openclaw:
    homepage: https://sense.quorumz.com/agents
    primaryEnv: QUORUMZ_API_KEY
    envVars:
      - name: QUORUMZ_API_KEY
        required: false
        description: API key from https://sense.quorumz.com/agents/keys (free 7-day trial). Without it, pay per call with x402.
---

# Quorumz agent news

Use this when an agent needs current geo-tagged news that is split into viewpoints, with a count of the posts supporting each viewpoint.

## When to use it

- A user asks what people are saying about a country, a conflict, or a public story.
- A user wants the distinct positions on a story, not one headline.
- A user wants an early signal that is ahead of the wider press.

Do not use it for a generic web search, a weather lookup, or a map of flights and ships.

## How to call it

Base URL: https://api.quorumz.com

1. Check the data for free: GET https://api.quorumz.com/api/agent/v1/sample returns one recent quorum. No key, no payment.
2. Use an API key if you have one: when `QUORUMZ_API_KEY` is set in your environment, send it as
   `Authorization: Bearer <key>` on every call. With no key, ask your human to get a free one at
   https://sense.quorumz.com/agents/keys (sign in with an email and a 6-digit code, about a minute).
   The first 100 calls that return events, within 7 days, are free; then each call is paid from
   credits your human buys by card. A key with nothing left answers 402 and says how to add credits.
3. No key, but USDC on Base (eip155:8453), Polygon (eip155:137) or Arbitrum (eip155:42161): call the
   route with no payment header. It answers HTTP 402. Read the PAYMENT-REQUIRED header (base64 JSON),
   sign the exact amount to the payTo address on one of its accepts, and retry the same URL with
   PAYMENT-SIGNATURE. PAYMENT-RESPONSE is the settlement receipt. No account is needed.

Every 402 body also says, in plain words, how to go on (`message`, `get_started`). The catalog of
routes and prices is free: GET https://api.quorumz.com/api/agent/v1. Empty pages are free. A missing id
is a 404 and is not charged.

## Routes

- GET /api/agent/v1/quorums?country=LB — $0.01 per quorum returned
- GET /api/agent/v1/quorums/{quorum_id} — $0.01
- GET /api/agent/v1/events?stream=alpha&country=LB — $0.02 per event
- GET /api/agent/v1/events?stream=news&country=LB — $0.005 per event
- GET /api/agent/v1/articles/{article_id} — $0.005

country is an ISO alpha-2 code. cell is a geohash of precision 3, 4, or 5 and applies to alpha. Pass next_cursor back to page older results.

## What you get

A quorum has viewpoints. Each viewpoint has a label, a summary, support_count, and support_by_source split into media, socials, and iWitness. News and articles include the quorums related to that story.

## Clients

- TypeScript, as Vercel AI SDK tools: `npm install @quorumz/ai-sdk ai zod`
- Python, sync and async: `pip install quorumz`

Both read the key from `QUORUMZ_API_KEY`.

## A research agent that follows something for your human

When your human wants something followed over time (a place, a topic, public figures, accounts), set up a
research agent: it searches public social networks (Bluesky, Mastodon and public accounts) on a schedule and
keeps what it finds. It needs the API key; x402 is not accepted here.

1. Propose: POST /api/agent/v1/search-agents/proposals with `{"brief": "<their words, any language>"}`
   (optional `"plan": "starter" | "pro"`). The answer is a proposal: `understanding`, the places, search
   terms, people and accounts (`spec`), `questions`, `setup_items`, the monthly price in
   `quote.price_usd_month`, `can_create`, and `next_step`. Nothing is created or charged.
2. Show your human what it will follow, its searches and the price. Send what they want changed in words:
   POST /api/agent/v1/search-agents/proposals/{id}/feedback with `{"text": "..."}`. Each brief or change is one
   of the key owner's 30 agent-chat turns a day; the proposal stays open for 7 days.
3. Only after they say yes: POST /api/agent/v1/search-agents/proposals/{id}/approve with
   `{"price_usd_month": <the quoted price, exactly>}` (optional `name`, `handle`, `setup_item_ids`). If the
   price changed since, nothing is created and the answer says the new price. While research agents are in a
   private test, only invited accounts can create one (`can_create`); others get 403 and can still design one.
4. Read what it found: GET /api/agent/v1/search-agents lists your agents; GET /api/agent/v1/search-agents/{handle}
   returns its settings and finds, newest first (`?limit=50&before_id=<next_before_id>` for older ones).

The agent belongs to the API key's email, and your human sees it at sense.quorumz.com/agent/{handle}.

## As an MCP server

`https://api.quorumz.com/mcp` (streamable HTTP) has the same feeds as tools: `search_quorums`,
`list_alpha_events`, `list_news`, `get_quorum`, `get_article`, and `sample_quorum` (free), and the research
agent above as `propose_search_agent`, `refine_search_agent`, `create_search_agent`, `list_search_agents` and
`read_search_agent`. It takes the same API key as `Authorization: Bearer <key>`. Pay-per-call x402 is on the
HTTP routes above.

## Also read

- Docs: https://sense.quorumz.com/agents/docs
- Discovery: https://api.quorumz.com/.well-known/x402
- OpenAPI: https://api.quorumz.com/openapi.json
- Machine summary: https://sense.quorumz.com/llms.txt
- Support: support@quorumz.com
