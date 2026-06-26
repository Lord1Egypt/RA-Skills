# MDT Consultation Schema

Complete data structure definition for Multi-Disciplinary Team (MDT) consultation records.

## Schema File

Complete JSON Schema definition: [schema.json](schema.json)

## Field Quick Reference

### Required Fields

| Field | Type | Description |
|-----|------|-------------|
| `consultation_id` | string | Consultation unique identifier (cons_YYYYMMDDHHmmssSSS) |
| `consultation_date` | string | Consultation date-time (ISO 8601) |
| `specialties_involved` | object[] | List of specialties involved in consultation |

### data_range (Data Range)

| Field | Type | Description |
|-----|------|-------------|
| `type` | enum | all/recent/date/date_range |
| `value` | string | Range value |
| `start_date` | string | Start date (YYYY-MM-DD) |
| `end_date` | string | End date (YYYY-MM-DD) |

### specialties_involved (Specialty Information)

| Field | Type | Description |
|-----|------|-------------|
| `specialty_code` | enum | Specialty code |
| `specialty_name` | string | Specialty name |
| `findings` | string | Analysis findings |
| `recommendations` | string[] | Recommendation list |
| `priority` | enum | high/medium/low |

### Specialty Code Enum

`cardio` (Cardiology) | `endo` (Endocrinology) | `gastro` (Gastroenterology) | `nephro` (Nephrology) | `heme` (Hematology) | `resp` (Pulmonology) | `neuro` (Neurology) | `onco` (Oncology) | `ortho` (Orthopedics) | `derma` (Dermatology) | `pedia` (Pediatrics) | `gyne` (Gynecology) | `general` (General Practice) | `psych` (Psychiatry)

### comprehensive_assessment (Comprehensive Assessment)

| Field | Type | Description |
|-----|------|-------------|
| `overall_health_status` | enum | excellent/good/fair/poor |
| `key_findings` | string[] | Key findings |
| `risk_factors` | object[] | Risk factors |

### recommendations.category (Recommendation Categories)

`lifestyle` (Lifestyle) | `medication` (Medication) | `follow_up` (Follow-up) | `further_testing` (Further Testing) | `specialist_referral` (Specialist Referral) | `monitoring` (Monitoring)

### Priority Enum

`urgent` (Urgent) | `high` (High) | `medium` (Medium) | `low` (Low)

## Data Storage

- Location: `data/mdt-consultations.json`
- Format: JSON array
- Mode: Append
