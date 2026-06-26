# Family Health Schema

Complete data structure definition for family health management and genetic risk assessment.

## Schema File

Complete JSON Schema definition: [schema.json](schema.json)

## Field Quick Reference

### Required Fields

| Field | Type | Description |
|-----|------|-------------|
| `family_id` | string | Family unique identifier (fam_YYYYMMDD_XXX) |
| `members` | object[] | Family member list |

### Member Relationships (relationship)

| Code | Description |
|-----|-------------|
| `self` | Self |
| `father` | Father |
| `mother` | Mother |
| `spouse` | Spouse |
| `son` | Son |
| `daughter` | Daughter |
| `brother` | Brother |
| `sister` | Sister |
| `paternal_grandfather` | Paternal grandfather |
| `paternal_grandmother` | Paternal grandmother |
| `maternal_grandfather` | Maternal grandfather |
| `maternal_grandmother` | Maternal grandmother |
| `half_brother` | Half-brother |
| `half_sister` | Half-sister |
| `adopted` | Adopted relationship |

### Blood Type Enum

`A` | `B` | `AB` | `O` | `unknown`

### Disease Categories (disease_category)

`cardiovascular` (Cardiovascular) | `metabolic` (Metabolic) | `cancer` (Cancer) | `respiratory` (Respiratory) | `autoimmune` (Autoimmune) | `neurological` (Neurological) | `psychiatric` (Psychiatric) | `other` (Other)

### Inheritance Patterns (inheritance_pattern)

`autosomal_dominant` (Autosomal dominant) | `autosomal_recessive` (Autosomal recessive) | `x_linked` (X-linked) | `mitochondrial` (Mitochondrial) | `multifactorial` (Multifactorial) | `unknown` (Unknown)

### Risk Levels (risk_level)

`high` (High risk >=70%) | `medium` (Medium risk 40-69%) | `low` (Low risk <40%)

### Recommendation Categories (category)

`screening` (Screening) | `lifestyle` (Lifestyle) | `medication` (Medication) | `monitoring` (Monitoring) | `vaccination` (Vaccination)

## Genetic Risk Score Calculation

```
Risk Score = (First-degree relatives affected × 40) +
            (Early-onset cases × 30) +
            (Family clustering × 30)

Risk Level:
- High Risk: >= 70%
- Medium Risk: 40% - 69%
- Low Risk: < 40%
```

## Data Storage

- Location: `data/family-health-tracker.json`
- Format: JSON object
- Mode: Update
