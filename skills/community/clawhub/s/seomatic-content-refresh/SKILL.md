---
name: seomatic-content-refresh
description: 'Find decaying content on the connected site, pages that used to earn more Search Console clicks than they do now, work out what each one is missing against today''s results, and stage refreshes for approval. Use when the user asks which posts to update, about content decay, old articles losing traffic, or a content refresh plan. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Search Console and page reads are free; SERP and keyword lookups use the free monthly allowance or AI credits.'
tools:
  - gsc_performance
  - gsc_insights
  - serp_competitors
  - site_pages
  - keyword_research
  - task_manage
---

# Content refresh

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

Refreshing a page that already ranked is usually faster than writing a new
one: it has links, history and proof it can rank. This skill picks the pages
worth it and says exactly what each needs.

## Prerequisite

Search Console must be connected. If a tool reports it is not, give the user
this link and stop: https://app.seomatic.ai/connect/gsc - it is one browser
step, then re-ask. Do not substitute guesses for GSC data.

## 1. Find the decay

`gsc_performance` action `compare_periods` on pages, with a long window
(90 days against the 90 before). Keep pages that lost at least 25% of clicks
AND still have meaningful impressions. A page with no impressions left is a
rewrite or a prune, not a refresh.

`gsc_insights` action `seasonality` to remove pages that dip every year.

## 2. Find what slipped

For each candidate, `gsc_performance` action `dimension_breakdown` with
`dimension` query and `filterPage`: which queries lost position, and which
new queries appeared that the page barely answers.

## 3. Compare with what ranks now

`serp_competitors` action `features` on the page's main queries, and
`site_pages` action `crawl` on the page itself. Look for:

- Out-of-date facts, prices, years, screenshots or steps.
- Sub-questions the ranking query now implies that the page never answers.
- A format mismatch (results now show lists or tools, the page is an essay).
- Thin sections against queries that grew.

`keyword_research` action `metrics` on any new query to size it. Use
`site_pages` action `analyze` for the page's score and critical issues.

## 4. The refresh brief

Per page: what lost (queries, positions, clicks with dates), what to add,
what to update, what to cut, and the expected outcome as a range. Specific:
"Add a section on 2026 pricing; the query 'X pricing' grew to 1,900
impressions and the page never mentions price" is a brief. "Update content"
is not.

Pages with nothing worth saving: say so. `content_prune` exists for them.

## Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead so the user can pass it on.

Check `task_manage` action `list` first so you do not stage a duplicate.
Then `task_manage` action `create` with up to 5 tasks: `content_refresh` per page (pass the decayed queries), `freshness_stamp` where only the date and facts are stale, `content_prune` only with the user's sign-off. Each task
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

- Do not refresh a page whose only problem is seasonality.
- Do not change a page that is still growing.
- Do not invent volumes. Every number comes from a tool result.
