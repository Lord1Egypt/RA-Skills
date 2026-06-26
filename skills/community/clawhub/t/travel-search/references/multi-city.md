# Multi-City Optimizer — Cheapest Route Across Multiple Destinations

Find the optimal order and routing for trips with 2+ cities.

## When to Use

- "I want to visit Rome, Paris, and Amsterdam in 10 days"
- "What's the cheapest order to do Barcelona → Prague → Berlin?"
- "Plan a 3-week Europe trip hitting London, Lisbon, and Athens"
- "Eurotrip with 5 cities, what's the best route?"

## The Problem

With N cities, there are N! possible orderings. For 4 cities that's 24 routes. For 5 it's 120. Checking every combination by searching flights would be too many API calls. Instead, use a smart heuristic.

## Optimization Strategy

### Step 1: Collect Cities

Extract all destinations from the user request. Also note the **origin** (home city) since the trip starts and ends there.

### Step 2: Build Price Matrix

For N cities, search the key inter-city flights to build a rough price map. Focus on:

1. **Origin → each city** (potential first stops)
2. **Each city → origin** (potential last stops)
3. **Between adjacent/likely pairs** (not every permutation)

Use Kiwi for this — it handles city names directly and returns quickly. Use a fixed date for comparison (midpoint of their travel window).

For 3 cities (A, B, C) from origin O, search:
```
O→A, O→B, O→C          (3 outbound options)
A→B, A→C                (2 inter-city from A)
B→A, B→C                (2 inter-city from B)
C→A, C→B                (2 inter-city from C)
A→O, B→O, C→O          (3 return options)
```
Total: 13 searches for 3 cities. Manageable.

For 4+ cities, reduce by only checking geographically sensible pairs:
- Cluster nearby cities (Rome+Barcelona = Southern Europe cluster)
- Search within clusters + between cluster endpoints
- Skip obviously bad routes (don't fly London→Athens→London→Rome)

### Step 3: Score Routes

For each viable route ordering, calculate:

```
Route cost = sum of all flight segments
Route time = sum of flight durations + layover time
```

**Geographic logic bonus:** Routes that flow geographically (west→east, north→south, or in a loop) get a bonus because:
- Fewer backtrack flights
- More logical travel flow
- Often cheaper due to shorter distances

### Step 4: Allocate Days

Distribute days across cities based on:

**City size heuristic:**
- Major capital / mega-destination (Paris, Tokyo, London, NYC): 3-4 days minimum
- Mid-size destination (Barcelona, Prague, Lisbon, Amsterdam): 2-3 days
- Small city / day-trip-able (Toledo, Bruges, Sintra): 1 day
- Transit/stopover: 0.5-1 day

**User preferences override:** If user says "I want more time in Rome", respect that.

**Travel days:** Each inter-city flight burns ~half a day. Account for this.

Formula:
```
Available activity days = total days - (number of flights × 0.5)
Distribute proportionally by city importance, respecting minimums.
```

### Step 5: Present the Optimized Route

```
🗺️ MULTI-CITY TRIP — [N] cities, [D] days

📍 Optimized route:
[Origin] → City 1 (X days) → City 2 (X days) → City 3 (X days) → [Origin]

✈️ Flights:
1. [Origin] → City 1 | [date] | $XX — [link]
2. City 1 → City 2 | [date] | $XX — [link]
3. City 2 → City 3 | [date] | $XX — [link]
4. City 3 → [Origin] | [date] | $XX — [link]
Total flights: $XXX

💡 Why this order:
- [Reason: geographic flow, cheapest combo, etc.]
- Saved $XX vs reverse order
- Alternative: [other route] would cost $XX more but [trade-off]

📅 Day allocation:
- City 1: [X] days ([dates])
- City 2: [X] days ([dates])
- City 3: [X] days ([dates])
```

Then generate a day-by-day itinerary for each city using the trip planner workflow (see `references/trip-planner.md`).

## Optimization Rules

1. **Always start from origin and return to origin** unless user specifies one-way.
2. **Minimize backtracking.** Rome→Paris→Barcelona is better than Rome→Barcelona→Paris (geographically).
3. **Check hub cities.** If a city is a major hub (London, Frankfurt, Istanbul, Dubai), it may be cheaper as first or last stop due to more flight options.
4. **Consider open-jaw.** Flying into City A and out of City C (without returning to A) is often cheaper than a loop. Present this option when relevant.
5. **Budget airlines between nearby cities.** Intra-Europe, budget carriers (Ryanair, EasyJet, Vueling) dominate short hops. Kiwi excels at finding these.
6. **Train alternatives for short hops.** Paris→Amsterdam, Barcelona→Madrid, Rome→Florence — sometimes the train is better. Mention when distance is <500km.
7. **Don't over-optimize.** If two routes differ by <$20, recommend the one with better flow/convenience, not the marginally cheaper one.

## Edge Cases

**2 cities:** Simple. Search Origin→A→B→Origin vs Origin→B→A→Origin. Pick cheaper.

**5+ cities:** Group into 2-3 geographic clusters. Optimize cluster order, then city order within clusters. This reduces search space dramatically.

**Flexible dates:** If user is flexible, search the cheapest departure date for the first leg, then build forward from there.

**One-way / no return:** User relocating or continuing elsewhere. Skip return leg, optimize the chain only.

**Mixed transport:** For short hops (<500km), mention train/bus as alternative. "Rome→Florence: $85 flight OR $35 train (1.5h, city-center to city-center)."
