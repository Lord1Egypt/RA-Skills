---
name: trip-plan
description: Generate day-wise travel itineraries with timings, food spots, activities, and transport. Handles "plan my trip", "make an itinerary", revisions like "swap days" or "make it cheaper", and adjusts plans when user has existing flights or trains.
---

# Trip Plan

## When to activate
- User picks a destination: "let's do Kasol", "plan Kasol"
- User says "plan my trip", "make an itinerary"
- User provides travel details: "my flight lands at 11 AM"
- User requests revisions: "swap day 1 and 2", "add a trek", "make it cheaper"

## How to generate
1. Confirm: destination, dates/duration, group size, budget (from conversation context)
2. Web search for current info:
   - "<destination> things to do <month> <year>"
   - "<destination> best restaurants cafes local food"
   - "<destination> to <nearby attraction> how to reach"
3. Build day-wise plan with real timings

## Handling existing bookings
If user says "my flight lands at 11 AM" or "taking the 8 PM bus":
- Start itinerary from arrival time, not morning
- Account for travel from airport/bus stand to stay
- "Flight lands 11 AM Kullu → 1.5 hr taxi to Kasol → Check-in 1 PM → Lunch →..."

## Itinerary format
📍 Kasol — 3 Days, 2 Nights (Mar 14-16)
Budget: ₹8,000/person

🗓️ Day 1 — Mar 14 (Arrival + Settle In)
11:00 AM  ✈️ Land at Kullu
11:30 AM  🚕 Taxi to Kasol (₹1500, 1.5 hrs)
1:00 PM   🏨 Check-in
1:30 PM   🍽️ Lunch at Evergreen Cafe
3:00 PM   🚶 Walk to Chalal village (30 min easy trail)
7:30 PM   🍽️ Dinner at Jim Morrison Cafe

🗓️ Day 2 — Mar 15 (Kheerganga Trek)
6:30 AM   🍽️ Breakfast + pack snacks
7:30 AM   🥾 Start Kheerganga Trek from Barshaini
1:30 PM   🏔️ Reach Kheerganga — hot springs!
3:30 PM   🥾 Start descent
8:00 PM   🍽️ Dinner at Little Italy

🗓️ Day 3 — Mar 16 (Manikaran + Departure)
9:30 AM   🚶 Walk to Manikaran Sahib
12:00 PM  🍽️ Langar lunch at Gurudwara
2:00 PM   🚕 Taxi to Bhuntar Airport
3:30 PM   ✈️ Flight back

💰 Budget Breakdown:
Transport: ₹4,500 | Stay: ₹2,400 | Food: ₹1,500 | Activities: ₹500
Total: ~₹8,900/person (excluding flights)

## Revision handling
- "swap day 1 and 2" → rearrange and adjust timings
- "make it cheaper" → budget stays, free alternatives
- "add a trek on day 2" → insert and adjust surrounding timings
- "I want one more day" → add Day 4 with new activities
- Show only the updated section, not the entire itinerary again

## Rules
- Give actual times (not "morning" or "afternoon")
- Use real place names from web search
- Include budget breakdown at the end
- Be realistic — don't pack 15 activities in a day
- Account for travel time between activities
