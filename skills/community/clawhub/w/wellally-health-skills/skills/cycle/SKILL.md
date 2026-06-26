---
name: cycle
description: Track menstrual cycle, PMS symptoms, ovulation prediction, and women's health insights
argument-hint: <operation_type+description, e.g.: start period started today, log heavy flow today, predict conception mode>
allowed-tools: Read, Write
schema: cycle/schema.json
---

# Menstrual Cycle Tracking Skill

Track menstrual cycles, PMS symptoms, ovulation prediction, and provide personalized health insights.

## Core Flow

```
User Input → Parse Operation Type → Execute Operation → Generate/Update Data → Save → Output Result
```

## Supported Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| start | Log period start | /cycle start period started today |
| end | Log period end | /cycle end ended today |
| log | Log daily entry | /cycle log heavy flow today abdominal pain |
| predict | Ovulation prediction | /cycle predict conception mode |
| history | View history | /cycle history 6 |
| analyze | Analyze patterns | /cycle analyze |
| status | Current status | /cycle status |
| settings | Configure settings | /cycle settings cycle-length=28 |

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation |
|----------------|-----------|
| start | start |
| end | end |
| log | log |
| predict | predict |
| history | history |
| analyze | analyze |
| status | status |
| settings | settings |

### Date Recognition

| Input | Date Format |
|------|-------------|
| today | Current date |
| YYYY-MM-DD | Specified date |
| Month DD | Specified date this year |
| Day X | Relative cycle day |

### Flow Intensity Recognition

| Keywords | Intensity | Value |
|----------|-----------|-------|
| very_heavy | very_heavy | 5 |
| heavy | heavy | 4 |
| medium | medium | 3 |
| light | light | 2 |
| spotting | spotting | 1 |

### Symptom Recognition

**Pain**: abdominal pain, lower back pain, headache, breast tenderness, joint pain
**Digestive**: bloating, diarrhea, constipation, nausea, appetite changes
**Emotional**: mood swings, irritability, anxiety, low mood, agitation
**Energy**: fatigue, tiredness, low energy, drowsiness

### Mood Recognition

**Positive**: happy, cheerful, calm, normal
**Negative**: low, anxious, irritable, agitated, depressed
**Neutral**: fair, normal, okay

### Energy Level Recognition

**High**: energetic, active, good
**Medium**: normal, fair, okay
**Low**: fatigued, tired, exhausted, no energy

## Step 2: Check Information Completeness

### start Operation Required:
- None (uses default date: today)

### start Operation Validation:
- Date cannot be in the future
- If there's an ongoing cycle, prompt to end it first

### end Operation Required:
- None (uses default date: today)

### end Operation Validation:
- Must have an active cycle
- End date must be after start date

### log Operation Required:
- description (log content)

### log Operation Recommended:
- date (optional, defaults to today)
- flow description
- symptoms

## Step 3: Interactive Prompts (If Needed)

### Scenario A: start Again Before Ending
```
Unfinished cycle detected

Current cycle: Started 2025-11-28
Tip: Please use /cycle end to end current cycle first
```

### Scenario B: end Without Active Cycle
```
No active cycle

Recent cycle: 2025-11-30 - 2025-12-04
Tip: Please use /cycle start to begin a new cycle
```

### Scenario C: Insufficient log Content
```
Please provide more log information, such as:
• Flow: heavy, medium, light
• Symptoms: abdominal pain, lower back pain, headache, etc.
• Mood: normal, low, anxious
```

## Step 4: Generate JSON

### Cycle Data Structure

```json
{
  "cycle_id": "cycle_20251228",
  "period_start": "2025-12-28",
  "period_end": null,
  "cycle_length": null,
  "period_length": null,
  "flow_pattern": {
    "day_1": "heavy",
    "day_2": "medium"
  },
  "pms_symptoms": {
    "start_date": null,
    "symptoms": {}
  },
  "daily_logs": [],
  "ovulation_date": null,
  "predictions": {},
  "notes": "",
  "created_at": "2025-12-28T08:00:00.000Z",
  "completed": false
}
```

### Daily Log Data Structure

```json
{
  "id": "log_20251228001",
  "date": "2025-12-28",
  "cycle_day": 1,
  "phase": "menstrual",
  "flow": {
    "intensity": "heavy",
    "description": "Heavy flow"
  },
  "symptoms": ["abdominal pain", "lower back pain"],
  "mood": "low",
  "energy_level": "low",
  "medication_taken": [],
  "notes": "",
  "created_at": "2025-12-28T20:00:00.000Z"
}
```

Complete schema definition: see [schema.json](schema.json).

## Step 5: Save Data

1. Read `data/cycle-tracker.json`
2. Update corresponding data
3. Write back to file
4. If detailed records exist, save to `data/周期记录/YYYY-MM/YYYY-MM-DD_周期记录.json`

## Execution Instructions

```
1. Parse user input and determine operation type
2. Execute corresponding logic based on operation type
3. Validate input data and state
4. Generate JSON compliant with schema.json
5. Save to data/cycle-tracker.json
6. Output operation result and summary to user
```

## Example Interactions

### Example 1: Start Cycle
```
User: /cycle start period started today

System:
Cycle record created

Cycle Information:
Period start: 2025-12-28

Prediction Information:
Expected next period: 2026-01-25
Expected ovulation date: 2026-01-11
Fertile window: January 6 - January 12

Current Status:
Cycle day: 1
Phase: Menstrual phase

Data saved to: data/周期记录/2025-12/2025-12-28_周期记录.json
```

### Example 2: Log Entry
```
User: /cycle log heavy flow today abdominal pain

System:
Daily log recorded

Log Information:
Date: 2025-12-28
Cycle day: 1
Phase: Menstrual phase

Flow: Heavy (level 4)
Symptoms: Abdominal pain
Mood: Normal
Energy: Medium

Cycle Progress:
Day 1/5 of current cycle (estimated)
Days to ovulation: 13
Days to next period: 27

Data saved to: data/周期记录/2025-12/2025-12-28_周期记录.json
```

### Example 3: Ovulation Prediction
```
User: /cycle predict conception mode

System:
Ovulation Prediction (Conception Mode)

Based on last 6 cycles:
Average cycle length: 28.5 days
Cycle regularity: 92% (very regular)

Ovulation Prediction:
Expected ovulation date: January 11, 2026

Detailed Fertile Schedule:
January 6 (Fertile day 1): 10% conception probability
January 7 (Fertile day 2): 15% conception probability
January 8 (Fertile day 3): 20% conception probability
January 9 (Fertile day 4): 25% conception probability
January 10 (Fertile day 5): 30% conception probability
January 11 (Ovulation day): 35% conception probability
January 12 (Fertile day 7): 15% conception probability

Best conception window: January 9 - January 11

Conception Advice:
• Start folic acid supplementation 3 months early (400-800μg/day)
• Maintain moderately frequent intercourse during fertile period
• Lie down for 15-30 minutes after intercourse
• Maintain healthy weight and regular sleep schedule
```

For more examples, see [examples.md](examples.md).
