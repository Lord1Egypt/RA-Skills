# Medication Record Schema

Complete data structure definition for medication records.

## Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `name` | string | Medication name |
| `generic_name` | string | Generic name |
| `dosage.value` | number | Dosage value |
| `dosage.unit` | enum | mg/g/ml/IU/tablets/pills/packets/vials/drops |
| `active` | boolean | Whether active |

## Frequency Types

| Type | Description |
|------|-------------|
| daily | Daily |
| weekly | Weekly |
| every_other_day | Every other day |
| as_needed | As needed |

## Medication Schedule (schedule)

| Field | Type | Description |
|-------|------|-------------|
| `weekday` | int | 1-7 (Monday to Sunday) |
| `time` | string | HH:MM format |
| `timing_label` | string | Time label (after breakfast/before bed, etc.) |
| `dose.value` | number | Dose for this time |
| `dose.unit` | string | Dose unit |

## Medication Log Status

| Status | Description |
|--------|-------------|
| taken | Taken |
| missed | Missed |
| skipped | Skipped |
| delayed | Delayed |

## Adherence Grading

| Grade | Range |
|-------|-------|
| Excellent | >= 90% |
| Good | 70-89% |
| Needs Improvement | < 70% |

## Data Storage

- Medication list: `data/medications/medications.json`
- Medication logs: `data/medication-logs/YYYY-MM/YYYY-MM-DD.json`
