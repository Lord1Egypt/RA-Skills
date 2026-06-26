# Plan Itinerary

Plan single-day or multi-day travel itineraries, organize multi-destination trips, optimize travel routes, estimate budgets, or create detailed day-by-day travel schedules. Supports domestic and international travel, solo trips, family travel, and group travel scenarios.

---

## Workflow

### Step 1: Requirement Analysis

Extract and confirm the following from the user's input:

| Parameter        | Required | Description                                    |
|------------------|----------|------------------------------------------------|
| destinations     | Yes      | Target cities/countries in visit order          |
| travel_dates     | Yes      | Start date, end date, or total days             |
| travelers        | No       | Number of adults, children, elderly; solo/group |
| budget_level     | No       | Budget/mid-range/luxury; or specific amount     |
| interests        | No       | Culture, food, nature, shopping, adventure, etc |
| constraints      | No       | Mobility limits, visa restrictions, diet needs  |
| pace_preference  | No       | Relaxed / moderate / intensive                  |

**Guidelines:**
- Destinations and dates are essential for planning. If missing, ask the user before proceeding so the itinerary is realistic.
- When only a destination is given, suggest a reasonable duration based on the destination type. Users may not know how long to stay.
- Budget level can often be inferred from context. "Backpacking" suggests budget, "luxury resort" suggests high-end.
- Default to "moderate" pace when not specified. Most travelers prefer a balanced schedule.

---

### Step 2: Destination Analysis

For each destination, analyze:

1. **Optimal stay duration**: How many days are ideal
2. **Must-see attractions**: Top landmarks, cultural sites, natural scenery
3. **Local specialties**: Food, shopping, unique experiences
4. **Geographic layout**: How attractions cluster geographically
5. **Seasonal factors**: Weather, peak/off-peak, festivals during travel dates

**Multi-destination planning:**
- Allocate days proportionally. Larger cities with more attractions deserve more time.
- First and last days often involve transit. Plan lighter activities on these days.
- Allow at least 1 full day per major city. Transit-heavy days leave little time for sightseeing.

#### Recommended Stay Duration

##### By Destination Type

| Destination Type           | Recommended Days | Examples                        |
|----------------------------|------------------|---------------------------------|
| Global megacity            | 4-6 days         | Tokyo, London, New York, Paris  |
| Major city                 | 3-4 days         | Barcelona, Bangkok, Istanbul    |
| Medium city                | 2-3 days         | Kyoto, Florence, Chiang Mai     |
| Small city / town          | 1-2 days         | Bruges, Hallstatt, Luang Prabang|
| Beach / resort destination | 3-5 days         | Bali, Maldives, Phuket         |
| Nature / national park     | 2-4 days         | Yellowstone, Zhangjiajie       |
| Cultural heritage site     | 1-2 days         | Angkor Wat, Machu Picchu       |

##### Adjustment Factors

- **First visit**: Add 1 day vs repeat visit
- **With children**: Add 1 day (slower pace, nap time)
- **Photography focus**: Add 0.5-1 day (golden hour, revisits)
- **Festival period**: Add 1 day to experience events
- **Relaxed pace**: Multiply by 1.3x
- **Intensive pace**: Multiply by 0.7x

#### Attraction Density Analysis

##### High-density destinations (many sights per km2)
- Strategy: Walk between sights, cluster by neighborhood
- Examples: Rome (historic center), Kyoto (temple district), Prague (old town)
- Plan: 3-4 major sights per day + meals + shopping

##### Medium-density destinations
- Strategy: Mix of walking and transit, 2-3 areas per day
- Examples: Tokyo (districts spread out), Bangkok (BTS/MRT connected)
- Plan: 2-3 major sights per day + transit time

##### Low-density destinations (sights spread far apart)
- Strategy: Dedicate half/full days to single areas
- Examples: Los Angeles, Australian outback, countryside regions
- Plan: 1-2 major areas per day, significant transit

#### Geographic Clustering Rules

1. Map all target attractions for a destination
2. Identify natural clusters (sights within 2 km of each other)
3. Assign each cluster to a half-day or full-day block
4. Order clusters to minimize backtracking
5. Place the most remote cluster on a dedicated day

#### Seasonal Considerations

##### Weather impact on itinerary

| Season Factor     | Adjustment                                        |
|-------------------|---------------------------------------------------|
| Extreme heat      | Schedule outdoor sights early morning or evening   |
| Rainy season      | Prepare indoor alternatives for each day           |
| Extreme cold      | Limit outdoor time; plan warm indoor breaks        |
| Peak tourist season| Pre-book everything; expect crowds; go early       |
| Off-season        | Some attractions may close; check before planning  |

##### Best travel seasons (general reference)

| Region               | Best Months        | Avoid              |
|----------------------|--------------------|--------------------|
| Southeast Asia       | Nov - Mar          | Jun - Sep (monsoon)|
| Japan                | Mar-May, Oct-Nov   | Jun-Jul (rainy)    |
| Europe               | May - Sep          | Nov - Feb (cold)   |
| Australia/NZ         | Oct - Mar          | Jun - Aug (winter) |
| East Africa (safari) | Jun - Oct          | Mar - May (rain)   |
| South America        | May - Sep (dry)    | Dec - Mar (wet)    |

*Note: These are general guidelines. Specific destinations within regions may differ. Encourage users to verify current conditions.*

#### Destination Pairing Rules

When users visit multiple destinations:

1. **Same country/region first**: Minimize long-haul transit
2. **North-to-south or east-to-west**: Follow a logical geographic path
3. **Big city + small town**: Alternate pace for variety
4. **Hub-and-spoke**: Use a central city as base for day trips when possible
5. **Avoid backtracking**: Route should not cross the same path twice
6. **Transit hub placement**: Plan overnight stays near transport hubs for
   early departures

#### Cultural Awareness Notes

When analyzing a destination, consider:

- **Local customs**: Dress codes for religious sites, tipping norms,
  greeting etiquette
- **Business hours**: Siesta culture (Spain, Italy afternoon closures),
  early closures (Japan, some shops close by 20:00)
- **Weekly patterns**: Many museums close on Mondays (Europe); Friday
  prayers may affect schedules (Middle East)
- **Holidays**: National holidays may close attractions or cause
  transport disruptions; but can offer unique festival experiences

---

### Step 3: Transportation Planning

Determine inter-city and intra-city transport:

#### Inter-city (between destinations)

| Distance        | Primary Mode              | Notes                              |
|-----------------|---------------------------|------------------------------------|
| < 200 km        | High-speed rail / driving | Door-to-door convenience           |
| 200-800 km      | High-speed rail           | No airport overhead, city-center to city-center |
| 800+ km         | Flight                    | Saves travel time                  |
| Cross-border    | Flight                    | Check visa transit requirements    |

#### Intra-city (within destination)

- Metro/subway: most cost-effective in major cities
- Walking: for clustered attractions (< 2 km apart)
- Taxi/ride-hailing: for remote spots, late nights, or with children/elderly

**Planning tips:**
- Schedule inter-city transit in mornings or evenings. This preserves daylight hours for sightseeing.
- Flights require 2-3 hours for check-in, security, and boarding. Factor this into your schedule.
- High-speed rail is more predictable. 30 minutes at the station is usually sufficient.

*Note: Regional transport options vary. Verify current routes and schedules with local sources.*

---

### Step 4: Itinerary Assembly

Build the day-by-day schedule following these principles:

#### Time allocation per day

| Time Block    | Duration  | Activity Type                        |
|---------------|-----------|--------------------------------------|
| Morning       | 08:00-12:00 | Major attractions, outdoor activities |
| Lunch         | 12:00-13:30 | Local cuisine experience             |
| Afternoon     | 13:30-17:30 | Museums, shopping, secondary sights  |
| Dinner        | 17:30-19:00 | Dining experience                    |
| Evening       | 19:00-21:30 | Night markets, shows, city walks     |

#### Assembly rules

1. **Geographic clustering**: Group nearby attractions in the same half-day
2. **Energy curve**: Place physically demanding activities in the morning;
   indoor/relaxing activities in the afternoon
3. **Meal integration**: Schedule meals near planned attraction areas
4. **Buffer time**: Add 30-min buffers between activities for transit/rest
5. **First day**: Lighter schedule if arriving after noon; check-in + nearby
6. **Last day**: Reserve morning for packing and checkout; airport/station
   transit by early afternoon
7. **Rest day**: For trips > 5 days, insert a half-rest day mid-trip
8. **Rain plan**: Note indoor alternatives for outdoor activities

#### Family/group adjustments

- With children (< 6 yrs): Max 2 major attractions per day; add nap time
- With elderly: Reduce walking; add rest stops; avoid steep terrain
- Group travel: Choose activities with broad appeal; build in free time

---

### Step 5: Budget Estimation

Provide a cost breakdown per person per day:

| Category       | Budget       | Mid-range    | Luxury       |
|----------------|--------------|--------------|--------------|
| Accommodation  | Hostel/budget hotel | 3-4 star hotel | 5-star/resort |
| Meals          | Street food/local | Mix of local & restaurants | Fine dining |
| Transport      | Public transit | Transit + occasional taxi | Taxi/private car |
| Activities     | Free/low-cost sights | Mix of paid & free | Premium experiences |

#### Regional Cost Benchmarks (USD per person/day)

- **Southeast Asia**: Budget $30-50, Mid-range $80-150
- **East Asia**: Budget $50-100, Mid-range $100-250
- **Europe**: Budget $60-120, Mid-range $150-300
- **Americas**: Budget $50-100, Mid-range $150-300
- **Oceania**: Budget $80-120, Mid-range $180-300

*These are estimates only. Actual costs vary by city, season, and personal choices.*

#### Cost Planning

**Budget allocation by category:**
- Accommodation: 25-40%
- Meals: 20-35%
- Transportation: 15-25%
- Activities: 10-20%
- Miscellaneous: 5-10%

**Fixed costs** (book in advance): Flights, trains, hotels, travel insurance, visa fees

**Variable costs** (daily spending): Meals, local transport, shopping, tips

#### Special Considerations

**Peak season surcharges** (30-80% higher):
- Christmas/New Year, Chinese New Year, Summer Jul-Aug, Cherry blossom (Japan)

**Family adjustments:**
- Children under 2: usually free on flights and hotels
- Children 2-11: typically 50-75% of adult flight cost
- Look for family tickets and child discounts at attractions

**Money-saving tips:**
- Book flights 6-8 weeks in advance
- Use city tourism passes (Paris Museum Pass, JR Pass)
- Free walking tours for city orientation
- Student/senior discounts (carry ID)

---

### Step 6: Output Generation

Generate the final itinerary following the structure below.

**A complete itinerary should include:**
1. Trip overview (destinations, dates, travelers, budget summary)
2. Day-by-day detailed schedule
3. Budget estimation table
4. Preparation checklist

#### Output Structure

**Trip Overview** - Include destinations, dates, travelers, pace, and estimated budget.

**Day-by-Day Schedule** - For each day:
- Morning: Major attractions, outdoor activities
- Afternoon: Museums, shopping, secondary sights
- Evening: Dining, night markets, shows
- Accommodation area recommendation
- Transit notes (if applicable)

Special days:
- **Transit Day**: Focus on inter-city travel, light activities near accommodation
- **First Day**: Arrival, check-in, neighborhood exploration
- **Last Day**: Checkout, last activity, departure

**Budget Summary** - Breakdown by category (flights, accommodation, transport, meals, activities, misc).

**For trips > 7 days**: Add an "At-a-Glance" summary table before day-by-day details.

#### Travel Preparation Checklist

Include key reminders at the end of the itinerary. Focus on essentials:

**Before You Go:**
- Passport valid for 6+ months beyond return date
- Visa applications submitted (check processing times)
- Travel insurance purchased
- Flights and accommodation booked

**Pack:**
- Passport and travel documents
- Medications in carry-on
- Power adapter for destination
- Weather-appropriate clothing
- Comfortable walking shoes

**For International Trips:**
- Notify bank of travel dates
- Arrange phone plan or local SIM
- Download offline maps
- Share itinerary with emergency contact

**With Children:**
- Child passport and consent letter (if traveling without both parents)
- Snacks, entertainment, and extra clothes
- Children's medications

**With Elderly:**
- Medical records summary
- List of medications
- Mobility aid arrangements at airports

---

## Expression Rules

- Use the user's language for the entire response
- Keep each day's description concise: 3-5 bullet points per time block
- Use clear time markers (morning/afternoon/evening or specific times)
- Highlight must-do items with emphasis
- Include practical tips inline (e.g. "arrive early to avoid queues")
- Provide the full itinerary in a single response; do not split across
  multiple messages
- For trips > 7 days, provide a summary table first, then day-by-day details
- For specific prices and opening hours, use ranges or say "check current rates" / "verify locally". Fabricated details can mislead travelers.

## General Rules

- Respect the user's stated budget and pace preference. They know their constraints best.
- For international trips, remind about visa, insurance, and currency exchange
- For destinations with safety concerns, include relevant travel advisories
- Suggest travel insurance for all international trips
- If the user's plan is unrealistic (too many cities, too few days), provide
  honest feedback and suggest alternatives
- When uncertain about specific local details, recommend the user verify
  with local sources rather than guessing
- Adapt the level of detail to the user's apparent experience level
  (first-time travelers get more tips; experienced travelers get less)

## Usage Examples

- "Help me plan a 5-day trip to Tokyo and Osaka"
- "Plan a family trip to Thailand for 7 days with 2 kids"
- "I have 3 days in Paris, what's the best itinerary?"
- "Plan a budget backpacking route through Southeast Asia for 2 weeks"
- "Create a honeymoon itinerary for Bali and Singapore, 10 days"
- "Help me arrange a road trip from Los Angeles to San Francisco"
