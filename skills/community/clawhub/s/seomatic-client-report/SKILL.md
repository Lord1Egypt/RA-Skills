---
name: seomatic-client-report
description: 'Write a monthly SEO report for a client or a boss from the connected site''s real data: Search Console clicks and positions against the prior period, what was changed and whether it worked, AI search visibility, and next month''s plan, in plain language with every number sourced. Use when the user asks for a client report, monthly SEO report, agency report, or an update for their boss or stakeholders. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
  - gsc_performance
  - gsc_insights
  - traffic_analytics
  - task_manage
  - get_ai_visibility
  - ai_citations
  - strategy_insights
---

# Client SEO report

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

A report a client reads in two minutes and trusts. Outcome first, then the
work, then the plan. Every number comes from a tool, with its date range.

## Prerequisite

Search Console must be connected. If a tool reports it is not, give the user
this link and stop: https://app.seomatic.ai/connect/gsc - it is one browser
step, then re-ask. Do not substitute guesses for GSC data.

If the user manages several sites, the tools are scoped to one workspace at a
time. Confirm which site this report is for before starting.

## 1. The headline numbers

`gsc_performance` action `compare_periods` (the month against the month
before; use 28 days if the user did not name dates). Clicks, impressions,
average CTR, average position. Then `gsc_insights` action `seasonality`: if
the change matches last year's pattern, the report says so. A client who sees
a seasonal dip explained trusts the next good month.

`gsc_insights` action `brand_split`: non-brand clicks are the number SEO
actually moves. Report it separately.

If GA4 is connected, `traffic_analytics` action `overview` and `sources`
for sessions, and `landing_pages` for where organic visitors arrive.

## 2. What we did, and did it work

`task_manage` action `list` with status `verified`, then `ineffective`,
`regressed` and `inconclusive`, and `in_progress` / `verifying` for work
still maturing. For each finished change: what changed, on which page, and
the measured result from the task's evidence. Report the ones that did not
work too. An agency report that only lists wins is not believed.

## 3. AI search

`get_ai_visibility`: brand visibility per engine (ChatGPT, Claude, Google AI
Overviews and any others tracked) against the previous scan. `ai_citations`
action `observed_citations` for real answers that cited the site. Skip the
section if no scan exists; do not fill it with guesses.

## 4. Next month

`strategy_insights` action `strategy` for the ranked big plays, and
`task_manage` action `list` with status `proposed` for work waiting on
approval. Three priorities, each with the reason in one line.

## Format

```
[Site] SEO report, [exact dates]

Summary: [one sentence, the outcome]

Results       This month   Last month   Change
Clicks        ...
Non-brand     ...
Impressions   ...
Avg position  ...

What we changed (N)
- [page]: [change] -> [measured result or "still measuring until <date>"]

AI search
- [engine]: [visibility] ([change])

Next month
1. ...
2. ...
3. ...

Waiting on you: [N] changes to approve at [link]
```

Plain words. No "synergies", no "leveraging", no unexplained acronyms.

## What not to do

- Do not take credit for a change the data does not attribute to the work.
- Do not hide a bad month. Explain it.
- Do not round in the flattering direction.
