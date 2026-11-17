---
name: seomatic-traffic-drop
description: 'Diagnose why organic traffic dropped on the connected site from real Search Console data: separate seasonality from real loss, find which pages and queries lost the clicks, check indexing and competitors, and rank what to fix first. Use when the user says traffic, clicks or rankings fell, or asks what happened to their SEO. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
  - gsc_performance
  - gsc_insights
  - gsc_indexing
  - serp_competitors
  - traffic_analytics
  - site_pages
  - task_manage
---

# Traffic drop diagnosis

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

"Traffic dropped" has five common causes and they need opposite fixes. This
skill finds which one it is, with numbers, before anyone touches a page.
Tools are scoped to the connected site, so never ask for a domain.

## Prerequisite

Search Console must be connected. If a tool reports it is not, give the user
this link and stop: https://app.seomatic.ai/connect/gsc - it is one browser
step, then re-ask. Do not substitute guesses for GSC data.

## 1. Confirm the drop is real

`gsc_insights` action `seasonality` first. It compares 16 months year over
year and says whether this is a real change or the same dip as last year. A
seasonal dip is not a problem to fix, and saying so is the most useful answer
you can give.

Then `gsc_performance` action `compare_periods` (28 days against the 28
before) and action `trend` to find the day it started. A cliff on one day
points at a change (a deploy, a migration, an update). A slow slope points at
competition or content decay.

GSC data lags 2-3 days. If the drop is in the last 48 hours, check
`gsc_performance` action `fresh` and say the numbers are provisional.

## 2. Find where the clicks went

- `gsc_performance` action `folder_rollup`: is it one section of the site or
  everything? Sitewide points at technical or algorithmic causes; one folder
  points at that folder.
- `compare_periods` on pages, then on queries: the 10 biggest losers by
  clicks lost, with position before and after.
- Position steady but clicks down: demand fell, or a SERP feature took the
  click. Check `serp_competitors` action `features` on the top lost queries.
- Position down: someone outranked you, or the page changed.

## 3. Rule out the technical causes

`gsc_indexing` action `batch_inspect` on the top losing URLs. Look for
"crawled - not indexed", a canonical pointing elsewhere, noindex, or a fetch
error. `gsc_insights` action `sitemaps` for sitemap errors. One noindex on a
template can take out a whole section overnight.

`site_pages` action `crawl` on the two biggest losers: did the title, H1 or
body change? A redesign that dropped the copy is a common, fixable cause.

## 4. Check it is not just measurement

If GA4 is connected, `traffic_analytics` action `sources` for the same
window. If organic sessions in GA4 held while GSC clicks fell (or the other
way round), the problem may be tracking, not SEO.

## 5. Give a verdict, then the fixes

Lead with one sentence: which cause, how sure you are, and the evidence.
"Clicks fell 34% from the 3rd. 80% of the loss is the /blog/ folder, and 6 of
its top 10 pages now show 'Crawled - not indexed'." Then the fixes, ranked by
clicks recovered. Say what you could not check.

## Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead so the user can pass it on.

Check `task_manage` action `list` first so you do not stage a duplicate.
Then `task_manage` action `create` with up to 5 tasks: `content_refresh` for decayed pages, `ctr_fix` (needs `queries`) where position held but CTR fell, `index_request` or `technical_fix` for indexing problems. Each task
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

- Do not blame "a Google update" without evidence. Name it only if the drop
  date and the pattern match, and say it is a hypothesis.
- Do not call a seasonal dip a drop.
- Do not invent numbers. Every figure comes from a tool result, with its date
  range quoted exactly.
