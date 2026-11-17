# Wishlist — Turning "Someday" Into A Date

**Contents:** [What A Usable Entry Contains](#what-a-usable-entry-contains) · [Choosing The Next Trip](#choosing-the-next-trip) · [Season Is A Calendar Problem, Not A Weather One](#season-is-a-calendar-problem-not-a-weather-one) · [Windows That Open Once](#windows-that-open-once) · [Cost Bands Before Research](#cost-bands-before-research) · [Killing Entries](#killing-entries)

**Before adding or ranking anything**, read `## Wishlist` and `## Trips` in `~/Clawic/data/travel/memory.md` — or `destinations.md` if the `## Boxes` index points there. Half of what people call a new idea is a place they already went, or already ruled out for a reason worth remembering.

## What A Usable Entry Contains

A place name is not an entry. Six fields, and the entry is decision-ready the day a window appears:

| Field | Why it is the one that matters |
|---|---|
| Why | One line, in their words. It decides the shape of the trip and, later, whether the trip delivered |
| Best window | Month range, plus what makes it that range — festival, season, crowd, price |
| Rough cost | Band with currency, party size and the date estimated. A number from three years ago is not a number |
| Duration | The minimum that makes the flight worth it, and the ideal. "3 days minimum, 8 ideal" is actionable; "a week or two" is not |
| Blocker | The single thing that stops it: lead time on a permit, a passport, a season, someone else's calendar, money |
| Source | Who or what put it on the list. "Marta's photos" is how you find out what they actually want to see |

The blocker field is the one that turns the list into a plan: sorted by blocker, the list says what to do this month rather than what to dream about.

## Choosing The Next Trip

Four constraints. The one with the least give decides, and it is almost never money.

1. **Window** — the actual free dates, from the calendar, not from optimism. A trip needs the days plus a recovery day at each end for anything long-haul.
2. **Season** — which wishlist entries have their window overlapping those dates. This eliminates faster than anything else and nobody checks it first.
3. **Company** — who is coming determines pace, budget and half the destination list (`companions.md`).
4. **Money** — the band from the entry, scaled by `trip_style`, against `daily_budget`.

Present two or three survivors with their totals and the one line that separates them, never a ranked list of ten. If nothing survives, say which constraint to relax and what it buys: usually moving the dates two weeks makes an impossible trip ordinary.

**Shortlist rule of thumb**: long-haul earns its cost above roughly 8-10 nights; under 4 nights, the flight time is a larger fraction of the trip than the trip. Short-haul inverts it — a 3-night European city break works, a 10-day one usually turns into a different, better trip somewhere else.

## Season Is A Calendar Problem, Not A Weather One

Price and crowd track **school holidays and the local festival calendar**, not the forecast. Three calendars to check before fixing dates, in this order:

- **The destination's school holidays**, and those of the countries that holiday there. August in the Mediterranean is not expensive because of the sun.
- **Public holidays and festivals at the destination**: some are the reason to go, some close everything for a week. Golden Week, Lunar New Year, Ramadan and Obon change availability, prices and opening hours far more than weather does.
- **Your own origin's holidays**, which set the fare on the days you can actually leave.

**Shoulder season** is the month either side of peak: most of the experience, materially less crowd and price, with the risk being a specific attraction closed for the season. Check the one thing they came for is open before recommending it — a shoulder-season trip to a place whose single draw is shut is worse than peak.

Rainy season is under-feared in some places and over-feared in others: an afternoon monsoon that clears by five is a scheduling constraint; a wet season that closes roads and cancels boats is a trip cancellation. Which one it is belongs in the entry.

## Windows That Open Once

Anything with finite capacity and a release date is booked the day it opens, whatever else is undecided (SKILL.md Rule 4). Put the release date in `## Due` the moment the entry goes on the list:

- Hiking permits and national-park quotas (Inca Trail, Half Dome, Kilimanjaro routes, some Japanese and Norwegian huts) — often months ahead and gone in hours
- Award seats: most airlines load schedules 330-360 days out, and award inventory is best at release and again in the last two weeks
- Single-property destinations: the one lodge in the reserve, the one ryokan in the valley
- Festival tickets and their accommodation, which sells before the tickets do
- Restaurant reservations that open on a fixed day, typically 30-90 days ahead at a fixed hour, local time
- Visa appointment slots, where the wait for the appointment dwarfs the processing time (`documents.md`)

## Cost Bands Before Research

A band with a date beats a precise number that is stale. Build it from `## Spend Baselines` if the region is already known, otherwise from a per-day estimate plus transport:

`band = transport (both ways, both people) + nights × lodging rate + days × daily rate + the fee stack`

Give it as a range with a ±20% honesty margin and the month it was made. When the same place gets revisited, the actual from the trip dossier replaces the estimate and the baseline updates — that is the whole reason the archive exists.

## Killing Entries

A wishlist that only grows stops being read. Review it against seasons at the cadence in `## Due`, and at each review:

- Entries whose reason has expired (the exhibition closed, the friend moved home) come off, with one line saying why — that line stops it being re-added in six months
- Entries blocked by the same thing for three reviews get their blocker escalated to a task or are cut
- Somewhere they have now been moves to `## Trips` and, if it is worth returning to, becomes a place file in `artifacts/`

**After adding, ranking or killing an entry**, write it in the same turn: the row in `## Wishlist` in `memory.md` (or `destinations.md` once it has split), and in `## Due` both any release date and the review date as the `Last run` of the wishlist-review row. Format and thresholds: `memory-template.md`.
