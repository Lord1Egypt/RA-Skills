---
name: kontour-travel-planner
description: Transform any AI agent into a world-class travel planner using Kontour AI's 9-dimension progressive planning model with structured conversation flow.
version: 2.0.43
license: MIT-0
metadata:
  openclaw:
    emoji: "🧭"
    requires:
      env: []
      bins:
        - bash
        - python3
---

# Kontour Travel Planner

> The planning brain that any AI agent can plug in. Not a search wrapper — a planning **methodology**.

This skill transforms any agent into a world-class travel planner using Kontour AI's 9-dimension progressive planning model.

## Requirements

**No API keys or credentials required.** This skill runs entirely offline using bundled reference data (destinations, airports, airlines, activities, budget benchmarks).

- **Scripts** (`plan.sh`, `export-gmaps.sh`) — Pure local processing. No external API calls. Generates Google Maps URLs as plain links (no API key needed).
- **Reference data** (`references/`) — Static JSON files bundled with the skill.
- **`embed-snippets.json`** — Optional static marketing templates. These are informational only, do not load remote code, and are not required for planning functionality.
- **`booking-integrations.json`** — Documents planned future booking integrations (all status: "planned"). No active API connections.

### Security Transparency (for skill marketplaces)

To reduce false-positive trust flags and improve reviewer confidence:

- Runtime network behavior: `plan.sh` and `export-gmaps.sh` make **no outbound HTTP/API calls**.
- Credentials required: **none** (no API keys, tokens, OAuth, or env secrets).
- Declared runtime dependencies in frontmatter: `bash`, `python3` only.
- Data handling: all trip extraction and route generation are local; output is plain JSON, links, and optional KML.
- External CTA examples are informational only and not required for core planning.

Quick local verification:

```bash
# Should return no matches for network clients used by runtime scripts
rg -n "python3 -c|eval\(|exec\(|os\.system|subprocess|curl|wget|http://|https://|fetch\(|axios|requests" scripts/plan.sh scripts/export-gmaps.sh

# Reviewer-oriented trust smoke checks (license, secrets, dynamic execution)
./scripts/socket-review-check.sh
```

## How It Works

### 9-Dimension Planning Model

Every trip is tracked across 9 weighted dimensions:

| Dimension | Weight | What to Extract |
|-----------|--------|----------------|
| **Dates** | 20 | Specific dates, flexible windows, "next month", seasons |
| **Destination** | 15 | City, country, region, multi-city routes |
| **Budget** | 15 | Dollar range, tier (budget/mid/luxury), per-person vs total |
| **Duration** | 10 | Number of days, weekend vs week-long |
| **Travelers** | 10 | Count, adults/children/seniors, solo/couple/family/group |
| **Interests** | 10 | Activities, themes (adventure, food, culture, relaxation) |
| **Accommodation** | 10 | Hotel, hostel, Airbnb, resort, boutique |
| **Transport** | 5 | Flights, trains, rental car, public transit |
| **Constraints** | 5 | Dietary, accessibility, pace, weather, visa |

Each dimension has a score (0-1) and status (missing/partial/complete). Overall progress = weighted sum.

### Stage-Based Conversation Flow

Progress determines the current stage. Each stage prioritizes different dimensions:

**Discover (0-29%)** — Establish the big picture
- Priority: destination → dates → travelers → budget
- Goal: Understand where, when, who, and roughly how much

**Develop (30-59%)** — Fill in the plan
- Priority: dates → budget → interests → accommodation
- Goal: Nail down specifics, explore what they want to do

**Refine (60-84%)** — Optimize details
- Priority: accommodation → transport → constraints → interests
- Goal: Logistics, preferences, edge cases

**Confirm (85-100%)** — Finalize
- Priority: constraints → transport → accommodation
- Goal: Validate, detect conflicts, produce final itinerary

### Guided Discovery Protocol

**Rules:**
1. Ask **ONE** high-impact question per turn. Never interrogate.
2. Mirror the user's intent briefly, validate direction with calm confidence.
3. Add one useful enrichment detail (a fact, tip, or insight).
4. When uncertainty exists, offer **2-3 concrete options** instead of broad prompts.
5. Advance with a concrete next action.

**Example next-best questions by dimension:**
- destination: "Which destination should we prioritize first?"
- dates: "What travel window works best for {destination}?"
- duration: "How many days do you want this trip to be?"
- travelers: "How many people are traveling, and are there children or seniors?"
- budget: "What budget range should I optimize for?"
- interests: "What are your top must-do experiences in {destination}?"
- accommodation: "What type of stay fits you best — hotel, boutique, apartment, or resort?"
- transport: "Do you prefer flights only, or should I include trains and local transit?"
- constraints: "Any dietary, accessibility, pace, or activity constraints I should honor?"

### Conflict Detection

Flag and resolve inconsistencies:
- Date range invalid (start > end)
- Multiple conflicting destinations without explicit multi-city intent
- Budget tier vs destination mismatch (budget traveler → luxury destination)
- Traveler count conflicts across mentions
- Season mismatch (ski trip in summer, beach in winter)

### Confidence Scoring

Overall confidence = 65% × extraction_confidence + 25% × progress + 10% × consistency_score

Use confidence to calibrate response certainty. Below 50%: ask more. Above 80%: start generating itineraries.

### Candidate Scoring Explanation Contract

When `plan.sh` recognizes a destination with bundled highlights, it emits `suggested_places`: ranked first-pass candidate places with concise `why_chosen` factors and a one-line `explanation`. Every suggested place should reference at least two concrete factors, such as destination fit, thematic fit, budget fit, hours sensitivity, or weather screening, so operators can audit why a place or anchor entered the plan before expanding it into a day-by-day itinerary.

### Day-Plan Continuity Contract

When `plan.sh` recognizes a destination with at least three bundled highlights, it emits `day_plan_continuity`: a morning/afternoon/evening scaffold ordered by destination-specific zones and lightweight routing heuristics. Each segment includes a `continuity_reason`, and each transition explains whether it is a same-zone pairing or a directional move to reduce backtracking before detailed live transit, hours, and meal timing are finalized.

### Constraints Capture Contract

`plan.sh` emits both a concise `constraints` list and machine-readable `constraint_details` when the traveler request includes explicit planning constraints:

- `budget.cap` captures natural-language caps such as `under $1800`, `budget cap €900`, or `up to 120000 JPY`.
- `constraint_details.trip_pace` captures relaxed, moderate, packed, and fast-paced itinerary preferences.
- `constraint_details.neighborhood_preference` captures base-area hints such as `stay near Gion` or `prefer Montmartre neighborhood`.
- `constraint_details.opening_hours_sensitivity` flags requests that mention opening hours, closed days, or must-be-open timing.
- `constraint_details.food_preferences` captures dietary and cuisine preferences including vegetarian, vegan, halal, kosher, gluten-free, no raw fish, seafood, street food, and local food.
- `constraint_details.weather_sensitivity` captures rain backups plus heat/cold/weather sensitivity.

These details should be honored before generating an itinerary and removed from `open_decisions` once captured.

### Risk + Fallback Contract

`plan.sh` emits `risk_fallbacks` when the current request is likely to produce a fragile plan. Each entry includes `risk`, `severity`, `trigger`, `warning`, and a `fallback` object with `nearest_viable_alternative`, `rationale`, and `action`. Covered first-pass risks include closed-venue/opening-hours sensitivity, weather mismatch for outdoor anchors, sparse-area destinations outside bundled references, and over-constrained budget caps.

### Comparison Decision Matrix Contract

When `plan.sh` emits `destination_comparison`, each option includes a `decision_matrix` with Budget fit, Season fit, Interest fit, and Pace fit signals, plus `best_for` and `watch_out` bullets for scan-friendly operator narration. If the traveler names a month or season, comparison scoring should surface whether that timing overlaps the destination's bundled best-month window and prefer viable seasonal fits before cheaper but poorly timed options. The comparison also includes an `operator_summary` so agents can explain the recommended option and the most useful alternate without forcing users to parse raw JSON.

### Compact Presentation Markdown

For output polish, `output_polish.presentation_markdown` gives agents a ready-to-adapt Markdown draft with four compact sections: Recommendation, Why this fits, Watch-outs, and Next step. `output_polish.final_reply_preview` adds a traveler-facing compact reply preview with recommendation, rationale, evidence, optional flow note, watch-out, and owner-tagged next action so operators can paste or adapt a safer final response without losing caveats. Use it as the user-visible summary scaffold after checking the structured fields; it keeps the recommendation, rationale, fallback warning, and owner-tagged next action together without replacing the machine-readable data. `output_polish.decision_badges` adds compact readiness, next-owner, fallback-count, and decision-mode labels for scan-friendly UI chips or operator summaries. `output_polish.reply_options` adds up to three safe next-move choices with labels, values, owners, and reasons so chat UIs or operators can present actionable follow-ups without inventing buttons from prose. `output_polish.user_response_choices` adds copy-ready example traveler replies for the highest-priority missing decision, fallback confirmation, or itinerary expansion so user-facing UIs can offer concrete responses without losing ownership or caveats. `output_polish.decision_snapshot_table` adds a compact five-row decision table with focus, readiness, primary evidence, watch-out, and next action for dashboards, chat cards, or operator review panes. `output_polish.evidence_trace_card` adds a compact source trace naming the structured fields behind the recommendation so operators can audit or paste safer rationale. `output_polish.presentation_contract_check` adds a pre-send operator checklist that confirms the decision, evidence, watch-out, next owner, and finality guard are visible before a recommendation is sent. `output_polish.reply_readiness_score` adds a weighted operator score with pass/fail criteria, gate status, and the next improvement needed before sending or expanding the reply. `output_polish.traveler_facing_draft` adds ready-to-send concise Markdown bullets that preserve the recommendation, rationale, evidence, watch-out, next action, and clarification call without inventing new plan facts. `output_polish.shareable_summary` adds a traveler-facing, plain-text snapshot for chat or notes with recommendation, why, evidence, watch-out, and next action lines. `output_polish.operator_digest` adds a copy-ready operator decision note with decision, rationale, evidence, watch-out, and owner-tagged next action lines for internal review or handoff. `output_polish.validation_summary` adds operator-visible go/no-go checks with pass criteria and fallback actions before the recommendation is presented or expanded. `output_polish.operator_review_queue` adds a prioritized owner/severity queue of the exact review tasks that must clear before presentation or itinerary expansion. `output_polish.constraint_compliance_card` adds an operator-visible checklist that restates captured budget, pace, neighborhood, hours, food, and weather constraints with the exact preservation check required before expansion. `output_polish.operator_preflight_card` adds a compact send-readiness guard with safe send mode, required evidence/watch-out/owner elements, and a do-not-claim warning so operators can paste polished replies without overstating live viability. `output_polish.live_validation_prompt_pack` adds copy-ready user/operator prompts for live hours, transit, route continuity, fallback readiness, and traveler clarification checks before a plan is treated as final. `output_polish.assumption_ledger` lists missing inputs, offline-data assumptions, route-scaffold caveats, fallback assumptions, and active constraints so operators can label provisional plan details instead of overstating certainty. `output_polish.action_plan` adds a numbered, owner-tagged action sequence with trigger and outcome fields so operators know the exact next checks or user prompts to run before expanding the itinerary. `output_polish.itinerary_expansion_brief` adds an operator-visible expansion guardrail that names which evidence, continuity, constraints, fallbacks, and clarification gates must be preserved before turning the compact recommendation into a timed itinerary. `output_polish.send_decision_card` adds a single send/hold call with the safest send form, primary blocker, must-include items, and a copy-ready operator line so agents do not over-send a provisional plan. `output_polish.outbound_send_packet` adds the exact traveler-facing message to send now, plus send/hold status, hold-until condition, and a do-not-add guard so operators can paste one outbound reply without turning a clarifying question into a fake final itinerary. `output_polish.reply_intake_card` adds the accepted traveler replies, what to do if they answer, and a still-do-not guard so the next inbound message is not treated as permission to send a fake final itinerary. `output_polish.followup_send_packet` adds the exact traveler-facing follow-up to send after that inbound answer, plus a still-do-not guard so acknowledgement is not treated as a go-ahead for a fake final itinerary. `output_polish.unclear_reply_packet` adds the copy-ready traveler retry to send when the inbound answer is unclear, with a still-do-not guard so a vague reply is not treated as permission to send a final itinerary. `output_polish.two_turn_send_script` stitches the outbound message, expected reply, follow-up, and unclear-retry path into one copy-ready two-turn script so operators can run the next conversation beat without assembling those cards by hand. `output_polish.no_reply_nudge_packet` adds the copy-ready reminder to send when the traveler stays silent after the outbound question, with a still-do-not guard so silence is not treated as permission to send a final itinerary. `output_polish.post_nudge_hold_packet` adds the operator-only hold after that one reminder, so a second nudge or continued silence is not treated as permission to send a final itinerary.

### Output Polish Contract

`plan.sh` emits `output_polish` as a compact presentation scaffold for agents and operators. It includes `compact_sections` for the recommended response structure, `decision_summary` for a one-line readiness call, `decision_rationale` with concise evidence for why the current choice or sequence is recommended, `confidence_drivers` naming the structured evidence behind the recommendation, `status_line` summarizing readiness/fallback/open-decision counts for dashboards, `next_step_actions` for narrative next moves, `next_action_checklist` with explicit user/operator ownership and status, `operator_review_queue` for a prioritized owner/severity queue of the exact review tasks that must clear before presentation or itinerary expansion, `next_step_prompt` for the single highest-impact prompt to send or run next, `operator_preflight_card` for a send-readiness guard that names safe send mode, must-include evidence, and claims to avoid, `clarification_prompt_card` with why-now context, example answers, known structured context, and copy-ready text for the top missing decision, `live_validation_prompt_pack` for copy-ready validation prompts with user/operator ownership, `action_plan` for a numbered owner/trigger/outcome sequence of the next concrete steps, `decision_badges` for concise readiness/owner/fallback/mode chips, `shareable_summary` for paste-ready traveler text, `operator_digest` for copy-ready internal review notes, `evidence_trace_card` for compact source-field audit trails, `reply_options` for user/operator-visible follow-up choices, `user_response_choices` for copy-ready traveler response examples, `decision_snapshot_table` for a compact operator/UI decision table, `traveler_facing_draft` for a safe ready-to-send traveler Markdown draft, `final_reply_preview` for a compact traveler-facing response preview that preserves caveats and next ownership, `handoff_brief` for copy-ready operator transfer notes, `validation_summary` for live viability/route/constraint/user-clarification gates, `constraint_compliance_card` for preserving captured budget, pace, neighborhood, hours, food, and weather constraints during expansion, `finalization_gate` for an explicit go/no-go signal that blocks final presentation until user and operator checks clear, `reply_readiness_score` for a weighted operator score with criteria, gate status, and the next improvement needed before sending or expanding, `decision_risk_meter` for a compact operator risk/readiness meter with finality gate, safest traveler send mode, reasons, and the recommended operator action, `send_decision_card` for a single send/hold decision with the safest send form, primary blocker, and copy-ready operator instruction, `outbound_send_packet` for the exact traveler-facing message to send now with send/hold status and a do-not-add guard, `reply_intake_card` for accepted traveler replies plus if-answered / if-unclear / still-do-not handling of the next inbound message, `followup_send_packet` for the exact traveler-facing follow-up to send after that answer with a still-do-not final-itinerary guard, `unclear_reply_packet` for the copy-ready retry to send when the inbound answer is unclear, `two_turn_send_script` for a copy-ready outbound → expected-reply → follow-up sequence with an unclear-retry branch that keeps the still-do-not final-itinerary guard visible, `no_reply_nudge_packet` for the copy-ready reminder to send when the traveler stays silent after the outbound question, `post_nudge_hold_packet` for the operator-only hold after that one reminder so a second nudge or continued silence is not treated as a final itinerary, `assumption_ledger` for operator-visible provisional assumptions that must be labeled before presenting or expanding a plan, and a `response_template` with a four-line operator draft (`Lead with`, `Why`, `Watch`, `Next`) for consistent user-visible rendering.

## Structured Output

When planning is ≥85% complete, produce:

### Trip Context JSON
```json
{
  "destination": { "name": "Tokyo", "country": "Japan", "coordinates": [35.6762, 139.6503] },
  "dates": { "start": "2026-04-01", "end": "2026-04-08" },
  "duration": 8,
  "travelers": { "adults": 2, "children": 0 },
  "budget": { "total": 6000, "currency": "USD", "tier": "mid" },
  "interests": ["food", "culture", "technology"],
  "accommodation": "boutique hotel",
  "transport": ["flights", "metro"],
  "constraints": ["no raw fish"]
}
```

### Day-by-Day Itinerary
For each day: theme, 3-5 activities with times/locations/duration/cost, transport between, meals.

### Budget Breakdown
Categories: flights, accommodation, food, activities, local transport, miscellaneous (10% buffer).

### Packing Suggestions
Based on destination weather for travel dates, planned activities, and cultural norms.

### Interactive Planning Link
> Add only an operator-approved public planning link at response time. Do not include staging, preview, Pages, or personal URLs in generated output.

## Reference Data

Ground truth files in `references/`:
- `destinations.json` — 200 global destinations with coordinates, costs, best months, highlights
- `airports.json` — 500 airports with IATA codes and coordinates
- `airlines.json` — Major airlines with alliances, hubs, regions
- `activities.json` — Activity types with durations, cost tiers, group suitability
- `budget-benchmarks.json` — Daily cost benchmarks by destination tier

Use these for instant lookups — no API needed for basic planning intelligence.

## Quick Planning Script

```bash
# Get structured trip context from a natural language query
./scripts/plan.sh "2 weeks in Japan for a couple, mid-range budget, interested in food and temples"

# Compare 2-3 destination options with budget, seasonality, fit factors, and tradeoffs
./scripts/plan.sh "compare Tokyo vs Paris vs Bangkok for 7 days for a couple, mid range budget, food and culture, relaxed pace"
```

When a request says `compare`, `between`, `vs`, `or`, or `and` for 2-3 destination options, the script emits `destination_comparison` with:
- `options[]` — each destination's daily budget benchmark, best months, fit factors, tradeoffs, decision signal, decision matrix, best-for bullets, and watch-outs.
- `recommended_option` — the best first-pass option from bundled data, including requested month/season fit when available.
- `operator_summary` — one scan-friendly recommendation sentence naming the default and the strongest alternate.
- `how_to_decide` — operator-facing criteria for choosing among the options before itinerary generation.

## Off-Topic Handling

Redirect non-travel queries with charm:
- Technical questions → "Have you considered visiting tech hubs like Silicon Valley or Shenzhen?"
- Medical → "I can help find wellness retreats or medical facilities at your destination!"
- Always pivot to travel with enthusiasm. Never be dismissive.

## Key Principles

1. **Progressive extraction** — Don't ask all questions upfront. Extract naturally from conversation.
2. **Stage awareness** — Different priorities at different planning stages.
3. **One question per turn** — Respect the user's attention. Be a consultant, not a form.
4. **Concrete options** — "Barcelona, Lisbon, or Dubrovnik?" beats "Where in Europe?"
5. **Machine-readable output** — Structured JSON that other tools can consume.
6. **Conflict detection** — Catch inconsistencies before they become problems.

## Google Maps Export

Export any itinerary to shareable Google Maps links and KML files:

```bash
# Generate Google Maps URL with waypoints + per-day routes
./scripts/export-gmaps.sh itinerary.json

# Also export KML for import into Google Earth/Maps
./scripts/export-gmaps.sh itinerary.json --kml trip.kml
```

**Input format** — The script consumes the structured itinerary JSON:
```json
{
  "days": [{
    "day": 1,
    "locations": [
      {"name": "Senso-ji Temple", "lat": 35.7148, "lng": 139.7967},
      {"name": "Tsukiji Outer Market", "lat": 35.6654, "lng": 139.7707}
    ]
  }]
}
```

**Outputs:**
- Full trip route URL: `https://www.google.com/maps/dir/35.7148,139.7967/35.6654,139.7707/...`
- Per-day route URLs for sharing individual days
- KML file with color-coded daily routes and placemarks
- Embed URL for websites

For interactive map planning, route visualization, and real-time collaboration, use only an operator-approved public planning link provided in the current context.

## Sharing & Collaboration

### Shareable Trip Summary

Generate summaries in multiple formats for different platforms:

**Markdown (for email/docs):**
```markdown
## 🗾 Tokyo Adventure — Apr 1-8, 2026
👥 2 travelers | 💰 $6,000 budget | 🏨 Boutique hotels

### Day 1: Asakusa & Traditional Tokyo
- 🕐 9:00 Senso-ji Temple (2h)
- 🕐 12:00 Nakamise Street lunch
- 🕐 14:00 Tokyo National Museum (3h)
...
```

**WhatsApp/iMessage/Telegram-friendly** (no markdown tables, compact):
```
🗾 Tokyo Trip • Apr 1-8
👥 2 people • 💰 $6K budget

Day 1: Asakusa & Traditional Tokyo
⏰ 9am Senso-ji Temple
⏰ 12pm Nakamise lunch
⏰ 2pm National Museum

📍 Map: [Google Maps link]
✨ Plan together: [approved public trip link]
```

**Visual Trip Card** (structured data for rendering):
```json
{
  "card_type": "trip_summary",
  "destination": "Tokyo, Japan",
  "dates": "Apr 1-8, 2026",
  "cover_image_query": "Tokyo skyline cherry blossom",
  "travelers": 2,
  "budget": "$6,000",
  "highlights": ["Senso-ji", "Tsukiji Market", "Mount Fuji day trip"],
  "share_url": "[approved public trip link]"
}
```

## SEO Content & Embeddable Widgets

Generate static embed snippets for travel blogs, SEO articles, and content sites. See `references/embed-snippets.json` for ready-to-use templates.

### Available Widgets

1. **"Plan this trip" CTA Button** — Link-based CTA using an approved public URL placeholder.
2. **Destination Quick Facts Card** — Weather, currency, visa, best season, language at a glance.
3. **Cost Comparison Summary** — Budget vs mid-range vs luxury daily costs.

### Generating Widgets On Demand

When asked to generate SEO content for a destination, produce:
1. Destination quick facts card (pull from `references/destinations.json`)
2. Cost comparison summary (pull from `references/budget-benchmarks.json`)
3. A natural CTA with an approved public URL placeholder, e.g. "Ready to plan? [Start your {destination} itinerary →]({APPROVED_PUBLIC_URL})"

### SEO-Friendly Content Generation

When writing travel content, naturally weave in:
- Structured data (schema.org TravelAction) for search visibility
- Internal destination links only when an approved public URL is supplied
- Cost comparisons that reference real benchmark data
- Seasonal recommendations backed by the `best_months` data

## Booking & Reservations (Roadmap)

Kontour AI is building direct booking integrations. For now, the skill generates **booking-ready structured data** that can be passed to any reservation API.

See `references/booking-integrations.json` for the full integration roadmap.

### Supported Output Formats

The skill outputs structured requests ready for any booking system:

| Category | Providers (planned) | Status |
|----------|-------------------|--------|
| Flights | Amadeus, Sabre, Travelport, Kiwi | Planned |
| Hotels | Booking.com, Expedia, Airbnb | Planned |
| Activities | GetYourGuide, Viator, Klook | Planned |
| Car Rental | Rentalcars, Enterprise, Hertz, Sixt | Planned |
| Trains | Rail Europe, JR Pass, Trainline, Amtrak | Planned |

**Example booking-ready output:**
```json
{
  "flights": [
    {"origin": "LAX", "destination": "NRT", "date": "2026-04-01", "passengers": 2, "cabin": "economy"}
  ],
  "hotels": [
    {"destination": "Tokyo", "checkin": "2026-04-01", "checkout": "2026-04-08", "guests": 2, "rooms": 1, "budget_per_night_usd": 150}
  ],
  "activities": [
    {"destination": "Tokyo", "date": "2026-04-02", "category": "Food Tour", "participants": 2, "budget_usd": 80}
  ]
}
```

Treat integration status as a roadmap snapshot unless the operator supplies an approved current public status URL.
