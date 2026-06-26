---
name: Taiwan
slug: taiwan
version: 1.0.0
homepage: https://clawic.com/skills/taiwan
description: Plan Taiwan trips with city-specific food, rail, hot spring, and regional tips that avoid tourist filler and logistics mistakes.
changelog: Initial release with city guides, rail planning, tea context, and practical Taiwan travel advice.
metadata: {"clawdbot":{"emoji":"🇹🇼","requires":{"bins":[],"config":["~/taiwan/"]},"os":["linux","darwin","win32"]}}
---

## When to Use

User planning a trip to Taiwan or needing practical local guidance: where to base, what each city does best, how to move around, what to eat, and what to avoid in weather-sensitive or holiday-sensitive periods.

## Architecture

Memory lives in `~/taiwan/`. If `~/taiwan/` doesn't exist or is empty, read `setup.md` and start naturally. See `memory-template.md` for structure.

```text
~/taiwan/
└── memory.md     # Trip context
```

## Quick Reference

| Topic | File |
|-------|------|
| **Cities** | |
| Taipei neighborhoods, rhythm, day trips | `taipei.md` |
| Taichung pacing, design, central hub strategy | `taichung.md` |
| Tainan food-first old-town planning | `tainan.md` |
| Kaohsiung harbor districts and southern base logic | `kaohsiung.md` |
| **Planning** | |
| First-timer and repeat-visitor routes | `itineraries.md` |
| Best base by budget and trip style | `accommodation.md` |
| Rail, maps, taxi, bike, and booking apps | `apps.md` |
| **Food & Drink** | |
| Regional dishes, breakfasts, night markets | `food-guide.md` |
| Tea regions, what to buy, how to order | `tea.md` |
| **Activities** | |
| Hot springs, scenic rides, cultural wins | `experiences.md` |
| Best beaches, islands, and swim realities | `beaches.md` |
| Easy urban hikes to alpine planning logic | `hiking.md` |
| Night markets, bars, music, late-night rhythm | `nightlife.md` |
| **Reference** | |
| North, central, south, east, islands breakdown | `regions.md` |
| Etiquette, payment reality, timing, temple manners | `culture.md` |
| Family travel pacing and kid-friendly structure | `with-kids.md` |
| **Practical** | |
| HSR, TRA, airport access, buses, driving | `transport.md` |
| SIMs, eSIMs, LINE, payment and data habits | `telecoms.md` |
| Emergency numbers, typhoon, earthquake, clinics | `emergencies.md` |

## Core Rules

### 1. Choose the Corridor Before the Wishlist
Don't say "see all of Taiwan in six days." Say "Use the west coast HSR spine for Taipei-Taichung-Tainan-Kaohsiung, and only add the east coast if you have extra days and weather flexibility."

### 2. Match the Base to the Trip
Taiwan is compact, but sleeping in the wrong place wastes the trip:
- Taipei for first-timers, museums, nightlife, and easy transit
- Taichung for a softer pace, cafes, and central Taiwan branching
- Tainan for food and history, not for a rushed checklist
- Kaohsiung for winter sun, harbor walks, and southern side trips

### 3. Transport Strategy Beats Distance Math
Use the right rail layer:
- HSR for long west-coast jumps
- TRA for east coast, local hops, and smaller cities
- MRT, YouBike, taxi, and walking for the last mile
- Car only when the plan is rural, alpine, or island-heavy

### 4. Timing Changes the Whole Experience
- Lunar New Year, long weekends, and major festivals reshape availability and crowd levels
- Summer means heat, humidity, and typhoon risk
- Winter is best for southern cities and many hot-spring trips
- Rain can destroy mountain or coast plans fast, so always give a backup

### 5. Taiwan Rewards Specific Food Advice
Don't say "try a night market." Say which city, which neighborhood, and what it is good for:
- Taipei for breadth and late convenience
- Tainan for breakfast, snacks, and old-school specialties
- Taichung for cafes and dessert stops
- Kaohsiung for duck rice, seafood, and easygoing evening eating

### 6. Call Out the Real Friction Points
Be explicit about what visitors routinely miss:
- Cash still matters at small stalls and local shops
- The biggest night market is not always the best one
- East coast and mountain plans need weather checks
- A scenic place that looks close on the map may still be a half-day move

### 7. Match the Traveler

| Traveler | Focus on |
|----------|----------|
| First-timer | `taipei.md`, `itineraries.md`, `transport.md`, `food-guide.md` |
| Food-first | `tainan.md`, `food-guide.md`, `tea.md`, `culture.md` |
| Relaxed repeat visitor | `taichung.md`, `regions.md`, `experiences.md` |
| Southern sun | `kaohsiung.md`, `beaches.md`, `nightlife.md` |
| Family | `with-kids.md`, `accommodation.md`, `transport.md` |

## Common Traps

- Trying to do Taipei, Sun Moon Lake, Tainan, Kaohsiung, and the east coast in one short trip
- Assuming every famous night market is worth the detour
- Booking east-coast or mountain days with zero weather backup
- Treating Taipei and Tainan like the same speed of city
- Relying on cards only, then getting stuck at cash-first spots
- Assuming rail solves the last mile everywhere
- Planning alpine or beach days without checking current conditions

## Security & Privacy

**Data that stays local:** Trip preferences in `~/taiwan/`

**This skill does NOT:** Access files outside `~/taiwan/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — Travel planning
- `food` — Food and cooking
- `chinese` — Chinese language
- `photography` — Travel photography and location planning

## Feedback

- If useful: `clawhub star taiwan`
- Stay updated: `clawhub sync`
