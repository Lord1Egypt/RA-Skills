# EyeHealthTracker Schema

Complete data structure definition for eye health tracking.

## Field Quick Reference

### Core Data Sections

| Field | Type | Description |
|-----|------|-------------|
| `vision_records` | array | Vision examination records |
| `iop_records` | array | Intraocular pressure records |
| `fundus_exams` | array | Fundus examination records |
| `screening_records` | object | Eye disease screening records |
| `habit_records` | array | Eye habit records |
| `checkup_reminders` | object | Examination reminders |

## vision_records Array Item

| Field | Type | Description |
|-----|------|-------------|
| `id` | string | Record ID |
| `date` | string | Examination date |
| `left_eye` | object | Left eye data |
| `right_eye` | object | Right eye data |
| `exam_type` | string | Examination type |
| `notes` | string | Notes |

### left_eye / right_eye Object

| Field | Type | Description |
|-----|------|-------------|
| `uncorrected_va` | number | Uncorrected visual acuity (0-2) |
| `corrected_va` | number | Corrected visual acuity (0-2) |
| `sphere` | number | Spherical power (-20 to +20) |
| `cylinder` | number | Cylindrical power (0 to -6) |
| `axis` | number | Axis (0-180) |

## iop_records Array Item

| Field | Type | Description |
|-----|------|-------------|
| `id` | string | Record ID |
| `date` | string | Examination date |
| `time` | string | Examination time (HH:mm) |
| `left_iop` | number | Left eye IOP (5-50 mmHg) |
| `right_iop` | number | Right eye IOP (5-50 mmHg) |
| `measurement_method` | string | Measurement method |
| `reference_range` | string | Reference range |

## fundus_exams Array Item

| Field | Type | Description |
|-----|------|-------------|
| `id` | string | Record ID |
| `date` | string | Examination date |
| `exam_type` | string | Examination type |
| `findings` | object | Examination findings |
| `comments` | string | Comments |

## screening_records Object

### glaucoma (Glaucoma Screening)
- `result`: negative/suspect/early/moderate/advanced

### cataract (Cataract Screening)
- `result`: none/grade_1/grade_2/grade_3/mature

### amd (Macular Degeneration Screening)
- `result`: none/early/intermediate/late

### diabetic_retinopathy (Diabetic Retinopathy Screening)
- `result`: none/mild/moderate/severe/proliferative

### dry_eye (Dry Eye Screening)
- `result`: none/mild/moderate/severe

## habit_records Array Item

| Field | Type | Description |
|-----|------|-------------|
| `date` | string | Record date |
| `screen_time_hours` | number | Screen usage hours |
| `outdoor_time_hours` | number | Outdoor activity hours |
| `break_20_20_20` | enum | 20-20-20 rule compliance |
| `viewing_distance_cm` | number | Viewing distance (cm) |
| `lighting` | enum | Lighting quality |

## Data Storage

- Location: `data/eye-health-tracker.json`
