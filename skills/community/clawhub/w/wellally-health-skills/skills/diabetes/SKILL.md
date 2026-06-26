---
name: diabetes
description: Diabetes management - blood glucose monitoring, HbA1c tracking, TIR analysis, hypoglycemia event logging, and complication screening
argument-hint: <operation_type+info, e.g.: record fasting 6.5, hba1c 6.8, hypo 3.4 sweating, screening retina none>
allowed-tools: Read, Write
schema: diabetes/schema.json
---

# Diabetes Management Skill

Comprehensive blood glucose monitoring and diabetes management to help control blood sugar and prevent complications.

## Core Flow

```
User Input -> Identify Operation Type -> Extract Parameter Info -> Check Completeness -> [Need Supplement] Ask User
                                                      |
                                                   [Information Complete]
                                                      |
                                              Generate JSON -> Save Data -> Output Confirmation
```

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation Type | Description |
|----------------|----------------|-------------|
| record, glucose, bg | glucose_record | Log blood glucose |
| hba1c, a1c | hba1c_record | Log HbA1c |
| trend | trend_analysis | View glucose trend |
| tir | tir_analysis | View Time in Range |
| hypo, hypoglycemia | hypo_event | Log hypoglycemia event |
| screening, complication | complication_screening | Complication screening |
| target | target_view | View glucose targets |
| achievement | achievement_view | View achievement status |
| medication | medication_management | Medication management |

### Glucose Type Keywords

| Input Keywords | Type Value | Target Range |
|----------------|------------|--------------|
| fasting | fasting | 4.4-7.0 |
| postprandial, 2h | postprandial_2h | <10.0 |
| bedtime | bedtime | 6.0-9.0 |
| random | random | - |

### Hypoglycemia Symptom Keywords

| Input Keywords | Symptom |
|----------------|---------|
| sweating | sweating |
| palpitations | palpitations |
| tremor | tremor |
| hunger | hunger |
| confusion | confusion |
| dizziness | dizziness |

### Complication Screening Types

| Input Keywords | Screening Type |
|----------------|----------------|
| retina, 眼底, 视网膜 | retinopathy |
| kidney, 肾脏, 肾 | nephropathy |
| nerve, 神经, 神经病变 | neuropathy |
| foot, 足, 足部 | foot_complication |

### Retinopathy Severity

| Input Keywords | Severity |
|----------------|----------|
| none | none |
| mild | mild |
| moderate | moderate |
| severe | severe |
| proliferative | proliferative |

### Nephropathy Status

| Input Keywords | Status |
|----------------|--------|
| normal | normal |
| microalbuminuria | microalbuminuria |
| macroalbuminuria | macroalbuminuria |

## Step 2: Check Information Completeness

### Glucose Record Required:
- Glucose value
- Glucose type (fasting/postprandial_2h/bedtime/random)

### HbA1c Record Required:
- HbA1c value (%)

### Hypoglycemia Event Required:
- Glucose value
- Symptoms (optional)

### Complication Screening Required:
- Screening type
- Result status

## Step 3: Interactive Prompts (If Needed)

### Scenario A: Missing Glucose Type
```
Please select glucose measurement type:
- fasting (fasting blood glucose)
- postprandial (2-hour post-meal blood glucose)
- bedtime (bedtime blood glucose)
- random (random blood glucose)
```

### Scenario B: Hypoglycemia Symptom Inquiry
```
Do you have any of the following symptoms?
- Sweating
- Palpitations
- Tremor
- Hunger
- Confusion
- Dizziness
```

### Scenario C: Missing Complication Screening Parameters
```
Please provide detailed screening results:
- Retina: none/mild/moderate/severe/proliferative
- Kidney: normal/microalbuminuria/macroalbuminuria + UACR + eGFR
- Nerve: normal/abnormal
- Foot: normal/low_risk/high_risk + Wagner grade
```

## Step 4: Generate JSON

### Glucose Record
```json
{
  "id": "glu_20250620070000001",
  "date": "2025-06-20",
  "time": "07:00",
  "type": "fasting",
  "value": 6.5,
  "unit": "mmol/L",
  "in_range": true,
  "target_range": "4.4-7.0"
}
```

### HbA1c Record
```json
{
  "date": "2025-06-15",
  "value": 6.8,
  "unit": "%",
  "target": "<7.0",
  "in_target": true,
  "change_from_previous": -0.3
}
```

### Hypoglycemia Event
```json
{
  "id": "hypo_20250618153000001",
  "date": "2025-06-18",
  "time": "15:30",
  "value": 3.4,
  "severity": "level_1",
  "symptoms": ["sweating", "palpitations"],
  "treatment": "glucose_tablets",
  "resolved": true
}
```

### Complication Screening
```json
{
  "retinopathy": {
    "status": "none",
    "last_exam": "2025-03-20",
    "next_exam": "2026-03-20"
  },
  "nephropathy": {
    "status": "microalbuminuria",
    "uacr": 45,
    "egfr": 78,
    "ckd_stage": "G2A2"
  },
  "neuropathy": {
    "status": "none",
    "monofilament_test": "normal"
  },
  "foot": {
    "status": "low_risk",
    "pulses_present": true,
    "ulcer": false,
    "wagner_grade": 0
  }
}
```

Complete schema definition: see [schema.json](schema.json).

## Step 5: Save Data

1. Read `data/diabetes-tracker.json`
2. Update corresponding sections based on operation type
3. Update statistics
4. Write back to file

## Execution Instructions

```
1. Identify operation type (record/hba1c/trend/tir/hypo/screening/target/achievement/medication)
2. Extract parameter information
3. Check required field completeness
4. If missing, ask user to supplement
5. Generate JSON compliant with schema.json
6. Save to data/diabetes-tracker.json
7. Output confirmation and medical recommendations
```

## Example Interactions

### Example 1: Record Fasting Glucose
```
User: record fasting 6.5

AI: Blood glucose measurement recorded
Time: 2025-06-20 07:00
Type: Fasting blood glucose
Value: 6.5 mmol/L
Status: Within target range (4.4-7.0)

Recommendation: Continue maintaining good blood glucose control
```

### Example 2: Record Hypoglycemia Event
```
User: hypo 3.4 sweating

AI: Hypoglycemia event recorded
Time: 2025-06-18 15:30
Blood glucose: 3.4 mmol/L
Severity: Level 1 (mild)
Symptoms: Sweating, Palpitations

Hypoglycemia Management Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Immediately take 15g fast-acting glucose
   - 3-5 glucose tablets
   - 150ml juice or sugary drink

2. Re-check after 15 minutes

3. If still below 3.9 mmol/L, repeat step 1

4. After glucose normalizes, if >1 hour until next meal, eat small amount of long-acting carbohydrate
```

### Example 3: Record HbA1c
```
User: hba1c 6.8

AI: HbA1c test result recorded
Value: 6.8%
Target: <7.0%
Status: On target

Change from last: -0.3% (improved)

Recommendation: Test HbA1c every 3 months
```

### Example 4: View Achievement Status
```
User: achievement

AI: Blood Glucose Achievement Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
HbA1c: 6.8% (target <7.0%) ✓ On target

Past 7 days glucose:
- Fasting: Average 6.2 mmol/L (achievement rate 85.7%)
- Post-meal 2h: Average 8.5 mmol/L (achievement rate 71.4%)
- Bedtime: Average 7.1 mmol/L (achievement rate 100%)

TIR: 72% (target >70%) ✓ On target
Hypoglycemia events: 1 (level 1)

Control Evaluation: Good blood glucose control, continue
```

For more examples, see [examples.md](examples.md).

## Medical Safety Boundaries

### Cannot Do:
- Provide specific medication dosage adjustment recommendations
- Directly prescribe or recommend specific medications
- Replace doctor's diagnosis and treatment decisions
- Predict disease prognosis or complication occurrence

### Can Do:
- Provide blood glucose monitoring records and trend analysis
- Provide HbA1c tracking and achievement status
- Provide complication screening records and reminders
- Provide hypoglycemia event records and analysis
- Provide lifestyle recommendations and medical visit reminders

### Emergency Medical Indications:
- Severe hypoglycemia (unconsciousness, coma)
- Diabetic ketoacidosis (nausea, vomiting, abdominal pain, deep breathing)
- Hyperosmolar hyperglycemic state (severe dehydration, confusion)
- Infection with fever and blood glucose >16.7 mmol/L
