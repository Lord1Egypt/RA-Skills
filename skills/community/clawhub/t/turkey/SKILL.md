---
name: Turkey
slug: turkey
version: 1.0.0
homepage: https://clawic.com/skills/turkey
changelog: "Initial release with verified Turkey entry rules, regional route playbooks, and practical travel logistics."
description: Plan Turkey trips with city-coast-Cappadocia routing, verified entry rules, domestic transport strategy, and practical seasonal safety.
metadata: {"clawdbot":{"emoji":"🇹🇷","requires":{"bins":[],"config":["~/turkey/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/turkey/` does not exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Turkey trip and needs practical guidance beyond generic highlights: visa pathway, route design, domestic transport choices, seasonal risks, regional tradeoffs, and on-the-ground execution.

## Architecture

Memory lives in `~/turkey/`. See `setup.md` for first activation flow and `memory-template.md` for the file structure.

```text
~/turkey/
└── memory.md     # Trip context and evolving constraints
```

## Quick Reference

| Topic | File |
|-------|------|
| **Entry and Arrival** | |
| Visa, e-Visa, passport, booking names | `entry-and-documents.md` |
| Customs, airport arrival, first-hour logistics | `customs-and-arrival.md` |
| **Planning Backbone** | |
| Regional route selection | `regions.md` |
| Sample itineraries | `itineraries.md` |
| Where to stay by route style | `accommodation.md` |
| Budget planning | `budget-and-costs.md` |
| Cards, cash, and tipping | `payments-and-tipping.md` |
| **Transport** | |
| Flights, rail, buses, ferries, city transit | `transport-domestic.md` |
| Driving and rental strategy | `road-trips-and-driving.md` |
| **History and Place Logic** | |
| Museum and archaeology planning | `archaeology-and-museums.md` |
| Istanbul playbook | `istanbul.md` |
| Cappadocia and Central Anatolia playbook | `cappadocia-and-central-anatolia.md` |
| Aegean and west coast playbook | `aegean-and-west-coast.md` |
| Mediterranean coast playbook | `mediterranean-coast.md` |
| Black Sea and eastern Anatolia playbook | `black-sea-and-eastern-anatolia.md` |
| Southeast and Mesopotamia playbook | `southeast-and-mesopotamia.md` |
| **Lifestyle and Execution** | |
| Food by region and meal style | `food-guide.md` |
| Nightlife by destination type | `nightlife.md` |
| Traveling with children | `family-travel.md` |
| Accessibility strategy | `accessibility.md` |
| **Safety and Conditions** | |
| Emergencies, scams, heat, earthquake and fire logic | `safety-and-emergencies.md` |
| Climate and seasonality planning | `weather-and-seasonality.md` |
| **Tools** | |
| Connectivity and practical digital stack | `telecoms-and-apps.md` |
| Official source map | `sources.md` |

## Core Rules

### 1. Route by Cluster, Not by Country Count
Turkey rewards fewer bases with better logic. Keep one macro-cluster per week: Istanbul, Cappadocia plus Central Anatolia, one west-coast cluster, one Mediterranean cluster, or one southeast history cluster.

### 2. Confirm Entry Pathway Before Non-Refundables
Use `entry-and-documents.md` first. Some travelers are visa-free, some need e-Visa, and some need a consular visa. Do not assume one rule fits every passport.

### 3. Match Transport to Geography
Always offer at least two movement models:
- Flight-heavy for west-east compression
- Surface-heavy for one cluster where scenery and archaeology matter more than speed

### 4. Make Every Plan Season-Aware
Use `weather-and-seasonality.md` before promising balloons, beaches, long ruins days, mountain roads, or Black Sea viewpoints. Heat, wind, wildfire smoke, snow, and shoulder-season service changes reshape the trip.

### 5. Protect the High-Friction Bookings
Lock the fragile pieces first:
- Balloon slots in Cappadocia
- Cave hotel or small old-town rooms
- Domestic flights on east-west moves
- Museum and archaeology timing when doing dense historical days
- Car rental for coast or inland routes

### 6. Budget With Real Turkey Math
Price the full route, not the hotel headline:
- Airport transfers and intercity repositioning
- Peak-season beach or resort premiums
- Fuel, tolls, parking, and valet patterns in coastal routes
- Museum/site passes and internal flight baggage fees

### 7. Build a Practical Operating Plan
Every output should include:
- Base city logic
- Day-by-day flow with transfer windows
- Reservation deadlines
- Weather or transport backup
- Safety and local-context notes for the chosen region

## Common Traps

- Treating Istanbul, Cappadocia, Antalya, Ephesus, and Mardin as one short seamless loop.
- Assuming all foreign travelers use the same visa pathway.
- Booking the wrong Istanbul airport and discovering it too late.
- Planning ruins, viewpoints, and beach time in July or August without heat logic.
- Using a rental car by default inside dense urban cores where parking and traffic dominate.
- Trying to "see the whole country" instead of choosing one west route or one east route.
- Locking a balloon-dependent Cappadocia schedule without a wind-cancellation backup.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/turkey/`

**This skill does NOT:** Access files outside `~/turkey/` or make network requests.

## Related Skills
Install with `clawhub install turkey` if user confirms:
- `travel` - General trip planning and itinerary structure
- `booking` - Reservation workflow and confirmation hygiene
- `car-rental` - Better rental strategy and handoff logistics
- `food` - Deeper restaurant and cuisine planning
- `turkish` - Language support for bookings, menus, and local interactions

## Feedback

- If useful: `clawhub star turkey`
- Stay updated: `clawhub sync`
