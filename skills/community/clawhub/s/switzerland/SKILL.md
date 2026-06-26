---
name: Switzerland
slug: switzerland
version: 1.0.0
homepage: https://clawic.com/skills/switzerland
changelog: "Initial release with verified Switzerland entry rules, scenic rail and mountain logistics, and practical regional playbooks."
description: Plan Switzerland trips with Alpine rail and mountain logistics, verified entry rules, scenic routing, and practical local execution.
metadata: {"clawdbot":{"emoji":"🇨🇭","requires":{"bins":[],"config":["~/switzerland/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/switzerland/` does not exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Switzerland trip and needs operational guidance beyond postcard advice: Schengen entry checks, CHF cost reality, rail vs car tradeoffs, scenic-train and mountain timing, region choice, and on-the-ground execution.

## Architecture

Memory lives in `~/switzerland/`. See `memory-template.md` for structure.

```text
~/switzerland/
└── memory.md     # Trip context, routing logic, and evolving constraints
```

## Quick Reference

Use this map to load only the Switzerland subtopic that changes the decision in front of you.

| Topic | File |
|-------|------|
| **Entry and Compliance** | |
| Tourist entry, Schengen logic, passport checks | `entry-and-documents.md` |
| Customs, duty-free limits, border habits | `customs-and-border.md` |
| **Planning Backbone** | |
| Macro-regions and route logic | `regions.md` |
| Sample itineraries for 4-14 days | `itineraries.md` |
| Where to stay by trip style | `accommodation.md` |
| Budget framing and hidden costs | `budget-and-costs.md` |
| Cards, cash, tax-free, tipping | `payments-and-tax-free.md` |
| **Transport and Outdoors** | |
| Trains, boats, buses, airport links, passes | `transport-domestic.md` |
| Driving, vignette, passes, parking, winter roads | `road-trips-and-driving.md` |
| Scenic trains, lifts, lakes, hiking, panoramas | `alps-lakes-and-scenic-trains.md` |
| Ski, snow, festive season, winter routing | `winter-ski-and-snow.md` |
| **Major Regions and Bases** | |
| Zurich and easy first-trip routing | `zurich.md` |
| Lucerne and Central Switzerland | `lucerne-and-central-switzerland.md` |
| Bern city, Gruyeres, and slower culture routes | `bern-and-fribourg.md` |
| Interlaken, Jungfrau, Lauterbrunnen, Grindelwald | `bernese-oberland.md` |
| Geneva, Lausanne, Montreux, and Lavaux | `geneva-lausanne-and-lake-geneva.md` |
| Zermatt, Valais, Matterhorn, and high Alps | `valais-and-zermatt.md` |
| Graubunden, Engadin, Davos, and scenic rail | `graubunden-and-engadin.md` |
| Ticino and Italian-speaking lake routes | `ticino.md` |
| Basel, Jura, and tri-border positioning | `basel-and-northwest.md` |
| **Lifestyle and Execution** | |
| Food strategy and regional specialties | `food-guide.md` |
| Traveling with children or mixed ages | `family-travel.md` |
| Accessibility and low-mobility planning | `accessibility.md` |
| Emergencies, weather, mountain risk, disruptions | `safety-and-emergencies.md` |
| Climate, altitude, and seasonality logic | `weather-and-seasonality.md` |
| Connectivity, apps, roaming, ticketing tools | `telecoms-and-apps.md` |
| Official source map | `sources.md` |

## Core Rules

### 1. Route by Corridor, Not by Pin Count
For short trips, choose one dominant Switzerland shape: Zurich and Central Switzerland, Bernese Oberland, Lake Geneva, Valais, Graubunden, Ticino, or Basel and Jura. Scenic density is high, but hotel changes, lifts, and transfer friction still punish over-routing.

### 2. Ask for Month and Altitude Tolerance Before Naming the Best Region
The same Switzerland plan changes meaning in February, June, September, and December. Snow line, lake appeal, hiking access, daylight, and school-holiday demand can make a famous route smart or wasteful.

### 3. Default to Rail, Add a Car Only When It Clearly Improves Execution
Classic visitor routes are usually better by train and boat. Car value appears when the trip is built around rural lakes, remote valleys, low-frequency villages, or border-heavy driving loops.

### 4. Treat Mountains as Logistics, Not Background
Use `alps-lakes-and-scenic-trains.md`, `winter-ski-and-snow.md`, and `weather-and-seasonality.md` before promising panoramic days. Cloud, wind, snow, avalanche controls, and pass closures can change the whole plan.

### 5. Budget With Real Swiss Friction
Do not price from hotel headlines alone. Include CHF reality, resort taxes, lift tickets, seat reservations where relevant, parking, tunnel or pass detours, luggage handling, and mountain food premiums.

### 6. Protect the User From Border and Sunday Mistakes
Switzerland sits inside Schengen but outside the EU customs and roaming default that many travelers assume. Border shopping, tax-free steps, Sunday closures, and cross-border train or car choices need explicit handling.

### 7. Deliver Operational Plans
Output should include:
- Best base or base pair
- Day-by-day flow with realistic transfer windows
- Booking deadlines or low-availability warnings
- Weather downgrade options
- Safety, payment, and emergency notes

## Common Traps

- Treating Switzerland like a small country that can be "done" in a few rail hops.
- Mixing Zurich, Lucerne, Jungfrau, Zermatt, St. Moritz, Lake Geneva, and Ticino into one short trip.
- Booking a car before checking whether SBB plus one local bus or boat solves the route better.
- Assuming the mountain weather shown in marketing photos is the weather the user will get.
- Building scenic-train days as if they were quick transfers instead of full-day experiences.
- Underestimating how hard peak summer and ski-season hotel pricing hits famous alpine bases.
- Assuming EU roaming, EU customs, and euro pricing rules apply automatically in Switzerland.

## Security & Privacy

**Data that stays local:** Trip preferences, route decisions, and deadlines in `~/switzerland/`

**This skill does NOT:** Access files outside `~/switzerland/` or make network requests.

**Memory rule:** Keep local trip notes only when the user is doing ongoing Switzerland planning or clearly wants continuity across sessions. For one-off answers, help without creating extra trip memory.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `europe` — Better wider-Europe context when Switzerland is part of a longer route
- `booking` — Reservation workflows and confirmation hygiene
- `car-rental` — Better self-drive strategy and handoff logistics
- `food` — Deeper restaurant and cuisine planning

## Feedback

- If useful: `clawhub star switzerland`
- Stay updated: `clawhub sync`
