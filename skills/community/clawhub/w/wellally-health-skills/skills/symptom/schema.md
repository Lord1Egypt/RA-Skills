# Symptom Record Schema

Complete data structure definition for symptom records.

## Field Quick Reference

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `record_date` | string | Record date |
| `symptom_date` | string | Symptom occurrence date |
| `original_input` | string | User's original input |

### Standardized Information (standardized)

| Field | Type | Description |
|-------|------|-------------|
| `main_symptom` | string | Main symptom (medical term) |
| `category` | enum | Symptom category |
| `body_part` | string | Body part |
| `severity` | enum | Mild/Moderate/Severe/Critical |
| `severity_level` | int | 1-4 |
| `duration` | string | Duration |

### Associated Symptoms (associated_symptoms)

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Symptom name |
| `present` | boolean | Whether present |

### Medical Assessment (medical_assessment)

| Field | Type | Description |
|-------|------|-------------|
| `urgency` | enum | Urgency level |
| `recommendation` | string | Recommended actions |
| `advice` | string | Specific advice |
| `red_flags` | array | Red flags |

## Symptom Categories

| Category | Example Symptoms |
|-----------|------------------|
| Respiratory | Cough, sputum, dyspnea |
| Cardiovascular | Palpitations, chest tightness, edema |
| Digestive | Abdominal pain, nausea, vomiting, diarrhea |
| Nervous | Headache, dizziness, insomnia |
| Urinary | Urinary frequency, urgency, dysuria |
| Endocrine | Polydipsia, polyuria, weight changes |
| Musculoskeletal | Joint pain, muscle pain |
| Systemic | Fever, fatigue, weight loss |

## Severity Levels

| Level | Description | Medical Advice |
|-------|-------------|----------------|
| 1 Mild | Does not affect daily activities | Home observation |
| 2 Moderate | Partially affects | Suggest observation or clinic visit |
| 3 Severe | Severely affects | Seek medical attention soon |
| 4 Critical | Life-threatening | Seek immediate medical attention |

## Data Storage

- Location: `data/symptom-records/YYYY-MM/YYYY-MM-DD_MainSymptom.json`
