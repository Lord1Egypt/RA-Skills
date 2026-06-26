# Medication Skill Examples

## 1. Add Medication

### Example 1: Once Daily
```
User: Aspirin 100mg once daily after breakfast

Save:
{
  "name": "Aspirin",
  "dosage": {"value": 100, "unit": "mg"},
  "frequency": {"type": "daily", "times_per_day": 1},
  "schedule": [
    {"weekday": 1, "time": "08:00", "timing_label": "After Breakfast"},
    {"weekday": 2, "time": "08:00", "timing_label": "After Breakfast"},
    ...
  ]
}
```

### Example 2: Twice Daily
```
User: Amlodipine 5mg twice daily morning and evening

Save:
{
  "name": "Amlodipine",
  "dosage": {"value": 5, "unit": "mg"},
  "frequency": {"type": "daily", "times_per_day": 2},
  "schedule": [
    {"weekday": 1, "time": "08:00", "timing_label": "Morning"},
    {"weekday": 1, "time": "20:00", "timing_label": "Evening"},
    ...
  ]
}
```

### Example 3: Once Weekly
```
User: Vitamin D 1000IU once weekly

Save:
{
  "name": "Vitamin D",
  "dosage": {"value": 1000, "unit": "IU"},
  "frequency": {"type": "weekly"},
  "schedule": [
    {"weekday": 1, "time": "08:00", "timing_label": "Monday Morning"}
  ]
}
```

## 2. Record Medication

### Example 4: Normal Medication
```
User: Already took Aspirin

Save:
{
  "status": "taken",
  "actual_time": "2025-12-31T08:15:00"
}
```

### Example 5: Missed Dose
```
User: Forgot to take Amlodipine

Save:
{
  "status": "missed",
  "notes": "Forgot to take"
}

Output make-up recommendation: If less than 2 hours from scheduled time, take immediately
```

## 3. View List

### Example 6: Medication List
```
User: View medication list

Output:
💊 My Medication List

1. Aspirin - 100 mg
   Once daily, take after breakfast

2. Amlodipine - 5 mg
   Twice daily, take morning and evening
```

## 4. Adherence Statistics

### Example 7: Weekly Statistics
```
User: This week's medication statistics

Output:
📊 Medication Adherence Statistics
Overall Adherence: 85.7% ✅

Aspirin: 100% ✅
Amlodipine: 78.6% ⚠️
```
