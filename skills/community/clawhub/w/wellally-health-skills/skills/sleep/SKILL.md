---
name: sleep
description: Record and track sleep patterns, evaluate sleep quality with PSQI/Epworth/ISI scales, identify sleep problems, and provide sleep hygiene recommendations. Use for insomnia tracking, sleep analysis, and sleep disorder screening.
argument-hint: <operation_type sleep_info, e.g.: record 23:00 07:00 good>
allowed-tools: Read, Write
schema: sleep/schema.json
---

# Sleep Quality Management Skill

Record sleep, evaluate sleep quality, identify sleep problems, and provide sleep hygiene recommendations.

## Medical Safety Disclaimer

The sleep assessment, problem identification, and recommendations provided by this system are for reference only and do not constitute medical diagnosis or treatment plans.

**Cannot Do:**
- Do not diagnose sleep disorders such as insomnia, sleep apnea, etc.
- Do not prescribe sleep medications or adjust medication dosages
- Do not replace professional sleep medicine treatment (such as CBT-I, CPAP, etc.)
- Do not handle severe sleep disorders or emergency situations

**Can Do:**
- Record and track sleep data
- Evaluate sleep quality trends
- Identify sleep problem risks
- Provide sleep hygiene recommendations
- Analyze sleep patterns and influencing factors

## When to Seek Medical Attention
- Insomnia persisting for more than 3 months, severely affecting daily life
- Symptoms of sleep apnea (snoring, waking up gasping, daytime sleepiness)
- Restless leg symptoms severely affecting sleep
- Severe sleepiness affecting work, study, or driving safety

## Core Flow

```
User Input → Identify Operation Type → [record] Parse Sleep Info → Save Record
                              ↓
                         [history/stats] Read Data → Display Report
                              ↓
                         [psqi/epworth/isi] Parse Assessment Results → Save → Display Interpretation
                              ↓
                         [problem] Parse Problem → Assess Risk → Save
                              ↓
                         [hygiene] Parse Habits → Assess → Provide Recommendations
                              ↓
                         [recommendations] Generate Personalized Recommendations
```

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation Type |
|----------------|----------------|
| record | record - Log sleep |
| history | history - View history records |
| stats | stats - Sleep statistical analysis |
| psqi, PSQI | psqi - PSQI assessment |
| epworth | epworth - Epworth Sleepiness Scale |
| isi, ISI | isi - ISI Insomnia Severity Assessment |
| problem | problem - Sleep problem identification |
| hygiene | hygiene - Sleep hygiene assessment |
| recommendations | recommendations - Get recommendations |

## Step 2: Parameter Parsing Rules

### Sleep Quality Description

| Input | quality Value |
|-------|--------------|
| excellent | excellent |
| very good | very good |
| good | good |
| fair | fair |
| poor | poor |
| very poor | very poor |

### Influencing Factor Recognition

| Input | Factor |
|-------|--------|
| caffeine_after_2pm | Caffeine after 2 PM |
| alcohol | Alcohol consumption |
| exercise: morning/afternoon/evening | Exercise time |
| screen_time: 90 | Screen time 90 minutes before bed |
| stress: low/medium/high | Stress level |

## Step 3: Generate JSON

### Sleep Record Data Structure

```json
{
  "id": "sleep_20250620_001",
  "date": "2025-06-20",
  "sleep_times": {
    "bedtime": "23:00",
    "sleep_onset_time": "23:30",
    "wake_time": "07:00",
    "out_of_bed_time": "07:15"
  },
  "sleep_metrics": {
    "sleep_duration_hours": 7.0,
    "time_in_bed_hours": 8.25,
    "sleep_latency_minutes": 30,
    "sleep_efficiency": 84.8
  },
  "awakenings": {
    "count": 2,
    "total_duration_minutes": 15,
    "causes": ["bathroom", "noise"]
  },
  "sleep_quality": {
    "subjective_quality": "fair",
    "quality_score": 5,
    "rested_feeling": "somewhat",
    "morning_mood": "neutral"
  }
}
```

### PSQI Assessment Data Structure

```json
{
  "date": "2025-06-20",
  "components": {
    "subjective_quality": 2,
    "sleep_latency": 1,
    "sleep_duration": 2,
    "sleep_efficiency": 1,
    "sleep_disturbances": 2,
    "hypnotic_use": 0,
    "daytime_dysfunction": 2
  },
  "total_score": 10,
  "interpretation": "Fair sleep quality"
}
```

### Epworth Sleepiness Scale Data Structure

```json
{
  "date": "2025-06-20",
  "responses": [
    {"situation": "sitting_reading", "score": 0},
    {"situation": "watching_tv", "score": 1},
    {"situation": "public_sitting", "score": 0},
    {"situation": "passenger_car", "score": 1},
    {"situation": "lying_afternoon", "score": 2},
    {"situation": "talking", "score": 0},
    {"situation": "after_lunch", "score": 1},
    {"situation": "traffic", "score": 0}
  ],
  "total_score": 5,
  "interpretation": "Normal"
}
```

## Step 4: Save Data

1. Read `data/sleep-tracker.json`
2. Update corresponding record sections
3. Write back to file

## PSQI Assessment Standards

### Score Range
- <=5: Good sleep quality
- 6-10: Fair sleep quality
- >=11: Poor sleep quality

### Component Scoring

| Component | 0 points | 1 point | 2 points | 3 points |
|-----------|----------|---------|----------|----------|
| Subjective sleep quality | Very good | Fairly good | Fairly bad | Very bad |
| Sleep latency | <=15 min | 16-30 min | 31-60 min | >60 min |
| Sleep duration | >7 hours | 6-7 hours | 5-6 hours | <5 hours |
| Sleep efficiency | >85% | 75-84% | 65-74% | <65% |
| Sleep disturbances | No issues | <1/week | 1-2/week | >=3/week |
| Hypnotic use | None | <1/week | 1-2/week | >=3/week |
| Daytime dysfunction | None | <1/week | 1-2/week | >=3/week |

## Epworth Sleepiness Scale Standards

| Total Score | Result |
|-------------|--------|
| 0-7 | Normal |
| 8-10 | Mild sleepiness |
| 11-15 | Moderate sleepiness |
| 16-24 | Severe sleepiness |

## ISI Insomnia Severity Standards

| Total Score | Result |
|-------------|--------|
| 0-7 | No clinically significant insomnia |
| 8-14 | Mild insomnia |
| 15-21 | Moderate insomnia |
| 22-28 | Severe insomnia |

For more examples, see [examples.md](examples.md).
