# Child Illness Management Data Structure

## Data File
`data/child-illness-tracker.json`

## Main Structure

### illness_records (Illness Records)

| Field | Type | Description |
|------|------|-------------|
| id | string | Illness record unique identifier |
| date | string | Record date |
| onset_date | string | Onset date |
| recovery_date | string | Recovery date (nullable) |
| days_illness | integer | Days ill |

### condition (Illness Information)

| Field | Type | Description |
|------|------|-------------|
| name | string | Illness name |
| category | string | Illness category: respiratory/gastrointestinal/skin/other |
| type | string | Illness type: viral/bacterial |
| severity | string | Severity: mild/moderate/severe |
| doctor_visit | boolean | Whether visited doctor |
| diagnosis | string | Diagnosis result |

### symptoms (Symptom Records)

| Field | Type | Description |
|------|------|-------------|
| name | string | Symptom name |
| severity | string | Severity: mild/moderate/severe |
| status | string | Status: improving/worsening/stable |

### fever_tracking (Fever Tracking)

| Field | Type | Description |
|------|------|-------------|
| date | string | Measurement time (ISO 8601 format) |
| temperature | number | Body temperature (Celsius) |
| medication | string | Medication given (nullable) |

### medications (Medication Records)

| Field | Type | Description |
|------|------|-------------|
| name | string | Medication name |
| dosage | string | Dosage |
| frequency | string | Dosing frequency |
| times_given | integer | Times administered |

### statistics (Statistics)

| Field | Type | Description |
|------|------|-------------|
| total_illnesses | integer | Total illness count |
| total_days_ill | integer | Total days ill |
| most_common_condition | string | Most common illness |
| illnesses_last_12_months | integer | Illnesses in last 12 months |
| doctors_visits | integer | Doctor visit count |
| emergency_visits | integer | Emergency room visit count |

## Illness Categories

| category | Description | Examples |
|----------|-------------|----------|
| respiratory | Respiratory system | Cold, bronchitis, pneumonia |
| gastrointestinal | Digestive system | Enteritis, diarrhea |
| skin | Skin system | Chickenpox, hand-foot-mouth disease |
| other | Other | Otitis media, conjunctivitis |
