# DiabetesTracker Schema

Complete data structure definition for diabetes management.

## Schema File

Complete JSON Schema definition: [schema.json](schema.json)

## Field Quick Reference

### Glucose Records

| Field | Type | Description |
|-------|------|-------------|
| type | enum | fasting/postprandial_2h/bedtime/random |
| value | number | Glucose value (mmol/L) |
| in_range | boolean | Whether in target range |

### HbA1c Records

| Field | Type | Description |
|-------|------|-------------|
| value | number | HbA1c value (%) |
| in_target | boolean | Whether on target |
| change_from_previous | number | Change from last |

### Hypoglycemia Events

| Field | Type | Description |
|-------|------|-------------|
| value | number | Glucose value (mmol/L) |
| severity | enum | level_1/level_2/level_3 |
| symptoms | array | List of symptoms |

### Complications Screening

| Field | Type | Description |
|-------|------|-------------|
| retinopathy.status | enum | none/mild/moderate/severe/proliferative |
| nephropathy.status | enum | normal/microalbuminuria/macroalbuminuria |
| neuropathy.status | enum | none/abnormal |
| foot.status | enum | normal/low_risk/high_risk |

## Enum Values

### Glucose Type
`fasting` | `postprandial_2h` | `bedtime` | `random`

### Hypoglycemia Severity
`level_1` | `level_2` | `level_3`

### Symptom Types
`sweating` | `palpitations` | `tremor` | `hunger` | `confusion` | `dizziness`

### Retinopathy Grade
`none` | `mild` | `moderate` | `severe` | `proliferative`

### Nephropathy Status
`normal` | `microalbuminuria` | `macroalbuminuria`

## Data Storage

- Location: `data/diabetes-tracker.json`
- Format: JSON object
