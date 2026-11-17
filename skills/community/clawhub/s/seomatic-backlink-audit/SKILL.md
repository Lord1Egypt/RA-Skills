---
name: seomatic-backlink-audit
description: 'Audit the connected site''s backlink profile with live data: referring domains, anchor text, link velocity and spam signals, compare with competitors, and find real link prospects (sites linking to competitors but not to you). Use when the user asks about backlinks, link building, domain authority, toxic links, or why competitors outrank them on authority. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Backlink and SERP lookups use the free monthly allowance or AI credits; Search Console reads are free.'
tools:
  - backlink_profile
  - serp_competitors
  - gsc_performance
  - task_manage
---

# Backlink audit

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

Links still decide many close rankings. This skill says whether authority is
actually the constraint for this site, and if so, where the next links can
realistically come from.

## 1. The profile

`backlink_profile` action `summary` (defaults to the connected site):
backlinks, referring domains, rank and spam score. Referring domains matter
far more than raw backlink count.

## 2. Quality and shape

- `backlink_profile` action `referring_domains`: the top linking domains.
  Are they real sites in the same space, or directories and scraped pages?
- `backlink_profile` action `anchors`: a natural profile is mostly brand
  and URL anchors. Many exact-match commercial anchors is a risk signal.
- `backlink_profile` action `velocity` (12 months): new against lost
  referring domains per month. A sudden spike of low-quality domains, or a
  steady loss, both need explaining.

## 3. Is authority the constraint?

`serp_competitors` action `domain_competitors`, then `backlink_profile`
action `summary` for the top 3. If the site's on-page work is good, its
queries sit at positions 5-15 (`gsc_performance` action `query_page_matrix`),
and competitors have several times its referring domains, authority is the
constraint. If competitors have a similar profile, it is not, and the money
is better spent on content.

## 4. Prospects

`backlink_profile` action `link_prospects` with the competitor domains:
sites linking to two or more competitors but not to this one. Sort by
relevance, not authority. For each, say why they linked to the competitor
(a resource page, a review, a list, a tool) because that is the pitch.

## 5. Report

1. Verdict: is authority the constraint, with the numbers.
2. Risks, if any (spam spikes, exact-match anchors), and whether they need
   action. Most low-quality links are ignored by Google; disavow is for
   manual actions and clear link schemes, not routine cleanup.
3. Top 10 prospects with the angle for each.

## Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead so the user can pass it on.

Check `task_manage` action `list` first so you do not stage a duplicate.
Then `task_manage` action `create` with up to 5 tasks: `link_building` with the prospect list and angles in the rationale. Each task
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

- Do not recommend buying links or link exchanges.
- Do not call every low-authority link "toxic".
- Do not quote a third-party authority score as if Google used it.
