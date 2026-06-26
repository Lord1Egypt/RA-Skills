# fitness Skill Examples

## I. Record Workout

### Example 1: Quick Record Running
```
User: /fitness record running 30minutes

Save:
{
  "date": "2025-06-20",
  "time": "07:00",
  "type": "running",
  "duration_minutes": 30,
  "intensity": { "level": "moderate", "rpe": 13 }
}
```

### Example 2: Detailed Record Cycling
```
User: /fitness record cycling 45minutes moderate_intensity

Save:
{
  "type": "cycling",
  "duration_minutes": 45,
  "intensity": { "level": "moderate", "rpe": 14 }
}
```

### Example 3: Record Swimming
```
User: /fitness record swimming 60minutes low_intensity

Save:
{
  "type": "swimming",
  "duration_minutes": 60,
  "intensity": { "level": "low", "rpe": 10 }
}
```

### Example 4: Running with Pace
```
User: /fitness record running 30 minutes distance 5km pace 6min_per_km

Save:
{
  "type": "running",
  "duration_minutes": 30,
  "distance_km": 5.0,
  "pace_min_per_km": "6:00"
}
```

### Example 5: With Heart Rate Data
```
User: /fitness record cycling 45 minutes moderate heart_rate 145 calories 400

Save:
{
  "type": "cycling",
  "duration_minutes": 45,
  "intensity": { "level": "moderate" },
  "heart_rate": { "avg": 145 },
  "calories_burned": 400
}
```

### Example 6: Strength Training
```
User: /fitness record strength 60 chest_training bench_press 50kg 3x12

Save:
{
  "type": "strength",
  "duration_minutes": 60,
  "notes": "Chest training bench_press 50kg 3x12"
}
```

### Example 7: Sports
```
User: /fitness record basketball 90 minutes competitive

Save:
{
  "type": "basketball",
  "duration_minutes": 90,
  "notes": "competitive"
}
```

## II. View Workout History

### Example 8: View Recent Records
```
User: /fitness history

Output:
📋 Recent Workout Records

2025-06-20 07:00 - Running 30 minutes Moderate intensity
2025-06-19 18:30 - Swimming 45 minutes Low intensity
2025-06-18 07:00 - Cycling 60 minutes Moderate intensity

Weekly Total: 3 workouts, 135 minutes
```

### Example 9: View Weekly Statistics
```
User: /fitness history week

Output:
Weekly Workout Records (June 14 - June 20)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Workout Count: 5 times
Total Duration: 240 minutes
Total Distance: 35 km
Calories Burned: 1800 kcal

Workout Type Distribution:
Running: 2 times
Cycling: 2 times
Swimming: 1 time
```

## III. Workout Statistics Analysis

### Example 10: Weekly Statistics
```
User: /fitness stats week

Output:
📊 Weekly Workout Statistics

Workout Volume:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Duration: 240 minutes (Average 34 min/session)
Total Distance: 35 km
Calories Burned: 1800 kcal

Workout Frequency: 5 days/week ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommendation: 3-5 days per week recommended, current meets recommendation

Intensity Distribution:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Low Intensity: 40%
Moderate Intensity: 60%
High Intensity: 0%

Comparison with Last Week:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Duration: +30 minutes ↗️
Distance: +5 km ↗️
Frequency: Unchanged
```

### Example 11: Specific Statistics
```
User: /fitness stats calories

Output:
Calorie Burn Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━
This Week: 1800 kcal
Average: 360 kcal/session
This Month: 7200 kcal
```

## IV. Fitness Goal Management

### Example 12: Set Weight Loss Goal
```
User: /fitness goal lose_weight 5kg 2025-06-30

Save:
{
  "goal_id": "goal_20250101",
  "category": "weight_loss",
  "title": "Lose 5 kg",
  "start_date": "2025-01-01",
  "target_date": "2025-06-30",
  "baseline_value": 75.0,
  "target_value": 70.0,
  "unit": "kg"
}
```

### Example 13: Set Running Goal
```
User: /fitness goal 5km_run 2025-08-15

Save:
{
  "category": "endurance",
  "title": "5 km run",
  "target_date": "2025-08-15"
}
```

### Example 14: Update Goal Progress
```
User: /fitness goal progress lose_weight 0.5kg

Update goal progress
```

### Example 15: View Goals
```
User: /fitness goal active

Output:
🎯 Active Goals

Lose 5 kg
━━━━━━━━━━━━━━━━━━━━━━━━━━
Start: 2025-01-01
Target: 2025-06-30
Current: 72.5 kg
Goal: 70.0 kg
Progress: 50% ⏳
Status: On track
```

## V. Workout Analysis

### Example 16: Trend Analysis
```
User: /fitness trend 30days

Output:
📈 Workout Trend Analysis (Last 30 days)

Workout Volume Trend:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 1: 120 minutes
Week 2: 180 minutes
Week 3: 210 minutes
Week 4: 240 minutes
Trend: Consistent increase ↗️

Intensity Distribution Change:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Low Intensity: 50% → 40%
Moderate Intensity: 50% → 60%

Progress Tracking:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Running Pace: 6'30" → 6'00" ✅
Workout Duration: Average 30 min → 40 min
```

## VI. Exercise Prescription Recommendations

### Example 17: Beginner Exercise Prescription
```
User: /fitness prescription beginner

Output:
🏋️ Beginner Exercise Prescription Reference

FITT Principles:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Frequency: 3-4 times per week
Intensity: RPE 11-13 (Somewhat hard)
Time: 20-30 minutes per session
Type: Primarily aerobic exercise

Recommended Activities:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Brisk walking: 3 times per week, 20-30 minutes each
• Cycling: 2 times per week, 30 minutes each
• Swimming: 1 time per week, 20-30 minutes each
• Strength training: 2 times per week, primarily bodyweight

Notes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Warm up 5-10 minutes before exercise
• Cool down and stretch 5-10 minutes after exercise
• Gradually increase exercise volume
• Stop immediately if you feel discomfort
```

### Example 18: Hypertension Patient Exercise Recommendations
```
User: /fitness prescription hypertension

Output:
Exercise Recommendations for Hypertension Patients

FITT Principles:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Frequency: 5-7 times per week
Intensity: Moderate intensity (40-60% max heart rate)
Time: 30-60 minutes per session
Type: Primarily aerobic exercise

Recommended Activities:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Brisk walking
• Cycling
• Swimming
• Tai Chi

Avoid:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• High-intensity interval training
• Heavy strength training
• Exercises with head below heart level

Notes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Measure blood pressure before exercise
• Do not exercise if BP >180/100 mmHg
• Avoid breath-holding movements
• Cool down gradually, don't stop suddenly
```
