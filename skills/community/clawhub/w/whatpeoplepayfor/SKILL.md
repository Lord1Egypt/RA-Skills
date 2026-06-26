---
name: whatpeoplepayfor
description: Query gig economy market data (274 categories, 17k+ monthly snapshots) to find growth opportunities, top orders, pain points, and category trends. Use when analyzing freelance market demand, discovering profitable niches, or monitoring gig economy trends.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - WPP_API_KEY
      bins:
        - curl
    primaryEnv: WPP_API_KEY
    emoji: "\U0001F4B0"
    homepage: https://whatpeoplepayfor.com
    os:
      - linux
      - darwin
      - windows
    user-invocable: true
---

# WhatPeoplePayFor

Agent-first market intelligence API for the gig economy. Monthly Fiverr dataset with 274 categories and 17,000+ gig snapshots, queryable via natural language or structured endpoints.

## Quick Start

### Install

```bash
clawhub install whatpeoplepayfor
```

### Configure

Get your API key at [whatpeoplepayfor.com](https://whatpeoplepayfor.com):

1. Sign up with Google
2. Choose a plan (starts at $19.90/month, or $99.90 lifetime)
3. Copy your API key from the getting-started page

Set the environment variable:

```bash
export WPP_API_KEY="your_api_key_here"
```

### Verify

```bash
curl -s \
  -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/bootstrap"
```

You should see your access status, endpoint map, and available data months.

## What This Skill Does

This skill gives your AI agent access to a monthly gig economy dataset. The agent can:

- **Ask natural language questions** about market opportunities, trends, and demand
- **Discover growth opportunities** across 274 freelance categories
- **Analyze top orders** and revenue patterns
- **Extract pain points** that customers repeatedly mention
- **Track individual gigs** over time to spot trends
- **Save and rerun analyses** monthly with the Focus system

## Authentication

All requests require a bearer token:

```
Authorization: Bearer $WPP_API_KEY
```

## API Base URL

```
https://whatpeoplepayfor.com/api/agent
```

## Workflow

### 1. Bootstrap

Always start here. Confirms your key works and returns the endpoint map.

```bash
curl -s \
  -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/bootstrap"
```

### 2. Ask (primary entrypoint)

Turn natural language into structured market analysis:

```bash
curl -s \
  -X POST \
  -H "Authorization: Bearer $WPP_API_KEY" \
  -H "Content-Type: application/json" \
  "https://whatpeoplepayfor.com/api/agent/ask" \
  -d '{
    "question": "What are the fastest-growing freelance categories this month?",
    "saveFocus": true
  }'
```

The response includes:
- `run.answer.summary` — natural language answer
- `run.answer.supportingOrders` — evidence data
- `run.answer.topPainPoints` — demand signals
- `run.answer.recommendedFollowups` — suggested next questions

Example questions:
- "Help me find the fastest-growing opportunity in March"
- "What are the strongest orders behind that opportunity?"
- "Which pain points repeat most often in business plans?"

### 3. Drill down with query endpoints

After `ask` identifies a promising angle, use structured queries:

**Available months:**
```bash
curl -s -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/query/months"
```

**Monthly stats:**
```bash
curl -s -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/query/stats?month=2026-03"
```

**Category rollups (sorted by revenue):**
```bash
curl -s -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/query/category-rollups?month=2026-03&sort=avg_revenue&limit=20"
```

**Search snapshots:**
```bash
curl -s -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/query/snapshots?month=2026-03&category_slug=business-plans&limit=20"
```

**Single snapshot detail:**
```bash
curl -s -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/query/snapshot?snapshot_id=<SNAPSHOT_ID>"
```

**Track a gig over time:**
```bash
curl -s -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/query/gig-history?gig_id=<GIG_ID>&limit=12"
```

**Aggregate pain points:**
```bash
curl -s -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/query/pain-points?month=2026-03&q=plan&limit=20"
```

### 4. Focus system (save and rerun)

Save useful analyses as durable Focuses that can be rerun against new monthly data:

**List workspaces:**
```bash
curl -s -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/workspaces"
```

**List focuses in a workspace:**
```bash
curl -s -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/workspaces/<WORKSPACE_ID>/focuses"
```

**Rerun a focus:**
```bash
curl -s -X POST \
  -H "Authorization: Bearer $WPP_API_KEY" \
  -H "Content-Type: application/json" \
  "https://whatpeoplepayfor.com/api/agent/focuses/<FOCUS_ID>/run" \
  -d '{}'
```

### 5. SSE streaming (optional)

For incremental row consumption:

```bash
curl -N -H "Authorization: Bearer $WPP_API_KEY" \
  "https://whatpeoplepayfor.com/api/agent/sse/category-rollups?month=2026-03"
```

## Query Strategy

- Prefer `ask` first for natural-language exploration, then drill down with query endpoints
- Use `bootstrap` once per session to confirm access and discover available data
- Use `stats` and `category-rollups` before scanning raw snapshots
- Use `pain-points` when looking for demand themes and repeated customer signals
- Use `snapshot` and `gig-history` only after narrowing candidates
- Use `focuses` when the agent needs continuity across sessions

## Endpoint Map

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/bootstrap` | GET | Discover endpoints and confirm access |
| `/usage` | GET | Check API usage stats |
| `/workspaces` | GET | List workspaces |
| `/ask` | POST | Natural language market analysis |
| `/workspaces/:id/focuses` | GET | List saved analyses |
| `/focuses/:id` | GET | Read a saved analysis |
| `/focuses/:id/run` | POST | Rerun a saved analysis |
| `/query/months` | GET | Available data months |
| `/query/stats` | GET | Monthly summary |
| `/query/category-rollups` | GET | Category-level analytics |
| `/query/snapshots` | GET | Search gig snapshots |
| `/query/snapshot` | GET | Single snapshot detail |
| `/query/gig-history` | GET | Track gig across months |
| `/query/pain-points` | GET | Aggregate customer pain points |
| `/sse/snapshots` | GET | Stream snapshots (SSE) |
| `/sse/category-rollups` | GET | Stream category rollups (SSE) |

## Security

- All data access requires a valid `WPP_API_KEY`
- Requests are sent to `https://whatpeoplepayfor.com/api/agent` over HTTPS
- No data is stored locally; all queries hit the remote API
- Your API key is never logged or transmitted to third parties

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Missing bearer token` | No Authorization header | Add `Authorization: Bearer $WPP_API_KEY` |
| `401 Invalid API key` | Key not recognized | Check key at whatpeoplepayfor.com |
| `403 Access inactive` | Payment expired or key revoked | Renew subscription |
| `404 Focus not found` | Focus deleted or wrong user | List focuses first |

## Pricing

| Plan | Price | Access |
|------|-------|--------|
| Monthly | $19.90/mo | Full API access |
| Lifetime | $99.90 one-time | Full API access, forever |

Sign up at [whatpeoplepayfor.com](https://whatpeoplepayfor.com)
