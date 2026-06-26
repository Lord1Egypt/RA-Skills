---
name: child-sleep
description: Track child sleep patterns, manage sleep schedules, and identify sleep problems. Use when user mentions child sleep, bedtime, waking up, nap, or sleep issues.
argument-hint: <operation_type: record/schedule/problem/analysis/routine/history, e.g.: record 9pm sleep 7am wake, schedule, problem difficulty falling asleep, analysis, routine>
allowed-tools: Read, Write
schema: child-sleep/schema.json
---

# Child Sleep Management Skill

Child sleep recording, schedule management and sleep problem identification, providing age-specific sleep duration references and schedule recommendations.

## Core Flow

```
User Input → Identify Operation Type → Read Child Information → Determine Sleep Standards by Age → Generate Assessment Report → Save Data
```

## Step 1: Parse User Input

### Operation Type Mapping

| Input | action | Description |
|------|--------|-------------|
| record | record | Log sleep |
| schedule | schedule | Schedule management |
| problem | problem | Sleep problems |
| analysis | analysis | Sleep analysis |
| routine | routine | Schedule recommendations |
| history | history | Historical records |

### Time Recognition

| Input Pattern | Parsed Result |
|---------------|---------------|
| 21:00 sleep, bedtime 21:00 | bedtime: 21:00 |
| 7:00 wake, wake 7:00 | wake_time: 07:00 |
| woke 1 time, wakeup 1 | night_wakeups: 1 |

## Step 2: Check Information Completeness

### record Operation Required:
- Bedtime (can infer from input or use default)
- Wake time (can infer from input or use default)

### Optional Information:
- Night wakeups
- Time to fall asleep
- Sleep quality description

## Step 3: Determine Sleep Standards by Age

| Age | Recommended Total Sleep | Night Sleep | Daytime Naps | Nap Count |
|-----|-------------------------|-------------|--------------|-----------|
| 0-3 months | 14-17 hours | 8-10 hours | 6-7 hours | 3-4 naps |
| 4-12 months | 12-16 hours | 9-12 hours | 3-4 hours | 2-3 naps |
| 1-2 years | 11-14 hours | 10-12 hours | 1.5-3 hours | 1-2 naps |
| 3-5 years | 10-13 hours | 10-12 hours | 0-2 hours | 0-1 naps |
| 6-12 years | 9-12 hours | 9-12 hours | 0 | 0 naps |
| 13-18 years | 8-10 hours | 8-10 hours | 0 | 0 naps |

## Step 4: Generate Assessment Report

### Sleep Quality Assessment

| Assessment Item | Standard |
|----------------|----------|
| Sleep duration | Within recommended range is normal |
| Time to fall asleep | Within 30 minutes is normal |
| Night wakeups | 0-1 times is normal (more for <1 year) |
| Sleep quality | Good energy, normal development is good |

### Normal Sleep Report Example:
```
Sleep record saved

Sleep Information:
Child: Xiaoming
Age: 2 years 5 months
Sleep date: Night of January 13, 2025

Bedtime: 21:00
Asleep time: 21:30
Wake time: 07:00
Total sleep duration: 9.5 hours

Night Status:
  Night wakeups: 1 time
  Wake duration: ~10 minutes
  Falling asleep: Self-soothing
  Sleep quality: Good

Sleep Assessment:
  Sleep duration normal (recommended 10-12 hours)
  Appropriate bedtime
  Normal night wakeups
  Good sleep quality

Daytime Naps:
  Nap count: 1 time
  Nap duration: ~2 hours
  Total sleep (including naps): ~11.5 hours

Schedule Recommendations:
  Continue current schedule
  Establish consistent bedtime routine
  Create good sleep environment

Data saved
```

### Sleep Insufficient Example:
```
Sleep Insufficient Alert

Sleep Information:
Child: Xiaoming
Age: 2 years 5 months
Sleep date: Night of January 13, 2025

Bedtime: 22:00
Asleep time: 23:00
Wake time: 06:30
Total sleep duration: 7.5 hours

Sleep Assessment:
  Insufficient sleep duration (recommended 10-12 hours)
  Late bedtime
  Difficulty falling asleep
  Frequent night wakeups

Possible Impact:
  Poor daytime energy
  Irritability
  Decreased appetite
  Lowered immunity

Improvement Recommendations:

Adjust Schedule
  Start bedtime routine 30 minutes early
  Fixed bedtime (20:30-21:00)

Optimize Bedtime Routine
  Stop screen time 1 hour before
  Quiet activities (picture books, warm bath)
  Fixed routine order

Improve Sleep Environment
  Room temperature 20-22°C
  Keep dark and quiet
  Comfortable bedding

If sleep deprivation persists:
  Consult pediatrician to rule out sleep disorders etc.

Data saved
```

## Step 5: Save Data

Save to `data/child-sleep-tracker.json`, including:
- child_profile: Child basic information
- sleep_records: Sleep records
- sleep_schedule: Schedule
- bedtime_routine: Bedtime routine
- sleep_problems: Sleep problem records
- statistics: Statistical information

## Common Sleep Problems

### Difficulty Falling Asleep
- Presentation: Cannot fall asleep 30+ minutes after bedtime
- Possible causes: Irregular schedule, over-tiredness, sleep environment
- Recommendations: Fixed schedule, start bedtime routine early

### Frequent Night Waking
- Presentation: Waking 2+ times nightly
- Possible causes: Hunger, discomfort, habitual waking
- Recommendations: Identify cause, gradually reduce intervention

### Early Rising
- Presentation: Waking before 6am and unable to return to sleep
- Possible causes: Sleep environment, schedule arrangement
- Recommendations: Adjust bedtime, block morning light

### Refusing Naps
- Presentation: Unwilling to nap during day
- Possible causes: Developmental stage, high energy
- Recommendations: Maintain quiet time, not force naps

### Night Terrors/Nightmares
- Presentation: Terrified crying at night
- Possible causes: Developmental stage, over-tiredness
- Recommendations: Soothe, don't wake

## Bedtime Routine Recommendations (2-3 Years)

### 1 Hour Before (20:00)
- Stop screen time
- Stop vigorous activities
- Switch to quiet mode

### 30 Minutes Before (20:30)
- Put away toys
- Use toilet, drink water
- Prepare for bath

### Bath Time (20:40)
- Warm bath (10-15 minutes)
- Put on pajamas/diaper

### Quiet Activities (21:00)
- Bedtime storybooks (2-3 books)
- Soft talking/singing
- Goodnight ritual

### Bedtime (21:15-21:30)
- Get into bed, cover with blanket
- Final comfort
- Say goodnight, leave room

## Execution Instructions

1. Read data/profile.json for child information
2. Determine sleep standards based on age
3. Analyze sleep information or generate recommendations
4. Save to data/child-sleep-tracker.json

## Medical Safety Principles

### Safety Boundaries
- No sleep disorder diagnosis
- No sleep medication recommendations
- No handling of severe problems like sleep apnea

### System Can
- Sleep recording and tracking
- Sleep pattern analysis
- Schedule recommendations
- Common problem guidance

## Important Notice

This system is for sleep recording and recommendation reference only, **cannot replace professional medical diagnosis**.

If following conditions occur, **please consult pediatrician**:
- Snoring with breathing pauses
- Frequent terrified crying at night
- Excessive daytime sleepiness
- Abnormal behaviors during sleep
- Long-term severe insomnia
