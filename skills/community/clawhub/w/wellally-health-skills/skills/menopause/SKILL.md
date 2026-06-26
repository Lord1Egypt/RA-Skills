---
name: menopause
description: Track menopause symptoms, HRT treatment, bone density, and health risk assessment
argument-hint: <operation_type+description, e.g.: start 48 2025-11-15, symptom hot flashes 5-10 times daily, bone -1.5>
allowed-tools: Read, Write
schema: menopause/schema.json
---

# Menopause Management Skill

Perimenopausal symptom tracking and management, providing menopause health assessment and management recommendations.

## Core Flow

```
User Input → Parse Operation Type → Execute Operation → Generate/Update Data → Save → Output Result
```

## Supported Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| start | Start menopause tracking | /menopause start 48 2025-11-15 |
| symptom | Log symptoms | /menopause symptom hot flashes 5-10 times daily moderate |
| hrt | Log HRT treatment | /menopause hrt start estradiol 1mg |
| bone | Log bone density | /menopause bone -1.5 osteopenia |
| status | View status | /menopause status |
| risk | Risk assessment | /menopause risk |

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation |
|----------------|-----------|
| start | start |
| symptom | symptom |
| HRT, hrt | hrt |
| bone | bone |
| status | status |
| risk | risk |

### Menopause Stage Recognition

```javascript
months_since_lmp = (today - lmp_date) / 30.44

if (months_since_lmp < 12) {
  stage = "perimenopausal"  // Perimenopause
} else if (months_since_lmp >= 12 && months_since_lmp < 36) {
  stage = "menopausal"  // Menopause
} else {
  stage = "postmenopausal"  // Postmenopause
}
```

### Symptom Type Recognition

| Keywords | Symptom Type | English |
|----------|--------------|---------|
| hot flashes | hot_flashes | hot flashes |
| night sweats | night_sweats | night sweats |
| sleep issues | sleep_issues | sleep issues |
| mood changes | mood_changes | mood changes |
| vaginal dryness | vaginal_dryness | vaginal dryness |
| joint pain | joint_pain | joint pain |

### Severity Recognition

| Keywords | Level | Score |
|----------|-------|-------|
| mild | 1 | 1 |
| moderate | 2 | 2 |
| severe | 3 | 3 |

### Frequency Recognition

| Input | Standardized |
|------|-------------|
| 5-10 times per day | 5-10_per_day |
| 3-4 times per night | 3-4_per_night |
| often | often |
| occasional | occasional |

### T-Score Recognition

| User Input | T-Score |
|------------|---------|
| -1.5 | -1.5 |
| 负1点五 | -1.5 |
| minus 1.5 | -1.5 |

### Bone Density Diagnosis Recognition

| Keywords | Diagnosis | T-Score Range |
|----------|-----------|---------------|
| normal | normal | T >= -1.0 |
| osteopenia | osteopenia | -2.5 < T < -1.0 |
| osteoporosis | osteoporosis | T <= -2.5 |

## Step 2: Check Information Completeness

### start Operation Required:
- age: Age (40-65)
- last_menstrual_period: Last menstrual period date

### start Operation Validation:
- Age should be 40-65
- LMP cannot be future date
- LMP should be within past 12 months

### symptom Operation Required:
- Symptom type
- Frequency or severity

### bone Operation Required:
- t_score: T-score

### hrt Operation Recommended:
- action: start/stop/effectiveness
- Medication information (when starting)

## Step 3: Interactive Prompts (If Needed)

### Scenario A: Missing Age
```
Please provide your age:
(Age should be 40-65)
```

### Scenario B: Missing LMP Date
```
Please provide your last menstrual period date:
(Format: YYYY-MM-DD)
```

### Scenario C: Unclear Symptom Frequency
```
What is the symptom frequency?
• X times per day
• X times per night
• Often
• Occasional
```

### Scenario D: Missing T-Score
```
Please provide bone density test T-score:
(e.g., -1.5)
```

## Step 4: Generate JSON

### Menopause Data Structure

```json
{
  "menopause_id": "menopause_20250101",
  "stage": "perimenopausal",
  "age": 48,
  "last_menstrual_period": "2025-11-15",
  "months_since_lmp": 0,

  "symptoms": {
    "hot_flashes": {
      "present": false,
      "frequency": null,
      "severity": null,
      "impact_on_life": null,
      "triggers": [],
      "last_updated": null
    },
    "night_sweats": {
      "present": false,
      "frequency": null,
      "severity": null
    },
    "sleep_issues": {
      "present": false,
      "type": null,
      "sleep_quality": null
    },
    "mood_changes": {
      "present": false,
      "symptoms": []
    },
    "vaginal_dryness": {
      "present": false,
      "severity": null
    },
    "joint_pain": {
      "present": false,
      "severity": null,
      "locations": []
    }
  },

  "symptom_history": [],

  "hrt": {
    "on_treatment": false,
    "considering": false,
    "medication": null,
    "type": null,
    "dose": null,
    "route": null,
    "start_date": null,
    "duration": null,
    "effectiveness": null,
    "effectiveness_rating": null,
    "side_effects": [],
    "notes": ""
  },

  "bone_density": {
    "last_check": null,
    "t_score": null,
    "z_score": null,
    "diagnosis": null,
    "diagnosis_category": null,
    "fracture_risk": null,
    "fracture_risk_level": null,
    "next_check_due": null,
    "calcium_intake": {},
    "vitamin_d": {},
    "weight_bearing_exercise": null,
    "fall_risk_factors": []
  },

  "cardiovascular_risk": {
    "last_assessment": null,
    "blood_pressure": null,
    "systolic": null,
    "diastolic": null,
    "bp_classification": null,
    "lipids": {},
    "blood_sugar": {},
    "risk_level": null,
    "risk_factors": [],
    "modifiable_factors": []
  },

  "lifestyle": {
    "exercise": {},
    "diet": {},
    "stress_management": [],
    "sleep_habits": null
  },

  "metadata": {
    "created_at": "2025-01-01T00:00:00.000Z",
    "last_updated": "2025-01-01T00:00:00.000Z"
  }
}
```

Complete schema definition: see [schema.json](schema.json).

## Step 5: Save Data

1. Read `data/menopause-tracker.json`
2. Update corresponding data
3. Write back to file
4. If detailed records exist, save to `data/menopause-records/YYYY-MM/YYYY-MM-DD_symptom-record.json`

## Execution Instructions

```
1. Parse user input and determine operation type
2. Execute corresponding logic based on operation type
3. Validate input data and state
4. Generate JSON compliant with schema.json
5. Save to data/menopause-tracker.json
6. Output operation result and summary to user
```

## Example Interactions

### Example 1: Start Menopause Tracking
```
User: /menopause start 48 2025-11-15

System:
Menopause tracking created

Basic Information:
Age: 48
Last menstrual period: November 15, 2025
Menopause stage: Perimenopause

Stage Description:
Perimenopause is the period from when ovarian function begins to decline until one year after menopause, typically lasting 4-10 years.

Common Symptoms:
• Irregular menstrual cycles
• Hot flashes and night sweats
• Mood swings
• Sleep disturbances
• Vaginal dryness

Recommended Checkups:
• Bone density test (recommended every 1-2 years)
• Cardiovascular risk assessment (blood pressure, lipids)
• Gynecological exam (annually)
• Breast exam (annually)

Lifestyle Recommendations:
• Regular exercise (3-5 times per week)
• Balanced diet (rich in calcium and vitamin D)
• Maintain healthy weight (BMI 18.5-24.9)
• Quit smoking and limit alcohol
• Stress management
• Adequate sleep

Data saved to: data/menopause-tracker.json
```

### Example 2: Log Hot Flash Symptoms
```
User: /menopause symptom hot flashes 5-10 times daily moderate

System:
Symptom recorded

Symptom Information:
Type: Hot flashes
Frequency: 5-10 times daily
Severity: Moderate

Current menopause stage: Perimenopause

Symptom Score:
Hot flash score: 14/12 (severe)

Overall symptom burden: 65/100 (moderate)

Assessment:
Moderate symptom burden affecting quality of life.

Recommendations:
• Lifestyle adjustments
• Regular exercise, stress reduction
• If symptoms significantly affect life, consider medical evaluation for HRT

Management Tips:
• Identify and avoid triggers (hot drinks, hot environments, stress)
• Wear layered clothing for easy adjustment
• Keep room temperature cool (18-22°C)
• Use cooling pillows
• Regular exercise (yoga, tai chi)

Data synced to symptom records
```

### Example 3: Log Bone Density
```
User: /menopause bone -1.5 osteopenia

System:
Bone density record updated

Bone Density Test Information:
Test date: June 15, 2025
T-score: -1.5
Z-score: -1.2
Diagnosis: Osteopenia

Fracture Risk Assessment:
Current risk: Low

Bone Density Changes:
2023: T-score -1.3 (normal)
2025: T-score -1.5 (osteopenia)
Change: Slight decline

Management Recommendations:
• Calcium: 1200-1500mg daily
• Vitamin D: 800-1000IU daily
• Weight-bearing exercise: 3-4 times weekly
• Strength training: 2-3 times weekly
• Quit smoking and limit alcohol

Follow-up Recommendation:
Next test: June 15, 2026 (1 year later)
```

For more examples, see [examples.md](examples.md).
