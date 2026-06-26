---
name: pregnancy
description: Track pregnancy health, prenatal checkups, symptoms, weight, blood pressure, and fetal development with support for multiple pregnancies
argument-hint: <operation_type+description, e.g.: start 2025-01-01, checkup week 12 NT normal, weight 62.5>
allowed-tools: Read, Write
schema: pregnancy/schema.json
---

# Pregnancy Management Skill

Full-cycle pregnancy tracking and management, from preconception to delivery, providing comprehensive pregnancy health monitoring and management.

## Core Flow

```
User Input → Parse Operation Type → Execute Operation → Generate/Update Data → Save → Output Result
```

## Supported Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| start | Start pregnancy record | /pregnancy start 2025-01-01 |
| checkup | Log prenatal checkup | /pregnancy checkup week 12 NT normal |
| symptom | Log symptoms | /pregnancy symptom nausea moderate |
| weight | Log weight | /pregnancy weight 62.5 |
| vital | Log vital signs | /pregnancy vital bp 115/75 |
| status | View status | /pregnancy status |
| next-checkup | Next checkup | /pregnancy next-checkup |
| type | Multiple pregnancy setting | /pregnancy type twins |
| fetal | Fetal information | /pregnancy fetal A weight 1200g |

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation |
|----------------|-----------|
| start | start |
| checkup | checkup |
| symptom | symptom |
| weight | weight |
| vital | vital |
| status | status |
| next, next-checkup | next-checkup |
| type, twins | type |
| fetal | fetal |

### Date Recognition

| Input | Standard Format |
|------|-----------------|
| YYYY-MM-DD | YYYY-MM-DD |
| this month X day | YYYY-MM-DD |
| last month | Calculate date |
| X weeks ago | Calculate date |

### Gestational Age Recognition

| User Input | Extracted Result |
|------------|------------------|
| week 12 | 12 weeks |
| 12w | 12 weeks |

### Checkup Type Recognition

| User Input | Standard Type |
|------------|---------------|
| NT | NT scan |
| Triple test, 唐筛 | Triple test |
| Anomaly scan | Anomaly scan |
| OGTT, 糖耐 | Glucose tolerance test |
| Routine | Routine checkup |

### Result Recognition

| Normal | Abnormal |
|--------|----------|
| normal | abnormal |
| low risk | high risk |
| negative | positive |

### Symptom Type Recognition

| Keywords | Symptom Type | English |
|----------|--------------|---------|
| nausea | nausea | nausea |
| fatigue | fatigue | fatigue |
| edema | edema | edema |
| back pain | back_pain | back pain |
| contractions | contractions | contractions |

### Severity Recognition

| Mild | Moderate | Severe |
|------|----------|--------|
| mild | moderate | severe |

### Blood Pressure Format Recognition

| User Input | Systolic | Diastolic |
|------------|----------|-----------|
| 120/80 | 120 | 80 |
| 120 over 80 | 120 | 80 |

## Step 2: Check Information Completeness

### start Operation Required:
- lmp_date: Last menstrual period date

### start Operation Validation:
- LMP cannot be future date
- LMP should be within past 10 months
- If active pregnancy exists, prompt to complete first

### checkup Operation Required:
- week: Gestational age
- check_type: Checkup type
- results: Results

### weight Operation Recommended:
- Weight value (number + unit)
- If no pre-pregnancy weight, prompt to set

### vital Operation Required:
- Blood pressure value or vital sign type

## Step 3: Interactive Prompts (If Needed)

### Scenario A: Missing LMP Date
```
Please provide your last menstrual period date:
(Format: YYYY-MM-DD)
```

### Scenario B: Active Pregnancy Exists
```
Active pregnancy record exists

Current pregnancy: LMP 2025-01-01, Due date 2025-10-08
Tip: Please complete current pregnancy before starting new record
```

### Scenario C: Missing Pre-Pregnancy Weight
```
Pre-pregnancy weight missing

Please set pre-pregnancy weight first:
/profile weight 60

Or:
/pregnancy weight 62.5 --pre-pregnancy 60
```

### Scenario D: Abnormal Checkup Results
```
Abnormal checkup results

Checkup item: Triple test (16 weeks)
Result: High risk (T21 risk 1:50)

Recommendations:
• Consult obstetrician immediately
• Consider NIPT or amniocentesis
• Do not panic, high risk does not equal diagnosis
```

## Step 4: Generate JSON

### Pregnancy Data Structure

```json
{
  "pregnancy_id": "pregnancy_20250101",
  "lmp_date": "2025-01-01",
  "due_date": "2025-10-08",
  "due_date_confidence": "medium",
  "corrected_by_ultrasound": false,

  "current_week": 0,
  "current_day": 0,
  "current_trimester": "first",
  "days_passed": 0,
  "days_remaining": 280,
  "progress_percentage": 0,

  "multi_pregnancy": {
    "pregnancy_type": "singleton",
    "fetal_count": 1,
    "fetal_profiles": [
      {
        "baby_id": "A",
        "estimated_weight": null,
        "position": null,
        "heart_rate": null,
        "amniotic_fluid_index": null,
        "growth_percentile": null
      }
    ]
  },

  "prenatal_checks": [
    {
      "check_id": "check_001",
      "week": 12,
      "check_type": "NT scan",
      "scheduled_date": "2025-03-25",
      "completed": false,
      "results": {},
      "preparation": "Full bladder required"
    }
  ],

  "symptoms": {
    "nausea": {"present": false, "severity": null},
    "fatigue": {"present": false, "severity": null},
    "edema": {"present": false, "severity": null}
  },

  "weight_tracking": [],
  "blood_pressure": [],
  "fetal_movement": {"tracking_started": false},

  "nutrition_plan": {
    "folic_acid": {"dose": "400μg", "frequency": "daily"},
    "iron": {"dose": null},
    "calcium": {"dose": null},
    "dha": {"dose": null}
  },

  "notes": "",
  "completed": false,
  "delivery_date": null,
  "delivery_outcome": null,

  "metadata": {
    "created_at": "2025-01-01T00:00:00.000Z",
    "last_updated": "2025-01-01T00:00:00.000Z"
  }
}
```

Complete schema definition: see [schema.json](schema.json).

## Step 5: Save Data

1. Read `data/pregnancy-tracker.json`
2. Update corresponding data
3. Write back to file
4. If detailed records exist, save to `data/pregnancy-records/YYYY-MM/YYYY-MM-DD_pregnancy-record.json`

## Execution Instructions

```
1. Parse user input and determine operation type
2. Execute corresponding logic based on operation type
3. Validate input data and state
4. Generate JSON compliant with schema.json
5. Save to data/pregnancy-tracker.json
6. Output operation result and summary to user
```

## Example Interactions

### Example 1: Start Pregnancy Record
```
User: /pregnancy start 2025-01-01

System:
Pregnancy record created

Pregnancy Information:
LMP: January 1, 2025
Due Date: October 8, 2025
Current gestational age: 0 weeks
Trimester: First trimester

Due date confidence: Medium (calculated from LMP)

Next Checkup:
12-week NT scan - March 25, 2025 (84 days away)
Preparation: Full bladder required

Checkup Schedule Overview:
12 weeks: NT scan
16 weeks: Triple test/NIPT
20 weeks: Anomaly scan
24 weeks: Glucose tolerance test
28 weeks: Routine checkup
32-36 weeks: Every 2 weeks
37-40 weeks: Weekly

Nutrition Recommendations:
• Folic acid: 400-800μg/day
• Iron: Supplement in 2nd/3rd trimester
• Calcium: 1000-1200mg/day
• DHA: 200-300mg/day

Data saved to: data/pregnancy-records/2025-01/2025-01-01_pregnancy-record.json
```

### Example 2: Log Checkup
```
User: /pregnancy checkup week 12 NT normal

System:
Checkup record updated

Checkup Information:
Gestational age: 12 weeks
Checkup item: NT scan
Date: March 25, 2025
Result: Normal (NT value 1.8mm)

This checkup completed

Next Checkup:
16-week Triple test - April 22, 2025 (28 days away)
Preparation: Fasting blood draw
```

### Example 3: Log Weight
```
User: /pregnancy weight 62.5

System:
Weight recorded

Weight Information:
Record date: March 20, 2025
Current gestational age: 12 weeks

Current weight: 62.5 kg
Pre-pregnancy weight: 60.0 kg
Weight gained: 2.5 kg
Current BMI: 23.1 (normal)

Weight Gain Assessment:
Recommended pregnancy weight gain: 11.5-16 kg
Current progress: Normal

Late pregnancy recommendations:
Weekly weight gain: 0.35-0.50 kg
```

### Example 4: Set Twins
```
User: /pregnancy type twins

System:
Multiple pregnancy type set

Pregnancy Type Information:
Type: Twin pregnancy
Fetal count: 2

Due Date Adjustment:
Original due date: October 8, 2025 (40 weeks)
Adjusted due date: September 17, 2025 (37 weeks)
Earlier by: 3 weeks

Checkup Frequency Adjustment:
• From 28 weeks: Every 2 weeks
• From 32 weeks: Weekly
• Add cervical length monitoring
• Add fetal growth monitoring

Weight Gain Recommendations:
Total recommended gain: 16-24 kg
Late pregnancy weekly gain: 0.5-0.7 kg

Recommendations:
• Consult Maternal-Fetal Medicine specialist (MFM)
• Consider referral to tertiary hospital
• Create delivery plan (discuss at 32-34 weeks)
```

For more examples, see [examples.md](examples.md).
