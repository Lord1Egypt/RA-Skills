---
name: route-weaver
description: "Smart travel planner — custom itineraries with budget, route optimization, and contingency plans"
---

# Route Weaver (route-weaver)

Intelligent travel itinerary planner. Takes user preferences, destination, days, budget, and party type, then produces optimized day-by-day itineraries with budget allocation, transport routing, contingency plans, and packing checklists.

## Workflow

1. Parse needs — extract: destination, trip length, total budget, party type (solo / couple / family with kids / seniors / mixed), interests (food / history / nature / shopping / nightlife), pace preference (relaxed / moderate / packed), dietary restrictions. Ask for missing mandatory fields.
2. Query destination — gather: top attractions (open hours, ticket prices, visit duration), local cuisine and recommended restaurants, hotels (location, price range), inter-city and intra-city transport options (flight/train/bus/metro/ride-hailing), weather forecast for trip dates.
3. Route optimization — order attractions geographically to minimize backtracking. Allocate time per spot (sightseeing + transit + buffer). Adjust pace for group type (family/seniors get more rest time). Suggest logical day zones (e.g. Day 1 west side, Day 2 east side).
4. Budget allocation — split total budget into: transport (30-40%), lodging (25-35%), tickets/activities (15-20%), food (10-15%), shopping/misc (5-10%). Adjust ratios for luxury/budget mode.
5. Generate multi-version — produce up to 3 versions:
   - **Budget**: youth hostel + street food + free attractions
   - **Comfort**: mid-range hotel + mix of restaurants + main attractions
   - **Luxury**: 4-5 star hotel + fine dining + premium experiences
6. Detailed daily itinerary — for each day: timeline (e.g. 08:00-09:00 breakfast at X, ¥YY), recommended restaurants with avg cost and signature dishes, transport options between stops, estimated walking distance. Note: "Day X — theme: culture / adventure / relaxation".
7. Contingency plans — for each day: rain alternative (indoor venue or covered activity), crowd avoidance suggestion (off-peak hours or lesser-known alternative), emergency contact info.
8. Packing checklist — generate by destination climate, trip length, and planned activities. Group by category (documents / electronics / clothing / toiletries / health).
9. Export — formatted PDF itinerary (readable, includes maps skeleton), shareable link (plain text summary for messaging), or calendar import (.ics file).

## Sample prompts

- `route-weaver plan --destination "成都" --days 4 --budget 5000 --type couple`
- `route-weaver plan --destination "东京" --days 7 --budget 15000 --type family --pace relaxed`
- `route-weaver plan --destination "云南大理" --days 3 --budget 2000 --type solo --interests nature,photography`
