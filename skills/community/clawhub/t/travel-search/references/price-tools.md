# Smart Price — Find the Best Deal, Every Time

The core philosophy: **best value = optimal intersection of price, quality, and convenience.** Not the cheapest. Not the most expensive. The smartest choice.

## Value Score System

Every option (flight, hotel, car) gets a mental **value score** based on:

```
Value = Quality ÷ Price × Convenience Factor
```

Where:
- **Quality:** rating, stars, airline reputation, reviews, amenities
- **Price:** total cost including hidden fees, taxes, baggage
- **Convenience:** duration, stops, location, check-in time, cancellation policy

The best option is the one with the **highest value score**, not the lowest price.

### Example — Flights
```
Option A: $120, 8h, 2 stops, budget airline, no baggage → score: low
Option B: $180, 4h, 1 stop, good airline, baggage included → score: HIGH ✅
Option C: $450, 3h, direct, premium airline → score: medium (overkill for most)
```
Recommend B. Mention A as budget alternative and C as premium option.

### Example — Hotels
```
Option A: $60/night, 6.5/10, far from center → score: low
Option B: $95/night, 8.8/10, walkable to everything → score: HIGH ✅  
Option C: $250/night, 9.2/10, luxury, pool, spa → score: medium (premium tier)
```
Recommend B. Mention A and C as alternatives.

## Price Calendar — Finding the Cheapest Dates

When user is flexible on dates ("when is it cheapest?", "sometime in June", "best time to go"):

### Method 1: Skiplagged Flex Calendar (fastest)

```bash
# Flexible departure dates
curl -s -X POST "https://mcp.skiplagged.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"initialize",
    "params":{"protocolVersion":"2025-06-18","capabilities":{},
    "clientInfo":{"name":"openclaw","version":"1.0"}}
  }' > /dev/null

curl -s -X POST "https://mcp.skiplagged.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":2,"method":"tools/call",
    "params":{"name":"sk_flex_departure_calendar","arguments":{
      "origin":"MAD",
      "destination":"FCO",
      "depart_date":"2026-06-01"
    }}
  }'
```

This returns a calendar grid showing the cheapest fare for each day around the target date. Present as:

```
📅 Cheapest dates to fly MAD → FCO in June:
- Jun 3 (Tue): $45 ← cheapest! 🔥
- Jun 4 (Wed): $52
- Jun 5 (Thu): $89
- Jun 10 (Mon): $48
- Jun 15 (Sun): $62
- Jun 20 (Fri): $112 (avoid weekends)
```

### Method 2: Skiplagged Return Calendar (round trip optimization)

After finding cheap departure dates, optimize the return:

```bash
curl -s -X POST "https://mcp.skiplagged.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":3,"method":"tools/call",
    "params":{"name":"sk_flex_return_calendar","arguments":{
      "origin":"MAD",
      "destination":"FCO",
      "depart_date":"2026-06-03",
      "trip_length":7
    }}
  }'
```

### Method 3: Kiwi Flex Range (±3 days)

```bash
# Search with departureDateFlexRange: 3 to check nearby dates
# See references/flights.md for full params
```

### Method 4: Skiplagged "Anywhere" (cheapest destination)

When user says "where should I go?" or "surprise me with something cheap":

```bash
curl -s -X POST "https://mcp.skiplagged.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":4,"method":"tools/call",
    "params":{"name":"sk_destinations_anywhere","arguments":{
      "origin":"MAD",
      "depart_date":"2026-06-01"
    }}
  }'
```

## Cross-Provider Comparison — The Core Engine

**Always search multiple providers and present the single best option.** This is what makes the skill valuable — the user doesn't have to check 4 websites.

### Flight Comparison Workflow

```
1. Search Kiwi (creative routing, budget airlines)
   ↓
2. Search Skiplagged (hidden city fares)
   ↓
3. Deduplicate (same route + similar time = same flight)
   ↓
4. Score each option (price × duration × stops × airline quality)
   ↓
5. Present: 🏆 Best Value + 💸 Cheapest + ⚡ Fastest
```

#### Execution — Parallel Search

Search both providers in one turn. Both are independent, no dependency:

**Kiwi:**
```bash
# Initialize + search (see references/flights.md)
# Sort by price, get top results
```

**Skiplagged:**
```bash
# Initialize + resolve IATA + search (see references/skiplagged.md)
# Get top results
```

#### Deduplication Rules

Two results are the "same flight" if:
- Same departure airport + arrival airport
- Departure time within 30 minutes
- Same number of stops

When duplicated: keep the cheaper one, note which provider had the better price.

#### Scoring Heuristic

For each unique flight, compute a mental value rank:

**Price weight: 40%** — lower is better, normalize within result set
**Duration weight: 30%** — shorter is better
**Stops weight: 15%** — fewer is better (0 stops = best, 2+ = worst)
**Convenience weight: 15%** — departure time (red-eye penalty), airline reputation, baggage included

Winner = highest combined score → label as 🏆 **Best Value**

### Accommodation Comparison Workflow

```
1. Search Skiplagged hotels
   ↓
2. Search Trivago hotels
   ↓
3. If apartments/homes/longer stay/group travel matter, also search Airbnb (see airbnb.md)
   ↓
4. Score by value, not price alone
   ↓
5. Present ONE best-value stay overall + hotel/Airbnb alternatives
```

#### Hotel Scoring

**Rating weight: 35%** — higher is better, minimum 7.0 for recommendations
**Price weight: 35%** — lower is better per night
**Location weight: 20%** — proximity to city center / user's vibe area
**Amenities weight: 10%** — WiFi, breakfast, pool, gym (bonus points)

Reject any hotel below 7.0 rating unless budget tier with nothing better.

#### Airbnb Scoring

Read `references/airbnb.md` for tool details. Use Airbnb especially when the user wants more space, a kitchen, group travel, longer stays, or neighborhood feel.

**Space/privacy weight: 30%** — entire place, bedrooms, common area
**Price weight: 25%** — nightly + total stay value
**Location weight: 20%** — neighborhood fit and convenience
**Amenities weight: 15%** — kitchen, washer, WiFi, workspace, AC, self check-in
**Policy/convenience weight: 10%** — cancellation, check-in ease, house rules

For solo short stays, hotels usually get a convenience bonus. For groups or 4+ nights, Airbnb often gets a value bonus.

### Car Rental Comparison

Only Skiplagged currently. Present sorted by price with car type noted:

```
🚗 Car Rentals [City] — [dates]
- Economy (Fiat 500): $25/day — [link]
- Compact (VW Golf): $32/day — [link]  ← 🏆 best value for most
- SUV (Nissan Qashqai): $48/day — [link]
```

## Presenting Comparison Results

Always lead with the **single best recommendation**, then alternatives:

```
🏆 BEST DEAL: [Flight/Hotel name]
   $XXX | [key details] | [why it's the best]
   🔗 Book: [link]

Also good:
- 💸 Cheapest: [option] — $XXX [trade-off note]
- ⚡ Fastest: [option] — $XXX [trade-off note]
- 💎 Premium: [option] — $XXX [what you get extra]
```

**Key rules:**
- **Never dump raw results.** Always curate, score, and recommend.
- **Explain the trade-offs.** "€30 cheaper but 4 hours longer" helps the user decide.
- **Include booking links for every option.** The user should be able to act immediately.
- **Flag hidden costs.** Budget airlines without baggage, hotels without breakfast, car rentals without insurance.
- **Mention price trends if relevant.** "Prices for this route are typically €X cheaper in [month]."

## Price Alert Patterns

When a deal is exceptionally good, flag it:

```
🔥 DEAL ALERT: This is 40% below average for this route!
```

Use these rough benchmarks for "good deal" detection:
- Intra-Europe flights under €50 one-way = great deal
- Transatlantic flights under $400 round trip = great deal
- Asia flights under $600 round trip from Europe = great deal
- Hotels in major cities under $80/night with 8+ rating = great deal

## Decision Tree — What to Search When

```
User wants flights
├── Specific dates → Kiwi + Skiplagged parallel search
├── Flexible dates → sk_flex_departure_calendar first, then search best dates
├── Flexible destination → sk_destinations_anywhere
└── Round trip optimization → sk_flex_return_calendar

User wants hotels / stays
├── Specific city + dates → Skiplagged + Trivago parallel search
├── Apartments / homes / long stay / group trip → also use Airbnb (see airbnb.md)
├── "Near [landmark]" → Trivago radius search
└── Budget comparison → search all relevant providers, score, recommend

User wants cars
└── Skiplagged sk_cars_search → sort by price, group by type

User wants "best way from A to B"
├── Search flights (Kiwi + Skiplagged)
├── Check if ferry makes sense (coastal/island route → Ferryhopper)
├── Compare: flight price+time vs ferry price+time
└── Recommend with clear trade-off explanation

User wants complete trip
└── See references/trip-planner.md (uses all of the above)
```
