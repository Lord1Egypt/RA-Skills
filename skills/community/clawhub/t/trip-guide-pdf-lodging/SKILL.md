---
name: trip-guide-pdf-lodging
description: Research, plan, revise, and deliver lodging-anchored travel guides as HTML/PDF with verified route data, hotel selection, fallback hotel swaps, curated screenshots, and formal copy. Use when a trip includes hotels, inns, guesthouses, resorts, multi-night stays, or when the user asks to make or revise an itinerary after a hotel changes, sells out, or becomes too expensive.
---

# Trip Guide PDF Lodging

Build the guide in HTML first. Export PDF only after route logic, lodging choice, and screenshots are stable.

Treat the hotel or lodging as the nightly anchor. Design each day around where the user sleeps, not around scenic spots alone.

## Core rules

1. Verify every hard number before writing it.
2. Separate **hard data** from **soft signal**.
   - Hard data: driving time, distance, tolls, hotel address, phone, opening hours, scenic latest entry.
   - Soft signal: renovation quality, noise risk, dining feel, queue risk, convenience impressions.
3. If lodging changes, recompute all dependent legs instead of text-replacing the hotel name.
4. Keep screenshots sparse and purposeful.
5. Use formal, compact copy unless the user explicitly wants casual tone.

## Workflow

### 1) Lock the planning frame

Extract:

- dates / trip length
- departure city
- trip style: self-drive, hiking, family, solo, etc.
- preference weights: scenery, comfort, food, crowd avoidance, budget
- output target: quick answer or polished HTML/PDF

If the user already gave enough constraints, start researching immediately.

### 2) Choose the lodging strategy first

Before writing the day plan, determine:

- single hotel vs multi-hotel
- town-center convenience vs scenic proximity
- parking requirement
- breakfast requirement if it changes departure time
- fallback lodging in case of sellout or price spike

The day plan should follow the lodging choice, not the other way around.

### 3) Choose sources by job

Read `references/source-selection.md` when deciding what to trust.

Default split:

- maps / official scenic pages / structured listings for hard numbers
- review sites and social posts for soft signal
- if Chinese travel/review sites are involved and normal search/fetch is weak, use `cn-review-sites-cdp`

### 4) Verify hard data before drafting

Check the numbers that decide feasibility:

- origin → lodging
- lodging → main scenic spot
- lodging → secondary scenic spot
- lodging → dinner / breakfast anchors when they matter in the final guide
- scenic opening hours / latest entry
- hotel phone / rating / address if shown

Re-run this step after every lodging change.

### 5) Design the itinerary from the lodging anchor

For each day, choose the nightly lodging first, then build:

- arrival window
- check-in / rest buffer
- meal window
- scenic entry window
- return buffer
- holiday congestion buffer

If the hotel moves from old town to new town, update the walking radius and dinner logic. Do not assume Day 1 still works unchanged.

### 6) Draft HTML first

Good structure:

- cover / conclusion box
- route overview
- day-by-day plan
- lodging section
- dining section
- risk notes / contingency

The top conclusion should tell the user:

- which lodging won
- why it won
- what fallback exists
- what tradeoff changed after the lodging decision

### 7) Use screenshots as evidence, not decoration

Keep only screenshots that support a decision:

- scenic proof image
- hotel listing / hotel note if it materially affects the recommendation
- restaurant listing snippet if it justifies a recommendation

Reject screenshots that are blank, QR-heavy, cluttered, or mostly irrelevant UI.

### 8) Run the QA gate before PDF export

Read `references/qa-checklist.md` and clear it.

Minimum gate:

- route numbers consistent with latest lodging choice
- time logic feasible
- screenshots clean
- tone formal enough
- filenames and variant names clear

### 9) Deliver and version clearly

Prefer scenario-specific filenames over destructive overwrites.

Examples:

- `*_final.html`
- `*_revision.html`
- `*_hotel-swap.html`
- `*_quanji.html`

When sending local files through OpenClaw messaging, prefer relative `MEDIA:./...` paths instead of absolute `MEDIA:/abs/path` paths.

## Revision logic

- **Visual-only feedback**: rework screenshots, typography, and tone.
- **Hotel change**: recompute every dependent leg and rewrite the daily structure affected by that hotel.
- **Budget pressure**: rerank hotels and surface tradeoffs explicitly.
- **Feasibility issue**: re-verify with maps / official sources and rebuild affected days.

## Read these references when needed

- `references/source-selection.md` — which source to trust for which data type
- `references/qa-checklist.md` — pre-export checklist for lodging-based guides
