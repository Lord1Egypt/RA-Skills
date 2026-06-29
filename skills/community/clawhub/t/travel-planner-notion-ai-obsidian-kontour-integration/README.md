# kontour-travel-planner

AI agent skill for world-class travel planning using a 9-dimension progressive planning model.

## Install

```bash
npx skills add kontour-travel-planner
```

Or browse on a supported skill marketplace.

## What This Skill Does

Transforms any AI agent into a travel planning consultant using a structured methodology:

- **9 weighted dimensions** — dates, destination, budget, duration, travelers, interests, accommodation, transport, constraints
- **4-stage conversation flow** — Discover → Develop → Refine → Confirm
- **Guided discovery** — one high-impact question per turn, concrete options, conflict detection
- **Structured output** — trip context JSON, candidate scoring explanations, output polish with owner-tagged next actions, day-by-day itinerary, budget breakdown, Google Maps export
- **Reference data** — 200 destinations, 500 airports, airlines, activities, budget benchmarks (no API needed)

## Reference Data

Ground truth files in `references/`:

| File | Contents |
|------|----------|
| `destinations.json` | 200 global destinations with coordinates, costs, best months |
| `airports.json` | 500 airports with IATA codes and coordinates |
| `airlines.json` | Major airlines with alliances, hubs, regions |
| `activities.json` | Activity types with durations, cost tiers |
| `budget-benchmarks.json` | Daily cost benchmarks by destination tier |
| `booking-integrations.json` | Integration roadmap for booking providers |
| `embed-snippets.json` | Optional static CTA/template examples |

## Constraint Capture Smoke Test

The planner extracts operator-visible constraint details from natural-language requests, including budget caps, trip pace, neighborhood/base preference, opening-hours sensitivity, food preference, and weather sensitivity. Run the offline regression check with:

```bash
./scripts/test-plan-constraints.sh
```

## Candidate Scoring Explanations

When the request includes a known destination, `scripts/plan.sh` now emits `suggested_places` with ranked highlights and concise `why_chosen` factors. Each explanation references at least two concrete scoring factors such as destination fit, thematic fit, budget fit, hours sensitivity, or weather screening, so operators can see why a place entered the first-pass plan.

## Day-Plan Continuity

For known destinations with enough ranked highlights, `scripts/plan.sh` emits `day_plan_continuity`: a morning/afternoon/evening sequencing scaffold with zones, coordinates, continuity reasons, and transition rationale. This gives operators a compact first pass that reduces avoidable backtracking before a full itinerary or route export is finalized, and `scripts/export-gmaps.sh` can now route directly from that scaffold when no explicit `days` itinerary exists yet.

## Risk + Fallback Warnings

When constraints make a first-pass plan fragile, `scripts/plan.sh` emits `risk_fallbacks` instead of failing bluntly. The warnings currently cover closed-venue/opening-hours risk, weather mismatch, sparse-area destinations outside bundled references, and over-constrained budget caps, with each warning naming the nearest viable alternative and the action to take before finalizing.

## Destination Comparison Support

When a request asks to compare 2-3 options, `scripts/plan.sh` emits `destination_comparison` with per-option budget benchmarks, best months, fit factors, tradeoffs, a decision matrix, best-for bullets, watch-outs, an operator summary, and a clear `recommended_option`. If the user names a month or season, the comparison highlights matching or risky timing so operators can explain the decision before committing to a destination-specific itinerary.

## Scripts

- `scripts/plan.sh` — Get structured trip context from natural language
- `scripts/export-gmaps.sh` — Export itinerary to Google Maps links and KML
- `scripts/gen-airports.py` — Generate airport reference data

## Marketplace privacy policy

- Do not disclose staging, preview, Pages, or deployment hostnames in marketplace text.
- Keep install and usage examples product-neutral and avoid personal/operator identifiers.
- Add approved public URLs only when the operator provides them in the current publishing context.

## License

MIT
