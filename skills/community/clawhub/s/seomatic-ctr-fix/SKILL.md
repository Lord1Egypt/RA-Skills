---
name: seomatic-ctr-fix
description: 'Find pages on the connected site that rank on page 1 but lose the click, using the site''s own Search Console CTR curve, check the SERP for features that steal clicks, and stage new titles and meta descriptions for approval. Use when the user asks to improve CTR, rewrite titles or meta descriptions, or get more clicks from rankings they already have. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Search Console and page reads are free; SERP and backlink lookups use the free monthly allowance or AI credits.'
tools:
  - gsc_insights
  - gsc_performance
  - serp_competitors
  - site_pages
  - task_manage
---

# CTR fix: titles and meta descriptions

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

The cheapest clicks in SEO: the page already ranks, it just loses the click to
the result next to it. No new content, no links, one edit.

## Prerequisite

Search Console must be connected. If a tool reports it is not, give the user
this link and stop: https://app.seomatic.ai/connect/gsc - it is one browser
step, then re-ask. Do not substitute guesses for GSC data.

## 1. Find pages under-earning their position

`gsc_insights` action `ctr_outliers` (28 days). It uses the SITE'S OWN CTR
curve, not an industry average, and flags pages in positions 1-10 with at
least 50 impressions earning under half the click rate their position should
earn. Those thresholds are the product's own, so this list matches the
dashboard.

For each candidate, `gsc_performance` action `dimension_breakdown` with
`dimension` query and `filterPage` to get the queries that page actually
shows for. The new title has to answer those, not a guessed keyword.

## 2. Rule out what a title cannot fix

`serp_competitors` action `features` with the page's top queries. If an AI
overview, a featured snippet, a map pack or ads sit above the result, CTR
collapsed for a reason the title cannot change. Say so and move on, or
recommend winning the feature (`faq_block`, `schema`) instead.

## 3. Read the current snippet

`site_pages` action `crawl`: current title, meta description, H1. Common
problems:

- The title leads with the brand, not the query.
- The title targets a different phrasing than the one that ranks.
- The meta description is missing, so Google writes its own.
- The title is truncated (over about 60 characters) and loses the point.
- Nothing in the snippet says why to click this result over the others.

## 4. Propose the rewrite

For each page: current title, proposed title, current meta, proposed meta,
the queries it answers, and the expected gain as a range from the site's own
curve ("roughly 30-50 more clicks a month at the current position"). Keep the
page's real promise. A title that over-promises gets the click and loses the
visitor.

## Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead so the user can pass it on.

Check `task_manage` action `list` first so you do not stage a duplicate.
Then `task_manage` action `create` with up to 5 tasks: `ctr_fix`, which REQUIRES `queries` (the GSC queries the new title is for). Each task
needs `targetKey` (the full page URL, or a topic for content work), a
`title` that states the goal in the user's words ("Get 'pricing calculator'
onto page 1", never "Optimize meta tags"), and a `rationale` with the
numbers behind it. Quote cost from each task's `estimatedCost.label`.

- Tell the user the cards are staged and where to approve them.
- Never approve on the user's behalf. Approval happens in SEOmatic, or
  through `task_manage` action `decide` only after the user says yes to that
  specific task.
- Approved auto-executable tasks start within seconds: read the result back
  with `task_manage` action `get` before you claim anything changed.

## What not to do

- Do not rewrite titles for pages in positions 11+. That is a ranking
  problem, not a snippet problem. Use striking-distance work instead.
- Do not quote an industry CTR curve.
- Do not stuff the query in twice. One clear match beats repetition.
