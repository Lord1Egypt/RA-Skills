# eye-health Skill Examples

## I. Record Vision Examination

### Example 1: Record Uncorrected Vision
```
User: /eye vision left 1.0 right 0.8

Save:
{
  "id": "vision_20250102000001",
  "date": "2025-01-02",
  "left_eye": { "uncorrected_va": 1.0 },
  "right_eye": { "uncorrected_va": 0.8 }
}
```

### Example 2: Record Corrected Vision
```
User: /eye vision corrected left 1.2 right 1.0

Save:
{
  "left_eye": { "corrected_va": 1.2 },
  "right_eye": { "corrected_va": 1.0 }
}
```

### Example 3: Record Refraction
```
User: /eye vision sphere -3.5 cylinder -0.5 axis 180

Save:
{
  "left_eye": {
    "sphere": -3.50,
    "cylinder": -0.50,
    "axis": 180
  }
}
```

### Example 4: Both Eyes Refraction
```
User: /eye vision left sphere -3.5 cylinder -0.5 axis 180 right sphere -4.0

Save:
{
  "left_eye": { "sphere": -3.50, "cylinder": -0.50, "axis": 180 },
  "right_eye": { "sphere": -4.00 }
}
```

## II. Record Intraocular Pressure

### Example 5: Record IOP
```
User: /eye iop left 15 right 16

Save:
{
  "id": "iop_20250102000001",
  "date": "2025-01-02",
  "time": "10:00",
  "left_iop": 15,
  "right_iop": 16,
  "reference_range": "10-21"
}
```

### Example 6: Specify Measurement Method
```
User: /eye iop left 15 right 16 Goldman 2025-01-15

Save:
{
  "left_iop": 15,
  "right_iop": 16,
  "measurement_method": "goldmann_applanation_tonometer",
  "date": "2025-01-15"
}
```

## III. Fundus Examination

### Example 7: Normal Fundus
```
User: /eye fundus normal

Save:
{
  "findings": {
    "left_eye": "normal",
    "right_eye": "normal",
    "overall": "normal"
  }
}
```

### Example 8: Diabetic Retinopathy
```
User: /eye fundus diabetic_mild

Save:
{
  "findings": {
    "overall": "diabetic_mild",
    "left_eye": "Mild diabetic retinopathy",
    "right_eye": "Mild diabetic retinopathy"
  }
}
```

## IV. Eye Disease Screening

### Example 9: Glaucoma Screening Negative
```
User: /eye screening glaucoma negative

Save:
{
  "glaucoma": {
    "last_screened": "2025-01-02",
    "result": "negative",
    "next_screening": "2026-01-02"
  }
}
```

### Example 10: Cataract Screening
```
User: /eye screening cataract grade_1

Save:
{
  "cataract": {
    "last_screened": "2025-01-02",
    "result": "grade_1"
  }
}
```

### Example 11: Multiple Screenings
```
User: /eye screening amd early, diabetic_retinopathy none

Save multiple screening results
```

## V. Eye Habits

### Example 12: Record Screen Time
```
User: /eye habit screen 4hours outdoor 1hour

Save:
{
  "date": "2025-01-02",
  "screen_time_hours": 4,
  "outdoor_time_hours": 1
}
```

### Example 13: 20-20-20 Rule Compliance
```
User: /eye habit break_20_20_20 yes

Save:
{
  "break_20_20_20": "yes"
}
```

## VI. View Status

### Example 14: View Eye Health Status
```
User: /eye status

Output:
📋 Eye Health Status

Recent Vision Examination:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Left Eye: 1.0 (uncorrected) / 1.2 (corrected)
Right Eye: 0.8 (uncorrected) / 1.0 (corrected)

Recent IOP:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Left Eye: 15 mmHg ✅
Right Eye: 16 mmHg ✅

Screening Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Glaucoma: Negative (2024-12-01)
Cataract: None (2024-12-01)
Macular Degeneration: None (2024-06-01)
```

### Example 15: View Vision Trend
```
User: /eye trend 6months

Output:
📈 Vision Change Trend (Last 6 Months)

Uncorrected Vision:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Left Eye: 1.0 → 0.9 → 1.0 (Stable)
Right Eye: 0.8 → 0.8 → 0.8 (Stable)

Refraction:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Left Eye: -3.50D (No change)
Right Eye: -4.00D (No change)
```

## VII. Examination Reminders

### Example 16: View Examination Reminders
```
User: /eye checkup

Output:
📅 Eye Examination Reminder

Next Examination: 2025-06-15 (154 days remaining)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Examination Items:
• Vision examination
• Intraocular pressure check
• Fundus examination

Preparation:
• Avoid wearing contact lenses 24 hours before examination
• Avoid driving if pupils will be dilated
```
