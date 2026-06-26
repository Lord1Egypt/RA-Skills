---
name: hypertension
description: Hypertension management - blood pressure monitoring, target organ damage assessment, cardiovascular risk evaluation, and medication tracking
argument-hint: <operation_type+info, e.g.: record 135/85, trend, average, risk assessment, kidney uacr 15>
allowed-tools: Read, Write
schema: hypertension/schema.json
---

# Hypertension Management Skill

Comprehensive blood pressure monitoring and management to help control blood pressure and reduce cardiovascular risk.

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
| record, bp, blood pressure | bp_record | Log blood pressure |
| trend | trend_analysis | View blood pressure trend |
| average | average_calculation | Calculate average BP |
| history | history_view | View history records |
| status | status_view | View achievement status |
| risk | risk_assessment | Cardiovascular risk assessment |
| target | target_view | View BP targets |
| heart | heart_assessment | Heart assessment record |
| kidney | kidney_assessment | Kidney assessment record |
| retina | retina_assessment | Retina assessment record |
| medication | medication_management | Medication management |

### Blood Pressure Value Parsing

Recognize format: `XXX/YY` or `XXX YY`
- Systolic: First value
- Diastolic: Second value

### Measurement Time Keywords

| Input Keywords | Time Value |
|----------------|------------|
| morning | morning |
| evening | evening |
| noon | noon |
| night | night |

### Measurement Position Keywords

| Input Keywords | Position Value |
|----------------|----------------|
| sitting | sitting |
| standing | standing |
| lying | lying |

### Measurement Arm Keywords

| Input Keywords | Arm Value |
|----------------|-----------|
| left | left |
| right | right |

### Target Organ Assessment Keywords

#### Heart Assessment
| Input Keywords | Exam Type |
|----------------|-----------|
| echo | echocardiogram |
| ecg | ecg |
| lvh | left_ventricular_hypertrophy |

#### Kidney Assessment
| Input Keywords | Indicator |
|----------------|-----------|
| uacr | uacr |
| egfr | egfr |
| creatinine | creatinine |

#### Retina Assessment
| Input Keywords | Grade |
|----------------|-------|
| grade-0 | grade_0 |
| grade-1 | grade_1 |
| grade-2 | grade_2 |
| grade-3 | grade_3 |
| grade-4 | grade_4 |

## Step 2: Check Information Completeness

### BP Record Required:
- Systolic (mmHg)
- Diastolic (mmHg)

### Target Organ Assessment Required:
- Assessment type
- Assessment result

### Cardiovascular Risk Assessment Needs:
- Age
- Gender
- Systolic BP
- Smoking status
- Diabetes status
- Total cholesterol
- HDL cholesterol
- Antihypertensive treatment status

## Step 3: Interactive Prompts (If Needed)

### Scenario A: Incomplete BP Values
```
Please provide complete BP reading, format: systolic/diastolic
Example: 135/85
```

### Scenario B: Additional Information Inquiry
```
Please supplement the following information (optional):
- Heart rate (pulse XX)
- Measurement time (morning/evening)
- Measurement position (sitting/standing/lying)
- Measurement arm (left/right)
```

### Scenario C: Missing Target Organ Assessment Parameters
```
Please provide assessment results:
- Echocardiogram: normal/abnormal/lvh
- ECG: normal/abnormal
- Urine microalbumin (UACR): value (mg/g)
- eGFR: value (ml/min/1.73m²)
- Retina grade: grade_0-4
```

## Step 4: Generate JSON

### Blood Pressure Record
```json
{
  "id": "bp_20250102080000001",
  "date": "2025-01-02",
  "time": "08:00",
  "systolic": 135,
  "diastolic": 85,
  "pulse": 78,
  "position": "sitting",
  "measurement_device": "home_monitor",
  "arm": "left",
  "classification": "High-normal",
  "in_target": false
}
```

### Target Organ Damage Assessment
```json
{
  "left_ventricular_hypertrophy": {
    "status": "none",
    "last_assessment": "2025-01-15",
    "method": "echocardiogram"
  },
  "microalbuminuria": {
    "status": "negative",
    "uacr": 15,
    "reference": "<30",
    "date": "2025-06-10"
  },
  "retinopathy": {
    "grade": "grade_0",
    "last_exam": "2025-03-20"
  },
  "arterial_stiffness": {
    "pwv": 7.5,
    "reference": "<10",
    "date": "2025-02-15"
  }
}
```

### Cardiovascular Risk Assessment
```json
{
  "assessment_date": "2025-06-20",
  "ascvd_risk_score": 12.5,
  "risk_level": "High",
  "risk_factors": [
    "Hypertension",
    "Age >55",
    "Elevated total cholesterol"
  ],
  "recommendations": [
    "Strict BP control",
    "Statin therapy",
    "Lifestyle intervention"
  ]
}
```

Complete schema definition: see [schema.json](schema.json).

## Step 5: Save Data

1. Read `data/hypertension-tracker.json`
2. Update corresponding sections based on operation type
3. Update statistics
4. Write back to file

## Execution Instructions

```
1. Identify operation type (record/trend/average/history/status/risk/target/heart/kidney/retina/medication)
2. Extract parameter information
3. Check required field completeness
4. If missing, ask user to supplement
5. Generate JSON compliant with schema.json
6. Save to data/hypertension-tracker.json
7. Output confirmation and medical recommendations
```

## Example Interactions

### Example 1: Record Blood Pressure
```
User: record 135/85 pulse 78

AI: Blood pressure measurement recorded
Time: 2025-01-02 08:00
Systolic: 135 mmHg
Diastolic: 85 mmHg
Pulse: 78 bpm
Classification: High-normal

Target: <130/80 mmHg
Status: Not on target (elevated systolic)

Recommendation: Reduce sodium intake, exercise regularly, monitor regularly
```

### Example 2: View Blood Pressure Trend
```
User: trend

AI: Blood pressure trend analysis (past 7 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average BP: 132/83 mmHg
Morning average: 135/85 mmHg
Evening average: 128/80 mmHg

Circadian rhythm: Dipper (normal)
Achievement rate: 71.4%

Trend: BP control stable, morning BP slightly elevated

Recommendation: Continue monitoring, pay attention to morning BP control
```

### Example 3: Cardiovascular Risk Assessment
```
User: risk

AI: Cardiovascular Risk Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━
10-year ASCVD risk: 12.5%
Risk level: High

Major risk factors:
- Hypertension (currently poorly controlled)
- Age >55
- Elevated total cholesterol

Recommendations:
1. Strict BP control to target
2. Consider statin therapy
3. Low-salt diet, regular exercise
4. Quit smoking, limit alcohol

Recommendation: Seek medical attention soon, consult doctor for treatment adjustment
```

### Example 4: View Achievement Status
```
User: status

AI: Blood Pressure Achievement Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
BP Target: <130/80 mmHg

Past 7 days:
- Average BP: 132/83 mmHg
- Days on target: 5/7 (71.4%)
- Achievement rate: 71.4%

Past 30 days:
- Average BP: 128/81 mmHg
- Days on target: 22/30 (73.3%)
- Achievement rate: 73.3%

Control Evaluation: BP control approaching target, keep working
```

For more examples, see [examples.md](examples.md).

## Medical Safety Boundaries

### Cannot Do:
- Provide specific medication dosage adjustment recommendations
- Directly prescribe or recommend specific medications
- Replace doctor's diagnosis and treatment decisions
- Predict disease prognosis or complication occurrence

### Can Do:
- Provide blood pressure monitoring records and trend analysis
- Provide target organ damage assessment records
- Provide cardiovascular risk calculation (for reference only)
- Provide lifestyle recommendations and medical visit reminders

### Emergency Medical Indications:
- Systolic >=180 mmHg AND diastolic >=120 mmHg
- Accompanied by chest pain, difficulty breathing, speech difficulty
- Headache, confusion, vision changes
- Facial or limb numbness/weakness
