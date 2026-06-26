---
name: trip-guide-pdf-car-sleep
description: Research, plan, revise, and deliver car-sleep travel guides as HTML/PDF with verified overnight parking, charging, toilet access, next-morning route anchors, and formal copy. Use when the user plans to sleep in the car, skip hotels, use Tesla/EV camp mode, optimize for chargers and public parking, or asks whether the hiking/scenic route should change after removing lodging.
---

# Trip Guide PDF Car Sleep

Build the guide in HTML first. Export PDF only after night-parking anchors, route logic, and screenshots are stable.

Treat night parking as the anchor for each day. For car-sleep trips, the real constraint is usually not the scenic spot—it is whether the user can park, charge, wash up, and leave smoothly the next morning.

## Core rules

1. Verify every hard number before writing it.
2. Separate **hard data** from **soft signal**.
   - Hard data: parking point, charger existence, toilet existence when relevant, route time, distance, tolls, scenic hours.
   - Soft signal: quietness, comfort, crowding feel, scenic vibe, overnight confidence level.
3. Distinguish `24h parking/charging access` from `overnight car-sleep explicitly allowed`.
4. If overnight permission is not explicitly verified, label the spot as a **candidate night anchor, permission unconfirmed** rather than claiming it is allowed.
5. Prefer anchors with explicit car-sleep / camping signal over generic public charger parking.
   - Best: official campsite / campground / scenic camping area
   - Next: repeatedly mentioned car-sleep / overnight stop in social results
   - Next: service area with strong facilities
   - Last resort: generic public parking + charger
6. If the night parking anchor changes, recompute all dependent legs.
7. Do not present a generic public charger parking lot as the main night anchor unless stronger overnight evidence is unavailable.
8. Use formal, compact copy unless the user explicitly wants casual tone.

## Workflow

### 1) Lock the planning frame

Extract:

- dates / trip length
- departure city
- vehicle type and whether EV charging matters
- trip style: solo, hiking, photography, family, etc.
- comfort vs scenery tradeoff
- output target: quick answer or polished HTML/PDF

### 2) Turn the request into car-sleep variables

Identify the variables that can change the whole plan:

- EV vs ICE
- charger dependence
- toilet dependence
- county-town first night vs scenic-adjacent first night
- main scenic line vs lighter backup line
- public parking vs scenic parking

Do not research these variables equally; prioritize the ones that make the trip operable.

### 3) Choose sources by job

Read `references/source-selection.md` when deciding what to trust.

Default split:

- maps / official scenic pages / structured listings for hard numbers
- notes and review sites for soft signal
- if Chinese travel/review sites are involved and normal search/fetch is weak, use `cn-review-sites-cdp`
- when Xiaohongshu detail pages degrade into 404 or blocked pages, still use search-result clustering as a soft-signal layer to detect which locations are repeatedly treated as camping / overnight spots

### 4) Verify hard data before drafting

Check the numbers and permissions that decide feasibility:

- origin → night parking anchor
- night parking anchor → main scenic spot
- scenic spot A → scenic spot B
- charger location and parking context
- nearby public toilet when the night plan depends on it
- scenic opening hours / latest entry
- whether overnight parking / overnight car-sleep permission is explicitly stated anywhere reliable

Re-run this verification after every night-anchor change.

### 5) Choose the night anchor before choosing the scenic order

For each night, rank anchors by:

1. overnight certainty
2. explicit camping / car-sleep signal strength
3. charger / refill certainty
4. next-morning route efficiency
5. nearby toilet / basic food access
6. scenic proximity

This order is intentional. “Closest to the scenic spot” is often not the best overnight point, and a generic 24-hour parking lot should lose to a repeatedly mentioned camping / overnight point.

### 6) Design the itinerary from the night anchor

For each day, choose the sleep point first, then build:

- arrival and recharge buffer
- dinner / wash-up window
- scenic entry window for the next morning
- return buffer
- holiday congestion buffer

If the user removes hotels, do not just delete the lodging section. Rebuild the schedule from the new sleep points.

### 7) Use screenshots as evidence

Keep only screenshots that support decisions:

- scenic proof image
- parking / charger context if the choice is non-obvious
- any visible sign or listing evidence about parking hours / overnight rules
- restaurant snippet only if it affects the overnight strategy

Reject screenshots that are blank, cluttered, QR-heavy, or mostly UI.

### 8) Run the QA gate before PDF export

Read `references/qa-checklist.md` and clear it.

Minimum gate:

- overnight anchors verified
- dependent route numbers recomputed
- screenshots clean
- tone formal enough
- filenames and variant names clear

### 9) Deliver and version clearly

Prefer scenario-specific filenames.

Examples:

- `*_tesla_sleep.html`
- `*_car-sleep.html`
- `*_parking-revision.html`

When sending local files through OpenClaw messaging, prefer relative `MEDIA:./...` paths instead of absolute `MEDIA:/abs/path` paths.

## Revision logic

- **Visual-only feedback**: clean screenshots and tighten prose.
- **Sleep-point change**: recompute all dependent legs and next-morning structure.
- **Charging concern**: elevate charger, toilets, and service-area fallback strength.
- **Weak overnight evidence**: demote generic public charger parking and replace it with a stronger camping / car-sleep signal point.
- **Comfort concern**: consider swapping the lighter scenic day to a more urban or public-facility-rich anchor.

## Read these references when needed

- `references/source-selection.md` — which source to trust for which car-sleep decision
- `references/qa-checklist.md` — pre-export checklist for car-sleep guides
