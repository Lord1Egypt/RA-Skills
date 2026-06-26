---
name: Sweden
slug: sweden
version: 1.0.0
homepage: https://clawic.com/skills/sweden
changelog: "Added verified Sweden entry rules, regional playbooks, rail and road logistics, and practical seasonal travel guidance."
description: Plan Sweden trips with verified entry rules, region-specific routing, rail-ferry logistics, and practical seasonal safety.
metadata: {"clawdbot":{"emoji":"🇸🇪","requires":{"bins":[],"config":["~/sweden/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/sweden/` does not exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Sweden trip and needs operational guidance beyond generic Nordic advice: Schengen entry checks, Stockholm versus west coast versus Lapland routing, rail-flight-car tradeoffs, season fit, budget reality, and on-the-ground execution.

## Architecture

Memory lives in `~/sweden/`. See `memory-template.md` for structure.

```text
~/sweden/
└── memory.md     # Trip context, constraints, booking status, and route decisions
```

## Quick Reference

| Topic | File |
|-------|------|
| **Entry and Compliance** | |
| Tourist entry, Schengen limits, EES, ETIAS, IDs | `entry-and-documents.md` |
| Customs, alcohol, cash, restricted goods | `customs-and-border.md` |
| **Planning Backbone** | |
| Macro-regions and route logic | `regions.md` |
| Sample itineraries for 5-14 days | `itineraries.md` |
| Where to stay by trip style | `accommodation.md` |
| Daily budget framing and hidden costs | `budget-and-costs.md` |
| Cards, cash, tax-free, alcohol buying reality | `payments-and-alcohol.md` |
| **Transport and Outdoors** | |
| Trains, flights, ferries, airport moves, local transit | `transport-domestic.md` |
| Self-drive, winter roads, ferries, parking | `road-trips-and-driving.md` |
| National parks, hiking, and right-to-roam logic | `nature-and-right-to-roam.md` |
| **Major Regions and Bases** | |
| Stockholm city playbook | `stockholm.md` |
| Stockholm archipelago strategy | `stockholm-archipelago.md` |
| Gothenburg and the west coast | `gothenburg-and-west-coast.md` |
| Malmo, Lund, and Skane routing | `malmo-and-skane.md` |
| Swedish Lapland and the far north | `swedish-lapland.md` |
| Dalarna and central Sweden | `dalarna-and-central-sweden.md` |
| Gotland and island planning | `gotland.md` |
| **Lifestyle and Execution** | |
| Food, fika, supermarkets, and dining rhythm | `food-guide.md` |
| Nightlife, festivals, alcohol, and late hours | `nightlife.md` |
| Traveling with children | `family-travel.md` |
| Accessibility and low-mobility planning | `accessibility.md` |
| Emergencies, alerts, and practical safety | `safety-and-emergencies.md` |
| Climate, daylight, snow, and shoulder seasons | `weather-and-seasonality.md` |
| Connectivity, apps, and payment tools | `telecoms-and-apps.md` |
| Official source map | `sources.md` |

## Core Rules

### 1. Route by Corridor, Not by Flag Count
For short trips, choose one main Sweden corridor: Stockholm and archipelago, west coast, south via Skane, central lake country, or Lapland. Sweden looks simple on a map but quality drops fast when every region becomes a stop.

### 2. Ask for Month Before Naming a Route
The correct Sweden plan changes radically by month. Daylight, snow cover, ferry frequency, archipelago service, aurora chances, swimming weather, and road safety all depend on season.

### 3. Confirm Schengen Math Before Locking Plans
Use `entry-and-documents.md` first for passport validity, Schengen day counting, EES rollout context, and whether the user is mixing Sweden with Denmark, Norway, Finland, or the Baltics.

### 4. Always Offer Two Transport Models
For any multi-stop trip, provide at least two viable patterns:
- Rail and ferry heavy: lower winter driving risk, more timetable dependence
- Flight or self-drive heavy: more reach, higher transfer or weather friction

### 5. Budget with Sweden Reality
Do not price from hotel headlines alone. Include airport transfer costs, rail supplements, island ferries, car parking, winter gear, restaurant alcohol, and shoulder-season opening patterns.

### 6. Protect the User from Nordic Overreach
Flag bad combinations early:
- Stockholm, Gothenburg, Gotland, and Lapland in one week
- Lapland winter trips without darkness or cold tolerance
- Summer archipelago or Midsummer travel booked too late
- Cross-border south-Sweden plans that ignore passport or ID checks

### 7. Deliver Operational Plans
Output should include:
- Best base or base pair
- Day-by-day flow with realistic transfer windows
- Booking deadlines or low-inventory warnings
- Weather backup and downgrade options
- Safety notes for cold, ferries, and remote areas

## Common Traps

- Treating Sweden as a compact city-break country where south, center, and far north fit naturally into one short itinerary.
- Assuming Schengen admin is trivial because the first arrival point is not Sweden.
- Choosing a rental car before checking whether rail plus one strategic base solves the trip better.
- Planning Lapland around aurora certainty instead of darkness, forecast, and backup activities.
- Ignoring ferry or island timetables in the archipelago and on Gotland.
- Underestimating how much alcohol, dining, and airport transfers move the real budget.
- Booking scenic summer trips without checking that some services are sharply seasonal.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/sweden/`

**This skill does NOT:** Access files outside `~/sweden/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `europe` — Broader Schengen and multi-country Europe planning
- `booking` — Reservation workflows and total-cost booking hygiene
- `food` — Deeper restaurant and cuisine planning
- `english` — Language support for bookings and practical interactions

## Feedback

- If useful: `clawhub star sweden`
- Stay updated: `clawhub sync`
