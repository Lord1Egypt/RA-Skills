---
name: web-search-digest
description: Search the web for a topic and produce a structured markdown digest with sources. Use when the user asks to research a topic, summarize recent findings, or collect references on a subject. NOT for: real-time monitoring, paid content, or deep scholarly literature reviews.
---

# Web Search Digest

Given a topic, search the web and return a structured markdown digest.

## Steps

1. **Parse the topic** — Extract the core subject and any filters (time range, language, region).
2. **Search** — Run `web_search` with the topic. Use `freshness` and `language` parameters when specified.
   - If results are insufficient (fewer than 5), broaden the query and retry once.
3. **Fetch & extract** — For the top 3-5 most relevant results, use `web_fetch` to extract readable content.
4. **Synthesize** — Produce a markdown digest with the following structure:

```markdown
# Digest: {topic}

**Generated:** {ISO timestamp}
**Sources consulted:** {count}

## Key Findings
- Bullet list of 3-6 main takeaways

## Detail by Source
### [{title}]({url})
- 2-3 sentence summary
- Relevance: high/medium/low

## Gaps & Open Questions
- What the search did not cover
```

5. **Deliver** — Return the digest as markdown. If the user requested a file, also write it to `digest-{slug}.md` in the workspace.

## Output Contract

- Always include the sources consulted count.
- Never fabricate facts not found in the fetched content.
- Mark uncertain claims with "reported" or "unverified".
