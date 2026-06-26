---
name: trip-search
description: Search for flights, hotels, and travel packages with real prices and booking links. Handles "find flights", "hotels in X", "cheapest way to reach X". Tracks costs against trip budget.
---

# Trip Search

## When to activate
- User asks for flights: "find flights", "flights to Kullu", "cheapest flight"
- User asks for hotels: "hotels in Kasol", "stay under ₹2000"
- User asks for transport: "how to reach Kasol from Delhi", "bus to Manali"

## Flight search
1. Web search for current flights:
   - "flights <origin> to <destination> <date> price"
   - "<origin> to <destination> flight <date> ixigo OR makemytrip"
2. Format top 3:

✈️ Flights: Delhi → Kullu, Mar 14

1. IndiGo 6E-2041 | 6:00 AM → 7:30 AM | ₹3,800
   🔗 Book: https://www.ixigo.com/...

2. SpiceJet SG-201 | 9:15 AM → 10:50 AM | ₹4,200
   🔗 Book: https://www.makemytrip.com/...

3. Air India AI-9543 | 2:00 PM → 3:35 PM | ₹5,100
   🔗 Book: https://www.airindia.com/...

💡 My pick: IndiGo 6 AM — cheapest + full day ahead.

⚠️ Prices from web search. Verify on booking site before paying.

## Hotel search
1. Web search:
   - "hotels <destination> under ₹<budget> per night"
   - "best hostels <destination> booking.com"
2. Format top 3:

🏨 Hotels in Kasol under ₹2,000/night

1. Parvati Riverside Camp | ₹1,200/night | ⭐ 4.2
   River view. Basic but clean.
   🔗 https://www.booking.com/...

2. The Hosteller Kasol | ₹1,500/night | ⭐ 4.3
   Private rooms. Cafe on-site.
   🔗 https://www.thehosteller.com/...

💡 My pick: Parvati Riverside — river view at ₹1,200 is unbeatable.

## Bus/train search
- Search: "bus <origin> to <destination> redbus"
- Search: "train <origin> to <destination> irctc"
- Include departure time, duration, price, booking link

## Budget tracking
After user selects something, show running total:

💰 Budget tracker (₹8,000):
✈️ Flight: ₹3,800
🏨 Stay (2 nights): ₹2,400
───────────────
Spent: ₹6,200 | Remaining: ₹1,800

## Rules
- Never make up prices — always web search for real data
- Max 3 options — no more
- Always include booking links
- Always include "prices may vary, verify before booking"
- Track budget if user mentioned one
