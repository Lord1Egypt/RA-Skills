---
name: search-bot
description: Real-time web search. Returns current results, titles, URLs, and an AI-synthesized summary.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "🔍"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# Search Bot

Real-time web search powered by Brave Search. Accepts a task or query string and returns current web results with titles, URLs, descriptions, and an AI-synthesized summary of findings. Useful for current events, research, news lookups, and any task requiring up-to-date information.

## When to Use

- Finding current news or recent events on any topic
- Researching products, companies, or public figures
- Looking up documentation, tutorials, or technical references
- Verifying facts with live web results
- Any task where training data cutoff is a limitation

## Usage Flow

1. Provide a `task` string describing what you want to find
2. Optionally set `num_results` (default 8, max 20)
3. AIProx routes to the search-bot agent
4. Returns ranked results plus an AI-written summary with key findings

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | API calls to orchestration endpoint |
| Network | api.search.brave.com | Web search queries (server-side) |
| Env Read | AIPROX_SPEND_TOKEN | Authentication for paid API |

## Make Request

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "latest developments in AI agent frameworks this week",
    "spend_token": "$AIPROX_SPEND_TOKEN"
  }'
```

### Response

```json
{
  "results": [
    {
      "title": "LangGraph 0.3 Released — New Agent Loop Primitives",
      "url": "https://blog.langchain.dev/langgraph-0-3",
      "description": "LangGraph 0.3 introduces native support for multi-agent handoffs...",
      "age": "2 days ago"
    }
  ],
  "summary": "This week saw significant updates to agent orchestration frameworks. LangGraph released version 0.3 with improved multi-agent coordination. OpenAI published new guidelines for tool-using agents. Several new open-source projects emerged targeting autonomous agent deployment.",
  "key_findings": [
    "LangGraph 0.3 adds native multi-agent handoff support",
    "OpenAI published updated agent safety guidelines",
    "Growing ecosystem of autonomous agent deployment tools"
  ],
  "most_relevant_url": "https://blog.langchain.dev/langgraph-0-3",
  "query": "latest developments in AI agent frameworks this week",
  "result_count": 8
}
```

## Trust Statement

Search Bot submits queries to Brave Search on your behalf. Queries are transient and not stored beyond the transaction. Results are summarized by Claude via LightningProx. Your spend token is used for payment only.
