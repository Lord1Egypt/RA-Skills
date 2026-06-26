# COPDTracker Schema

Complete data structure definition for COPD management.

## Schema File

Complete JSON Schema definition: [schema.json](schema.json)

## Field Quick Reference

### Lung Function

| Field | Type | Description |
|-----|------|-------------|
| fev1 | number | Forced expiratory volume in 1 second (L) |
| fev1_percent_predicted | int | Percentage of predicted value (%) |
| fvc | number | Forced vital capacity (L) |
| fev1_fvc_ratio | number | FEV1/FVC ratio |
| gold_grade | enum | Grade 1/Grade 2/Grade 3/Grade 4 |

### CAT Score

| Field | Type | Description |
|-----|------|-------------|
| total_score | int | Total score (0-40) |
| impact_level | enum | Low/Medium/High/Very High |
| items | object | Individual scores for 8 items |

### mMRC Score

| Field | Type | Description |
|-----|------|-------------|
| grade | int | Grade (0-4) |
| severity | enum | Mild/Moderate/Severe dyspnea |

### Exacerbations

| Field | Type | Description |
|-----|------|-------------|
| severity | enum | mild/moderate/severe |
| triggers | array | List of triggers |
| hospitalized | boolean | Whether hospitalized |
| recovery_days | int | Recovery days |

## Enum Values

### GOLD Grade
`Grade 1` | `Grade 2` | `Grade 3` | `Grade 4`

### CAT Impact Level
`Low` | `Medium` | `High` | `Very High`

### Exacerbation Severity
`mild` | `moderate` | `severe`

### Trigger Types
`viral_infection` | `bacterial_infection` | `air_pollution` | `weather_change` | `non_adherence`

## Data Storage

- Location: `data/copd-tracker.json`
- Format: JSON object
