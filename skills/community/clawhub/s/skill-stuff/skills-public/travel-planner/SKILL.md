---
name: travel-planner
description: Plans trips end-to-end covering research, flights, hotels, itinerary, packing list, and local tips. Use when a user is planning any trip.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
allowed-tools: web_search web_fetch
metadata:
  openclaw.emoji: "✈️"
  openclaw.user-invocable: "true"
  openclaw.category: life-admin
  openclaw.tags: "travel,trips,flights,hotels,itinerary,planning,packing"
  openclaw.triggers: "plan a trip,I'm going to,book flights,travel plans,help me plan my trip,what should I pack"
  openclaw.homepage: https://clawhub.com/skills/travel-planner


# Travel Planner

Tell it where you're going and when. It does the rest.

Research, flights, hotels, day-by-day itinerary, what to pack, what to know before you land.
Integrates with your calendar. Updates appointment-manager with any bookings made.

---

## File structure

```
travel-planner/
  SKILL.md
  preferences.md     ← travel style, budget, airlines, hotel preferences
  trips/
    [DESTINATION]-[DATE].md    ← one file per trip
```

---

## Setup flow (one-time)

### Step 1 — Travel preferences

Ask once. Store in preferences.md. All future trips use this.

**Style:**
- Budget / mid-range / comfortable / luxury?
- City break / nature / culture / mix?
- Prefer a plan or prefer to figure it out as you go?

**Flights:**
- Any preferred airlines or alliances?
- Seat preference (aisle/window)?
- Max connections? Max total journey time?
- Home airport(s)?

**Hotels:**
- Prefer central location or quieter/cheaper?
- Any hotel groups you're loyal to?
- Private room always, or open to apartments/airbnb?

**Food:**
- Dietary requirements?
- Any cuisines to prioritise or avoid?

**Budget range:**
- Rough per-day budget for accommodation?
- Rough total budget for a typical trip?

### Step 2 — Write preferences.md

```md
# Travel Preferences

## Style
[description of travel style]

## Flights
home airports: [list]
preferred airlines: [list]
max connections: [N]
seat: [aisle/window]

## Hotels
location: [central/flexible]
style: [hotel/apartment/flexible]
budget per night: [range]

## Food
dietary: [requirements]
priorities: [cuisines / types]

## Budget
typical daily budget: [range]
```

---

## Trip planning flow

When user says "plan a trip to X" or "I'm going to X from [DATE] to [DATE]":

### Step 1 — Clarify what's needed

Ask (briefly, max 2 questions):
- Is this leisure or business? (affects itinerary style)
- What's the rough budget?
- Solo, couple, family, group?
- Anything specific they want to do — a concert, a restaurant, a hike?
- What's already booked (flights? hotel?) and what needs doing?

### Step 2 — Research the destination

web_search for:
- Current travel requirements (visa, entry rules, health)
- Best areas to stay for their travel style
- Transport from airport
- What's worth doing in the time they have
- Any events or festivals during their dates
- Anything to know right now (strikes, construction, seasonal factors)

### Step 3 — Find flights (if needed)

Search for flights matching preferences:
- Home airport to destination
- Dates ± 1 day if flexible
- Sorted by: best combination of price, duration, connections

Present top 3 options:
> **Option 1:** [AIRLINE] · [DEPARTURE] → [ARRIVAL] · [DURATION] · [PRICE]
> [Any notable details — direct, good seat selection, etc.]

Ask: "Want me to find the booking link, or will you book directly?"
If booking link: use web_fetch to find the direct booking URL.

### Step 4 — Find accommodation (if needed)

Search based on preferences:
- Location: central neighbourhood or near specific area they mentioned
- Style and budget from preferences.md
- Dates

Present 3 options with:
- Name, price per night, location, key features
- Direct booking link
- Any warnings (bad reviews, far from transport, etc.)

### Step 5 — Build the itinerary

Day-by-day plan based on:
- Duration of trip
- Their travel style (planned vs loose)
- What they said they wanted to do
- Logical geographic grouping (don't send them across the city twice)

Format:

**Day 1 — [DATE] · Arrival**
- [TIME]: Land at [AIRPORT], [transport to accommodation]
- [TIME]: Check in at [HOTEL]
- Evening: [recommendation for first evening — easy, close, no jet lag]

**Day 2 — [DATE] · [Theme]**
- Morning: [activity] — [why / practical note]
- Afternoon: [activity]
- Evening: [restaurant recommendation] — [one sentence on why]

Keep it loose for leisure trips. Tighter for short city breaks.
Always include one "if you have time" option per day.

### Step 6 — Packing list

Generated based on:
- Destination climate and season (web_search for weather forecast if dates are soon)
- Duration
- Activities planned
- Travel style

Not a generic list. A specific one.
"4 days in Berlin in November" gets a different list than "10 days in Thailand in March."

### Step 7 — Need to know

5-7 bullet points. Things that would have been annoying to discover on arrival.

> • Entry: [visa requirement or entry rule]
> • Currency: [cash vs card situation]
> • Transport: [how to get around — app, card, etc.]
> • Tipping: [local norm]
> • Safety: [anything to be aware of — specific to destination]
> • Language: [key phrases if useful]
> • One local thing: [something that makes the destination what it is]

### Step 8 — Write trip file

Create `trips/[DESTINATION]-[DATE].md` with the full plan.
Add trip to calendar if Google Calendar is connected.
Add any bookings made to appointment-manager if installed.

---

## Pre-trip checklist

48 hours before departure, send a reminder:

> ✈️ **[DESTINATION] in 2 days**
>
> **To check:**
> • Passport validity
> • Online check-in opens [DATE] (if flight known)
> • [Any visa or entry requirement if applicable]
> • Download offline maps for [DESTINATION]
> • Local currency — [note]
>
> **Your trip file:** `/trip [DESTINATION]`

---

## Management commands

- `/trip [destination] [dates]` — start planning a trip
- `/trip [destination]` — view existing trip plan
- `/trip checklist [destination]` — show pre-trip checklist
- `/trip add [destination] [note]` — add a note to an existing trip
- `/trip packing [destination]` — regenerate packing list
- `/trip update [destination] [change]` — update plans
- `/trip past` — list past trips

---

## Integration with other skills

**appointment-manager:**
Any flights or hotels booked via the skill get logged as appointments with the full reminder chain.

**morning-briefing:**
Trip dates appear in the morning briefing starting 7 days before departure.

**calendar:**
Trip added as a multi-day event with itinerary summary in the description.

---

## What makes it good

The "need to know" section is the most immediately useful output.
Entry requirements, tipping, transport apps, currency — these are the things that actually
affect the first hour of a trip.

The itinerary should be loose enough to be usable but structured enough to save decisions.
The goal is not a minute-by-minute schedule — it's a frame that makes spontaneity easier,
not harder.

The pre-trip reminder 48 hours out is when people actually need it.
Not two weeks before. 48 hours before, when packing starts.
