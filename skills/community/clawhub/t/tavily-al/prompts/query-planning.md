# Prompt: Query Planning

## Purpose
Turn a single user question into one or more well-scoped Tavily search queries. The model should decompose multi-part questions, pick effective keywords, and apply time and domain scoping so searches are cheap, precise, and fresh.

## Reusable prompt template
```
You are planning Tavily web searches for the question below.

User question:
{{user_question}}

Context (optional):
- Today's date: {{today}}
- Known authoritative domains: {{authoritative_domains}}
- Freshness requirement: {{freshness_need}}   # none | recent | breaking

Produce a search plan as JSON:
{
  "intent": "<one sentence: what the user actually wants>",
  "sub_questions": ["<atomic question 1>", "<atomic question 2>"],
  "queries": [
    {
      "query": "<concise keyword-focused query, no filler words>",
      "topic": "general | news",
      "time_range": "none | day | week | month | year",
      "include_domains": [],
      "exclude_domains": [],
      "search_depth": "basic | advanced",
      "rationale": "<why this scoping>"
    }
  ]
}

Rules:
- Decompose ONLY if the question has independent parts; otherwise emit one query.
- Use topic="news" + a time_range when {{freshness_need}} is recent/breaking.
- Strip filler words; keep distinctive entities, dates, and qualifiers.
- Use include_domains only when authoritative sources are known.
- Prefer search_depth="basic" unless the topic is niche or contested.
```

## Variables
| Variable | Description |
|----------|-------------|
| `{{user_question}}` | The raw question from the user. |
| `{{today}}` | Current date, for resolving relative time references. |
| `{{authoritative_domains}}` | Optional list of trusted domains to scope to. |
| `{{freshness_need}}` | `none`, `recent`, or `breaking`; controls `topic`/`time_range`. |

## Example use
Fill the template with `user_question = "How does the latest iPhone compare to last year's on battery, and what's the price?"`, `today = 2026-05-31`, `freshness_need = recent`. The model should emit two sub-questions (battery comparison; price) and two scoped queries.

## Bad example
```
query: "tell me everything about the new iphone and the old one and prices and reviews and battery and cameras please"
topic: "general"
time_range: "none"
```
Too broad, filler-laden, no freshness despite a "latest" question, conflates multiple intents into one query.

## Good example
```json
{
  "intent": "Compare current vs prior iPhone on battery life and current price.",
  "sub_questions": ["iPhone 16 vs iPhone 15 battery life", "iPhone 16 current price"],
  "queries": [
    { "query": "iPhone 16 vs iPhone 15 battery life comparison", "topic": "general", "time_range": "year", "include_domains": [], "exclude_domains": [], "search_depth": "advanced", "rationale": "Niche comparison; advanced depth helps." },
    { "query": "iPhone 16 price 2026", "topic": "news", "time_range": "month", "include_domains": ["apple.com"], "exclude_domains": [], "search_depth": "basic", "rationale": "Price changes; recent + official domain." }
  ]
}
```

> Verification needed: confirm the exact accepted `time_range` values and domain-scoping parameter names with https://docs.tavily.com
