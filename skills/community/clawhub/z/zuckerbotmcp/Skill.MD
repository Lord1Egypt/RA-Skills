---
name: zuckerbot
description: >
  Use this skill whenever the user or agent needs to interact with Facebook or Instagram ads via Meta's API.
  Trigger this skill when: the user wants to launch, create, or manage Facebook/Instagram ad campaigns;
  the user asks about ad performance, metrics, or results; the user mentions Meta, Facebook, or Instagram
  advertising in any context; an agent needs ad infrastructure to run a campaign autonomously; the user
  wants to pause, resume, or modify a running campaign; or the user wants to A/B test ad variants.
  Even if the user doesn't say "ZuckerBot" — if ads on Meta are involved, use this skill.
compatibility:
  tools:
    - zuckerbot MCP server (npm: zuckerbot-mcp@0.2.7)
  auth:
    - Facebook OAuth (via zuckerbot.ai developer page)
    - ZuckerBot API key (generated post-OAuth)
---

# ZuckerBot Skill

ZuckerBot gives AI agents the ability to create, launch, monitor, and manage Facebook and Instagram ad campaigns via the Meta Ads API. All tools are available via the ZuckerBot MCP server.

## Authentication

Before any tool can be called, the user must:
1. Connect their Facebook account at **zuckerbot.ai** (OAuth flow)
2. Generate an API key from the developer page
3. Provide the API key — ZuckerBot stores credentials, so this is a one-time step per session

If the user hasn't authenticated yet, prompt them to visit zuckerbot.ai before proceeding.

---

## Tools Reference

### `zuckerbot_preview_campaign`
Generate a campaign preview and strategy from a business URL — before spending anything.

**When to use:** User wants to explore what a campaign might look like, or you need to research the business before creating a campaign.

**Key inputs:**
- `url` — the business or landing page URL
- `api_key` — ZuckerBot API key

**Output:** Campaign strategy, suggested targeting, budget recommendations, ad creative concepts.

---

### `zuckerbot_create_campaign`
Create a full campaign with strategy, targeting, budget, and ad creative recommendations.

**When to use:** User wants to build a campaign ready for launch. Use after `preview` if the user wants to iterate, or directly if they have clear goals.

**Key inputs:**
- `business_url` or business description
- `objective` — one of: `traffic`, `leads`, `conversions`, `awareness` (default: `traffic`)
- `budget_daily` — daily budget in USD
- `api_key`

**Output:** A structured campaign object ready to pass to `launch_campaign`.

---

### `zuckerbot_generate_ad_creative`
Generate AI-powered ad creative images for Facebook/Instagram.

**When to use:** User wants visual assets for their campaign, or when launching a campaign that needs imagery.

**Key inputs:**
- Campaign context / description
- `api_key`

**Output:** Generated image(s) suitable for Meta ad placements.

---

### `zuckerbot_launch_campaign`
Launch a single campaign variant on Meta (Facebook/Instagram).

**When to use:** User has a campaign ready and wants to go live with one variant.

**Key inputs:**
- Campaign object (from `create_campaign` or user-provided)
- `api_key`

**Output:** Campaign ID, live status, confirmation summary.

---

### `zuckerbot_launch_all_variants` (A/B Testing)
Launch multiple ad variants simultaneously for A/B testing.

**When to use:** User wants to test multiple creatives, headlines, or audiences against each other. Preferred over single launch when optimisation is the goal.

**Key inputs:**
- Array of campaign variant objects
- `api_key`

**Output:** Array of campaign IDs and launch confirmations per variant.

---

### `zuckerbot_get_performance`
Fetch real-time performance metrics for a campaign.

**When to use:** User asks how a campaign is performing, wants to see results, or you need data to make optimisation recommendations.

**Key inputs:**
- `campaign_id` — from launch confirmation
- `api_key`
- `date_preset` — defaults to `maximum` (all-time); supports standard Meta date presets

**Output:** Impressions, clicks, CTR, spend, CPM, CPC, conversions (if tracked), ROAS.

---

### `zuckerbot_pause_campaign`
Pause or resume a running campaign.

**When to use:** User wants to stop spending on a campaign temporarily, or resume a paused one.

**Key inputs:**
- `campaign_id`
- `action` — `pause` or `resume`
- `api_key`

**Output:** Updated campaign status confirmation.

---

### `zuckerbot_research_competitors`
Analyse competitor ads for a given business category and location.

**When to use:** User wants to understand the competitive landscape before launching, or wants creative/targeting inspiration.

**Key inputs:**
- Business category
- Location
- `api_key`

**Output:** Competitor ad analysis, positioning insights, creative patterns.

---

### `zuckerbot_research_market`
Get market intelligence for an industry and location.

**When to use:** User wants audience size estimates, market sizing, or industry benchmarks before committing budget.

**Key inputs:**
- Industry / niche
- Location
- `api_key`

**Output:** Market size, audience estimates, benchmark CPMs and CTRs.

---

### `zuckerbot_research_reviews`
Get review intelligence for a business.

**When to use:** User wants to understand customer sentiment, surface proof points for ad copy, or identify pain points competitors are missing.

**Key inputs:**
- Business name or URL
- `api_key`

**Output:** Review themes, sentiment summary, standout quotes usable in ad copy.

---

### `zuckerbot_sync_conversion`
Send conversion feedback to Meta's algorithm to improve targeting.

**When to use:** User has confirmed conversions (purchases, leads, sign-ups) and wants to feed that signal back to Meta for optimisation. Use after campaigns have been running and have conversion data.

**Key inputs:**
- Conversion event data
- `campaign_id`
- `api_key`

**Output:** Confirmation that the conversion signal was sent to Meta.

---

## Recommended Workflows

### Launch a new campaign from scratch
1. `research_market` → understand audience size and benchmarks
2. `research_competitors` → analyse the landscape
3. `preview_campaign` → generate strategy from URL
4. `create_campaign` → build the campaign object
5. `generate_ad_creative` → create visuals
6. `launch_all_variants` → go live with A/B test variants
7. `get_performance` → monitor results

### Quick launch (user has clear brief)
1. `create_campaign` → build campaign
2. `launch_campaign` → go live
3. `get_performance` → check results

### Performance check
1. `get_performance` with `campaign_id`
2. Summarise metrics, flag anything underperforming
3. Recommend `pause_campaign` or budget adjustment if needed

---

## Notes

- **Objective options:** `traffic` (default), `leads`, `conversions`, `awareness`
- **A/B testing:** Always prefer `launch_all_variants` over multiple single launches — it's cleaner and Meta treats the variants as a proper split test
- **Meta pixel:** If the user has a pixel installed (e.g. ID: `1511887479858007`), mention that conversion tracking is available and suggest `sync_conversion` after campaign results come in
- **Credentials:** ZuckerBot uses stored credentials — once the user authenticates, the API key handles all subsequent calls without re-auth
