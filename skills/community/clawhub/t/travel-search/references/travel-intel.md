# Travel Intel — Destination Intelligence

Practical destination information to complement flight/hotel searches. Enhances trip planning with real-world context.

## When to Use

- Any trip planning (automatically append key intel to itineraries)
- "What do I need to know about traveling to Japan?"
- "Do I need a visa for Thailand?"
- "What's the weather like in Barcelona in June?"
- "How do I get around in Rome?"

## Weather

Use the weather skill or wttr.in directly:

```bash
# Current + 3-day forecast
curl -s "wttr.in/Barcelona?format=v2"

# JSON for programmatic use
curl -s "wttr.in/Barcelona?format=j1"

# One-liner
curl -s "wttr.in/Barcelona?format=%c+%t+(feels+like+%f),+%w+wind,+%h+humidity"
```

### Best Travel Seasons (general patterns)

**Mediterranean (Spain, Italy, Greece, Turkey, Croatia):**
- Best: Apr-Jun, Sep-Oct (warm, fewer crowds, lower prices)
- Peak: Jul-Aug (hot, crowded, expensive)
- Off-season: Nov-Mar (cool/rainy, cheapest, many closures)

**Northern Europe (UK, Scandinavia, Benelux, Germany):**
- Best: May-Sep (long days, mild weather)
- Peak: Jun-Aug
- Off-season: Oct-Mar (dark, cold, but Christmas markets Nov-Dec)

**Southeast Asia (Thailand, Vietnam, Bali, Philippines):**
- Best: Nov-Mar (dry season for most)
- Monsoon: Jun-Oct (varies by country; Bali's dry season is Apr-Oct)
- Cheapest: May-Jun, Sep-Oct (shoulder)

**Japan:**
- Cherry blossom: late Mar-mid Apr (crowded, book months ahead)
- Best: Mar-May, Oct-Nov (mild, beautiful)
- Avoid: Jun-Jul (rainy season), Aug (hot + humid)

**Caribbean:**
- Best: Dec-Apr (dry, peak season)
- Hurricane: Jun-Nov (cheapest, but risky)
- Sweet spot: May or early Dec

**South America:**
- Seasons reversed from Northern Hemisphere
- Patagonia: Nov-Mar only
- Amazon: Jun-Oct (dry, easier travel)
- Andes: May-Sep (dry season)

**East Africa (Kenya, Tanzania):**
- Safari best: Jun-Oct (dry, animals concentrate at water)
- Wildebeest migration: Jul-Oct (Masai Mara)

## Visa Quick Reference

The agent should use its general knowledge for visa requirements. Key patterns:

**Passport power tiers (for common origins):**

US/EU/UK/Canada/Australia/Japan passport holders:
- Visa-free or visa-on-arrival to 170+ countries
- Notable exceptions needing advance visa: Russia, China (sometimes), India, Brazil (reciprocity varies)

Latin American passports (varies widely):
- Schengen/EU: most need visa (except some like Chile, Argentina, Brazil for short stays)
- USA: most need B1/B2 visa or ESTA equivalent
- Within Latin America: mostly visa-free

**Always recommend the user verify** at their country's foreign affairs website or sites like iVisa. Visa rules change frequently.

Format:
```
🛂 Visa: [Visa-free for X days / Visa required / eVisa available]
⚠️ Verify at [official source] — rules change frequently
```

## Currency & Money

For each destination, mention:

```
💱 Currency: [name] ([code])
💳 Cards: [widely accepted / cash preferred / mixed]
🏧 ATMs: [widely available / limited]
💡 Tip: [practical money tip]
```

Key patterns the agent knows:
- **Western Europe:** EUR (most), cards widely accepted, contactless common
- **UK:** GBP, cards everywhere, almost cashless
- **Japan:** JPY, surprisingly cash-heavy despite being tech-forward, carry ¥10,000+ notes
- **Southeast Asia:** Local currency, cash preferred in markets/small shops, ATMs everywhere but fees vary
- **Latin America:** Mix of local + USD accepted in tourist areas. ATM withdrawal often best rate.
- **Turkey:** TRY, volatile exchange — check rate before going, cards accepted in cities

**Tipping patterns:**
- USA/Canada: 15-20% expected
- Europe: rounding up or 5-10%, not obligatory
- Japan: no tipping (can be offensive)
- Southeast Asia: not expected, appreciated at 10%
- Latin America: 10% standard in restaurants

## Local Transport

For each destination, provide the essential "how to get around" info:

**Airport → City:**
```
🛬 Airport transfer:
- [Best option]: [name, price, duration]
- [Alternative]: [name, price, duration]
- ⚠️ Avoid: [common tourist trap if any]
```

**Getting around:**
```
🚇 Metro/subway: [exists? passes available?]
🚌 Bus: [useful? tourist-friendly?]
🚕 Taxi/rideshare: [Uber? Bolt? local app?]
🚶 Walking: [walkable city? safe?]
🚲 Bike: [bike share? cycling culture?]
```

Key city transport patterns:
- **London:** Oyster/contactless, Tube is king, Uber works, Heathrow Express £25 vs Tube £5
- **Paris:** Navigo pass, Metro excellent, CDG: RER B €11 vs taxi €55
- **Tokyo:** Suica/Pasmo card, trains are everything, Narita Express ¥3,250
- **Rome:** Roma Pass, Metro limited but buses extensive, walk the center, Fiumicino: Leonardo Express €14
- **Barcelona:** T-Casual card, Metro good, walkable center, El Prat: Aerobus €7
- **Bangkok:** BTS/MRT for main areas, Grab (not Uber), Don Mueang: bus ฿30 vs taxi ฿300
- **NYC:** MetroCard/OMNY, subway 24/7, JFK: AirTrain+subway $10.75 vs taxi ~$70

## Safety Notes

Only mention when genuinely relevant. Do not fear-monger.

Mention if:
- Specific neighborhoods to avoid at night
- Common tourist scams for that destination
- Health precautions (mosquito-borne diseases, altitude, water safety)
- Emergency number (if not obvious)

Format:
```
⚠️ Safety:
- [Specific, actionable tip]
- Emergency: [number]
```

## Power & Connectivity

```
🔌 Plug type: [type] — [adapter needed?]
📱 SIM/eSIM: [recommendation for tourist data]
🌐 WiFi: [generally available? quality?]
```

## Presentation

When adding travel intel to a trip plan, keep it concise — a short block at the end:

```
🌍 TRAVEL INTEL — [Destination]

🌤️ Weather (Jun): 25-32°C, sunny, occasional afternoon showers
🛂 Visa: Visa-free for 90 days (US passport)
💱 Currency: EUR — cards widely accepted
🚇 Getting around: Metro + walking. Buy T-Casual (€11.35, 10 rides)
🛬 Airport: Aerobus to Plaça Catalunya, €7, 35 min
💡 Tips:
- Dinner starts at 9-10 PM (not 7!)
- Siesta 2-5 PM — many small shops close
- Tap water is safe
🔌 Plug: Type C/F (standard EU) — US travelers need adapter
```

Keep this to 8-12 lines max. Only include what's genuinely useful for a first-time visitor.
