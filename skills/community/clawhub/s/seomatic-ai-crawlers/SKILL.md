---
name: seomatic-ai-crawlers
description: 'Check which AI bots crawl the connected site (GPTBot, ChatGPT-User, PerplexityBot, ClaudeBot, Google-Extended and more), what they fetch, whether robots.txt blocks them, and how crawls turn into AI citations and assistant referrals. Use when the user asks if ChatGPT or Perplexity can see their site, about AI crawlers, GPTBot, robots.txt for AI, or llms.txt. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Every read in this skill is free.'
tools:
  - get_ai_crawler_activity
  - get_ai_funnel
  - ai_citations
  - site_audit
  - site_pages
  - task_manage
---

# AI crawler check

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

An AI assistant can only cite a page it can fetch. This skill checks which AI
bots reach the site, what they read, and where the chain from crawl to
citation breaks.

## 1. Who visits

`get_ai_crawler_activity`: AI bots that visited, classified by purpose:

- **Answer-time retrieval** (ChatGPT-User, Perplexity-User and similar): a
  real person asked an assistant a question and it fetched your page live.
  This is the one closest to a customer.
- **AI-search indexing** (OAI-SearchBot, PerplexityBot): building the index
  assistants search.
- **Model training** (GPTBot, ClaudeBot, Google-Extended, CCBot): feeding
  future models. Blocking these is a legitimate business choice and does not
  remove the site from AI search.

If there is no crawler data, the site's logs are not connected. Say so and
point to https://app.seomatic.ai/dashboard/integrations.

## 2. Is anything blocked by mistake

`site_pages` action `crawl` on the homepage and a key page, and read
robots.txt. Common mistakes:

- A blanket "block all AI" rule copied from a blog post that also blocks the
  search and retrieval bots, removing the site from ChatGPT search.
- A CDN or firewall bot rule that returns 403 to AI user agents.
- Key content rendered only in JavaScript, which most AI fetchers do not run.

The `site_audit` tool flags noindex leaks and canonical problems that hurt
AI search the same way they hurt Google.

## 3. Crawl to citation

`get_ai_funnel`: per page, cited (engines named it as a source), crawled
(bots fetched it), referred (GA4-measured visits from assistants). Read the
gaps:

- Crawled, never cited: the page is reachable but not the best answer.
- Cited, never crawled recently: the citation is from an old copy.
- Never crawled: check links, sitemap and blocks.

`ai_citations` action `observed_citations` shows the real answers that cited
the site.

## 4. Report

Which bots reach the site and which are blocked (on purpose or not), the top
pages AI reads, and the 3 fixes with the biggest effect.

## Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead so the user can pass it on.

Check `task_manage` action `list` first so you do not stage a duplicate.
Then `task_manage` action `create` with up to 5 tasks: `robots_txt` for a wrong block, `geo_enrichment` for crawled-but-never-cited pages, `technical_fix` for rendering problems. Each task
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

- Do not present llms.txt as required. No major engine has said it
  uses it; it is cheap to add, not a fix.
- Do not recommend blocking or allowing training bots as a ranking tactic.
  It is a licensing choice; present it as one.
