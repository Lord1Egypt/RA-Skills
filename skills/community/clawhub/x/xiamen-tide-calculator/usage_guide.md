# Xiamen Tide Calculator Skill - Usage Guide (Enhanced)

## Installation

Install the `xiamen-tide-calculator.skill` file in WorkBuddy to use this skill.

## Features

### Basic Features
- Accurate tide time calculation for Xiamen waters based on lunar calendar dates
- Automatic tide size classification (spring tide / middle tide / neap tide)
- Best beachcombing time windows

### Enhanced Features ⭐
- **Beachcombing Scoring System**: Comprehensive scoring based on tides, time, season, and other factors
- **Beachcombing Mode**: All-around beachcombing advice
- **Location Recommendations**: Best beachcombing spots based on tide size
- **Equipment Suggestions**: Equipment checklist based on season
- **Safety Reminders**: Tide rise warnings and safety precautions
- **Multi-day Comparison**: Compare beachcombing scores across multiple days, recommend best dates

## Usage Examples

### Standard Tide Query

**User**: "Xiamen tide today"
**User**: "Xiamen lunar 3rd month 5th day tide"

**Output**:
```
【Xiamen Tide · Lunar 3/15】
High Tide 1: 12:00
High Tide 2: Next Day 00:24
Low Tide 1: 05:48
Low Tide 2: 18:12
Best Beachcombing: 03:48-06:48 (Window 1), 16:12-19:12 (Window 2)
Tide Size: Middle Tide
Beachcombing Score: 6.4 (Recommended)
```

### Beachcombing Advice Query ⭐

**User**: "Is today good for beachcombing in Xiamen?"
**User**: "Best time for beachcombing"
**User**: "Beachcombing advice"

**Output**:
```
【Xiamen Beachcombing Advice · Lunar 3/2】

🌊 Beachcombing Score: 9.0 (Highly Recommended)

⏰ Best Beachcombing Periods:
  - Window 1: Previous Day 17:24 - Previous Day 20:24
  - Window 2: 05:48-08:48

📍 Recommended Locations:
  - Wuyuan Bay: Large tidal range, rich marine life
  - Xiang'an Coast: Wide mudflats, diverse species
  - Huandao Road: Convenient transportation, suitable for beginners

🐟 Expected Harvest:
  - Clams, sea snails, small crabs, oysters, small shrimp

🧰 Equipment Suggestions:
  - Essential: Small shovel, bucket, non-slip shoes, gloves
  - Recommended: Lighting equipment, light jacket
  - Special Note: Pleasant weather, pack light

⚠️ Safety Reminders:
  - Beachcombing window ends at 08:48, tide starts rising afterwards, please evacuate in time
  - Go with companions, do not beachcomb alone
  - Watch out for reef areas,小心 slippery surfaces

📊 Tide Information:
  - Tide Size: Spring Tide
  - Low Tide 1: Previous Day 19:24
  - Low Tide 2: 07:48
  - High Tide 1: 01:36
  - High Tide 2: 14:00

🌡️ Current Season:
  - Spring - Pleasant weather, active marine life, best beachcombing season

💡 Beachcombing Tips:
  - Arrive 1 hour before the beachcombing window
  - Focus on the 2 hours before low tide for peak marine activity
  - Protect the marine ecosystem, harvest responsibly
  - Take your trash with you when not beachcombing, protect the ocean
```

### Multi-day Comparison Query ⭐

**User**: "Which day next week is best for beachcombing?"
**User**: "Xiamen beachcombing recommendations for next 10 days"

**Output**:
```
【Next 10 Days Beachcombing Recommendations】

🌟 Highly Recommended:
  - Lunar 3/2 - Score: 9.0
    Reason: Spring tide + Daytime low tide + Spring bonus (1.0 pts)
    Best Beachcombing: Previous Day 17:24-Previous Day 20:24 (Window 1), 05:48-08:48 (Window 2)
    Low Tide Times: Previous Day 19:24, 07:48
    Recommended Locations: Wuyuan Bay: Large tidal range, rich marine life

  - Lunar 3/3 - Score: 9.0
    Reason: Spring tide + Daytime low tide + Spring bonus (1.0 pts)
    Best Beachcombing: Previous Day 18:12-Previous Day 21:12 (Window 1), 06:36-09:36 (Window 2)
    Low Tide Times: Previous Day 20:12, 08:36
    Recommended Locations: Wuyuan Bay: Large tidal range, rich marine life

✅ Recommended:
  - Lunar 3/1 - Score: 7.4
    Reason: Middle tide + Good time window
    Best Beachcombing: Previous Day 16:36-Previous Day 19:36, 05:00-08:00
    Recommended Locations: Huandao Road: Convenient transportation

  ... (other recommended dates)

📊 Summary:
  - Best beachcombing date: Lunar 3/2 (9.0 pts)
  - Highly recommended days: 2
  - Recommended days: 6
  - Fair days: 2
  - Not recommended days: 0
```

## Beachcombing Scoring System

### Scoring Factors
1. **Tide Size** (Weight 40%)
   - Spring tide: 4.0 points
   - Middle tide: 2.4 points
   - Neap tide: 0.8 points

2. **Time Window** (Weight 30%)
   - Window duration and quality

3. **Tide Distribution** (Weight 20%)
   - Daytime low tide bonus

4. **Seasonal Factor** (Weight 10%)
   - Spring/Autumn: 1.0 points
   - Summer: 0.7 points
   - Winter: 0.4 points

### Recommendation Levels
- **Highly Recommended** (8.0-10.0): Spring tide + Daytime low tide + Suitable season
- **Recommended** (6.0-7.9): Spring or middle tide + Basic conditions met
- **Fair** (4.0-5.9): Middle tide + Some conditions average
- **Not Recommended** (0.0-3.9): Neap tide or poor conditions

## Beachcombing Location Recommendations

### Spring Tide Period
- Wuyuan Bay: Large tidal range, rich marine life
- Xiang'an Coast: Wide mudflats, diverse species

### Middle Tide Period
- Huandao Road: Convenient transportation
- Jimei Aoyuan: Suitable for family beachcombing
- Zengcuo'an Beach: Soft sandy bottom

### Neap Tide Period
- Suggest waiting for spring tide
- Less marine life during neap tides, limited harvest

## Equipment Suggestions

### Seasonal Differences

**Spring/Autumn**:
- Essential: Small shovel, bucket, non-slip shoes, gloves
- Recommended: Lighting equipment, light jacket
- Special Note: Pleasant weather, pack light

**Summer**:
- Essential: Small shovel, bucket, non-slip shoes, gloves
- Recommended: Lighting equipment, sun hat, sunscreen, drinking water
- Special Note: Hot weather, beware of heatstroke

**Winter**:
- Essential: Small shovel, bucket, non-slip shoes, gloves
- Recommended: Light jacket, warm hat, hot water, lighting equipment
- Special Note: Cold weather, keep warm

## Technical Notes

- Calculations are based on standard tide formulas for Xiamen waters
- Times use 24-hour format
- Automatically handles cross-day situations (annotated as "Next Day" or "Previous Day")
- Supports lunar date input
- Beachcombing scores comprehensively consider tides, time, season, and other factors

## Direct Script Usage

### Standard Mode
```bash
python scripts/tide_calculator.py --lunar-day 15 --lunar-month 3
```

### Beachcombing Mode ⭐
```bash
python scripts/tide_calculator.py --lunar-day 2 --lunar-month 3 --beach-mode
```

### Multi-day Comparison ⭐
```bash
python scripts/compare_beach_days.py --lunar-month 3 --start-day 1 --days 10
```

## Notes

- Current version requires lunar date input
- Solar-to-lunar conversion needs manual handling
- Lunar dates must be between 1-30
- Tide times are for reference only, actual weather may affect results
- Safety reminders are very important, please follow them
- Protect the marine ecosystem, harvest responsibly

## Future Improvement Plans

1. Integrate lunar conversion library for automatic solar-to-lunar conversion
2. Add current date auto-detection
3. Integrate weather API for more accurate beachcombing advice
4. Add more beachcombing location information
5. Handle leap month special cases

## Changelog

### v2.0 (2026-04-02) ⭐
- Added beachcombing scoring system
- Added beachcombing mode
- Added multi-day comparison
- Added location recommendations
- Added equipment suggestions
- Added safety reminders

### v1.0 (2026-04-02)
- Basic tide calculation
- Tide size classification
- Beachcombing time windows

## Contact

If you have questions or suggestions, please contact the developer.
