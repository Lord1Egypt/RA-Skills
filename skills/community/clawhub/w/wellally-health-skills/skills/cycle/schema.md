# CycleTracker Schema

Complete data structure definition for women's health cycle tracking.

## Schema File

Complete JSON Schema definition: [schema.json](schema.json)

## Field Quick Reference

### Root Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `created_at` | string | ISO 8601 creation time |
| `last_updated` | string | ISO 8601 last update time |
| `user_settings` | object | User settings |
| `cycles` | array | Cycle records array |
| `current_cycle` | object/null | Currently active cycle |
| `statistics` | object | Statistics data |
| `predictions` | object | Prediction data |

### user_settings

| Field | Type | Default | Description |
|-----|------|--------|-------------|
| `average_cycle_length` | int | 28 | Average cycle length (21-40 days) |
| `average_period_length` | int | 5 | Average period length (2-10 days) |
| `pregnancy_planning` | bool | false | Pregnancy planning mode |

### cycle object

| Field | Type | Description |
|-------|------|-------------|
| `cycle_id` | string | Cycle ID, format: cycle_YYYYMMDD |
| `period_start` | string | Period start date (YYYY-MM-DD) |
| `period_end` | string/null | Period end date |
| `cycle_length` | int/null | Cycle length (days) |
| `period_length` | int/null | Period length (days) |
| `flow_pattern` | object | Flow pattern |
| `pms_symptoms` | object | PMS symptoms |
| `daily_logs` | array | Daily log array |
| `ovulation_date` | string/null | Ovulation date |
| `predictions` | object | Prediction data |
| `notes` | string | Notes |
| `created_at` | string | ISO 8601 creation time |
| `completed` | bool | Whether completed |

### daily_log object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Log ID |
| `date` | string | Date (YYYY-MM-DD) |
| `cycle_day` | int | Cycle day number |
| `phase` | enum | Phase: menstrual/follicular/ovulation/luteal |
| `flow` | object | Flow information |
| `symptoms` | string[] | Symptom list |
| `mood` | string | Mood status |
| `energy_level` | enum | Energy: high/medium/low |
| `medication_taken` | string[] | Medications taken |
| `notes` | string | Notes |

## Enum Values

### flow.intensity
`spotting` | `light` | `medium` | `heavy` | `very_heavy`

### phase
`menstrual` (Menstrual) | `follicular` (Follicular) | `ovulation` (Ovulation) | `luteal` (Luteal)

### energy_level
`high` | `medium` | `low`

### prediction_confidence
`low` | `medium` | `high` | `very_high`

## Data Storage

- Main file: `data/cycle-tracker.json`
- Detailed records: `data/cycle-records/YYYY-MM/YYYY-MM-DD_cycle-record.json`
- Mode: Update/append
