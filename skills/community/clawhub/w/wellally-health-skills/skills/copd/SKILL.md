---
name: copd
description: COPD management - lung function monitoring (FEV1), symptom assessment (CAT, mMRC), exacerbation tracking, and vaccination records
argument-hint: <operation_type+info, e.g.: fev1 1.8 65%, cat score 18, mmrc 2, exacerbation moderate>
allowed-tools: Read, Write
schema: copd/schema.json
---

# COPD Management Skill

Long-term management of Chronic Obstructie Pulmonary Disease (COPD), including lung function monitoring, symptom assessment, and exacerbation prevention.

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
| fev1, lung-function | lung_function | Lung function test record |
| cat | cat_assessment | CAT score |
| mmrc | mmrc_assessment | mMRC dyspnea scale |
| symptom | symptom_record | Symptom record |
| exacerbation | exacerbation_record | Exacerbation record |
| medication | medication_management | Medication management |
| vaccine | vaccine_record | Vaccination record |
| status | control_status | View control status |
| assessment | gold_assessment | GOLD group assessment |

### Lung Function Keywords Mapping

| Input Keywords | Field | Example |
|----------------|-------|--------|
| fev1, fev | fev1 | 1.8 (L) |
| predicted, percent, % | fev1_percent_predicted | 65 (%) |
| fvc, fvc | fvc | 3.2 (L) |
| ratio | fev1_fvc_ratio | 0.56 |

### Symptom Type Keywords

| Input Keywords | Symptom Type |
|----------------|--------------|
| dyspnea | dyspnea |
| cough | cough |
| sputum | sputum |
| wheeze | wheeze |

### Sputum Color Keywords

| Input Keywords | Color Value |
|----------------|-------------|
| white | white |
| clear | clear |
| yellow | yellow |
| green | green |
| purulent | purulent |

### Sputum Volume Keywords

| Input Keywords | Volume Value |
|----------------|---------------|
| scanty | scanty |
| moderate | moderate |
| abundant | abundant |

### Exacerbation Severity

| Input Keywords | Severity |
|----------------|-----------|
| mild | mild |
| moderate | moderate |
| severe | severe |

### Exacerbation Triggers

| Input Keywords | Trigger |
|----------------|---------|
| viral | viral_infection |
| bacterial | bacterial_infection |
| pollution | air_pollution |
| weather | weather_change |

## Step 2: Check Information Completeness

### Lung Function Record Required:
- FEV1 value (L)

### CAT Score Required:
- Total score (0-40 points)

### mMRC Score Required:
- Grade (0-4 level)

### Symptom Record Required:
- Symptom type
- Severity or description

### Exacerbation Record Required:
- Severity (mild/moderate/severe)

## Step 3: Interactive Prompts (If Needed)

### Scenario A: Incomplete Lung Function Values
```
Please provide complete lung function data:
- FEV1 value (L)
- FEV1 percent predicted (%)
- FVC value (L) [optional]
- FEV1/FVC ratio [optional]
```

### Scenario B: Missing CAT Score
```
Please perform CAT scoring (each item 0-5 points):
1. Cough
2. Sputum
3. Chest tightness
4. Shortness of breath climbing stairs
5. Limitation in housework activities
6. Confidence in outdoor activities
7. Sleep quality
8. Energy level

Or enter total score directly (0-40 points)
```

### Scenario C: Missing mMRC Grade
```
Please select mMRC grade (0-4):
Grade 0 - Only shortness of breath during strenuous exercise
Grade 1 - Shortness of breath when walking fast or climbing incline
Grade 2 - Walk slower than peers or need to stop to catch breath
Grade 3 - Need to stop after 100m or few minutes
Grade 4 - Severe shortness of breath, cannot leave home
```

## Step 4: Generate JSON

### Lung Function Record
```json
{
  "date": "2025-06-10",
  "post_bronchodilator": {
    "fev1": 1.8,
    "fev1_percent_predicted": 65,
    "fvc": 3.2,
    "fev1_fvc_ratio": 0.56
  },
  "gold_grade": "Grade 2",
  "interpretation": "Moderate airflow limitation"
}
```

### CAT Score Record
```json
{
  "date": "2025-06-20",
  "total_score": 18,
  "max_score": 40,
  "interpretation": "Moderate symptom impact",
  "impact_level": "Medium",
  "items": {
    "cough": 2,
    "sputum": 2,
    "chest_tightness": 2,
    "breathlessness_climbing": 3,
    "activity_limitation": 2,
    "confidence_outdoors": 2,
    "sleep": 3,
    "energy": 2
  }
}
```

### Exacerbation Record
```json
{
  "id": "exace_20250215000000001",
  "date": "2025-02-15",
  "severity": "moderate",
  "triggers": ["viral_infection"],
  "symptoms": ["increased_dyspnea", "purulent_sputum"],
  "treatment": ["antibiotics", "prednisone"],
  "hospitalized": false,
  "recovery_days": 10
}
```

Complete schema definition: see [schema.json](schema.json).

## Step 5: Save Data

1. Read `data/copd-tracker.json`
2. Update corresponding sections based on operation type
3. Update statistics
4. Write back to file

## Execution Instructions

```
1. Identify operation type (fev1/cat/mmrc/symptom/exacerbation/medication/vaccine/status/assessment)
2. Extract parameter information
3. Check required field completeness
4. If missing, ask user to supplement
5. Generate JSON compliant with schema.json
6. Save to data/copd-tracker.json
7. Output confirmation and medical recommendations
```

## Example Interactions

### Example 1: Lung Function Record
```
User: fev1 1.8 65%

AI: Lung function test result recorded
FEV1: 1.8 L (65% predicted)
GOLD Grade: Grade 2 (moderate)
Interpretation: Moderate airflow limitation

Recommendation: Regular lung function recheck, at least once a year
```

### Example 2: CAT Score
```
User: cat score 18

AI: CAT score recorded
Total score: 18/40
Impact: Moderate impact
Grade: Medium

Symptom control needs improvement, consult doctor for treatment adjustment
```

### Example 3: Exacerbation Record
```
User: exacerbation moderate viral_infection

AI: Exacerbation event recorded
Date: 2025-06-20
Severity: Moderate
Trigger: Viral infection

This is the 1st exacerbation this year

If symptoms continue to worsen for more than 3 days, seek medical attention
```

### Example 4: View Status
```
User: copd status

AI: COPD Control Status Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOLD Grade: Grade 2 (moderate)
Symptom assessment: CAT 18 (moderate impact)
Lung function: FEV1 1.8L (65%)

Exacerbations: 1 this year (last: 2025-02-15)
Medication: Tiotropium 18μg qd
Vaccination: Flu vaccine (2024-10), Pneumonia vaccine (2023-05)

Control Evaluation: Symptom control suboptimal, recommend optimizing treatment
```

For more examples, see [examples.md](examples.md).

## Medical Safety Boundaries

### Cannot Do:
- Provide specific medication dosage adjustment recommendations
- Directly prescribe or recommend specific medications
- Replace doctor's diagnosis and treatment decisions
- Predict disease prognosis or rate of lung function decline

### Can Do:
- Provide lung function monitoring records and trend analysis
- Provide symptom scoring and assessment (CAT, mMRC)
- Provide exacerbation records and trigger tracking
- Provide medication reminders and vaccination reminders
- Provide lifestyle recommendations and medical visit reminders

### Emergency Medical Indications:
- Significantly worsened dyspnea, unrelieved by rest
- Purple lips or fingernails (cyanosis)
- Confusion, drowsiness, or coma
- Chest pain, suspected myocardial infarction or pneumothorax
