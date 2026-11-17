---
name: seomatic-competitor-gap
description: 'Compare the connected site with its real search competitors: who ranks for the same keywords, the keywords they win that the site does not, their SERP features, and the backlink gap, then turn the gap into ranked opportunities. Use when the user asks about competitors, competitor keywords, content gap, or why a competitor outranks them. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Search Console and page reads are free; SERP, keyword and backlink lookups use the free monthly allowance or AI credits.'
tools:
  - serp_competitors
  - gsc_performance
  - keyword_research
  - backlink_profile
  - site_pages
  - task_manage
---

# Competitor gap

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

"Our competitors" in a founder's head and "who outranks us in Google" are
often different lists. Start from the second one.

## Prerequisite

Search Console must be connected. If a tool reports it is not, give the user
this link and stop: https://app.seomatic.ai/connect/gsc - it is one browser
step, then re-ask. Do not substitute guesses for GSC data.

## 1. Find the real search competitors

`serp_competitors` action `domain_competitors` for the connected site:
domains ranking for the same keywords. Compare with the names the user
gives you. A competitor the user never mentioned that shares half the
keywords is worth pointing out.

## 2. Size them

`serp_competitors` action `domain_overview` for the site and the top 3
competitors: organic visibility, keyword distribution by position. One table,
so the user sees the gap at a glance.

## 3. The keyword gap

`serp_competitors` action `domain_rankings` for each competitor. Keep
keywords where the competitor is in the top 10 and the site is absent or past
20. Cross-check with `gsc_performance` action `query_pages`: the site may
rank for a phrasing the tool did not catch.

Group the gap by intent and topic, not as a keyword list. Then
`keyword_research` action `metrics` on the most promising groups for
volume, difficulty and intent.

## 4. Why they win

For the top 3-5 gap topics, `serp_competitors` action `features` and
`site_pages` action `crawl` on the competitor's ranking page. Is it a page
type the site does not have (a tool, a comparison, a template)? More depth?
Then `backlink_profile` action `summary` for both domains: if the gap is
authority, content alone will not close it, and `backlink_profile` action
`link_prospects` (with the competitors) lists sites linking to them but
not to you.

## 5. Ranked opportunities

| Topic | Competitor ranking | Their page type | Site today | Effort | Why |
| --- | --- | --- | --- | --- | --- |

Rank by (demand x fit with the business) / effort. Topics the site cannot
credibly own come last, or out.

## Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead so the user can pass it on.

Check `task_manage` action `list` first so you do not stage a duplicate.
Then `task_manage` action `create` with up to 5 tasks: `content_create` for a missing page (targetKey is the topic), `striking_distance` (with `queries`) where the site already ranks 11-20, `link_building` for the authority gap. Each task
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

- Do not copy a competitor's page. Match the intent, beat the substance.
- Do not report a gap in keywords the business does not sell.
