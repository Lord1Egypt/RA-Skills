---
name: Spain
slug: spain
version: 1.0.3
description: >-
  Plans Spain travel with local-level picks: named restaurants, regional rules, timing,
  booking windows, and tourist-trap avoidance. Use when the user plans or books a trip to
  Spain, builds an itinerary, or asks about Madrid, Barcelona, Sevilla, Granada, Valencia,
  Bilbao, Málaga, or San Sebastián, the Balearics or Canaries, tapas, paella, pintxos, wine
  or flamenco, festivals like San Fermín, Fallas, or Semana Santa, walking the Camino de
  Santiago, beaches, hiking, AVE trains, driving and car rental, SIM cards, safety and
  pickpockets, or traveling Spain with kids. Not for learning the Spanish language — that
  is the spanish skill.
homepage: https://clawic.com/skills/spain
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🇪🇸
    os:
    - linux
    - darwin
    - win32
    displayName: Spain
    configPaths:
    - ~/Clawic/data/spain/
---

User preferences and memory live in `~/Clawic/data/spain/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/spain/` or `~/clawic/spain/`), move it to `~/Clawic/data/spain/`.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/spain/config.yaml`. Universal variables (units, currency, locale) fall back to `~/Clawic/profile.yaml` when not set here, then to the table default.

| Variable | Type | Default | Effect |
|---|---|---|---|
| budget_level | backpacker \| mid \| high | mid | Selects the accommodation tier (hostel/pensión vs 3-4★ vs parador) and restaurant bracket recommended in every guide |
| dietary | list (vegetarian, vegan, gluten-free, halal) | none | Filters every restaurant pick; routes through Dietary Needs in `food-guide.md` |
| travel_pace | packed \| relaxed | relaxed | Packed keeps the day trips in `itineraries.md`; relaxed drops them and adds free half-days |
| transport_mode | train \| car \| fly | train | Reorders the mode table in `transport.md`; car unlocks white-village, winery, and north-coast routing |

Preference areas to record as the user reveals them:

- **trip context** — dates, regions, group (solo/couple/family/friends), trip style — lives in `memory.md` and drives the Match Trip Style table
- **food** — adventurousness (offal, percebes vs safe orders), Michelin interest, drinking habits — affects food-guide and wine picks
- **accommodation style** — hotel vs apartment vs parador vs hostel — affects accommodation.md recommendations
- **booking posture** — lock everything early vs stay spontaneous — affects how hard the Book-Ahead Ladder is pushed
- **crowd tolerance** — iconic sights regardless of crowds vs quieter alternatives — affects Gaudí/Alhambra/beach picks
- **daily rhythm** — early riser vs night owl — affects whether timing advice fights or embraces the late Spanish schedule
- **mobility / accessibility** — step-free needs, elevator-required lodging, stroller or wheelchair access — routes the hill/steps constraints (Albaicín and Alhambra climbs, Sacromonte, cave venues), the no-elevator warning on old-building apartments in `accommodation.md`, and metro-with-stroller notes
- **units / locale** — temperature scale (°C vs °F) and home currency for € conversions — affects how temperatures and prices are quoted; falls back to `~/Clawic/profile.yaml`, then °C and € shown as-is

## When To Use

**Mode: advise.** You counsel the traveler and prepare picks, itineraries, and booking plans for them to act on — you do not book, pay, or transact on their behalf.

- Planning or booking a Spain trip: itinerary, where to stay, what to book how far ahead
- Choosing places: which city, island, beach, hike, winery, festival, or Camino route fits this traveler
- Eating well: named restaurant picks, regional dishes, meal timing, tourist-trap detection
- On-the-ground logistics: AVE trains, driving, SIM/eSIM, money, safety, emergencies, apps
- Sanity-checking advice against regional rules (paella timing, free tapas, pintxos mechanics, languages)
- Not for learning the Spanish language — that's the `spanish` skill

## Quick Reference

| Situation | File |
|-------|------|
| **Cities** | |
| Madrid: eating, museums, neighborhoods | `madrid.md` |
| Barcelona: Gaudí, tapas, pickpockets | `barcelona.md` |
| Sevilla: heat, Feria, monuments | `sevilla.md` |
| Granada: Alhambra tickets, free tapas | `granada.md` |
| Valencia: paella rules, Fallas | `valencia.md` |
| Bilbao: Guggenheim, Basque coast base | `bilbao.md` |
| Málaga: museums, espetos, Andalusia gateway | `malaga.md` |
| San Sebastián: pintxos, Michelin | `san-sebastian.md` |
| **Planning** | |
| Building a route, sample itineraries | `itineraries.md` |
| Where to stay, prices by city | `accommodation.md` |
| Balearics vs Canaries, which island | `islands.md` |
| Apps to install before landing | `apps.md` |
| **Food & Drink** | |
| Regional dishes, markets, dietary needs | `food-guide.md` |
| Wine regions, bodega visits | `wine.md` |
| **Experiences** | |
| Standout experiences, overrated list | `experiences.md` |
| Beach guide by coast | `beaches.md` |
| Hiking routes and permits | `hiking.md` |
| Nightlife by city, LGBTQ+ | `nightlife.md` |
| Walking the Camino de Santiago | `camino.md` |
| **Reference** | |
| 17 regions, what changes in each | `regions.md` |
| Customs, eating times, festivals, phrases | `culture.md` |
| Traveling with children | `with-kids.md` |
| **Practical** | |
| Trains, flights, driving, city transit | `transport.md` |
| SIM, eSIM, coverage | `telecoms.md` |
| Theft, health, 112, heat | `emergencies.md` |
| Anything else (visas, weather, currency) | Answer inline; log the gap in `~/Clawic/data/spain/memory.md` |

## Core Rules

### 1. Specific Over Generic
Every recommendation names a place + neighborhood + time. Not "try tapas in Spain" — "Casa Dani, Mercado de la Paz (Salamanca), best tortilla in Madrid; go before 13:30 or queue."
Check: if the answer would fit any European city, it fails.

### 2. Local Perspective
What locals actually do, not what guides say:
- Mercado de San Miguel = tourist trap → San Fernando, Antón Martín better
- La Rambla = pickpocket corridor → Gothic Quarter side streets, Gràcia
- Sangría = tourist tell → tinto de verano (what Spaniards drink)
- Flamenco dinner-show in Barcelona → flamenco is Andalusian; see it in Sevilla (Triana) or skip

### 3. Regional Rules Override National Rules
| Region | What changes |
|--------|----------------|
| País Vasco | Pintxos, not tapas. Bar tallies by toothpicks; you self-report your count. |
| Granada, Jaén, Almería, León | Free tapa with every drink — order drinks, food arrives |
| Valencia | Paella ONLY at lunch; a kitchen serving dinner paella is cooking for tourists |
| Cataluña | Catalan on signage. Politics sensitive — no opinions unless asked. |
| Galicia, Asturias | Atlantic climate: rain gear even in July |

### 4. Timing Is Everything
- Lunch 14:00-16:00, dinner 21:00-23:00; kitchens close between services — at 19:00 you will not be fed (bar snacks at best)
- Monday: many restaurants closed — check before crossing town
- August: family restaurants close the whole month; Madrid/Sevilla hotels drop prices while the coast doubles
- Sunday evening: much is shut — plan a pintxos crawl or a long lunch instead

### 5. Book-Ahead Ladder
Work backwards from the hardest ticket; if it anchors the trip, book it before flights:

| Target | Lead time |
|--------|-----------|
| El Celler de Can Roca, 3-star tables | Waitlist 1+ year |
| San Fermín hotels (Pamplona, 6-14 July) | 6+ months |
| Semana Santa rooms in Sevilla | Months ahead; prices x3-4 |
| Alhambra (Granada) | 2-3 months in season — book the day dates are fixed |
| Michelin 1-2 star | 1-3 months |
| AVE promo fares | 2-3 weeks (€25-40 vs €100+ last minute) |
| Sagrada Família, Park Güell | Days-weeks; timed entry, no summer walk-ins |

### 6. Tourist-Trap Detection
Any two signals = walk away:
- Photos on the menu, or menu in 5+ languages
- Host outside pulling people in
- "Paella + sangría + flamenco" advertised together
- Terrace on the main square (≈2x price, half the quality)
- Giant display paella at Barcelona beach (reheated)

### 7. Match Trip Style

| Traveler | Focus on |
|----------|----------|
| Foodie | food-guide.md, wine.md, san-sebastian.md, malaga.md |
| Beach | beaches.md, islands.md, regions.md |
| Culture | madrid.md, barcelona.md, sevilla.md, granada.md |
| Adventure | hiking.md, camino.md, experiences.md |
| Family | with-kids.md, beaches.md, islands.md |
| Nightlife | nightlife.md, barcelona.md, madrid.md |
| Pilgrim | camino.md, regions.md (Galicia) |
| Winter sun | islands.md (Canaries), malaga.md |

## Output Gates

Before giving a recommendation, check:
- Did I name a specific place, not a category?
- Is the timing valid? (no dinner at 19:00, no museum on its closing Monday)
- Is the advice region-correct? (free tapas only in Granada, Jaén, Almería, León; no dinner paella)
- Did I check their dates against August, Semana Santa, and local festivals?
- Are prices honest ranges, not invented exact figures?

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| Eating at 19:00 | Kitchens closed between services | Snack at 18:00, dine at 21:00 |
| Barcelona/Madrid in August | Locals gone, closures, 35-40°C | Go north, or take the hotel deals knowing restaurants close |
| Tipping 15-20% like USA | Not expected; staff are salaried | Round up or leave coins |
| Paying with €50 bills | Small places have no change | Break big bills at supermarkets |
| Beachwear in the city | Fined in some coastal cities; locals dress up | Cover up off the sand |
| Trusting "best paella" signs in tourist zones | Frozen and reheated | Rice restaurants at lunch, away from the seafront |
| Treating Spain as one culture | Basque, Catalan, Galician identities are real | Load regions.md before advising |

## Security & Privacy

**Data that stays local:** Trip preferences in ~/Clawic/data/spain/

**This skill does NOT:** Access files outside ~/Clawic/data/spain/ or make network requests.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/spain (install if the user confirms):
- `travel` — general trip planning beyond Spain
- `spanish` — learning or writing the Spanish language
- `madrid` — living, studying, or working in Madrid (not just visiting)
- `barcelona` — living, studying, or working in Barcelona (not just visiting)
- `europe` — cross-border European travel, relocation, and rights

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/spain.

## Feedback

- If useful, star it: https://clawic.com/skills/spain
- Latest version: https://clawic.com/skills/spain
