---
name: rankdelta
description: SEO and AI visibility through the Rankdelta MCP server. Check how a brand shows up in ChatGPT, Perplexity, Gemini and Google AI Overviews, see which competitors the AI recommends instead, track Google rankings, research keywords, audit pages and pull backlink and domain overviews.
version: 1.0.0
metadata:
  openclaw:
    emoji: "✦"
    homepage: https://rankdelta.ai
    primaryEnv: RANKDELTA_API_KEY
    requires:
      env:
        - RANKDELTA_API_KEY
    envVars:
      - name: RANKDELTA_API_KEY
        required: true
        description: Personal Rankdelta API key (sk_rankdelta_…), created in Settings → API & MCP.
---

# Rankdelta

[Rankdelta](https://rankdelta.ai) is an open-source (AGPL) SEO and AI-visibility platform. Its hosted MCP server gives agents the same data as the web app: AI share of voice, the competitors AI answers name instead of you, Google rankings, keyword research, page audits, backlinks and domain overviews. Every call is scoped to the account that owns the API key.

## Setup

1. Create an account at [rankdelta.ai](https://rankdelta.ai) (7-day trial, then paid plans).
2. Open **Settings → API & MCP**, click **Create key** and copy the `sk_rankdelta_…` value. It is shown once.
3. Store it as `RANKDELTA_API_KEY`. Never paste the key into a chat message.
4. Add the MCP server (streamable HTTP) with the key as a Bearer token:

```bash
claude mcp add rankdelta --transport http https://mcp.rankdelta.ai/mcp \
  --header "Authorization: Bearer $RANKDELTA_API_KEY"
```

Clients that take an `mcpServers` JSON block:

```json
{
  "mcpServers": {
    "rankdelta": {
      "url": "https://mcp.rankdelta.ai/mcp",
      "headers": { "Authorization": "Bearer ${RANKDELTA_API_KEY}" }
    }
  }
}
```

Full setup for Cursor, OpenCode, Claude and ChatGPT: https://rankdelta.ai/docs/mcp

## Tools

| Tool | What it does | Credits |
|---|---|---|
| `list_sites` | List your tracked sites | free |
| `add_site` | Register a site (name + URL) within your plan limit | free |
| `get_ai_visibility` | AI share of voice, last 30 days | free |
| `list_ai_recommendations` | Competitors AI recommends instead of you | free |
| `list_engines` | Supported AI engines | free |
| `list_visibility_prompts` | A site's AI-visibility prompts | free |
| `add_visibility_prompts` | Add your own prompts within the plan limit | free |
| `set_visibility_prompt_active` | Pause or resume a prompt | free |
| `run_visibility_scan` | Capped AI-visibility scan (default 6 prompts, max 12) | costs credits |
| `setup_ai_visibility` | One-shot AI-visibility setup for a new site | costs credits |
| `list_ranks` | Tracked keywords with the latest Google position | free |
| `track_rank` | Add a keyword to the rank tracker | free |
| `set_rank_active` | Pause or resume a tracked keyword | free |
| `check_ranks` | Fresh Google SERP check for tracked keywords | costs credits |
| `keyword_research` | Keyword ideas with volume, difficulty, CPC and intent | uses lookups |
| `audit_page` | On-page and technical snapshot of a URL | uses lookups |
| `backlink_summary` | Backlinks and referring domains | uses lookups |
| `domain_overview` | Organic traffic and keywords for a domain | uses lookups |
| `generate_article` | GEO-oriented article draft | costs credits |

Paid tools share the account's monthly spend cap with the web app, so a looping agent cannot go over it.

## How to use it

- Start with `list_sites` to get the site id, then pass it to the site-scoped tools.
- For "are we showing up in ChatGPT?": `get_ai_visibility`, then `list_ai_recommendations` to see who gets named instead.
- Ask before running anything marked "costs credits", and keep `run_visibility_scan` at the default 6 prompts unless the user asks for more.
- Search volumes, difficulty and traffic are estimates. AI answers are sampled, so share of voice is a measurement with noise: say so when you report it.

## Example requests

- "List my Rankdelta sites."
- "What's my AI share of voice for example.com, and who does ChatGPT recommend instead?"
- "Keyword ideas for 'ai seo tool' with volume and difficulty."
- "Audit https://example.com/pricing and summarize the issues."
- "Track 'ai seo tool' for example.com, then check ranks."
