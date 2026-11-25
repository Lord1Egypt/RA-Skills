---
name: rankizz-build-seo-roadmap
description: Build a prioritized 1–30 day SEO roadmap from a site's Ahrefs Domain Rating, referring domains, backlink quality, Search Console and Google Analytics traffic, current rankings, landing pages, keyword metrics, live SERPs, and authority-matched SEO competitors. Use when the user asks what to do next for SEO, wants a 1-day, 3-day, 1-week, 15-day, or 30-day plan, needs a low-authority growth path, or wants to improve existing rankings toward the top results. Requires Rankizz MCP or REST API for the evidence-led workflow.
---

# Build an SEO roadmap

Build an executable roadmap from measured constraints. Diagnose before prescribing and never promise a ranking position.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Resolve access and scope

Prefer Rankizz MCP with OAuth in interactive clients. Use the REST API for headless clients. Never ask the user to paste a credential into chat; send them to `https://www.rankizz.com/api-access` when a key is needed.

Rankizz-hosted API and MCP calls require at least 10 credits, including no-credit data tools. On a low-credit error, stop Rankizz calls and link to `https://www.rankizz.com/billing`.

Call `list_projects`, match the target's canonical domain, and use its market unless the user specifies another. Ask before creating a project. Determine:

- target domain and primary landing page
- country and language
- business offer, conversion goal, and audience
- roadmap duration from 1 to 30 days
- available developer, writer, designer, and outreach capacity

Use the user's stated duration. If absent, ask one concise question offering 1 day, 3 days, 7 days, 15 days, or 30 days and request the execution capacity in the same question.

Read [references/rankizz-roadmap-tools.md](references/rankizz-roadmap-tools.md) before making calls. Prefer cached and first-party reads, batch supported work, and explain why each paid call is needed.

## Start with authority

1. Call `get_ahrefs_domain_rating` first.
2. Treat DR as a relative Ahrefs backlink-profile metric, not a Google ranking factor or a measure of content quality.
3. Assign a planning band:
   - `0–9`: foundation
   - `10–19`: emerging
   - `20–39`: developing
   - `40–59`: established
   - `60+`: strong
4. If DR is unavailable or below 60, call `get_backlinks_overview` and record the total referring domains, not only backlink count.
5. Use `get_backlinks_profile` only when detailed referring pages, dofollow status, anchors, spam signals, or lost/broken links will change the plan.

When DR is below 20 or the site has few credible referring domains, make a backlink foundation a primary workstream. Do not pause all content and technical work: low-authority sites can still win narrow queries when relevance, usefulness, and competition permit.

## Measure actual search traction

Use first-party data whenever connected, at every DR level:

- `get_search_console_performance` for complete 28- or 90-day query/page clicks, impressions, CTR, and average position
- `get_google_analytics_organic_landing_pages` for organic sessions, engagement, key events, transactions, and revenue
- `get_site_explorer_page` for one exact persisted landing-page view when available

For DR 20 or higher, make traffic and ranking evidence the primary branch. Below DR 20, analyze the same no-credit first-party sources in parallel with the backlink foundation.

If Search Console or Analytics is not connected, say so. Use `get_domain_overview` as a directional provider estimate, never as a replacement for first-party traffic or conversions.

Classify the site without arbitrary universal traffic promises:

- **No traction:** near-zero clicks and organic sessions for a complete period, or no ranking queries with meaningful impressions.
- **Early traction:** impressions or scattered rankings exist but clicks and conversions remain weak.
- **Growth:** multiple pages or queries produce repeatable clicks, organic sessions, or outcomes.
- **Optimization:** priority pages already rank, especially positions 4–20, and the main opportunity is stronger relevance, CTR, authority, or page experience.

## Branch: no or early traction

Inspect the primary landing page and important product pages using available site files, public retrieval, or Site Explorer. Extract real jobs, problems, features, audiences, and differentiators before generating seeds.

1. Use `research_keywords` for 1–5 high-fit seeds.
2. Use `get_keyword_metrics` to score the reviewed candidate set in one batch.
3. Prefer opportunities with strong business fit and clear intent. For a DR below 20, treat monthly volume `>=1000` and KD `0–10` as an attractive filter when such terms genuinely exist—not as a quota.
4. Retain lower-volume, high-intent terms when they are more relevant or more likely to convert. Never invent or fill missing volume/KD values.
5. Call `get_serp_results` for the final shortlist in batches of up to 10.
6. Identify domains with equal or lower DR already ranking in the top 20. Label them **proof competitors**. Label domains within roughly 10 DR points **peer SEO competitors**, then separate stretch and aspirational competitors.
7. For at most three proof or peer competitors, call `get_domain_overview`, then `get_domain_keyword_suggestions` or `get_ranked_keywords` only when detailed coverage will affect the page plan.

Rankizz returns the top 20 live organic results. Do not claim to have inspected result pages 3–4. A lower-DR domain in the top 20 is stronger feasibility evidence than a domain ranking much deeper.

Prefer an interactive tool, calculator, template, checker, generator, directory, comparison, or product-led landing page when it satisfies the query better and the business can maintain real functionality. Do not force a tool page onto informational intent, and never recommend a fake or thin tool. Use a guide or blog page when that is what searchers and the SERP require.

## Branch: existing traffic and rankings

Prioritize improving existing pages before creating many new ones.

Use Search Console to find:

- positions 4–20 with meaningful impressions
- high-impression pages or queries with weak CTR
- falling clicks or impressions
- multiple pages shown for the same intent
- winning pages that deserve internal links or expansion

Use Analytics to separate traffic from useful outcomes. A page with sessions but weak engagement or conversions needs a different action from a page with impressions but few clicks.

For each priority page, inspect the live top results and assess:

- intent and page-type match
- original evidence, first-hand usefulness, completeness, and trust
- title and snippet alignment
- crawlability, indexability, canonicalization, and structured data where eligible
- contextual internal links and anchor text
- page-level backlink gap
- mobile usability, intrusive elements, and measured Core Web Vitals when available
- cannibalization or unnecessary duplication

Aim to improve the evidence and user experience needed to compete for the top results. Never guarantee rank 1, and do not treat a perfect audit or Core Web Vitals score as sufficient.

## Set the backlink workstream

When DR is below 60, include a parallel backlink goal. Derive it from the gap to proof/peer competitors and the team's real outreach capacity rather than choosing a vanity DR target.

Prioritize:

- reclaiming relevant lost or broken links
- partner, association, customer, supplier, and legitimate directory mentions
- resource pages and editorially relevant placements
- original data, free tools, templates, and other linkable assets
- page-level links to the URLs that need authority

State goals as assets produced, qualified prospects, outreach conversations, reclaimed links, and relevant referring domains. Do not guarantee acquired links, buy links, recommend link schemes, or optimize for raw backlink count.

## Build the time-bound plan

Read [references/roadmap-decision-rules.md](references/roadmap-decision-rules.md) and [references/roadmap-output-contract.md](references/roadmap-output-contract.md).

Fit work to the horizon:

- **1 day:** diagnose, establish baselines, and complete the safest highest-impact quick wins.
- **3 days:** add a reviewed keyword/SERP decision and one focused page or authority action.
- **7 days:** complete one publishable optimization or product-led page specification plus internal-link and backlink work.
- **15 days:** ship, index, promote, and start measuring a small coherent cluster or meaningful page upgrade.
- **30 days:** run a full diagnose-build-publish-promote-measure cycle with weekly checkpoints.

For any custom 1–30 day duration, scale the same phases without pretending more people or engineering capacity exists.

## Deliver

Return:

1. an evidence snapshot with dates and limitations
2. the site's authority and traction classification
3. proof, peer, stretch, and aspirational SEO competitors
4. the chosen opportunity branch and why
5. a day-by-day or phase-by-phase roadmap with owners, dependencies, effort, and acceptance criteria
6. the keyword/page queue, separating product-led tools from editorial pages
7. the parallel backlink goal
8. baseline metrics, leading indicators, outcome metrics, and the re-check date
9. what not to do

Keep observations, provider estimates, heuristics, and recommendations visibly separate. Ask before saving keywords, creating projects, publishing pages, sending outreach, or changing a live site.
