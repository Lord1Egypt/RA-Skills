# HypertensionTracker Schema

Complete data structure definition for hypertension management.

## Schema File

Complete JSON Schema definition: [schema.json](schema.json)

## Field Quick Reference

### Blood Pressure Records

| Field | Type | Description |
|-------|------|-------------|
| systolic | int | Systolic BP (mmHg) |
| diastolic | int | Diastolic BP (mmHg) |
| pulse | int | Heart rate (bpm) |
| position | enum | sitting/standing/lying |
| classification | enum | BP classification |
| in_target | boolean | Whether on target |

### Target Organ Damage

| Field | Type | Description |
|-------|------|-------------|
| left_ventricular_hypertrophy.status | enum | none/present |
| microalbuminuria.uacr | number | Urine microalbumin/creatinine ratio |
| retinopathy.grade | enum | grade_0-4 |

### Cardiovascular Risk

| Field | Type | Description |
|-------|------|-------------|
| ascvd_risk_score | number | ASCVD risk score (%) |
| risk_level | enum | Low/Moderate/High/Very High Risk |
| risk_factors | array | List of risk factors |

## Enum Values

### BP Classification
`Normal BP` | `High-Normal` | `Grade 1 Hypertension` | `Grade 2 Hypertension` | `Grade 3 Hypertension`

### Measurement Position
`sitting` | `standing` | `lying`

### Risk Level
`Low Risk` | `Moderate Risk` | `High Risk` | `Very High Risk`

### Retina Grade
`grade_0` | `grade_1` | `grade_2` | `grade_3` | `grade_4`

## Data Storage

- Location: `data/hypertension-tracker.json`
- Format: JSON object
