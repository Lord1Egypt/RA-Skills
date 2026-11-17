---
name: seomatic-weekly-brief
description: 'Write a short weekly SEO brief for the connected site from real Search Console data - what changed in the last 7 days, whether a drop is a ranking loss or a SERP-feature or seasonal effect, and the one thing to do this week. Made to run as a Claude or ChatGPT scheduled task every Monday. Use when the user asks for a weekly brief, a weekly SEO update, or "what changed this week". Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Every read in this skill is free and uses no free questions.'
tools:
  - gsc_performance
  - gsc_insights
  - get_started
---

# Weekly SEO brief

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

Every read below is Search Console or site data: FREE, and it uses none of the
free monthly questions.

1. **Compare the weeks**: `gsc_performance` for the last 7 days against the 7
   before (clicks, impressions, the pages and queries that moved most). Use
   the site totals, not a sum of the top rows: a top-N cut invents losses.
2. **Explain any drop before calling it one**: a query that lost clicks at the
   same position is usually a SERP feature or seasonality, not a ranking loss.
   `gsc_insights` separates the two. Never claim which SERP feature took the
   clicks unless a tool shows it.
3. **Pick ONE action**, backed by a number from the data (a striking-distance
   query with its impressions, or a page whose click-through is far below its
   position's norm).
4. **Write it in under 150 words**: what changed, why, the one thing to do. If
   nothing meaningful changed, say so in one line; do not pad.
5. If Search Console is not connected, say so and relay the connect link the
   tool returns. `get_started` gives a site check without it.

## Run it every week

In Claude or ChatGPT, create a scheduled task for Monday morning, with
SEOmatic connected, and use this instruction:

> Using SEOmatic, write my weekly SEO brief in under 150 words: what changed
> in the last 7 days vs the 7 before, whether any drop is a ranking loss or a
> SERP-feature or seasonal effect, and the ONE thing to do this week.
