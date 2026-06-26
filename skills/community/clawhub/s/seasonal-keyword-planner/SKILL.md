---
name: Seasonal Keyword Planner
description: Map ecommerce keywords to a 12-month demand curve and produce a month-by-month plan for listings, ads, and content timing.
---

# Seasonal Keyword Planner

## Introduction

Knowing *when* shoppers search is as valuable as knowing *what* they search for. Demand for most ecommerce keywords is not flat — it rises and falls on predictable seasonal curves, and the sellers who pre-position before a peak win cheaper clicks and higher organic rankings than those who react after traffic has already arrived. This skill maps each target keyword against a twelve-month demand curve, identifies peaks, shoulder seasons, and troughs, and turns that into a concrete month-by-month action plan for listing optimization, ad budget pacing, and content publishing.

The output separates **evergreen** keywords (steady year-round) from **seasonal spikes** (which require precise timing), and flags **early-mover windows** — the two-to-four weeks before a peak when search interest is climbing but competition is still low. That window is where the leverage is.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Keyword classification | Each term tagged evergreen / seasonal / event-driven | Most tagged | Treated all as flat |
| Timing the prep | Optimize 3–4 weeks before the demand rise | Optimize at the peak | React after the peak |
| Evidence for a peak | Pattern confirmed across multiple years/sources | Single-year trend | Assumption from the calendar alone |
| Ad pacing | Budget shifted toward rising/peak months | Even monthly spend | Heavy spend in troughs |
| Content lead time | Publish 4–6 weeks before peak so it can rank | At peak | After peak |
| Early-mover window | Explicitly identified per seasonal term | Implied | Missed |
| Cannibalization check | Overlapping keywords coordinated | Noted | Competing against self |
| Output usability | Month-by-month, action-per-keyword | Quarterly | Vague "ramp up in Q4" |

## What this skill solves

- **Reacting too late** — optimizing a listing or launching ads after demand has already peaked, paying premium CPCs for traffic everyone else is also chasing.
- **Flat-budget waste** — spreading ad spend evenly across 12 months when demand is concentrated in a few.
- **Missed early-mover windows** — failing to capture the low-competition ramp before a seasonal surge.
- **Content that ranks too late** — publishing gift guides or comparison posts at the peak, when they need 4–6 weeks to climb the SERP.
- **Confusing evergreen with seasonal** — over-investing in steady terms during their (nonexistent) "season," or under-investing in true spikes.
- **Keyword cannibalization** — multiple listings/pages competing for the same seasonal term.
- **No shared calendar** — merchandising, ads, and content teams working off different timelines.

## Workflow

1. **Gather inputs.** Confirm the `keywords` list (5–30 terms) and the `product_category`. Capture the `target_markets` (seasonality differs by hemisphere and country) and any known launch or promo dates.

2. **Classify each keyword.** Tag every term as evergreen, seasonal, or event-driven (tied to a specific retail moment). See `references/seasonality-methodology.md`.

3. **Plot the demand curve.** For each seasonal/event term, identify peak month(s), the rising shoulder, the falling shoulder, and the trough. Base this on multi-year patterns and the retail calendar in `references/ecommerce-seasonal-calendar.md` — and clearly mark where a pattern is assumed vs evidenced.

4. **Find the early-mover window.** For each seasonal term, mark the 2–4 weeks before the rise where prep should happen.

5. **Build the month-by-month plan** using `references/output-template.md`: for each month, what to optimize, where to move ad budget, and what content to publish — keyed to specific keywords.

6. **Coordinate to avoid cannibalization.** Group overlapping keywords so listings and content target distinct intents rather than competing.

7. **Add lead times and a measurement note**, then run `assets/quality-checklist.md`.

## Inputs

- **keywords (required):** 5–30 target keywords or phrases. Example: "fleece jacket, packable down jacket, rain shell, hiking base layer."
- **product_category (required):** The category these keywords sit in, used to anchor the seasonal pattern. Example: "outdoor apparel."
- **target_markets (optional):** Countries/regions; seasonality flips between hemispheres. Defaults to US.
- **known_dates (optional):** Planned launches, restocks, or promotions to align the plan around.
- **channels (optional):** Where the plan applies — Amazon SEO, Google Shopping, TikTok Shop, organic blog. Defaults to all relevant.

## Worked example 1 — Outdoor apparel (US)

**Inputs:** keywords = "packable down jacket, rain shell, hiking base layer, fleece jacket"; category = outdoor apparel; market = US.

**Classification & curve (excerpt):**
- *packable down jacket* — **seasonal**, peaks **Oct–Dec** (cold-weather + gifting). Rising shoulder Sep; trough May–Jul. Early-mover window: **late Aug–early Sep.**
- *rain shell* — **seasonal**, two peaks: **Mar–Apr** (spring rain) and **Sep** (back-to-trail). 
- *hiking base layer* — **seasonal**, peaks **Oct–Nov**; gift-driven secondary bump in **Dec**.
- *fleece jacket* — **near-evergreen** with a lift **Sep–Jan**.

**Plan excerpt:**
> **August:** refresh *packable down jacket* listing copy + images; publish "best packable jackets" guide (needs lead time to rank by Oct). 
> **September:** shift ad budget toward *down jacket* and *base layer*; capture the early-mover window before competitors. 
> **October–December:** peak — maximize bids on *down jacket*, *base layer*; run gift-guide content. 
> **May–July:** trough — pull *down jacket* spend, redirect to spring/summer terms; keep *fleece* evergreen presence.

**Why it works:** prep happens in the low-competition window, content is published with time to rank, and budget follows the curve instead of fighting it.

## Worked example 2 — Home fitness (US + AU)

**Inputs:** keywords = "adjustable dumbbells, resistance bands, yoga mat, home gym setup"; category = home fitness; markets = US + Australia.

**Key insight surfaced:** *New-Year resolution* demand spikes **late Dec–Jan** in both markets, but Australia adds a **secondary Jun–Jul** lift (Southern-Hemisphere winter, indoor training). The plan therefore double-weights *adjustable dumbbells* and *home gym setup* prep in **early December** (for the Jan peak) and again in **late May** for the AU winter, while *yoga mat* trends closer to evergreen with a January bump.

**Why it works:** it catches that the same keyword has different curves per hemisphere, so the AU plan isn't a copy of the US plan.

## Common mistakes

1. **Optimizing at the peak instead of before it.** Listings and content need lead time; arriving at the peak means arriving late.
2. **Treating every keyword as seasonal (or none as).** Misclassification wastes budget. Tag evergreen vs seasonal explicitly.
3. **Even ad spend across the year.** Concentrate budget where the demand is.
4. **Publishing content too late to rank.** Allow 4–6 weeks for SEO content to climb before the peak.
5. **Copying one market's calendar onto another.** Hemispheres flip; holidays differ. Plan per market.
6. **Ignoring the early-mover window.** The cheap-click, low-competition ramp is the highest-leverage period.
7. **Self-cannibalization.** Multiple pages chasing the same term split authority. Coordinate intent.
8. **Assuming a peak from the calendar without evidence.** Mark assumptions; validate with real volume data where available.
9. **One-and-done.** Seasonality shifts; revisit the plan each quarter.
10. **No measurement loop.** Without tracking rank/CPC by month, you can't tell if pre-positioning worked.

## Resources

- `references/seasonality-methodology.md` — classifying keywords, reading curves, evergreen vs seasonal, and finding early-mover windows.
- `references/ecommerce-seasonal-calendar.md` — the major retail demand moments by month and category.
- `references/output-template.md` — the month-by-month planning table to deliver in.
- `assets/quality-checklist.md` — pre-delivery quality gate.
