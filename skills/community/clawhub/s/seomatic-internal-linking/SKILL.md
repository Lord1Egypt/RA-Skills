---
name: seomatic-internal-linking
description: 'Plan internal links for the connected site from real data: find pages that rank on page 2 or are not indexed and need link support, find the strong pages that can pass it, and stage specific contextual links with anchors for approval. Use when the user asks about internal linking, orphan pages, link equity, or helping a page rank. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
  - gsc_performance
  - gsc_indexing
  - site_pages
  - site_audit
  - task_manage
---

# Internal linking plan

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

Internal links are the one ranking signal fully in the site owner's hands.
The goal is not "more links": it is links from pages Google already trusts
to pages that are close to ranking, with anchors that say what the target is.

## Prerequisite

Search Console must be connected. If a tool reports it is not, give the user
this link and stop: https://app.seomatic.ai/connect/gsc - it is one browser
step, then re-ask. Do not substitute guesses for GSC data.

## 1. Pick the targets (pages that need help)

- Striking distance: `gsc_performance` action `query_page_matrix`, pages with
  queries in positions 8-20 and real impressions.
- Not indexed: `gsc_indexing` action `batch_inspect` on important pages;
  "discovered" or "crawled - not indexed" often means too few links.
- Money pages the business cares about.

## 2. Pick the sources (pages that can give)

`gsc_performance` action `top_pages`: pages with the most clicks and
impressions are the ones Google crawls and trusts most. A source must be on
the same topic as the target, or the link reads as forced.

## 3. Find the natural spot

`site_pages` action `crawl` on each source. Find the sentence that already
talks about the target's topic. A link there, on words that describe the
target, is worth more than a "related posts" box. If no sentence fits, say
so: a bridging sentence may be needed, and that is a bigger edit.

The `site_audit` tool reports broken internal links across up to 30 pages:
fix those first, they leak what you are trying to pass.

## 4. The plan

| Source page | Sentence / spot | Anchor | Target page | Why |
| --- | --- | --- | --- | --- |

Anchors describe the target ("pricing calculator for agencies"), never
"click here", and vary across sources. Three to five good links to a target
is plenty.

## Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead so the user can pass it on.

Check `task_manage` action `list` first so you do not stage a duplicate.
Then `task_manage` action `create` with up to 5 tasks: `internal_links` on the SOURCE page URL, naming the target and anchor in the rationale; `broken_link_fix` for broken ones. Each task
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

- Do not link from unrelated pages to push a money page.
- Do not use the exact same anchor everywhere.
- Do not add links to navigation or footers as a ranking fix.
