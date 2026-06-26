---
name: xiamen-tide-calculator
description: Xiamen Tide Calculator v3.2, used for calculating Xiamen waters tide times and beachcombing advice. Supports automatic solar-to-lunar date conversion, current date auto-detection, and leap month handling. Calculates high/low tide times based on date, classifies tide size, provides beachcombing scores, location recommendations, equipment suggestions, and safety reminders. New features: multi-window analysis, pros/cons descriptions, recommendation index, integrated window feature. Trigger scenarios: (1) Tide queries like "Xiamen tide today", (2) Beachcombing advice queries like "Is today good for beachcombing?", "Best beachcombing time", (3) Multi-day comparisons like "Which day next week is best for beachcombing?", (4) Querying tide info for specific dates. Supports standard mode and beachcombing mode.
---

# Xiamen Tide Calculator v3.2

## Copyright Notice

**Author**: Ke Yingjie
**Created**: April 2, 2026
**Last Updated**: April 3, 2026
**Version**: v3.2

### License

This skill is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Ke Yingjie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Disclaimer

1. **Accuracy Notice**: This skill is based on standard tide calculation formulas for Xiamen waters and is for reference only. Actual tide times may be affected by weather, atmospheric pressure, terrain, and other factors. It is recommended to use it in combination with on-site observation or official tide tables.

2. **Safety Warning**: Beachcombing involves certain risks. Please pay attention to safety:
   - Tide rise speed may exceed expectations
   - Reef surfaces are slippery and may cause falls
   - Marine life may cause injuries
   - Weather changes may bring danger

3. **Limitation of Liability**: Users assume all risks when using this skill for beachcombing activities. The developer is not responsible for any direct or indirect losses arising from the use of this skill.

4. **Data Sources**:
   - Tide calculation formula: Based on empirical formulas for Xiamen waters
   - Lunar conversion: Uses the zhdate open-source library
   - Location recommendations: Based on publicly available information

### Version History

- **v3.2** (2026-04-03): Added integrated window feature, optimized cross-day window display
- **v3.1** (2026-04-02): Added multi-window analysis and pros/cons description features
- **v3.0** (2026-04-02): Solar-to-lunar conversion, current date detection, leap month handling
- **v2.0** (2026-04-02): Added beachcombing mode, scoring system, multi-day comparison
- **v1.0** (2026-04-02): Initial release, basic tide calculation

### Contact

For questions or suggestions, please provide feedback via the WorkBuddy platform.

### Open Source Repository

This skill is open-sourced on GitHub. Contributions are welcome!

**GitHub Repository**: https://github.com/kingwingshome/xiamen-tide-calculator

**Open Source Content**:
- Complete source code
- Skill documentation
- Usage guides
- New feature guides

**Welcome**:
- ⭐ Star support
- 🔄 Fork improvements
- 📝 Submit Issues
- 💡 Contribute code

---

## Workflow

When a user asks about Xiamen tides:

1. **Determine Date**:
   - Supports solar date (YYYY-MM-DD format) auto-conversion to lunar
   - Supports current date auto-detection (--today parameter)
   - Supports direct lunar date input
   - Auto-detects leap months
2. **Determine Mode**: Based on user question, decide between standard mode or beachcombing mode
3. **Calculate Tides**: Call `scripts/tide_calculator.py` to calculate tides and beachcombing advice
4. **Integrate Windows** (optional): Use --integrated parameter to merge previous/next day windows, showing all available windows for the day
5. **Output Results**: Return information using the appropriate template

## Mode Selection

### Standard Mode
Use when: User only asks about tide times
- "Xiamen tide today"
- "Xiamen lunar 5th day tide"
- "April 2, 2025 Xiamen tide"
- "Tide schedule"

**Invocation**:
```bash
# Use current date
python scripts/tide_calculator.py --today

# Use solar date
python scripts/tide_calculator.py --solar-date 2025-04-02

# Use lunar date
python scripts/tide_calculator.py --lunar-day 15 --lunar-month 3
```

### Beachcombing Mode
Use when: User asks about beachcombing advice
- "Is today good for beachcombing?"
- "Best beachcombing time"
- "Beachcombing advice"
- "Where is good for beachcombing?"

**Invocation**:
```bash
# Current date beachcombing advice
python scripts/tide_calculator.py --today --beach-mode

# Specific date beachcombing advice
python scripts/tide_calculator.py --solar-date 2025-04-02 --beach-mode
python scripts/tide_calculator.py --lunar-day 2 --lunar-month 3 --beach-mode

# Integrated window mode (recommended) ⭐
python scripts/tide_calculator.py --solar-date 2026-04-05 --beach-mode --integrated
```

## New Features v3.0 ⭐

### 1. Solar-to-Lunar Date Auto-Conversion
- Supports solar date input (YYYY-MM-DD format)
- Auto-converts to lunar date for tide calculation
- Integrated zhdate library for accurate conversion

### 2. Current Date Auto-Detection
- Use --today parameter to automatically get current date
- Auto-converts to lunar date
- Suitable for quick queries about today's conditions

### 3. Leap Month Handling
- Auto-detects leap months
- Annotates "Leap X Month" in output during leap months
- Annotates "(Leap Month)" in tide size during leap months
- Extra +0.2 points in beachcombing score during leap months
- Provides special tips during leap months

## Output Format

### Standard Mode Output (Supports Leap Month)
```
【Xiamen Tide · Lunar 2025/3/5】
High Tide 1: HH:MM
High Tide 2: HH:MM or Next Day HH:MM
Low Tide 1: HH:MM or Previous Day HH:MM
Low Tide 2: HH:MM
Best Beachcombing: HH:MM-HH:MM (Window 1), HH:MM-HH:MM (Window 2)
Tide Size: Spring Tide / Middle Tide / Neap Tide (Leap Month)
Beachcombing Score: X.X (Recommendation Level)
```

### Beachcombing Mode Output (Supports Leap Month)
```
【Xiamen Beachcombing Advice · Lunar 2025 Leap 6/2】

🌊 Beachcombing Score: X.X (Recommendation Level)

⏰ Best Beachcombing Periods:

  【Window 1】HH:MM-HH:MM
  └─ Time Type: Morning/Afternoon/Evening/Early Morning
  └─ Advantages:
     ✅ Advantage 1
     ✅ Advantage 2
     ✅ Advantage 3
  └─ Notes:
     ❌ Note 1
     ❌ Note 2
  └─ ⭐ Recommendation Index: ⭐⭐⭐⭐⭐

  【Window 2】HH:MM-HH:MM
  └─ Time Type: Morning/Afternoon/Evening/Early Morning
  └─ Advantages:
     ✅ Advantage 1
     ✅ Advantage 2
     ✅ Advantage 3
  └─ Notes:
     ❌ Note 1
     ❌ Note 2
  └─ ⭐ Recommendation Index: ⭐⭐⭐⭐

📍 Recommended Locations:
  - Location 1: Description
  - Location 2: Description
  - Note: Tides may vary slightly during leap months (shown during leap months)

🐟 Expected Harvest:
  - Creature 1, Creature 2, Creature 3

🧰 Equipment Suggestions:
  - Essential: Tool 1, Tool 2
  - Recommended: Tool 3, Tool 4

⚠️ Safety Reminders:
  - Safety tip 1
  - Safety tip 2

📊 Tide Information:
  - Tide Size: Spring/Middle/Neap Tide (Leap Month)
  - Detailed tide times

🌡️ Current Season:
  - Season - Season description

💡 Beachcombing Tips:
  - Beachcombing tips and advice
  - During leap months, tides may vary slightly, on-site observation recommended (shown during leap months)
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

5. **Leap Month Factor** (Extra bonus) ⭐
   - Leap month: +0.2 points

### Recommendation Levels
- **Highly Recommended** (8.0-10.0): Spring tide + Daytime low tide + Suitable season
- **Recommended** (6.0-7.9): Spring or middle tide + Basic conditions met
- **Fair** (4.0-5.9): Middle tide + Some conditions average
- **Not Recommended** (0.0-3.9): Neap tide or poor conditions

## Tide Size Classification

- **Spring Tide**: Lunar 2nd, 3rd, 17th, 18th (best for beachcombing)
- **Middle Tide**: Other dates
- **Neap Tide**: Lunar 8th, 9th, 23rd, 24th (not recommended for beachcombing)
- **Leap Month Annotation**: Annotates "(Leap Month)" after tide size during leap months ⭐

## Beachcombing Windows

2 hours before low tide → 1 hour after low tide, one window per low tide point.

## Multi-day Comparison Query

When a user asks "Which day next week is best for beachcombing?":
1. Calculate daily beachcombing scores (supports leap month detection)
2. Sort by score
3. Recommend the top 3 highest-scoring days
4. Provide detailed advice

**Invocation**:
```bash
python scripts/compare_beach_days.py --lunar-month 3 --start-day 1 --days 10
```

## Notes

- Times use 24-hour format, cross-day annotated as "Next Day" or "Previous Day"
- Lunar dates must be between 1-30
- Tide calculations are based on standard formulas for Xiamen waters
- Beachcombing scores comprehensively consider tides, time, season, leap months, etc.
- Safety reminders are very important, please follow them
- Tides may vary slightly during leap months, on-site observation recommended ⭐

## New Features v3.1 ⭐⭐

### Multi-Window Analysis
- Auto-identifies time type for each window (morning, afternoon, evening, early morning)
- Filters non-current-day windows, only showing available beachcombing windows for the day
- Provides detailed pros and cons for each window
- Gives recommendation index based on time type (⭐⭐⭐-⭐⭐⭐⭐⭐)

### Time Window Types
- **Morning** (6:00-12:00): Good lighting, high safety, recommendation ⭐⭐⭐⭐⭐
- **Afternoon** (12:00-18:00): Good lighting, ample prep time, recommendation ⭐⭐⭐⭐
- **Evening** (18:00-21:00): Cool temperature, soft light, recommendation ⭐⭐⭐⭐⭐
- **Early Morning** (4:00-6:00): Quiet environment, most seafood, recommendation ⭐⭐⭐

### Window Pros/Cons Description
Each window provides:
- **Advantages**: 3-5 main benefits
- **Notes**: 2-3 things to watch out for
- **Recommendation Index**: Auto-rated based on time type

### Practical Application Scenarios
- Helps users choose the best window based on personal schedule
- Clearly understand pros and cons of each window for informed decisions
- Distinguish between current-day and non-current-day windows to avoid confusion

## New Features v3.2 ⭐⭐⭐

### Integrated Window Feature
- **Problem**: In single-day tide calculations, some windows may show as "Previous Day" or "Next Day" across days
- **Solution**: Calculate tides for the day before and after, integrate all available windows for the target day
- **Effect**: Users see complete beachcombing windows for the day, not cross-day windows

### How It Works
Taking April 5th as an example:

1. **Calculate April 4th tides**:
   - Window 1: Previous Day 17:24 - Previous Day 20:24 (not current day)
   - Window 2: 05:48-08:48 (early morning)

2. **Calculate April 5th tides**:
   - Window 1: Previous Day 18:12 - Previous Day 21:12 (not current day)
   - Window 2: 06:36-09:36 (morning)

3. **Calculate April 6th tides**:
   - Window 1: Previous Day 19:00 - Previous Day 22:00 (not current day)
   - Window 2: 07:24-10:24 (morning)

4. **Integrated Result**:
   - April 5th's Window 2 (06:36-09:36) from the current day
   - April 6th's Window 1 (Previous Day 19:00 - Previous Day 22:00) actually belongs to April 5th evening

5. **Final Output**:
   - Window 1: 06:36-09:36 (Morning)
   - Window 2: 19:00-22:00 (Evening) ⭐ Integrated from April 6th

### Usage
```bash
# Enable integrated window feature (recommended)
python scripts/tide_calculator.py --solar-date 2026-04-05 --beach-mode --integrated
```

### Comparison of Results

**Without --integrated**:
```
April 5th beachcombing times:
  Window 1: Previous Day 18:12 - Previous Day 21:12 (non-current day window) ⚠️
  Window 2: 06:36-09:36 (Morning)
```

**With --integrated**:
```
April 5th beachcombing times:
  Window 1: 06:36-09:36 (Morning)
  Window 2: 19:00-22:00 (Evening) ⭐ From April 6th
```

### User Value
1. **More Complete Information**: See all available beachcombing windows for the day without missing any
2. **More Intuitive**: Users expect to see today's times, not cross-day annotations
3. **Better Decisions**: Clearly know there are morning and evening windows to choose from
4. **Avoid Confusion**: No need to manually calculate cross-day window correspondences

## Dependency Requirements ⭐

- Python 3.6+
- zhdate library (for lunar conversion): `pip install zhdate`
