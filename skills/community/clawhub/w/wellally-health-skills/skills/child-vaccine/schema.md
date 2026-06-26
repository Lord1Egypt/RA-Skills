# Child Vaccination Data Structure

## Data File
`data/child-vaccine-tracker.json`

## Main Structure

### scheduled_vaccines (Scheduled Vaccines)

| Field | Type | Description |
|------|------|-------------|
| vaccine_id | string | Vaccine unique identifier (e.g., hepb_b1) |
| vaccine_name | string | Vaccine name |
| category | string | Category: class_1/class_2 |
| dose | string | Dose: 1st dose, 2nd dose, etc. |
| scheduled_date | string | Scheduled vaccination date |
| status | string | Status: pending/scheduled/completed/missed |
| actual_date | string | Actual vaccination date (if completed) |
| batch_number | string | Batch number (optional) |
| manufacturer | string | Manufacturer (optional) |
| clinic | string | Vaccination clinic (optional) |
| notes | string | Notes (optional) |

### Status Values

| Value | Description |
|-------|-------------|
| pending | To be scheduled |
| scheduled | Scheduled |
| completed | Completed |
| missed | Missed |

### upcoming (Upcoming Vaccinations)

| Field | Type | Description |
|------|------|-------------|
| vaccine_id | string | Vaccine ID |
| vaccine_name | string | Vaccine name |
| dose | string | Dose |
| scheduled_date | string | Scheduled date |
| days_until | integer | Days until vaccination |

### overdue (Overdue Vaccinations)

| Field | Type | Description |
|------|------|-------------|
| vaccine_id | string | Vaccine ID |
| vaccine_name | string | Vaccine name |
| dose | string | Dose |
| scheduled_date | string | Scheduled date |
| days_overdue | integer | Days overdue |

### reactions (Adverse Reactions)

| Field | Type | Description |
|------|------|-------------|
| date | string | Occurrence date |
| vaccine_name | string | Vaccine name |
| symptoms | string | Symptom description |
| severity | string | Severity: mild/moderate/severe |
| treatment | string | Treatment method |
| resolved | boolean | Whether resolved |

### Severity Levels

| Value | Description |
|-------|-------------|
| mild | Mild: Local redness, low fever, slight irritability |
| moderate | Moderate: Fever >39, obvious discomfort |
| severe | Severe: Severe allergic reaction, convulsions, medical care needed |

### statistics (Statistics)

| Field | Type | Description |
|------|------|-------------|
| total_vaccines | integer | Total scheduled vaccines |
| class_1_completed | integer | Class 1 vaccines completed |
| class_2_completed | integer | Class 2 vaccines completed |
| overdue_count | integer | Overdue count |
| next_vaccine_date | string | Next vaccination date |

## Class 1 Vaccination Schedule

| Age | Vaccines |
|-----|----------|
| Birth | Hep B (1st dose), BCG |
| 1 month | Hep B (2nd dose) |
| 2 months | Polio (1st dose) |
| 3 months | Polio (2nd dose), DTaP (1st dose) |
| 4 months | Polio (3rd dose), DTaP (2nd dose) |
| 5 months | DTaP (3rd dose) |
| 6 months | Hep B (3rd dose), Meningococcal A (1st dose) |
| 8 months | MMR (1st dose), Japanese Encephalitis (1st dose) |
| 9 months | Meningococcal A (2nd dose) |
| 18 months | DTaP (4th dose), MMR (2nd dose), Hep A |
| 2 years | Japanese Encephalitis (2nd dose) |
| 3 years | Meningococcal A+C (1st dose) |
| 4 years | Polio (4th dose) |
| 6 years | DTaP (5th dose), Meningococcal A+C (2nd dose) |

## Class 2 Recommended Vaccines

| Vaccine | Schedule | Recommendation |
|---------|----------|----------------|
| Varicella | 12 months, 4 years | Recommended |
| PCV13 | 2, 4, 6 months + 12-15 months | Recommended |
