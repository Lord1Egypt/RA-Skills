---
name: seomatic-cannibalization
description: 'Find keyword cannibalization on the connected site: queries where two or more of its own pages compete in Google, from real Search Console data, decide which page should win, and stage the consolidation, retarget or redirect for approval. Use when the user asks about cannibalization, duplicate content, pages competing, or rankings that flip between URLs. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Free tier covers every read in this skill.'
tools:
  - gsc_insights
  - gsc_performance
  - site_pages
  - task_manage
---

# Keyword cannibalization

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

Two pages splitting one query usually means neither ranks as well as one
would. But most "cannibalization" reports are noise: a homepage and a product
page both showing for the brand name is normal. This skill finds the cases
that actually cost clicks.

## Prerequisite

Search Console must be connected. If a tool reports it is not, give the user
this link and stop: https://app.seomatic.ai/connect/gsc - it is one browser
step, then re-ask. Do not substitute guesses for GSC data.

## 1. Pull the real conflicts

`gsc_insights` action `cannibalization` (28 days, `minImpressions` 50).
It returns queries where several of the site's pages earn impressions. Then
`gsc_performance` action `query_pages` on the top candidates to see each
page's own clicks, impressions and position for that query.

## 2. Keep only the ones that cost something

A conflict matters when:

- Two pages both sit in positions 5-30 for the query, and neither is
  clearly winning, or
- The ranking URL flips between pages week to week (`gsc_performance` action
  `dimension_breakdown` with `dimension` date and `filterQuery`), or
- The page Google prefers is the wrong one (a blog post outranking the money
  page for a buying query).

Drop brand queries and cases where one page has over 80% of the clicks. Those
are already resolved.

## 3. Pick the winner and the fix

`site_pages` action `crawl` both pages. Then choose one of four fixes:

| Situation | Fix | Task type |
| --- | --- | --- |
| Same intent, one page clearly stronger | Merge the weaker into the stronger | `consolidate` |
| Different intents, wrong page ranking | Retarget the weaker away from the query | `cannib_retarget` (needs `queries`) |
| Weaker page has no value of its own | 301 it to the winner | `redirect` |
| Both deserve to exist | Clarify with internal links pointing at the winner | `internal_links` |

`redirect` removes a URL from the index. It needs the user's explicit
sign-off on that specific URL, and `task_manage` action `decide` requires
`confirmDestructive: true` for it. Never set that on your own judgment.

## 4. Present it

For each conflict: the query, both pages with their own numbers, which page
should win and why, and the fix. Five real conflicts beat fifty rows.

## Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead so the user can pass it on.

Check `task_manage` action `list` first so you do not stage a duplicate.
Then `task_manage` action `create` with up to 5 tasks: `consolidate`, `cannib_retarget` (with `queries`), `redirect`, or `internal_links` as chosen above. Each task
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

- Do not redirect anything without the user naming that URL and agreeing.
- Do not report brand-query overlap as a problem.
- Do not pick the winner by URL shape. Pick it by intent and its own numbers.
