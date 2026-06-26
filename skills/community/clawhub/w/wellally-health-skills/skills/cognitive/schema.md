# CognitiveAssessment Schema

Complete data structure definition for cognitive function assessment.

## Schema File

Complete JSON Schema definition: [schema.json](schema.json)

## Field Quick Reference

### MMSE/MoCA Tests

| Field | Type | Description |
|-----|------|-------------|
| test_type | string | mmse or moca |
| date | string | Test date |
| total_score | int | Total score |
| interpretation | string | Result interpretation |

### Cognitive Domain Assessment

| Field | Type | Description |
|-----|------|-------------|
| domain | enum | memory/executive/language/visuospatial |
| status | enum | normal/mild_impairment/moderate_impairment/severe_impairment |
| last_assessment | string | Last assessment date |

### ADL/IADL Assessment

| Field | Type | Description |
|-----|------|-------------|
| activity | enum | Activity item |
| status | enum | independent/needs_assistance/dependent/supervision_needed |

## Enum Values

### Cognitive Domains (domain)
`memory` | `executive` | `language` | `visuospatial`

### Functional Status (status)
`normal` | `mild_impairment` | `moderate_impairment` | `severe_impairment`

### ADL Status
`independent` | `needs_assistance` | `dependent`

### IADL Status
`independent` | `needs_assistance` | `supervision_needed` | `dependent`

### Risk Level
`Low Risk` | `Medium Risk` | `High Risk`

## Data Storage

- Location: `data/cognitive-assessment.json`
- Format: JSON object
