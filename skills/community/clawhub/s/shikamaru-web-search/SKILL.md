---
name: web-search
description: "Search the public web through Exa's hosted MCP endpoint without an API key. Use this whenever the user needs discovery rather than direct retrieval: finding relevant documentation, recent announcements, product pages, blog posts, comparisons, or current external context. Prefer this skill when the user does not already have a specific URL, or when you should first identify the best sources before using web-fetch on one of them."
compatibility: opencode
metadata:
  transport: exa-mcp
  runtime: node
---

# Web Search

Use this skill for web discovery.

Typical cases:
- the user wants recent facts, news, releases, or announcements
- you need to find the right docs page, blog post, repo, or product page
- you need multiple external sources before summarizing or comparing them
- the user asks vague things like “find the official docs”, “look up current pricing”, or “see what changed recently”

If the user already gave an exact URL and wants its contents, use `web-fetch` instead.

## Command

Run:

```bash
node ./search.mjs --query "<query>"
```

Optional flags:
- `--numResults <n>`
- `--type auto|fast|deep`
- `--livecrawl fallback|preferred`
- `--contextMaxCharacters <n>`

Example:

```bash
node ./search.mjs \
  --query "Anthropic Model Context Protocol latest announcements" \
  --numResults 5 \
  --type fast
```

## How to form good queries

Turn the user's request into a focused search query before running the tool.

Prefer queries that include:
- the exact product, company, library, framework, or topic name
- the aspect you need, such as pricing, release notes, docs, migration guide, API reference, benchmark, or comparison
- time qualifiers when relevant, like `2026`, `latest`, `recent`, or a version number
- source hints when useful, such as `site:docs.example.com` or `site:github.com`

When needed, do multiple narrower searches instead of one broad search.

Examples:
- `next.js app router caching docs site:nextjs.org`
- `openai responses api pricing 2026`
- `cloudflare workers durable objects migration guide`
- `site:github.com vercel ai sdk tool calling examples`

## Search strategy

1. Start with a tight query.
2. Review the returned sources and snippets.
3. If results are weak, refine the query rather than repeating the same one.
4. If you identify a promising URL that needs close inspection, follow up with `web-fetch`.
5. For comparisons or research summaries, prefer gathering a few solid sources over many noisy ones.

## Choosing options

Use the defaults unless the task clearly calls for something else.

- `--type auto`: good default
- `--type fast`: use for quick fact-finding and straightforward discovery
- `--type deep`: use for harder research tasks where recall matters more than speed
- `--numResults`: lower it for narrow queries, increase it when surveying a space
- `--contextMaxCharacters`: increase only when you truly need more returned context
- `--livecrawl preferred`: use when freshness matters and you want more live data

## How to handle output

The CLI returns raw search context from Exa.

After searching:
- summarize the findings instead of dumping the raw output unless the user asks for it
- cite or mention the most relevant sources clearly
- call out uncertainty, stale-looking results, or conflicts between sources
- if the user asked a precise question and the search output is still ambiguous, fetch one or two authoritative pages and inspect them with `web-fetch`

## Failure handling

If the search fails or returns weak results:
- tighten or reframe the query
- reduce scope to a specific vendor, site, product, or timeframe
- split a compound question into separate searches
- tell the user plainly if the source quality is weak or current information is hard to verify

## Notes

- No API key is required.
- The endpoint mirrors opencode's Exa-backed search flow.
- This skill is for discovery first; pair it with `web-fetch` for detailed page retrieval.
