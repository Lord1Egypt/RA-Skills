# Allergy History Schema

Complete data structure definition for allergy history records.

## Field Quick Reference

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `allergen.name` | string | Allergen name |
| `allergen.type` | enum | drug/food/environmental/other |
| `severity.level` | enum | mild/moderate/severe/anaphylaxis |
| `severity.level_code` | int | Severity level 1-4 |

### Reaction Records

| Field | Type | Description |
|-------|------|-------------|
| `reactions` | array | List of allergic reactions |
| `reactions[].reaction` | string | Reaction symptom |
| `reactions[].onset_time` | string | Onset time |
| `reactions[].severity` | string | Severity level |

### Discovery and Confirmation

| Field | Type | Description |
|-------|------|-------------|
| `discovery.date` | string | Discovery date |
| `discovery.age_at_discovery` | string | Age at discovery |
| `confirmation.method` | string | Confirmation method |

### Management Information

| Field | Type | Description |
|-------|------|-------------|
| `current_status.status` | enum | active/resolved |
| `management.avoidance_strategy` | string | Avoidance strategy |
| `management.medical_alert` | boolean | Medical alert |

## Severity Classification

| Level | Code | Description |
|-------|------|-------------|
| Mild | 1 | Local skin reaction, no systemic effect |
| Moderate | 2 | Significant discomfort, requires treatment |
| Severe | 3 | Severe reaction, requires medical intervention |
| Anaphylaxis | 4 | Life-threatening, requires emergency resuscitation |

## Data Storage

- Location: `data/allergies.json`
- Format: JSON object
