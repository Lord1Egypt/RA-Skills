# Trip Planner — Universal Itinerary Generator

Generate complete, personalized trip itineraries with real prices and booking links. Adapts to any traveler, any destination, any style.

## Design Principle

Rather than listing every possible travel style, this planner uses a **dimensional profiling system**. Every trip is a unique blend of dimensions — like mixing colors. "Honeymoon in Bali" and "solo backpacking in Vietnam" both use the same framework but produce completely different results.

The agent already understands human intent. This document provides the **structured workflow** and **travel-specific knowledge** the agent needs to deliver real prices and actionable itineraries.

## Step 1: Profile the Trip

There are **two modes** for gathering trip info:

### Mode A: Quick (default)
When the user gives a direct request ("find me flights to Rome"), extract what you can from their message and **ask only what's truly missing** (usually just dates or origin). Infer everything else. Most users want fast answers, not questionnaires.

### Mode B: Guided Intake
When the user asks for a **full trip plan**, wants help deciding, or explicitly asks for a questionnaire, use this **conversational intake**. Ask in ONE message, not one question at a time:

```
Let's plan your trip! A few quick questions:

1. 📍 Where do you want to go? (city, country, or "surprise me")
2. 🛫 Where are you flying from?
3. 📅 When? (specific dates, or flexible like "sometime in June")
4. ⏱️ How many days?
5. 👥 Who's going? (solo, couple, family, friends + how many)
6. 💰 Budget range? (budget / mid-range / premium / no limit)
7. ✨ What's the vibe? What do you want to feel or experience?
   (examples: "eat everything", "chill on a beach", "see all the history",
   "party", "romantic", "adventure", or just tell me in your own words)

Answer as many or as few as you want — I'll figure out the rest!
```

**Rules for the intake:**
- **Always in ONE message.** Never drip-feed questions one by one.
- **All questions are optional except destination.** If they only answer 3 of 7, work with that.
- **Accept any format.** Full sentences, single words, emojis, bullet points — all valid.
- **Never repeat questions they already answered** in their original message.
- **Skip the intake entirely** if the user already gave enough info to work with.
- **Adapt language** to the user's language (if they write in Spanish, ask in Spanish).

After receiving answers (or partial answers), proceed to profiling:

### Core Dimensions

Every trip lives somewhere on these spectrums. The user's words place them naturally:

**Budget:** free → budget → mid-range → premium → ultra-luxury
- Infer from: price mentions, accommodation type, airline class, word choice ("cheap" vs "treat ourselves")
- Default: mid-range

**Energy:** relaxed → moderate → active → intense
- Infer from: activity mentions, trip length vs destinations, physical activities, age/group context
- Default: moderate

**Social:** solo introspective → solo social → couple → small group → large group → family
- Infer from: pronouns ("I" vs "we"), mentions of partner/kids/friends, group size
- Default: solo or couple (ask if ambiguous)

**Structure:** completely open → loose framework → planned with flexibility → tightly scheduled
- Infer from: "go with the flow" vs "I want to see everything" vs specific requests
- Default: planned with flexibility

**Focus:** This is the trip's personality — what the traveler cares about most. Unlike the spectrums above, focus is a **weighted blend** of interests. Every trip mixes multiple interests at different intensities.

Interest categories (the agent should recognize these and any related concepts, synonyms, or adjacent ideas — this list is illustrative, not exhaustive):

- **Culture & History** — museums, ruins, architecture, heritage, traditions, local customs, UNESCO sites, galleries, street art, neighborhoods with character
- **Food & Drink** — restaurants, street food, markets, cooking classes, wine, beer, coffee culture, food tours, Michelin, local specialties, dietary exploration
- **Nature & Outdoors** — hiking, parks, mountains, lakes, forests, beaches, diving, snorkeling, kayaking, cycling, skiing, surfing, camping, stargazing
- **Nightlife & Social** — bars, clubs, rooftops, live music, pub crawls, festivals, social hostels, karaoke, casino
- **Wellness & Rest** — spa, yoga, meditation, thermal baths, retreat, beach lounging, slow mornings, digital detox, hot springs, hammam
- **Romance & Intimacy** — couples dinners, sunset spots, scenic stays, privacy, honeymoon, anniversary, proposal-worthy locations
- **Shopping & Markets** — boutiques, outlets, luxury brands, flea markets, artisan crafts, souvenirs, bazaars, vintage
- **Art & Creativity** — galleries, studios, workshops, street art tours, photography spots, design districts, maker spaces
- **Sports & Events** — football, F1, tennis, surfing, marathons, Olympics, local sports, stadium tours
- **Music & Performance** — concerts, festivals, opera, jazz, flamenco, local folk, theater, busking scenes
- **Family & Kids** — theme parks, zoos, aquariums, interactive museums, playgrounds, kid-friendly everything, safety, nap schedules
- **Learning & Growth** — language classes, university tours, workshops, historical deep-dives, cultural immersion, volunteer work
- **Spirituality & Reflection** — temples, churches, mosques, pilgrimage routes, meditation, silent retreats, sacred sites
- **Photography & Visual** — viewpoints, golden hour spots, iconic landmarks, photogenic streets, drone-friendly, landscape shots
- **Wildlife & Eco** — safaris, whale watching, sanctuaries, national parks, eco-lodges, conservation, bird watching
- **Adventure & Adrenaline** — bungee, paragliding, zip-lining, canyoning, off-road, extreme sports, survival experiences
- **Work & Productivity** — coworking, WiFi quality, time zones, café culture, long-stay, bleisure, quiet hotels
- **Road Trip & Freedom** — scenic routes, car rental, vanlife, multiple stops, flexibility, countryside, coastal drives
- **Local & Authentic** — non-touristy, hidden gems, local neighborhoods, homestays, off-beaten-path, "live like a local"
- **Accessibility** — wheelchair access, limited mobility, sensory needs, medical proximity, elevator access, flat terrain
- **Pet Travel** — pet-friendly hotels, parks, transport rules, quarantine info, vet access
- **Sustainable & Eco** — low carbon, train over plane, eco-lodges, local economy, plastic-free, carbon offset

**When no focus is specified:** Default blend — 35% culture, 25% food, 20% local/walking, 10% nature, 10% rest. This satisfies the majority of travelers.

**The agent should freely interpret any user description**, including creative or unconventional requests ("I want a chaotic trip", "surprise me", "my vibe is Studio Ghibli", "dark tourism", "only free things"). The categories above are anchors, not boundaries.

### Secondary Signals (detect if mentioned, never ask)

- **Dietary needs** — vegetarian, vegan, halal, kosher, gluten-free, allergies → affects every food recommendation
- **Accommodation style** — hotel, hostel, Airbnb, resort, boutique, camping, glamping, villa, ryokan, riad → often implied by budget
- **Transport preference** — walking, public transit, taxi/rideshare, rental car, bike → affects logistics
- **Time personality** — early bird vs night owl → affects scheduling
- **Mobility/health** — anything physical → affects activity selection
- **First visit vs returning** — "I've been before" means skip the obvious tourist spots
- **Special occasions** — birthday, anniversary, graduation, retirement → add a special element

## Step 2: Search Flights

Read `references/flights.md` (Kiwi) or `references/skiplagged.md`.

Strategy by budget:
- **Budget:** Sort by price, accept layovers, use `departureDateFlexRange: 3`
- **Mid-range:** Sort by quality. Prefer ≤1 stop, reasonable duration.
- **Premium:** Sort by duration, prefer direct or business class (`cabinClass: "C"`)

Always present:
- 💸 Cheapest option
- ⚡ Fastest option
- 🎯 Best value (recommended)

Each with deep link.

## Step 3: Search Accommodation

Read `references/skiplagged.md` and/or `references/hotels.md`. If apartments, homes, longer stays, workcations, or group travel are relevant, also read `references/airbnb.md`.

Match to profile:
- **Budget:** Cheapest with decent rating (≥7.0). Mention hostels for backpackers.
- **Mid-range:** Best rating-to-price ratio. 3-4★, rating ≥8.0.
- **Premium:** Highest rated. 4-5★, unique features (pool, view, spa, design).
- **Apartment/home fit:** Prefer Airbnb when kitchen, laundry, workspace, privacy, or extra space matter.

Location priority by focus:
- Nightlife → near bar district
- Culture → near old town / museum quarter
- Food → near market district or foodie neighborhood
- Beach → oceanfront or walking distance
- Work → near coworking / business district with good WiFi
- Family → safe area, near parks / attractions

Present 2-3 options even if user specified a tier (gives choice). When Airbnb is relevant, compare **hotel vs Airbnb** directly and recommend the overall best-value stay.

## Step 4: Budget Breakdown

```
Flight:        $XXX (actual)
Hotel:         $XXX (actual, N nights)
Daily costs:   $XX/day × N days = $XXX
  ├─ Food
  ├─ Transport  
  └─ Activities
─────────────────────────────
TOTAL:         ~$X,XXX
```

### Daily Cost Benchmarks (per person, USD)

Western Europe (Paris, London, Amsterdam, Zurich): Budget $40-60 | Mid $80-130 | Premium $160+
Southern Europe (Rome, Barcelona, Lisbon, Athens): Budget $30-50 | Mid $60-100 | Premium $130+
Eastern Europe (Prague, Budapest, Krakow, Belgrade): Budget $20-35 | Mid $40-70 | Premium $100+
Scandinavia (Stockholm, Copenhagen, Oslo): Budget $50-70 | Mid $90-140 | Premium $180+
UK & Ireland: Budget $40-60 | Mid $80-130 | Premium $160+
USA & Canada: Budget $50-70 | Mid $90-150 | Premium $200+
Japan: Budget $40-60 | Mid $80-130 | Premium $170+
South Korea: Budget $30-50 | Mid $60-100 | Premium $130+
Southeast Asia (Thailand, Bali, Vietnam): Budget $15-25 | Mid $35-60 | Premium $90+
South Asia (India, Sri Lanka, Nepal): Budget $10-20 | Mid $25-50 | Premium $80+
China: Budget $20-35 | Mid $50-80 | Premium $120+
Middle East (Dubai, Doha, Amman, Oman): Budget $40-60 | Mid $80-140 | Premium $200+
Latin America (Mexico, Colombia, Argentina, Peru): Budget $15-30 | Mid $35-65 | Premium $100+
Caribbean: Budget $30-50 | Mid $60-100 | Premium $150+
Africa (Morocco, Kenya, South Africa, Egypt): Budget $15-30 | Mid $40-80 | Premium $120+
Central Asia (Georgia, Uzbekistan, Kazakhstan): Budget $15-25 | Mid $30-55 | Premium $80+
Australia & New Zealand: Budget $50-70 | Mid $90-140 | Premium $180+
Pacific Islands (Fiji, Maldives, Tahiti): Budget $40-60 | Mid $80-150 | Premium $250+

## Step 5: Build Day-by-Day Itinerary

### Daily Structure

```
📅 Day X — [Date] ([Day of week]) — [Theme/Area]
🌅 Morning: [activity]
🍽️ Lunch: [area or cuisine]
🌇 Afternoon: [activity]
🍽️ Dinner: [area or cuisine]
🌙 Evening: [optional activity]
💡 Tip: [practical tip]
```

### Rules

1. **Day 1 = Arrival.** Adjust for arrival time. Late arrival → check-in + dinner only.
2. **Last Day = Departure.** Early flight → just check-out. Late flight → morning activity.
3. **Rest day.** Include one for trips > 5 days. Day 4 or 5, lighter schedule.
4. **Cluster geographically.** Group activities by area to minimize transit.
5. **Timing awareness:** Museums early (less crowd), markets morning, parks golden hour, nightlife late (especially Southern Europe / Latin America).
6. **Match pacing to energy dimension.** Relaxed: 1-2 activities. Moderate: 2-3. Active: 4-5. Intense: dawn to midnight.
7. **Weight activities toward focus.** Foodie? Every meal is a highlight. Adventure? Day trips. Cultural? Top museums. Party? Evenings are the main event.
8. **Mention practical details:** Free entry days, best neighborhoods, local customs, tipping, safety, dress codes, reservation needs.
9. **Day trips** for 5+ day stays. One excursion to a nearby town/attraction. The agent knows popular pairings (Paris→Versailles, Madrid→Toledo, Tokyo→Kamakura, etc.).
10. **Special occasion touch.** If birthday/anniversary/honeymoon, add one special element (rooftop dinner, surprise activity, scenic spot).

## Step 6: Present

Format for chat (no markdown tables):

```
✈️ [DESTINATION] — [N] days | [DATES]
[One-line profile: "Romantic foodie getaway on a mid-range budget"]

💰 Budget
- ✈️ Flight: $XXX — [link]
- 🏨 Hotel: $XXX (N nights) — [link]
- 🍽️🚇🎟️ Daily: ~$XX × N = $XXX
- 💵 **Total: ~$X,XXX**

🏨 [Hotel] — [stars]★ [rating]/10 — $XX/night
📍 [Neighborhood] — [why it fits]

📅 Day-by-day...

🔗 Book:
- Flight: [link]
- Hotel: [link]

💡 Tips:
- [2-3 destination tips]
```

## Adaptation

The dimensional system means infinite combinations work naturally:

- "Solo digital nomad in Lisbon for a month" → budget-mid, relaxed energy, work focus, long-stay accommodation, coworking spots, café culture
- "Surprise anniversary trip under $3000" → premium within budget, romance focus, moderate energy, agent picks the destination
- "Chaotic 3-day Tokyo trip, we want to see EVERYTHING" → mid-range, intense energy, culture+food+nightlife blend, packed schedule
- "Accessible trip to Barcelona, my mom uses a wheelchair" → mid-range, relaxed energy, accessibility priority, flat-terrain attractions, elevator-access hotels
- "Dark tourism in Eastern Europe" → budget-mid, culture focus (but specifically: Chernobyl, Auschwitz, Cold War sites, bunkers), moderate energy
- "We're 8 friends doing a bachelor party in Cartagena" → mid-range, intense energy, nightlife+beach+adventure focus, large group logistics
- "Studio Ghibli vibes in rural Japan" → mid-range, relaxed energy, nature+art focus, countryside ryokans, forests, small towns, train journeys
- "I just got divorced and need to find myself" → solo, moderate energy, wellness+spirituality+nature focus, flexible structure, meaningful experiences
