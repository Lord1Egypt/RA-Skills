---
name: seomatic-local-seo-weekly
description: 'Run a local business''s weekly SEO in one pass - what moved in its tracked searches (daily positions per city, the Google Maps top 3, AI Overviews), reviews waiting for a reply, this week''s Google Business Profile update, and calls from the profile - then stage every fix for approval. Made to run as a Claude, ChatGPT or Cursor scheduled task every Monday. Use when a plumber, clinic, salon, shop or the agency behind them asks "how did my local SEO do this week" or "what do I need to approve". Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Reads are free; tracking searches and drafting replies or updates use credits, quoted first.'
tools:
  - rank_tracking_read
  - rank_tracking
  - business_profile
  - business_profile_manage
  - task_manage
---

# Local SEO weekly

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

One pass, every Monday, for a business that wins customers nearby. Reads are
FREE. Anything that changes the website or the Google Business Profile is
staged as an approval card: nothing goes live until the person approves it.

## 1. Rankings: what moved, and why

`rank_tracking_read` action `tracked`. It returns the one-sentence summary,
every tracked search with today's place, its 7-day change, its place in the
Google Maps top 3, whether an AI Overview names the business, who ranks
above, and `moved_this_week` with the cause and any fix already staged.

- Lead with the summary sentence, then at most three moves, worst first.
- A drop that has a staged fix: say so and give the task id.
- Positions are true places on one results page from one city, checked
  daily. `search_console_average` is Google's own weekly average across
  every city and device; when they differ, both are true. Say which is which.
- Nothing tracked yet: `rank_tracking_read` action `suggest`, then offer
  `track` with the searches the person picks. `track` without
  `confirm: true` returns the monthly credits: tell the person the number
  and only call again with `confirm: true` after they agree.

## 2. Reviews waiting for a reply

`business_profile` action `reviews`. Each new review already has a drafted
reply in the business's voice, waiting as a card. Show the 1 to 3 star ones
first, each with its draft. Never post anything yourself; the person approves
each reply (or several at once) with `task_manage` action `decide_batch`.

## 3. This week's update

`business_profile` action `updates`: profile completeness, the edits
waiting, this week's update if one is drafted, and the updates already
published (Google no longer reports views per update, so do not quote
any). If none is drafted, ask the person for ONE line about a recent job
(and a photo URL if they have one), then `business_profile_manage` action
`draft_update`. Updates keep the profile active; never sell them as a
ranking lever. No phone number in the
text (Google rejects those).

## 4. Calls

`business_profile` action `overview`: calls, direction requests, website
clicks and times shown over 30 days, with the agent's changes marked. Calls
are the number an owner cares about: lead the closing line with them.

## Rules that never bend

- The business name, address and primary category change only when the
  person explicitly asks; a name with a city or a service added gets
  profiles suspended, and SEOmatic refuses it.
- Review requests go to every customer: `business_profile` action
  `review_link`. Never suggest asking only happy customers or offering
  anything for a review (Google policy and the FTC review rule).
- If `business_profile` says the profile is not connected, send the person
  to https://app.seomatic.ai/dashboard/settings?tab=integrations and carry on
  with the rankings.
- If `business_profile` says access is pending, say plainly that Google has
  not opened Business Profile access yet, that approved changes are held and
  go live the day it opens, and carry on with the rankings.

## The brief

Five short lines: the rankings sentence, the worst move and its fix, the
reviews waiting, this week's update, the calls. Then the cards to approve.

## Run it every week

In Claude, ChatGPT or Cursor, create a scheduled task for Monday morning, with
SEOmatic connected, and use this instruction:

> Using SEOmatic, run my local SEO weekly: what moved in my tracked searches
> and why, the reviews waiting for a reply (unhappy ones first, with their
> drafts), this week's Business Profile update, and my calls. List the cards
> I need to approve; do not approve anything yourself.
