---
name: seomatic-local-seo
description: 'Review local SEO for the connected business: Google Business Profile calls, reviews and profile gaps, daily Rank Tracker positions (Google Maps top 3, page one, AI Overviews) for the searches that matter, local queries in Search Console, LocalBusiness schema and location pages, then stage the fixes. Use when the user runs a local business, asks about Google Maps, the local pack, reviews, Google Business Profile or city pages. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Business Profile, Rank Tracker and Search Console reads are free; tracking searches, a city grid and drafted replies or updates use AI credits, quoted first.'
tools:
  - business_profile
  - business_profile_manage
  - rank_tracking_read
  - rank_tracking
  - local_presence
  - gsc_performance
  - site_pages
  - keyword_research
  - campaign_manage
  - task_manage
---

# Local SEO review

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

For a local business, the map pack and the Business Profile often bring more
customers than the website's organic rankings. This skill checks both, from
the business's own connected data.

## Prerequisites

- Google Business Profile: `business_profile` action `overview`. If it says
  the profile is not connected, send the user to
  https://app.seomatic.ai/dashboard/settings?tab=integrations and stop that
  part. If it says access is pending, Google has not opened Business Profile
  access yet: approved changes are held and go live the day it opens.
- Search Console for the website half: https://app.seomatic.ai/connect/gsc.

## 1. The profile

`business_profile` action `overview` (per location when there are several):
calls, direction requests, website clicks and times shown over 30 days,
category advice, Ask Maps readiness, the Google Maps top 3 next to you, and
any possible duplicate listing. Then `business_profile` action `reviews`:
average rating, count, and the reviews waiting for a reply (each already has a
drafted reply). Under about 4.2 stars, or a fraction of the competitors'
review count, is usually the first constraint, and it is fixed off-site
(asking every customer: `business_profile` action `review_link`), not on the
website. Say so plainly. `business_profile` action `updates` gives profile
completeness (hours, holiday hours, service areas, services) and this week's
update.

## 2. Local positions

Rank Tracker first: `rank_tracking_read` action `tracked` returns every
tracked search with today's place per city and device, the Google Maps top 3,
page one, AI Overviews, who ranks above, and what moved this week with its
cause. Nothing tracked yet: `rank_tracking_read` action `suggest`, then offer
`rank_tracking` action `track` with the 3-5 searches that bring customers
("plumber near me" is not useful; "emergency plumber Lyon" is). `track`
without `confirm: true` returns the monthly credits: tell the user the number
and only call again with `confirm: true` after they agree. For a one-off
check without tracking, `local_presence` action `visibility` still works
(billed per check).

## 3. Local queries on the website

`gsc_performance` action `top_queries` and `dimension_breakdown` with
`dimension` country or page. Which service + city queries does the site
already earn impressions for, and on which page? A city query landing on the
homepage means a location page is missing.

## 4. The website signals

`site_pages` action `crawl` on the homepage and contact page:

- Name, address and phone written the same way as on the profile.
- LocalBusiness structured data present and matching (`local_schema` builds
  it from the profile itself, no invented ratings).
- A page per real service area or location, with something specific to say
  about it. Doorway pages with only the city name swapped hurt.

## 5. Report

Lead with the single biggest constraint (usually reviews, a missing location
page, or inconsistent NAP), then the rest ranked.

## Offer to stage the work

Staging needs a paid SEOmatic plan (the key carries the `agents:act` scope).
It costs no credits, runs nothing, and always waits for the user's approval.
On a free key the staging actions are locked and say which plan includes
them: describe the specific fix instead so the user can pass it on.

Profile fixes are staged with `business_profile_manage`: `propose_edit` for
hours, holiday hours, services, service areas or the description (the
business name, address and primary category need `confirm: true` and the
user's explicit yes, one at a time), `draft_update` for this week's update
from one line about a recent job, `redraft_reply` for a review reply in a
different tone. Each comes back as an approval card; nothing is published
until the user approves it.

Check `task_manage` action `list` first so you do not stage a duplicate.
Then `task_manage` action `create` with up to 5 tasks: `local_schema` for LocalBusiness markup, `content_create` for a missing service page. For location pages, use `campaign_manage` action `propose_location_pages` (drafts on the site's own layout) instead of single tasks. Each task
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

- Do not suggest fake reviews, review gating, rewards for reviews, or
  keyword-stuffing the business name on the profile. They break Google's
  policy and get profiles suspended.
- Do not create city pages for places the business does not serve.
