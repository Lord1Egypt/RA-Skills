---
name: seomatic-striking-distance
description: 'Find the connected site''s striking-distance queries (page-2 rankings, positions 11-20, where one edit reaches page 1) from real Search Console data, quantify the click upside, and stage the specific fixes for approval. Use when the user wants quick SEO wins, more traffic without new content, or asks what to optimize first. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
  - serp_competitors
  - site_pages
  - backlink_profile
  - task_manage
---

# Striking-distance sprint

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

The cheapest traffic on any site is already ranking. A query sitting at
position 8 has proven the page can rank and proven people search it; the only
missing piece is a push. This skill finds those, sizes them honestly, and
stages the specific fix.

Every read here is FREE and reads the workspace's own Search Console data.
Tools are already scoped to the connected site, so never ask for a domain.

## Prerequisite

Search Console must be connected. If a tool reports it is not, give the user
this link and stop: https://app.seomatic.ai/connect/gsc - it is one browser
step, then re-ask. Do not substitute guesses for GSC data.

## 1. Pull the candidate set

`gsc_performance` action `query_page_matrix`, 28 days. This returns
query-page PAIRS, which is what matters: the same query can be split across
two pages, and a query ranking 9th on the wrong page is a different problem
from one ranking 9th on the right page.

Filter to **positions 11-20** with at least **10 impressions**. These are the
bands SEOmatic itself uses (`STRIKING_MIN_POS`/`MAX_POS`/`MIN_IMPRESSIONS` in
the product), so the skill and the app agree on what "striking distance" means

- a shortlist here matches what the dashboard would show.

- **Positions 11-20 is page 2.** The page has proven it can rank for the
  query; one edit reaches page 1. That is the whole thesis.
- **Positions 1-10 are a DIFFERENT problem** and need a different tool. A
  page-1 result earning less than half its expected CTR is a snippet
  failure, not a ranking one - see step 3.
- **Beyond 20** is not a push, it is a rewrite. Say so rather than selling it
  as a quick win.

Use a HIGH limit (100+). These queries have few clicks by definition, so a
default click-ranked sample systematically misses them.

## 2. Size the upside, honestly

For each pair: `impressions x (expected CTR at target position - current CTR)`.

The expected-CTR figure is where most estimates become fiction. Do NOT use a
published industry CTR curve; use the SITE'S OWN. `gsc_insights` action
`ctr_outliers` gives the empirical curve for this property, which differs
enormously by brand strength, SERP shape and vertical.

State the estimate as a range, and say what it assumes. "Roughly 40-60 more
clicks a month if it reaches position 3" is honest. "+52 clicks" is not.

## 3. Separate the two failure modes

They look identical in the data and need opposite fixes.

- **Ranks fine, loses the click** (positions 1-10, at least 50 impressions,
  CTR under HALF the site's expected curve). The ranking is already won; the
  title and meta are losing the click. `gsc_insights` action `ctr_outliers`
  applies exactly these thresholds and surfaces them directly. Cheapest fix
  in SEO: no new content, no links.
- **Nearly ranks** (positions 11-20, the set from step 1). CTR is roughly
  normal for the position. Content or authority is the constraint, not the
  snippet - rewriting the title here changes nothing.

Before recommending a title rewrite for a low-CTR pair, check
`serp_competitors` action `features` with those queries. If an AI overview
or a featured snippet now sits above the result, CTR collapsed for a reason
the title cannot fix, and the honest recommendation is different: win the
feature, or accept the ceiling. Reporting "low CTR, rewrite the title" here
sends the user at an unwinnable target.

## 4. Read the actual pages

`site_pages` action `crawl` on the top 5 candidate pages. Compare what the
page says against what the query asks. You are looking for a specific,
nameable gap:

- The query asks a question the page never directly answers.
- The title targets a different phrasing than the one ranking.
- The intent is mismatched (a commercial query landing on a blog post).

If the page already covers the query well and still sits at 11, say so. The
constraint is probably authority, not on-page, and `backlink_profile` action
`summary` will tell you whether the site can realistically outrank what is
above it. A push that needs links is not a quick win.

## 5. Present a shortlist, not a dump

Ten ranked opportunities beat a hundred rows. For each:

| Query | Page | Position | Est. monthly clicks | The specific change |
| ----- | ---- | -------- | ------------------- | ------------------- |

The last column is the one that matters. "Optimize the page" is not a
recommendation. "The title targets 'pricing' but the ranking query is 'cost
per user' - lead the title with the query phrasing" is.

## 6. Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead and pass that on.

`task_manage` action `create`, type `ctr_fix` for snippet work or
`striking_distance` for content pushes, passing the target queries. Then:

- Tell the user the cards are staged and where to approve them.
- Approved auto-executable tasks start running within SECONDS, so poll
  `task_manage` action `get` shortly after and report what actually changed.
  The evidence block carries before and after.
- Never approve on the user's behalf, and never claim a result you have not
  read back from the task.

## What not to do

- Do not invent search volumes. Every number comes from GSC or a named tool.
- Do not present the full matrix. The value is the judgment about which ten
  matter.
- Do not promise ranking movement with a date. Say what changed and what you
  will measure.
- Do not call a seasonal dip an opportunity. Check `gsc_performance` action
  `trend` first; a query that dips every year at this time is a cycle.
