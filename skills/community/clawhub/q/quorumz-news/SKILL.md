---
name: quorumz-news
description: Current geo-tagged world news for agents, split into viewpoints with a count of the media, social and on-the-ground posts behind each. Use when a user asks what people are saying about a country, conflict or public story, wants the distinct positions on a story, or wants an early signal ahead of the wider press. Pay per call with an API key (free 7-day trial) or with x402 in USDC on Base, Polygon or Arbitrum.
version: 1.0.0
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

1. Read the free catalog: GET https://api.quorumz.com/api/agent/v1
2. Call the route you need with no payment header.
3. If the response is HTTP 402, read the PAYMENT-REQUIRED header. It is base64 JSON. Its accepts list USDC on Base (eip155:8453), Polygon (eip155:137) and Arbitrum (eip155:42161): sign the exact amount to the payTo address on the one you hold, then retry the same URL with PAYMENT-SIGNATURE.
4. Read PAYMENT-RESPONSE for the settlement receipt.

Empty pages are free. A missing id is a 404 and is not charged.

## Routes

- GET /api/agent/v1/quorums?country=LB — $0.01 per quorum returned
- GET /api/agent/v1/quorums/{quorum_id} — $0.01
- GET /api/agent/v1/events?stream=alpha&country=LB — $0.02 per event
- GET /api/agent/v1/events?stream=news&country=LB — $0.005 per event
- GET /api/agent/v1/articles/{article_id} — $0.005

country is an ISO alpha-2 code. cell is a geohash of precision 3, 4, or 5 and applies to alpha. Pass next_cursor back to page older results.

## What you get

A quorum has viewpoints. Each viewpoint has a label, a summary, support_count, and support_by_source split into media, socials, and iWitness. News and articles include the quorums related to that story.

## Two ways to pay

1. API key paid by credit card: your human signs up at https://sense.quorumz.com/agents/keys
   and gives you a key. Send it as `Authorization: Bearer <key>`; if `QUORUMZ_API_KEY` is set
   in your environment, that is the key. The first 100 calls that
   return events, within 7 days, are free; then each call is paid from credits your human
   buys by card. With no credits, a call answers 402.
2. x402 in USDC on Base, Polygon or Arbitrum: no account. Answer the 402 with a signed payment.

## Also read

- Docs: https://sense.quorumz.com/agents/docs
- Discovery: https://api.quorumz.com/.well-known/x402
- OpenAPI: https://api.quorumz.com/openapi.json
- Machine summary: https://sense.quorumz.com/llms.txt
- Support: support@quorumz.com
