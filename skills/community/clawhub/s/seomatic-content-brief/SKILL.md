---
name: seomatic-content-brief
description: 'Write a content brief for one target keyword grounded in real data: search intent, what the current top results cover, SERP features, the queries the connected site already shows for, and the internal links to add, then score the finished draft before publishing. Use when the user asks for a content brief, an article outline, what to include in a post, or to check a draft before it goes live. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
version: 1.0.0
license: MIT
homepage: https://app.seomatic.ai
metadata:
  paperclip:
    requirements:
      env: []
      binaries: []
      mcp: [seomatic]
  openclaw:
    requires:
      mcp: [seomatic]
  hermes:
    requires_mcp_servers: [seomatic]
mcp:
  servers:
    seomatic:
      url: https://app.seomatic.ai/api/mcp
      transport: streamable-http
      auth: oauth
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Search Console reads and draft scoring are free; keyword and SERP lookups use the free monthly allowance or AI credits.'
tools:
  - keyword_research
  - serp_competitors
  - gsc_performance
  - site_pages
  - task_manage
  - generate_article
---

# Content brief

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

A brief is the difference between an article that ranks and one that only
exists. This one is built from the live results and the site's own data, so a
writer (human or AI) knows exactly what to cover and why.

## 1. The keyword

`keyword_research` action `metrics` on the target and 3-5 variants: volume,
difficulty, CPC, intent. `keyword_research` action `related` for the
questions people search around it.

If Search Console is connected, `gsc_performance` action `query_pages` on
the target: if the site already has a page ranking for it, the brief is for a
refresh of that page, not a new one. Two pages on one intent compete.

## 2. The results today

`serp_competitors` action `features`: AI overview, featured snippet, people
also ask, video, local pack. Each changes what the page should include (a
direct 40-60 word answer near the top for a snippet, short sections answering
each "people also ask" question).

`site_pages` action `crawl` on the top 3 ranking pages. Note the format
(guide, list, tool, comparison), the sections they all share (the minimum),
and what none of them cover (the angle).

## 3. The brief

```
Target keyword: ...      Intent: ...      Format: ...
Working title: ...       Meta description: ...

Must cover (the top results all do):
- ...
Angle (none of them do):
- ...
Questions to answer directly:
- ...
Internal links: from [existing page] to this one, and from this one to [page]
Facts to verify before publishing: ...
Length: as long as the answer needs; the top results run [range]
```

Internal link sources come from `site_pages` action `inventory` and
`gsc_performance` action `top_pages` (pages on the same topic with traffic).

## 4. Score the draft

When the user has a draft, `site_pages` action `score_draft` with the text.
It is deterministic and free, and it checks the structure before anything is
published. Fix what it flags, then compare the draft against the "must cover"
list above.

## Turning it into work

On a paid plan, `task_manage` action `create` with type `content_create`
(targetKey = the topic, rationale = the brief) stages it for approval. On any
plan, `generate_article` writes one research-grounded article from the brief
for one prepaid article unit; tell the user the cost before calling it.

## What not to do

- Do not set a word count target. Coverage decides length.
- Do not copy headings from competitors. Cover the intent better.
- Do not invent statistics for the writer to cite.
