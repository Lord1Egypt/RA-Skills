---
name: cognitive
description: Cognitive function assessment tracking for elderly - MMSE/MoCA tests, cognitive domain evaluation, ADL/IADL assessment, and risk monitoring
argument-hint: <operation_type+info, e.g.: mmse score 27, moca 24, domain memory mild_impairment, adl independent>
allowed-tools: Read, Write
schema: cognitive/schema.json
---

# Cognitive Function Assessment Skill

Manages cognitive function assessment for the elderly, including MMSE, MoCA tests, cognitive domain evaluation, and daily function assessment.

## Core Flow

```
User Input -> Identify Operation Type -> Extract Parameter Info -> Check Completeness -> [Need Supplement] Ask User
                                                      |
                                                   [Information Complete]
                                                      |
                                              Generate JSON -> Save Data -> Output Confirmation
```

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation Type | Description |
|----------------|----------------|-------------|
| mmse | mmse_test | MMSE Mini-Mental State Examination |
| moca | moca_test | MoCA Montreal Cognitive Assessment |
| domain | cognitive_domain | Cognitive domain assessment |
| adl | adl_assessment | Activities of Daily Living assessment |
| iadl | iadl_assessment | Instrumental ADL assessment |
| status | cognitive_status | View cognitive status |
| trend | trend_analysis | View change trends |
| risk | risk_assessment | Cognitive function risk assessment |

### Cognitive Domain Keywords Mapping

| Input Keywords | Domain Name |
|----------------|--------------|
| memory | memory |
| executive | executive |
| language | language |
| visuospatial | visuospatial |

### Function Status Keywords Mapping

| Input Keywords | Status Value |
|----------------|--------------|
| normal | normal |
| mild | mild_impairment |
| moderate | moderate_impairment |
| severe | severe_impairment |
| independent | independent |
| needs_assistance | needs_assistance |
| dependent | dependent |
| supervision_needed | supervision_needed |

### ADL Item Keywords

| Input Keywords | Item Name |
|----------------|-----------|
| bathing | bathing |
| dressing | dressing |
| toileting | toileting |
| transferring | transferring |
| continence | continence |
| feeding | feeding |

### IADL Item Keywords

| Input Keywords | Item Name |
|----------------|-----------|
| shopping | shopping |
| cooking | cooking |
| managing_medications | managing_medications |
| using_telephone | using_telephone |
| managing_finances | managing_finances |
| housekeeping | housekeeping |
| transportation | transportation |
| laundry | laundry |

## Step 2: Check Information Completeness

### MMSE Test Required:
- Total score (0-30 points)

### MoCA Test Required:
- Total score (0-30 points)
- Education level (optional, for score adjustment)

### Cognitive Domain Assessment Required:
- Domain name (memory/executive/language/visuospatial)
- Function status (normal/mild_impairment/moderate_impairment/severe_impairment)

### ADL/IADL Assessment Required:
- Item name
- Function status

## Step 3: Interactive Prompts (If Needed)

### Scenario A: Missing MMSE/MoCA Score
```
Please provide test total score (0-30 points)
```

### Scenario B: Missing Cognitive Domain Assessment Information
```
Please specify the cognitive domain to assess:
- memory (memory)
- executive (executive function)
- language (language ability)
- visuospatial (visuospatial ability)

What is the function status?
- normal (normal)
- mild_impairment (mild impairment)
- moderate_impairment (moderate impairment)
- severe_impairment (severe impairment)
```

### Scenario C: Missing ADL/IADL Items
```
Please provide specific activity items and function status
```

## Step 4: Generate JSON

### MMSE Test Record
```json
{
  "test_type": "mmse",
  "date": "2025-06-20",
  "total_score": 27,
  "max_score": 30,
  "interpretation": "Normal",
  "items": {
    "orientation": 10,
    "registration": 3,
    "attention": 5,
    "recall": 3,
    "language": 6
  }
}
```

### MoCA Test Record
```json
{
  "test_type": "moca",
  "date": "2025-06-20",
  "total_score": 24,
  "adjusted_score": 25,
  "education_years": 12,
  "max_score": 30,
  "interpretation": "Mild Cognitive Impairment"
}
```

### Cognitive Domain Assessment Record
```json
{
  "domain": "memory",
  "status": "mild_impairment",
  "assessment_date": "2025-06-20",
  "notes": "Short-term memory impaired, long-term memory preserved"
}
```

### ADL Assessment Record
```json
{
  "activity": "bathing",
  "status": "independent",
  "assessment_date": "2025-06-20"
}
```

Complete schema definition: see [schema.json](schema.json).

## Step 5: Save Data

1. Read `data/cognitive-assessment.json`
2. Update corresponding sections based on operation type
3. Update statistics
4. Write back to file

## Execution Instructions

```
1. Identify operation type (mmse/moca/domain/adl/iadl/status/trend/risk)
2. Extract parameter information (scores, cognitive domains, function status, etc.)
3. Check required field completeness
4. If missing, ask user to supplement
5. Generate JSON compliant with schema.json
6. Save to data/cognitive-assessment.json
7. Output confirmation and interpretation results
```

## Example Interactions

### Example 1: MMSE Test
```
User: mmse score 27

AI: MMSE test result recorded
Total score: 27/30
Interpretation: Normal
Next assessment: 2026-06-20
```

### Example 2: Cognitive Domain Assessment
```
User: domain memory mild_impairment

AI: Cognitive domain assessment recorded
Cognitive domain: Memory (memory)
Status: Mild impairment (mild_impairment)

Currently impaired cognitive domain: Memory
```

### Example 3: ADL Assessment
```
User: adl independent

AI: ADL assessment result recorded
All 6 basic activities: Independent
Dependency level: No dependency
```

### Example 4: View Status
```
User: cognitive status

AI: Cognitive Function Status Report
━━━━━━━━━━━━━━━━━━━━━━━━
Latest MMSE: 27/30 (Normal) - 2025-06-20
Latest MoCA: 24/30 (Mild impairment) - 2025-06-15

Cognitive domain status:
- Memory: Mild impairment
- Executive function: Normal
- Language: Normal
- Visuospatial: Normal

Daily function:
- ADL: Independent
- IADL: Needs assistance (2 items)
```

For more examples, see [examples.md](examples.md).

## Medical Safety Boundaries

### Cannot Do:
- Diagnose cognitive impairment or dementia
- Replace neurologist/geriatrician professional assessment
- Provide specific medication treatment plans

### Can Do:
- Cognitive function screening (MMSE/MoCA)
- Cognitive decline trend tracking
- Activities of daily living assessment (ADL/IADL)
- Cognitive domain function assessment
- Risk warning and medical visit recommendations

### Medical Visit Recommendations:
Seek medical attention if:
- MMSE <= 26 points
- MoCA <= 25 points
- Multiple cognitive domains impaired
- ADL/IADL function decline
- Rapid cognitive decline
