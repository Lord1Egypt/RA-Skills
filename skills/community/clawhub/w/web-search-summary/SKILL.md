---
name: web-search-summary
description: Search the web for a topic and produce a structured summary with key findings, sources, and actionable takeaways. Best for quick research briefs, competitive landscape scans, and topic overviews.
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: []
---

# Web Search Summary

Produce a structured research brief from a web search query in a single pass.

## When to Use

- User asks for a summary of a topic found via web search
- Need a quick research brief with cited sources
- Competitive landscape, market scan, or technology overview
- Any "what's the latest on X" or "summarize what's happening with Y"

## When NOT to Use

- Deep-dive research requiring multiple follow-up searches → use iterative search instead
- Real-time monitoring → use cron + search instead
- The user already provided the content → summarize directly, skip search

## Steps

1. **Search** — Call `web_search` with the user's query, `count=10`, `freshness` set appropriately.
2. **Fetch** — For the top 3-5 most relevant results, call `web_fetch` with `maxChars=3000` to get readable content.
3. **Synthesize** — Produce a structured summary (see format below).

## Output Format

```markdown
## Summary
<2-3 sentence overview>

## Key Findings
- Finding 1 (with source)
- Finding 2 (with source)
- ...

## Notable
- Point worth flagging
- ...

## Sources
1. <title> — <URL>
2. <title> — <URL>
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| query | yes | — | Search query |
| freshness | no | (none) | `day`, `week`, `month`, `year` |
| count | no | 10 | Number of search results (1-10) |
| maxChars | no | 3000 | Max chars per fetched page |

## Example

**Input:** `"latest in AI coding agents 2026"`

**Output:**
> ## Summary
> The AI coding agent space has matured significantly in 2026, with multi-agent orchestration and IDE-native experiences dominating...
>
> ## Key Findings
> - Multi-agent workflows are now standard (Source: a16z report)
> - IDE-native integration has surpassed CLI-first tools (Source: Stack Overflow survey)
> - ...
>
> ## Sources
> 1. a16z — https://a16z.com/ai-coding-2026
> 2. Stack Overflow — https://stackoverflow.com/survey-2026
