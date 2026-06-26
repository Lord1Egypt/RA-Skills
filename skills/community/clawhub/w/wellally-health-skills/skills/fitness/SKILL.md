---
name: fitness
description: Record exercise, manage fitness goals, generate workout prescriptions, and analyze fitness trends. Use when user wants to log workouts, track progress, or get exercise recommendations.
argument-hint: <operation_type exercise_info, e.g.: record running 30minutes>
allowed-tools: Read, Write
schema: fitness/schema.json
---

# Exercise and Fitness Management Skill

Record exercise, manage fitness goals, generate workout prescriptions, and analyze fitness trends.

## Medical Safety Disclaimer

**Important: The exercise recommendations and analysis provided by this system are for reference only and do not constitute medical advice or specific exercise prescriptions.**

**Cannot Do:**
- Do not provide specific exercise prescriptions - exercise prescriptions must be formulated by doctors or exercise specialists
- Do not handle exercise injuries - injuries require medical attention
- Do not assess cardiovascular risk - medical evaluation required before exercise
- Do not replace professional guidance - complex exercises require professional coach guidance

**Can Do:**
- Exercise data recording and analysis
- Fitness goal management
- Exercise trend identification
- General exercise recommendations
- Reference recommendations based on health conditions

## Core Flow

```
User Input → Identify Operation Type → [record] Parse Exercise Info → Save Record
                              ↓
                         [history/stats] Read Data → Display Report
                              ↓
                         [goal] Parse Goal → Update Goal → Save
                              ↓
                         [analysis] Read Data → Analyze Trends → Display Results
                              ↓
                         [prescription] Based on Health Status → Provide Reference Recommendations
```

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation Type |
|----------------|----------------|
| record | record - Log exercise |
| history | history - View history records |
| stats | stats - Exercise statistical analysis |
| goal | goal - Goal management |
| analysis | analysis - Exercise analysis |
| prescription | prescription - Exercise prescription recommendations |
| precautions | precautions - Precautions |

### Exercise Type Recognition

#### Aerobic Exercise
| Keywords | Type |
|----------|------|
| running | running |
| walking | walking |
| cycling | cycling |
| swimming | swimming |
| jump_rope | jump_rope |
| aerobics | aerobics |
| elliptical | elliptical |
| rowing | rowing |

#### Strength Training
| Keywords | Type |
|----------|------|
| strength | strength |
| calisthenics | calisthenics |
| machine_weights | machine_weights |
| free_weights | free_weights |
| resistance_bands | resistance_bands |

#### Ball Sports
| Keywords | Type |
|----------|------|
| basketball | basketball |
| soccer | soccer |
| badminton | badminton |
| ping_pong | ping_pong |
| tennis | tennis |
| volleyball | volleyball |

#### Other Exercises
| Keywords | Type |
|----------|------|
| yoga | yoga |
| pilates | pilates |
| tai_chi | tai_chi |
| dance | dance |
| hiking | hiking |
| skiing | skiing |

### Intensity Recognition

| Input | level | rpe |
|-------|-------|-----|
| low | low | 9-11 |
| moderate | moderate | 12-14 |
| high | high | 15-17 |
| rpe 13 | moderate | 13 |
| heart_rate 145, hr 145 | moderate | ~13 |

## Step 2: Parse Exercise Parameters

### Duration Recognition
- "30 minutes" → 30
- "1 hour" → 60
- "90 minutes" → 90

### Distance Recognition
- "5km" → 5.0
- "3 km" → 3.0
- "1000m" → 1.0 |

### Pace Recognition
- "6min_per_km" → "6:00"
- "5'30"" → "5:30"

### Heart Rate Recognition
- "heart_rate 145" → {avg: 145}
- "hr 145 max 165" → {avg: 145, max: 165}

### Calorie Recognition
- "calories 300" → 300
- "burned 400 kcal" → 400 |

## Step 3: Generate JSON

### Exercise Record Data Structure

```json
{
  "date": "2025-06-20",
  "time": "07:00",
  "type": "running",
  "duration_minutes": 30,
  "intensity": {
    "level": "moderate",
    "rpe": 13
  },
  "heart_rate": {
    "avg": 145,
    "max": 165,
    "min": 120
  },
  "distance_km": 5.0,
  "pace_min_per_km": "6:00",
  "calories_burned": 300,
  "how_felt": "good",
  "notes": "Felt comfortable, steady pace"
}
```

### Fitness Goal Data Structure

```json
{
  "goal_id": "goal_20250101",
  "category": "weight_loss",
  "title": "Lose 5 kg",
  "start_date": "2025-01-01",
  "target_date": "2025-06-30",
  "baseline_value": 75.0,
  "current_value": 70.5,
  "target_value": 70.0,
  "unit": "kg",
  "progress": 90,
  "status": "on_track"
}
```

## Step 4: Save Data

1. Read `data/fitness-tracker.json`
2. Update corresponding record sections
3. Write back to file

## FITT Principle Reference

### Frequency（频率）
- Exercise days per week
- General recommendation: 3-5 days/week

### Intensity（强度）
- Target heart rate zone = (220 - age) × 60-80%
- RPE 12-16（somewhat hard to hard）
- MET value reference

### Time（时间）
- Warm-up: 5-10 minutes
- Main exercise: 20-60 minutes
- Cool-down: 5-10 minutes

### Type（类型）
- Aerobic exercise: running, swimming, cycling, etc.
- Strength training: bodyweight, machines, free weights
- Flexibility training: stretching, yoga
- Balance training: tai chi, single-leg stand

## Goal Types

| Type | Description | Example |
|------|-------------|---------|
| weight_loss | Weight loss goal | Lose 5 kg |
| muscle_gain | Muscle gain goal | Gain 2 kg muscle |
| endurance | Endurance goal | Run 5K under 30 minutes |
| health | Health goal | Lower resting heart rate |
| habit | Habit formation | Exercise 4 days per week |

For more examples, see [examples.md](examples.md).
