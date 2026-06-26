# PregnancyTracker Schema

Complete data structure definition for pregnancy management.

## Schema File

Complete JSON Schema definition: [schema.json](schema.json)

## Field Quick Reference

### Root Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `created_at` | string | ISO 8601 creation time |
| `last_updated` | string | ISO 8601 last update time |
| `current_pregnancy` | object/null | Current pregnancy record |
| `pregnancy_history` | array | Pregnancy history |
| `statistics` | object | Statistics data |
| `settings` | object | Settings |

### current_pregnancy Fields

| Field | Type | Description |
|-------|------|-------------|
| `pregnancy_id` | string | Pregnancy ID, format: pregnancy_YYYYMMDD |
| `lmp_date` | string | Last menstrual period date |
| `due_date` | string | Due date |
| `due_date_confidence` | enum | Confidence: low/medium/high |
| `corrected_by_ultrasound` | bool | Whether ultrasound corrected |
| `current_week` | int | Current gestational week |
| `current_day` | int | Current gestational day |
| `current_trimester` | enum | Trimester: first/second/third |
| `days_passed` | int | Days passed |
| `days_remaining` | int | Days remaining |
| `progress_percentage` | int | Progress percentage |

### multi_pregnancy Fields

| Field | Type | Description |
|-------|------|-------------|
| `pregnancy_type` | enum | Pregnancy type: singleton/twins/triplets/quadruplets |
| `fetal_count` | int | Fetal count (1-4) |
| `detection_method` | string | Detection method |
| `detection_confidence` | string | Detection confidence |
| `fetal_profiles` | array | Fetal profile array |
| `adjusted_due_date` | string/null | Adjusted due date |
| `adjusted_delivery_week` | int | Adjusted delivery week |

### fetal_profile Fields

| Field | Type | Description |
|-------|------|-------------|
| `baby_id` | string | Fetal identifier (A/B/C/D) |
| `estimated_weight` | object/null | Estimated weight |
| `position` | object/null | Fetal position |
| `heart_rate` | object/null | Fetal heart rate |
| `amniotic_fluid_index` | object/null | Amniotic fluid index |
| `growth_percentile` | object/null | Growth percentile |

### prenatal_check Fields

| Field | Type | Description |
|-------|------|-------------|
| `check_id` | string | Check ID |
| `week` | int | Gestational week |
| `check_type` | string | Check type |
| `check_type_en` | string | English type |
| `scheduled_date` | string | Scheduled date |
| `completed` | bool | Whether completed |
| `completed_at` | string/null | Completion time |
| `results` | object | Results |
| `preparation` | string | Preparation notes |

### symptoms Fields

| Field | Type | Description |
|-------|------|-------------|
| `nausea` | object | Nausea |
| `fatigue` | object | Fatigue |
| `edema` | object | Edema |
| `back_pain` | object | Back pain |
| `contractions` | object | Contractions |

### weight_tracking Fields

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date |
| `week` | int | Gestational week |
| `weight` | number | Weight |
| `weight_unit` | string | Unit |
| `weight_gain` | number | Weight gain |
| `bmi` | number | BMI |
| `bmi_category` | string | BMI category |
| `recommended_total_gain` | string | Recommended total gain |
| `weekly_gain` | number/null | Weekly gain |
| `gain_status` | string | Gain status |

## Enum Values

### current_trimester
`first` (First Trimester 1-13 weeks) | `second` (Second Trimester 14-27 weeks) | `third` (Third Trimester 28-42 weeks)

### pregnancy_type
`singleton` (Singleton) | `twins` (Twins) | `triplets` (Triplets) | `quadruplets` (Quadruplets)

### due_date_confidence
`low` (Low) | `medium` (Medium) | `high` (High)

### bmi_category
`underweight` (Underweight <18.5) | `normal` (Normal 18.5-24.9) | `overweight` (Overweight 25-29.9) | `obese` (Obese >=30)

### gain_status
`low` (Insufficient gain) | `normal` (Normal) | `high` (Excessive gain)

## Data Storage

- Main file: `data/pregnancy-tracker.json`
- Detailed records: `data/pregnancy-records/YYYY-MM/YYYY-MM-DD_pregnancy-record.json`
- Mode: Update/append
