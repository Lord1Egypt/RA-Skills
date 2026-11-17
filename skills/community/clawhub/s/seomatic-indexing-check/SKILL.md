---
name: seomatic-indexing-check
description: 'Check whether Google indexes the connected site''s important pages using the real Search Console URL Inspection data: find pages that are not indexed, explain each reason in plain words, check sitemaps, and stage the fixes. Use when the user asks if a page is indexed, why a page is not on Google, or about crawled not indexed, discovered not indexed, canonical or noindex problems. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
  - gsc_indexing
  - gsc_insights
  - gsc_performance
  - site_pages
  - site_audit
  - task_manage
---

# Indexing check

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

A page Google does not index cannot rank, so this is the first thing to rule
out. Use Search Console's own URL Inspection data, not a guess from a crawl.

## Prerequisite

Search Console must be connected. If a tool reports it is not, give the user
this link and stop: https://app.seomatic.ai/connect/gsc - it is one browser
step, then re-ask. Do not substitute guesses for GSC data.

## 1. Choose what to inspect

If the user named URLs, inspect those. Otherwise build the list from what
matters: `site_pages` action `inventory` for the site's real pages, and
`gsc_performance` action `top_pages` for the ones earning clicks. Money pages
and recently published pages first.

## 2. Inspect

`gsc_indexing` action `inspect` for one URL with full diagnostics, or
`batch_inspect` for many. For each page read: coverage state, last crawl,
Google-selected canonical against the declared one, robots and noindex, and
mobile usability where present.

## 3. Translate each status

| Status | What it means | Usual fix |
| --- | --- | --- |
| Crawled - currently not indexed | Google read it and decided it is not worth indexing | Make it more useful or distinct (`content_refresh`), link to it (`internal_links`) |
| Discovered - currently not indexed | Google knows the URL but has not crawled it | Internal links, sitemap, request indexing (`index_request`) |
| Duplicate, Google chose different canonical | Google indexes another URL instead | Fix the canonical (`canonical`) or consolidate |
| Excluded by noindex | The page tells Google not to index it | Remove noindex if unintended (`robots_directives`) |
| Blocked by robots.txt | Google may not crawl it | Fix robots.txt (`robots_txt`) |
| Page with redirect / 404 | Not a real page | Fix the internal links pointing at it (`broken_link_fix`) |

Some exclusions are correct (tag archives, cart pages, staging URLs). Say so.

## 4. Check the sitemaps

`gsc_insights` action `sitemaps`: submitted, errors, and how many URLs are
indexed against submitted. A sitemap full of redirects or noindexed URLs
wastes crawl. If there is no sitemap submitted, `sitemap_submit` fixes it.

For a site-wide view, the `site_audit` tool crawls up to 30 pages and catches
noindex leaks and canonical mismatches across templates.

## 5. Report

One line per page: URL, status in plain words, why, the fix. Then the count:
"14 of 20 key pages indexed; 4 are crawled but not indexed, 2 point their
canonical at the homepage."

## Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead so the user can pass it on.

Check `task_manage` action `list` first so you do not stage a duplicate.
Then `task_manage` action `create` with up to 5 tasks: `index_request`, `canonical`, `robots_directives`, `robots_txt`, `sitemap_submit`, `internal_links` or `content_refresh` as the status calls for. `noindex` and `redirect` are destructive and need `confirmDestructive: true` after the user signs off on that URL. Each task
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

- Do not promise a page will be indexed by a date. Requesting indexing asks
  Google; it does not force it.
- Do not request indexing for a page that is excluded for a good reason.
