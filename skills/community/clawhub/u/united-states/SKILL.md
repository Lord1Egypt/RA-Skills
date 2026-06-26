---
name: United States
slug: united-states
version: 1.0.0
homepage: https://clawic.com/skills/united-states
changelog: "Initial release with verified U.S. entry rules, region playbooks, and practical tourism logistics."
description: Plan United States trips with region-specific routing, verified entry rules, transport logistics, and practical tourist safety.
metadata: {"clawdbot":{"emoji":"🇺🇸","requires":{"bins":[],"config":["~/united-states/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/united-states/` doesn't exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a U.S. trip and needs practical guidance beyond generic advice: entry requirements, region choice, route design, transport decisions, seasonal risks, and on-the-ground execution.

## Architecture

Memory lives in `~/united-states/`. See `memory-template.md` for structure.

```
~/united-states/
└── memory.md     # Trip context and evolving constraints
```

## Quick Reference

| Topic | File |
|-------|------|
| **Entry and Border** | |
| Visa, ESTA, I-94, IDs | `entry-and-documents.md` |
| Customs, cash, restricted items | `customs-and-border.md` |
| **Planning Backbone** | |
| Regions and route strategy | `regions.md` |
| Sample itineraries (7-21 days) | `itineraries.md` |
| Accommodation strategy | `accommodation.md` |
| Budget and cost planning | `budget-and-costs.md` |
| Tipping and payment habits | `tipping-and-payments.md` |
| **Transport** | |
| Domestic flights, rail, transit | `transport-domestic.md` |
| Driving and road trips | `road-trips-and-driving.md` |
| **Nature and Parks** | |
| Passes, reservations, seasonal access | `national-parks.md` |
| **Major Regions and Cities** | |
| New York City playbook | `new-york-city.md` |
| Washington, DC playbook | `washington-dc.md` |
| California playbook | `california.md` |
| Florida playbook | `florida.md` |
| Southwest and Rockies playbook | `southwest-and-rockies.md` |
| Pacific Northwest playbook | `pacific-northwest.md` |
| Great Lakes and Midwest playbook | `great-lakes-and-midwest.md` |
| Deep South and New Orleans playbook | `deep-south-and-louisiana.md` |
| Hawaii and Alaska playbook | `hawaii-and-alaska.md` |
| **Lifestyle and Execution** | |
| Food by region and style | `food-guide.md` |
| Nightlife strategy by city type | `nightlife.md` |
| Traveling with children | `family-travel.md` |
| Accessibility strategy | `accessibility.md` |
| **Safety and Conditions** | |
| Emergencies, alerts, air quality | `safety-and-emergencies.md` |
| Climate and seasonality planning | `weather-and-seasonality.md` |
| **Tools** | |
| Connectivity and essential apps | `telecoms-and-apps.md` |
| Research sources map | `sources.md` |

## Core Rules

### 1. Route by Geography, Not by Bucket List
Anchor around one macro-region per week of travel. U.S. distance and transfer friction are a bigger quality lever than attraction count.

### 2. Entry and Compliance First
Before itinerary work, confirm the correct travel pathway (`entry-and-documents.md`): visa vs ESTA, passport validity, I-94 context, and acceptable domestic ID rules.

### 3. Make Every Plan Season-Aware
Use `weather-and-seasonality.md` and `national-parks.md` before promising outdoor-heavy plans. Heat, storms, wildfire smoke, snow, and park reservation systems can invalidate perfect-looking schedules.

### 4. Always Offer Two Transport Models
For each route, provide at least two options with tradeoffs:
- Flight-heavy (faster, higher airport overhead)
- Rail/road-heavy (slower, more scenery, different logistics)

### 5. Price Reality, Not Sticker Price
Budget with real trip math: taxes at checkout, tips where expected, parking/toll risk, resort/destination fees, checked bag costs, and transfer costs.

### 6. Flag Tourist Traps Proactively
Call out common mistakes before users commit:
- Overstuffed coast-to-coast itineraries
- Peak-season parks without reservations
- Car rental in dense cores where parking dominates cost
- Theme-city weekends without crowd and weather buffers

### 7. Deliver Actionable Plans
Output should include:
- Base city strategy
- Day-by-day flow with transfer windows
- Reservation deadlines
- Backup plan for weather or delays
- Safety and emergency quick notes

## Common Traps

- Treating the U.S. like a compact country where five cities in one trip is normal.
- Ignoring entry/admin steps until the final week.
- Using one fixed itinerary regardless of season or hazard conditions.
- Underestimating domestic transfer time between airports, hotels, and final neighborhoods.
- Choosing accommodation by nightly rate only, ignoring transport cost and time.
- Assuming all parks and attractions allow same-day spontaneous access in peak windows.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/united-states/`

**This skill does NOT:** Access files outside `~/united-states/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `car-rental` — Better rental strategy and handoff logistics
- `booking` — Reservation workflows and confirmation hygiene
- `food` — Deeper culinary planning for each destination
- `english` — Language support for calls, bookings, and service interactions

## Feedback

- If useful: `clawhub star united-states`
- Stay updated: `clawhub sync`
