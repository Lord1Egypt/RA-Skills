---
name: Romania
slug: romania
version: 1.0.0
homepage: https://clawic.com/skills/romania
changelog: "Initial release with regional trip logic, city playbooks, mountain and Black Sea guidance, and practical local execution."
description: Plan Romania trips with regional contrasts, Transylvania and Black Sea logistics, local food cues, and practical local guidance.
metadata: {"clawdbot":{"emoji":"🇷🇴","requires":{"bins":[],"config":["~/romania/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/romania/` does not exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Romania trip and needs help that goes beyond generic Europe advice: route shape, regional differences, local food, mountain and seaside timing, practical logistics, and what is worth skipping.

## Architecture

Memory lives in `~/romania/`. If `~/romania/` does not exist or is empty, run `setup.md`. See `memory-template.md` for structure.

```text
~/romania/
└── memory.md     # Trip context, route logic, and evolving constraints
```

## Quick Reference

Use this map to load only the Romania subtopic that changes the decision in front of you.

| Topic | File |
|-------|------|
| **Cities** | |
| Bucharest entry hub and urban strategy | `bucharest.md` |
| Brasov and first Transylvania base | `brasov.md` |
| Cluj-Napoca for cafes, festivals, and western access | `cluj-napoca.md` |
| Sibiu for slower culture and southern Transylvania | `sibiu.md` |
| **Planning** | |
| Region choice and route logic | `regions.md` |
| Sample itineraries for 3-10 days | `itineraries.md` |
| Where to stay by trip style | `accommodation.md` |
| Essential travel apps | `apps.md` |
| **Food and Drink** | |
| Dishes, markets, and restaurant logic | `food-guide.md` |
| Wine regions, tuica, palinca, and ordering cues | `wine.md` |
| **Experiences** | |
| High-value Romania experiences | `experiences.md` |
| Black Sea coast and Danube Delta choice | `black-sea.md` |
| Carpathian hiking and mountain safety | `carpathians-and-hiking.md` |
| **Reference** | |
| Culture, etiquette, and language cues | `culture.md` |
| Family travel and mixed-age planning | `with-kids.md` |
| **Practical** | |
| Trains, buses, driving, and route tradeoffs | `transport.md` |
| SIMs, data, and roaming | `telecoms.md` |
| Safety, health, and emergency response | `emergencies.md` |
| Setup process | `setup.md` |
| Memory structure | `memory-template.md` |

## Core Rules

### 1. Route by Region, Not by Castle Count
Romania works best when the trip has one dominant shape:
- Bucharest plus Brasov for first-timers
- Southern Transylvania for pretty towns and mountain access
- Cluj plus Apuseni for a younger, western-facing trip
- Black Sea or Danube Delta only in warm-season windows

### 2. Specific Beats Generic
Do not say "visit Transylvania." Say which base, how many nights, what it unlocks, and what the tradeoff is:
- Brasov for easiest first trip and day trips
- Sibiu for slower old-town rhythm and southern routes
- Cluj for urban energy, festivals, and west-side access

### 3. Flag Tourist Traps and Overhyped Stops
Be explicit when something is popular but weak:
- Bran Castle is an icon, not the best castle experience
- Bucharest Old Town is good for a walk, noisy for sleeping
- Mamaia is for party energy, not the best quiet seaside
- Pele's Castle can justify a detour; random "Dracula" branding usually cannot

### 4. Treat Transport and Season as Core Planning Inputs
- Trains are best on some corridors, but not all
- Drives that look short on a map can be slow on mountain roads
- Black Sea logic changes sharply outside June to early September
- Winter mountain plans need backup options for fog, ice, and closures

### 5. Match the Trip Style Early

| Traveler | Best starting files |
|----------|---------------------|
| First-time culture trip | `bucharest.md`, `brasov.md`, `itineraries.md` |
| Food-led trip | `food-guide.md`, `wine.md`, `bucharest.md`, `sibiu.md` |
| Nature and hiking | `carpathians-and-hiking.md`, `regions.md`, `brasov.md` |
| Family trip | `with-kids.md`, `accommodation.md`, `black-sea.md` |
| Beach trip | `black-sea.md`, `transport.md`, `accommodation.md` |

### 6. Protect the User From Practical Friction
Always cover the execution details that break Romania trips:
- airport or rail entry point
- cash vs card expectations
- realistic transfer times
- weekday vs weekend crowd patterns
- when local verification is smart for hours, tickets, or weather

## Common Traps

- Treating Bucharest as the whole point of Romania instead of the transport hub
- Trying to combine Bucharest, Brasov, Sibiu, Cluj, the Black Sea, and the Delta in one short trip
- Booking Bran Castle as the centerpiece and skipping stronger town or mountain time
- Assuming every rail leg is efficient because the distance looks short
- Choosing Mamaia for a calm family beach week in peak party season
- Going into bear territory with food, poor timing, or zero trail planning
- Building Black Sea plans in shoulder season and expecting full-summer atmosphere

## Security & Privacy

**Data that stays local:** Trip preferences, route decisions, and saved constraints in `~/romania/`

**This skill does NOT:** Access files outside `~/romania/` or make network requests.

**Memory rule:** Keep local trip notes only when the user is actively planning Romania or clearly wants continuity across sessions. For one-off answers, help without creating extra trip memory.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `europe` — Better wider-Europe context when Romania is part of a longer route
- `food` — Deeper restaurant and cuisine planning
- `booking` — Reservation workflows and confirmation hygiene
- `family` — Extra support when multiple ages or family constraints drive the plan

## Feedback

- If useful: `clawhub star romania`
- Stay updated: `clawhub sync`
