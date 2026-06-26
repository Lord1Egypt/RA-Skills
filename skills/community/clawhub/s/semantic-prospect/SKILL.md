---
name: semantic-prospect
version: 1.0.0
description: AI-powered semantic lead prospecting – discovers, qualifies, and enriches high-intent business opportunities from web communities, forums, Reddit, and public discussions. Returns prioritized prospect records with intent scores, context notes, and agent-ready actions. Free tier includes Brave Search and LLM queries — no third-party API keys needed. Lightweight SaaS component from Simply Semantics for sales bots, AI agents, enrichment, and outbound workflows.
tags: ["semantic", "prospecting", "lead-generation", "sales", "enrichment", "ai-agent", "intent-detection", "saas-component", "brave-search", "llm"]
homepage: https://www.simplysemantics.com/semantic-prospect.html
author: Simply Semantics (@simplysemantics)
license: MIT

requires:
  env:
    - name: SIMPLY_SEMANTICS_API_KEY
      required: true
      description: Your Semantic Prospect API key. Generated when you create an account at https://dashboard.simplysemantics.com/sp/. This key authenticates your requests — it is scoped to your account and does not grant access to any other service.

metadata:
  clawbot:
    emoji: "🔍💼"
    requires:
      env: ["SIMPLY_SEMANTICS_API_KEY"]
      primaryEnv: "SIMPLY_SEMANTICS_API_KEY"
    files: []
---

# Semantic Prospect

**Quick summary**  
AI semantically understands context across web sources (Reddit, forums, communities, public discussions) to identify high-intent prospects with real buying signals. It qualifies, scores, enriches, and organizes leads into action-ready records — perfect for sales teams, SaaS companies, consultants, course creators, and especially AI agents/bots that can autonomously nurture and convert.

## Authentication

`SIMPLY_SEMANTICS_API_KEY` is **always required**. This is your personal API key generated when you create an account at https://dashboard.simplysemantics.com/sp/. It authenticates your requests and is scoped to your Semantic Prospect account only — it does not grant access to any other Simply Semantics service or any third-party system.

**What "no configuration required" means:** You do NOT need to supply third-party search API keys (Brave, Perplexity, xAI, etc.) to use the free tier. The platform provides its own search keys for free-tier queries. You only need your `SIMPLY_SEMANTICS_API_KEY` for authentication.

Optionally, you can add your own Brave Search or LLM API keys in the dashboard to bypass free-tier limits.

## Free tier limits

- **Weekly free searches**: 10 per week (shared across Brave Search and LLM when using platform-provided keys)
- **LLM free queries**: 5 total (limited to 3 results per query)
- **Monthly lead quota**: 50 leads
- Add your own Brave or LLM API key via the dashboard to bypass weekly limits and get up to 10 results per LLM query

## Privacy & data handling

- **Data sources**: All leads are discovered from publicly accessible web content only (public forums, Reddit, community boards). No private data, no login-walled content, no PII databases are accessed.
- **Data retention**: Leads are stored in your account for your review and export. They are not shared with other users or third parties.
- **No credential collection**: The platform never reads, collects, or stores your third-party API keys on the server side. If you add your own Brave or LLM key in the dashboard, it is stored encrypted in your account's strategy configuration and used only to make search requests on your behalf.
- **No cross-service data sharing**: Your Semantic Prospect data is isolated to your account. It is not shared with other Simply Semantics services (e.g. Semantic Shield).
- **Compliance**: Users are responsible for ensuring their use of lead data complies with each source community's terms of service. Semantic Prospect only surfaces publicly available information.

## When to use this skill (activation triggers)

Activate **Semantic Prospect** when the user:
- Wants to find qualified leads/opportunities in specific industries, topics, keywords, or communities.
- Asks to "discover prospects", "find high-intent leads", "qualify opportunities", "scan communities for buyers", "build targeted list from Reddit/forums", "identify pain-point discussions".
- Provides targeting criteria (e.g. keywords, industry, location filters) and wants semantic/intent-based results.
- Needs enriched prospect data for outbound, enrichment, or agent handoff.

Do **NOT** use for:
- Generic web search or scraping (use browser tools)
- PII-heavy or non-public data lookup
- Real-time monitoring of private channels
- Non-business/opportunity focused queries (e.g. news, memes)

## How to use (instructions for the agent)

1. **Extract targeting criteria** — Pull from user message:
   - Keywords/topics (e.g. "compliance tools", "Series B fintech")
   - Industries/verticals
   - Communities/sources (Reddit subs, forums, niche boards)
   - Filters (location, engagement level, intent signals)
   - Optional: custom qualification rules or ICP description

2. **Validate** — If missing core criteria (keywords or industry/topic) → ask: "Please specify keywords, industry, or communities to prospect in."

3. **Call the API** — POST to the Semantic Prospect endpoint.

   URL: `https://dashboard.simplysemantics.com/sp/mcp/forum-leads-api`

   Headers:
   ```text
   x-api-key: ${SIMPLY_SEMANTICS_API_KEY}
   Content-Type: application/json
   ```

> ⚠️ **IMPORTANT: Default strategy is `mock` (test data)**
>
> New accounts default to the `mock` strategy, which returns **fake sample leads** for testing purposes only.
> Mock leads contain synthetic data — no real users, URLs, or contact information. They are safe to inspect.
> You **must** explicitly set `"strategy": "brave"` or `"strategy": "llm"` in the request body to get real results.
> The user can also change their default strategy in the dashboard under Search Strategies → "Set as Default",
> but when calling via API, always pass the `strategy` field explicitly.
>
> If the response contains `"is_mock": true` or `"search_strategy": "mock"`, the results are test data — not real leads.

### Example: Mock / Testing (fake sample data — DEFAULT for new accounts)

```json
{
  "niche": "marketing",
  "keywords": ["test"]
}
```

Omitting `"strategy"` uses the user's default, which is `mock` for new accounts. Returns synthetic test leads with `"is_mock": true`. Mock data contains no real personal information — it is safe for testing and integration validation.

### Example: LLM Web Search (real AI-powered results)

```json
{
  "niche": "marketing",
  "nicheLabel": "Digital Marketing Services",
  "keywords": ["SEO help", "Google ranking", "social media manager"],
  "strategy": "llm"
}
```

Free tier: 5 LLM queries (3 results each), counts toward 10 weekly free searches. No third-party API key setup needed — the platform provides its own.

### Example: Brave Search (real web search results)

```json
{
  "niche": "fitness",
  "nicheLabel": "Personal Training & Fitness",
  "keywords": ["need personal trainer", "looking for fitness coach"],
  "strategy": "brave"
}
```

Free tier: counts toward 10 weekly free searches. No third-party API key setup needed — the platform provides its own.

### Request body fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `niche` | string | no | Target niche key (default: `"marketing"`) |
| `nicheLabel` | string | no | Display name for the niche |
| `keywords` | string[] | no | Search keywords |
| `strategy` | string | no | `"llm"`, `"brave"`, or `"mock"`. **Defaults to user's preferred strategy (mock for new accounts).** Always pass explicitly for real results. |

### Output

```json
{
  "leads": [
    {
      "url": "https://www.reddit.com/r/smallbusiness/comments/abc123",
      "poster_username": "auto_shop_owner",
      "intent_summary": "Running an auto repair shop with paper invoices, need affordable shop management software",
      "lead_score": 88,
      "contact_hint": "Comparing tools, budget up to $200/month, ready to buy",
      "source_forum": "reddit.com",
      "is_mock": false,
      "search_strategy": "llm",
      "search_rank": 1,
      "niche": "marketing"
    }
  ],
  "strategy": "llm",
  "free_tier": {
    "maxResults": 3
  }
}
```

Notes on the response:
- `search_strategy` — which engine found the lead: `brave`, `llm`, or `mock`
- `is_mock` — `true` when mock/test strategy was used; these are NOT real leads
- `free_tier` — only present when LLM free tier was used; `maxResults` indicates the cap on results per query
- `search_rank` — position in the raw search results before scoring

4. **Parse & format** — Transform response into clean report for the user.
   - If `is_mock` is `true` on any lead, warn the user that results are test data and they should set `strategy` to `"llm"` or `"brave"` for real leads.
5. **Edge cases**
- 401/403 → "Missing or invalid SIMPLY_SEMANTICS_API_KEY. Set the env var to use this skill."
- 429 → "Rate limit reached (monthly quota, weekly free searches, or LLM free queries exhausted). Retry later, add your own API key, or contact info@simplysemantics.com"
- No results → "No high-intent matches found with current criteria. Try broadening keywords or sources."
- Error → fallback polite message + suggest refining input