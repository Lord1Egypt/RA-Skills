---
name: reddapi
description: Use this skill to access Reddit's full data archive via reddapi.dev API. Features semantic search, vector search, lead generation, subreddit discovery, and real-time trend analysis. Perfect for market research, competitive analysis, lead generation, and niche opportunity discovery.
license: MIT
keywords:
  - reddit
  - api
  - search
  - market-research
  - niche-discovery
  - lead-generation
  - social-media
---

# reddapi.dev Skill

## Overview

Access **Reddit's complete data archive** through reddapi.dev's powerful API. This skill provides semantic search, vector search, AI-powered lead generation, subreddit discovery, and trend analysis capabilities.

**Key Advantage:** This is a **third-party service** (not Reddit official), meaning:
- ✅ **No rate limits** - Unlimited QPS and request volume (plan-based)
- ✅ **No time restrictions** - 24/7 availability
- ✅ **50K+ subreddits** - 1024D vector index over 1.5M+ posts
- ✅ **AI lead scoring** - Auto-classify posts by buying intent (0-100)
- ✅ **Full Reddit archive** - Access historical and real-time discussions

## Usage in Conversation

After installing this skill, simply ask in natural language:

### Finding User Pain Points
```
What are people complaining about with iPhone battery life?
Find discussions about frustrating problems with NOTION
Search for user frustrations with current TOOL_NAME
```

### Competitive Analysis
```
What do people think about COMPETITOR_A vs COMPETITOR_B?
Find common complaints about COMPETITOR
What are the main problems users have with ALTERNATIVE_TOOL?
```

### Lead Generation (NEW!)
```
Find B2B leads for project management software
Who is looking for alternatives to Stripe?
Find startups complaining about CRM pricing
Discover high-intent leads for marketing tools
```

### Discovering Opportunities
```
Find discussions that start with "I wish there was an app that..."
What do users want but can't find in existing products?
Search for "best way to" discussions about TOPIC
```

### Trend Analysis
```
What trending topics are growing fast in Reddit discussions?
Find emerging trends in AI/ML communities
What are people discussing about TOPIC lately?
```

### Research & Validation
```
Search for real user feedback on PRODUCT_NAME
Find problems users mention with CATEGORY tools
What are the top frustrations in INDUSTRY?
```

## Key Features

### 🔍 Semantic Search
Natural language search across millions of Reddit posts and comments. AI-powered understanding of context and meaning.

### ⚡ Vector Search
Fast vector similarity search. No LLM processing, returns results in seconds.

### 🎯 Lead Generation
AI-powered business lead discovery from Reddit discussions. Every match is scored 0-100 on signal strength and tagged with:
- **lead_type**: `pain_point`, `solution_request`, `complaint`, `feature_request`, `comparison`
- **pain_point**: What the user is frustrated about
- **opportunity**: What solution they're looking for
- **industry**: Inferred industry from context
- **target_product**: The product they're complaining about or comparing

### 📊 Trends API
Discover trending topics with engagement metrics (post count, upvotes, sentiment, growth rate).

### 📝 Subreddit Discovery
List and explore subreddits by topic or engagement.

## HTTP API Reference

**Base URL:** `https://reddapi.dev`

**Authentication:** `Authorization: Bearer YOUR_API_KEY`

### POST /api/v1/leads (NEW!)
```bash
curl -X POST "https://reddapi.dev/api/v1/leads" \
  -H "Authorization: Bearer ***" \
  -H "Content-Type: application/json" \
  -d '{"query": "people frustrated with CRM software", "limit": 20, "min_score": 70}'
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Natural language lead query |
| limit | number | No | Results (default: 20) |
| min_score | number | No | Minimum lead score 0-100 |

**Response fields per lead:**
- `lead_score` (0-100): AI buying intent score
- `lead_type`: pain_point, solution_request, complaint, feature_request, comparison
- `pain_point`: Specific frustration identified
- `opportunity`: Business opportunity inferred
- `industry`: Inferred industry
- `target_product`: Product being discussed

### POST /api/v1/search/semantic
```bash
curl -X POST "https://reddapi.dev/api/v1/search/semantic" \
  -H "Authorization: Bearer ***" \
  -H "Content-Type: application/json" \
  -d '{"query": "best productivity tools for remote teams", "limit": 100}'
```

### POST /api/v1/search/vector
```bash
curl -X POST "https://reddapi.dev/api/v1/search/vector" \
  -H "Authorization: Bearer ***" \
  -H "Content-Type: application/json" \
  -d '{"query": "electric vehicle", "limit": 30, "start_date": "2025-11-01", "end_date": "2025-12-31"}'
```

### POST /api/v1/trends
```bash
curl -X POST "https://reddapi.dev/api/v1/trends" \
  -H "Authorization: Bearer ***" \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2025-01-01", "end_date": "2025-01-31", "limit": 20}'
```

### GET /api/v1/subreddits
```bash
curl "https://reddapi.dev/api/v1/subreddits?search=programming&limit=100" \
  -H "Authorization: Bearer ***"
```

## Use Cases

### Lead Generation
```bash
# Find high-intent B2B leads
curl -X POST "https://reddapi.dev/api/v1/leads" \
  -H "Authorization: Bearer ***" \
  -d '{"query": "SaaS founders complaining about Stripe fees", "limit": 20, "min_score": 80}'
```

### Market Research
```bash
# Analyze competitor discussions
curl -X POST "https://reddapi.dev/api/v1/search/semantic" \
  -H "Authorization: Bearer ***" \
  -d '{"query": "COMPETITOR problems complaints", "limit": 200}'
```

### Niche Discovery
```bash
# Find underserved user needs
curl -X POST "https://reddapi.dev/api/v1/search/semantic" \
  -H "Authorization: Bearer ***" \
  -d '{"query": "I wish there was an app that", "limit": 100}'
```

### Trend Analysis
```bash
# Monitor topic growth
curl -X POST "https://reddapi.dev/api/v1/trends" \
  -H "Authorization: Bearer ***"
```

## Environment Variables

```bash
export REDDAPI_API_KEY="***"
```

Get your free API key at: https://reddapi.dev

## Pricing

| Plan | Price | Monthly Searches |
|------|-------|------------------|
| Free | $0 | 3 |
| Lite | $19.9/mo | 500 |
| Starter | $49/mo | 5,000 |
| Pro | $99/mo | 15,000 |

All plans include access to all endpoints (search, leads, trends, subreddits).

Sign up at https://reddapi.dev to get started.

## Related Skills

- **niche-hunter**: Automated opportunity discovery
- **reddit-insights**: Detailed API reference with query strategies
