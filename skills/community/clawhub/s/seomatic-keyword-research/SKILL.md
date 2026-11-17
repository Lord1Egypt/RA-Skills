---
name: seomatic-keyword-research
description: 'Do keyword research grounded in the connected site: start from the queries it already earns in Search Console, expand with real volume, difficulty, intent and trends data, cluster by intent, and pick which keywords map to which page. Use when the user asks for keyword research, keyword ideas, what to write about, search volume, or a keyword strategy. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Search Console and trends reads are free; volume, difficulty and SERP lookups use the free monthly allowance or AI credits.'
tools:
  - gsc_performance
  - keyword_research
  - keyword_clusters
  - serp_competitors
  - site_pages
  - get_target_terms
  - task_manage
---

# Keyword research

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

Generic keyword research starts from a seed and ends with a spreadsheet of
terms the site has no chance at. This skill starts from what Google already
thinks the site is about, and ends with keywords mapped to pages.

## 1. Start from evidence

- `get_target_terms`: the searches the business has said bring it customers,
  each with the page that should show. If they exist, they are the anchor.
- `gsc_performance` action `top_queries` (90 days, high limit): what the
  site already shows for, including queries with impressions but no clicks.
  Those are the cheapest keywords on the list.
- `keyword_clusters` action `list`: clusters SEOmatic has already built for
  this site.

If Search Console is not connected, say the research will be weaker and ask
for 3-5 seed terms and the business's main offer.

## 2. Expand

`keyword_research` action `suggestions` from the strongest 3-5 seeds, then
`metrics` on the shortlist: volume, difficulty, CPC, intent. `trend`,
`compare_trends` and `related` (free, Google Trends) for direction: a
keyword halving year on year is a bad bet.

## 3. Check the SERP before committing

`serp_competitors` action `features` on the top candidates. A keyword
whose results are all marketplaces, or answered fully in an AI overview, is
worth less than its volume says. CPC is a better guide to commercial value
than volume.

## 4. Cluster and map

Group by intent: one page per intent, not one page per keyword. Then map
each cluster to a page: an existing one (`site_pages` action `inventory`)
or a new one. Two clusters mapped to the same page, or one cluster spread over
three pages, is a problem to flag.

| Cluster | Main keyword | Volume | Difficulty | Intent | Page (existing / new) |
| --- | --- | --- | --- | --- | --- |

## 5. Recommend an order

1. Keywords the site already shows for at positions 8-20 (fastest).
2. High-intent clusters with an existing page that under-covers them.
3. New pages for clusters the site can credibly own.

## Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead so the user can pass it on.

Check `task_manage` action `list` first so you do not stage a duplicate.
Then `task_manage` action `create` with up to 5 tasks: `striking_distance` (with `queries`) for group 1, `content_refresh` for group 2, `content_create` (targetKey = the topic) for group 3. Each task
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

- Do not present a 500-row keyword list. The value is the selection.
- Do not invent volumes or difficulty. Quote the tool's numbers.
- Do not recommend keywords outside what the business actually sells.
