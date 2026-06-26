---
name: travel-planning
description: Create comprehensive, personalized travel itineraries with day-by-day plans, budget breakdowns, packing lists, and practical tips for any destination.
homepage: https://www.lonelyplanet.com/
metadata: {"clawdbot":{"emoji":"✈️","requires":{"bins":["curl"]}}}
---

# Travel Planning Skill

## Purpose
This skill helps create comprehensive, personalized travel itineraries with day-by-day plans, budget breakdowns, packing lists, and practical travel tips.

## When to Use This Skill
Trigger this skill when users request:
- Travel itineraries or trip planning
- Vacation schedules or holiday plans
- Destination recommendations with detailed plans
- Travel budgets or cost estimates
- Packing lists for trips
- Multi-city tour planning
- Weekend getaway planning
- Honeymoon or special occasion trip planning

Keywords: "travel plan", "itinerary", "trip to", "vacation plan", "travel guide", "visit [destination]", "packing list", "travel budget"

## Core Principles

### 1. Personalization
- **Always ask clarifying questions** about:
  - Travel dates and duration
  - Budget range (budget/mid-range/luxury)
  - Travel style (relaxed/moderate/packed)
  - Interests (culture, food, adventure, relaxation, etc.)
  - Travelers (solo, couple, family, group)
  - Dietary restrictions or accessibility needs

### 2. Comprehensive Coverage
Every travel plan should include:
- **Daily itinerary** with time estimates
- **Accommodation recommendations** (3+ options per budget tier)
- **Transportation details** (getting there and around)
- **Budget breakdown** (flights, hotels, food, activities, misc)
- **Packing list** (essentials, weather-appropriate items)
- **Practical tips** (visa, currency, best time to visit, safety)
- **Food recommendations** (must-try dishes and restaurants)
- **Backup plans** for weather or closures

### 3. Realistic Timing
- Account for travel time between locations
- Include buffer time for rest, meals, unexpected delays
- Don't over-schedule (3-4 major activities per day max)
- Suggest flexible vs. fixed time slots

### 4. Local Insights
- Recommend off-the-beaten-path experiences
- Include local customs and etiquette
- Suggest best times to visit popular spots (avoid crowds)
- Mention seasonal events or festivals
- Include emergency contacts and useful phrases

## Output Format

### Structure Your Travel Plan As:

```
# [Destination] Travel Itinerary
## Trip Overview
- Duration: X days
- Travel Dates: [dates]
- Budget: $X - $X
- Travel Style: [relaxed/moderate/packed]
- Best for: [type of traveler]

## Pre-Trip Preparation
### Visa & Entry Requirements
[Details]

### Currency & Budget
[Breakdown]

### Best Time to Visit
[Season recommendations]

### Packing List
#### Essentials
- Item 1
- Item 2

#### Weather-Specific
- Item 1

#### Tech & Documents
- Item 1

## Day-by-Day Itinerary

### Day 1: [Theme/Focus]
**Morning (9:00 AM - 12:00 PM)**
- 9:00 AM: Activity 1 [duration, cost]
  - Why: [brief explanation]
  - Tip: [insider advice]

**Afternoon (12:00 PM - 6:00 PM)**
- 12:30 PM: Lunch at [restaurant]
  - Must-try: [dish]
  - Budget: $X per person

**Evening (6:00 PM onwards)**
- 7:00 PM: Activity 3
  - Details

**Accommodation**
- Budget: [Hotel name] - $X/night
- Mid-range: [Hotel name] - $X/night  
- Luxury: [Hotel name] - $X/night

[Repeat for each day]

## Getting Around
### From Airport to City
[Options with costs]

### Local Transportation
[Best options: metro, taxi, bike, etc.]

## Food Guide
### Must-Try Dishes
1. Dish name - Where to find it
2. Dish name - Where to find it

### Restaurant Recommendations
**Budget-Friendly**
- Restaurant 1 [cuisine, price range]

**Mid-Range**
- Restaurant 1

**Fine Dining**
- Restaurant 1

## Budget Summary
| Category | Estimated Cost |
|----------|----------------|
| Flights | $X - $X |
| Accommodation (X nights) | $X - $X |
| Food (X days) | $X - $X |
| Activities & Entrance Fees | $X - $X |
| Local Transportation | $X - $X |
| Shopping & Misc | $X - $X |
| **TOTAL** | **$X - $X** |

## Practical Tips
### Safety
- [Tip 1]
- [Tip 2]

### Local Customs
- [Custom 1]
- [Custom 2]

### Useful Phrases
- Hello: [translation]
- Thank you: [translation]
- How much?: [translation]

### Emergency Contacts
- Police: [number]
- Tourist Help: [number]
- Embassy: [number]

## Alternative Plans
### Rainy Day Activities
- Option 1
- Option 2

### If Time is Short
[Condensed version highlights]

### Extensions
[Nearby destinations for longer trips]
```

## Best Practices

### DO:
✅ Use web search to verify current information (opening hours, prices, events)
✅ Provide 3+ options for hotels in different price ranges
✅ Include specific costs and time estimates
✅ Mention booking tips (advance reservations needed?)
✅ Add personal touches ("This café has the best sunset views")
✅ Consider different traveler types (solo, family, elderly)
✅ Include rest time and flexibility
✅ Suggest booking platforms when relevant
✅ Mention seasonal considerations
✅ Provide map references or neighborhood names

### DON'T:
❌ Over-schedule (leave breathing room)
❌ Ignore practical concerns (distance, travel time)
❌ Forget about meals and rest
❌ Assume unlimited budget
❌ Neglect safety or health considerations
❌ Provide outdated information (always search for recent data)
❌ Create one-size-fits-all plans
❌ Forget about alternative options

## Tool Usage

### When to Use Web Search:
- Current prices and opening hours
- Recent reviews or changes
- Seasonal events and festivals
- Updated visa requirements
- Current exchange rates
- New attractions or closures
- Weather patterns for travel dates

### When to Use Places Search:
- Finding specific restaurants
- Locating hotels in desired areas
- Discovering attractions and activities
- Getting exact addresses and coordinates

### When to Use Maps Display:
- Showing daily route visualization
- Displaying hotel locations
- Mapping out walking tours
- Illustrating multi-city itineraries

## Example Queries

**Good triggers:**
- "Plan a 5-day trip to Tokyo"
- "I need an itinerary for Paris with a $3000 budget"
- "Create a romantic getaway plan for Bali"
- "Family vacation to Orlando - 7 days"
- "Backpacking Southeast Asia for 3 weeks"

**Follow-up questions to ask:**
- "What's your approximate budget for this trip?"
- "Are you interested more in culture, food, adventure, or relaxation?"
- "Do you prefer a packed schedule or a relaxed pace?"
- "Any must-see attractions or experiences you want to include?"
- "Are there any dietary restrictions or accessibility needs?"

## Quality Checklist

Before delivering the travel plan, verify:
- [ ] Daily schedule is realistic (not overwhelming)
- [ ] Budget breakdown is comprehensive
- [ ] Transportation between activities is considered
- [ ] Accommodation options across price ranges
- [ ] Packing list matches destination climate
- [ ] Practical info (visa, currency) included
- [ ] Food recommendations with variety
- [ ] Backup plans for weather/closures
- [ ] Local tips and cultural notes
- [ ] All costs are current (searched recently)

## Customization Based on Traveler Type

### Solo Travelers
- Include safety tips
- Suggest social activities (tours, hostels)
- Mention solo-friendly restaurants

### Couples
- Romantic spots and experiences
- Fine dining options
- Photo-worthy locations

### Families
- Kid-friendly activities
- Restaurant with children's menus
- Nap/rest time in schedule
- Nearby medical facilities

### Budget Travelers
- Free activities
- Street food recommendations
- Budget accommodation (hostels)
- Money-saving tips

### Luxury Travelers
- Premium experiences
- Fine dining
- Spa and wellness
- Private tours or transfers

## Final Notes

The goal is to create a travel plan that feels like it was crafted by an experienced travel agent who knows the destination intimately. Balance structure with flexibility, and always prioritize the traveler's safety, comfort, and enjoyment.

Remember: A great itinerary inspires excitement while providing practical confidence that the trip will go smoothly.
