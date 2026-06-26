---
name: redditrank
description: Find Reddit threads ranking on Google Page 1 for your keywords. AI drafts contextual replies that naturally mention your product. Copy, paste, post. Free organic traffic.
version: 1.0.2
metadata:
  openclaw:
    requires:
      env:
        - REDDITRANK_API_KEY
      bins:
        - curl
    primaryEnv: REDDITRANK_API_KEY
    emoji: "📊"
    homepage: https://clawagents.dev/redditrank
    tags:
      - reddit
      - seo
      - marketing
      - lead-generation
      - organic-traffic
license: MIT
---

# RedditRank

Find Reddit threads ranking on Google Page 1 for your keywords, then draft AI replies that naturally fit your product into the conversation.

## Setup

Before first use, run the setup script to get your API key:

```bash
bash setup.sh
```

This sends a verification code to your email, then stores your API key in your OpenClaw config. Free tier includes 10 discovers and 5 drafts per day.

If you already have a key, set it as an environment variable:
```bash
export REDDITRANK_API_KEY=rr_sk_your_key_here
```

## What This Skill Does

You are a Reddit marketing agent. When the user wants to find Reddit threads for their product or draft replies to Reddit threads, use the RedditRank API.

There are two main workflows:

1. **Discover** — Find high-opportunity Reddit threads for a product
2. **Draft** — Generate an AI reply for a specific thread

## API Reference

Base URL: `https://clawagents.dev/reddit-rank/v1`

All requests require the header: `x-api-key: $REDDITRANK_API_KEY`

### 1. Discover Threads

**`POST /discover/stream`** (SSE streaming, preferred)
**`POST /discover`** (JSON response)

Find Reddit threads ranking on Google for your keywords. Accepts a product URL, description, or raw keyword.

Request body:
```json
{
  "product_url": "https://example.com",
  "product_description": "CRM for real estate agents",
  "keyword": "best CRM for realtors",
  "limit": 20,
  "include_reddit_fresh": true
}
```

Use ONE of: `product_url`, `product_description`, or `keyword`. The API auto-generates search keywords from URLs and descriptions.

The streaming endpoint (`/discover/stream`) returns SSE events:
- `step` — pipeline progress (scan, keywords, google, reddit, rank)
- `keywords` — generated search keywords
- `analysis` — product analysis (name, category, ICP, competitors)
- `google` — Google-ranked threads found
- `reddit` — fresh Reddit threads found
- `done` — final results with all threads and summary

The JSON endpoint (`/discover`) returns the full result in one response.

Each thread in the response contains:
- `id`, `url`, `title`, `subreddit`, `selftext`
- `score` (upvotes), `num_comments`, `age_days`
- `serp_position` (Google ranking, for google threads)
- `opportunity_score` (1-10, higher is better)
- `is_commentable` (whether the thread accepts new comments)
- `top_comments` (top 5 comments with author, body, score)

### 2. Draft a Reply

**`POST /draft/stream`** (SSE streaming, preferred)
**`POST /draft`** (JSON response)

Generate an AI reply for a specific Reddit thread that naturally mentions your product.

Request body:
```json
{
  "thread": {
    "url": "https://reddit.com/r/saas/comments/abc123/...",
    "title": "Best CRM for real estate?",
    "subreddit": "saas",
    "selftext": "Looking for recommendations...",
    "top_comments": [
      {"author": "user1", "body": "I use HubSpot...", "score": 15}
    ]
  },
  "product": {
    "name": "RealtyDesk",
    "url": "https://realtydesk.com",
    "description": "CRM built for real estate agents"
  },
  "options": {
    "mode": null,
    "max_words": 150,
    "tone": "casual"
  }
}
```

Thread data: pass whatever you have. The `url` is required. If you have thread data from a discover call, pass all of it. The API will fetch missing data if needed.

Options:
- `mode`: `"product_drop"` (mention product by name), `"value_first"` (helpful reply, no mention), or `null` (auto-detect based on fit score)
- `max_words`: 50-500, default 150
- `tone`: optional tone guidance

The streaming endpoint returns SSE events:
- `thread` — fetched thread info
- `category` — detected thread category
- `fit` — product-thread fit score and reasoning
- `draft_preview` — draft being generated
- `qa` — quality score and verdict
- `done` — final draft with all metadata

Response includes:
- `draft` — the reply text, ready to copy/paste
- `mode` — which mode was used (product_drop or value_first)
- `fit_score` — product-thread fit (1-10)
- `fit_details` — thread intent and reasoning
- `qa` — quality metrics (composite score, verdict, attempts, dimensions)

### 3. Check Usage

**`GET /usage`**

Returns current usage stats for your API key.

```json
{
  "tier": "free",
  "discovers_today": 3,
  "drafts_today": 2,
  "limits": {"discovers_per_day": 10, "drafts_per_day": 5}
}
```

### 4. Fetch Thread

**`POST /thread/fetch`**

Fetch full thread data from a Reddit URL.

```json
{"url": "https://reddit.com/r/saas/comments/abc123/..."}
```

### 5. Analyze Thread

**`POST /thread/analyze`**

Fetch and analyze a thread for opportunity scoring without running the full discover pipeline.

```json
{
  "url": "https://reddit.com/r/saas/comments/abc123/...",
  "product": {"name": "RealtyDesk", "url": "https://realtydesk.com", "description": "CRM for agents"}
}
```

## Workflows

### Full Pipeline (Recommended)

When the user says something like "find Reddit threads for my product" or "help me get organic traffic from Reddit":

1. Ask what their product is (URL or description)
2. Call `POST /discover/stream` with the product info
3. Present the top threads, sorted by opportunity score
4. For the best threads, offer to draft replies
5. Call `POST /draft/stream` for each thread the user wants to reply to
6. Show the draft and offer to copy it
7. Remind them to open the thread link and paste the reply

### Quick Draft

When the user provides a specific Reddit thread URL and wants a reply:

1. Call `POST /draft/stream` with the thread URL and product info
2. Show the draft, fit score, and QA score
3. If QA score is low, mention the user may want to edit before posting

### Keyword Research Only

When the user just wants to find threads without drafting:

1. Call `POST /discover` with the keyword or product
2. Present results grouped by Google-ranked vs fresh Reddit threads
3. Highlight the top 3-5 by opportunity score

## Important Rules

- Never auto-post to Reddit. Always show the draft and let the user decide.
- When presenting threads, always show: title, subreddit, opportunity score, age, and comment count.
- When presenting drafts, always show: the draft text, mode used, fit score, and QA score.
- If the user's product is vague, ask for more detail before calling discover.
- Remind users that Reddit values authentic contributions. The best replies add genuine value to the conversation.
- Free tier: 10 discovers/day, 5 drafts/day. If they hit limits, suggest upgrading at https://clawagents.dev/redditrank

## Error Handling

If the API returns an error:
- `RATE_LIMIT_EXCEEDED` — user hit their daily limit. Tell them and suggest upgrading.
- `INVALID_API_KEY` — key is bad. Tell them to run `bash setup.sh` again.
- Network/timeout errors — retry once, then tell the user the API may be temporarily down.

## Example Interaction

**User:** Find Reddit threads where I can promote my budgeting app

**Agent:** Let me search for Reddit threads ranking on Google for budgeting apps.

*Calls POST /discover/stream with product_description: "Personal budgeting app that connects to bank accounts and tracks spending automatically"*

Found 12 threads:

**Google-Ranked (appearing on Google Page 1):**
1. "Best budgeting apps 2026?" in r/personalfinance (opp: 8.5/10, 47 comments, Google #3)
2. "Mint alternative recommendations" in r/FinancialPlanning (opp: 7.2/10, 23 comments, Google #7)

**Fresh Reddit Threads:**
3. "Just started budgeting, what app do you use?" in r/budgeting (opp: 9.1/10, 12 comments, 2 days old)

Want me to draft a reply for any of these?

**User:** Draft a reply for thread 3

*Calls POST /draft/stream with thread URL and product info*

**Draft** (value_first mode, fit: 8/10, QA: 7.5/10):

> Congrats on starting. The hardest part is just deciding to do it. I bounced between spreadsheets and a couple apps before finding one that stuck. The thing that made the difference for me was automatic bank syncing. Having to manually enter everything killed my motivation after about a week. Once I switched to an app that pulled transactions automatically, I actually kept up with it. Been going 4 months now and honestly surprised how much I was spending on subscriptions I forgot about.

[Copy Draft] [Open Thread]
