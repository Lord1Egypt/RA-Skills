---
name: male-fertility
description: Male fertility health tracking including semen analysis, hormone monitoring, and infertility assessment
argument-hint: <operation_type, e.g.: semen volume 2.5ml/hormone testosterone 15.5/status>
allowed-tools: Read, Write
schema: male-fertility/schema.json
---

# Male Fertility Health Skill

Male fertility health tracking and management, including semen analysis records, hormone level monitoring, and infertility factor assessment.

## Core Flow

```
User Input → Identify Operation Type → Parse Information → Check Completeness → Generate JSON → Save Data
                                     |
                              [Ask when information insufficient]
```

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation |
|----------------|-----------|
| semen | Semen analysis |
| hormone | Hormone levels |
| varicocele | Varicocele |
| infection | Reproductive tract infection |
| status | View status |
| diagnosis | View diagnosis |

### Semen Parameter Recognition

| Parameter | Keywords | Extract |
|-----------|----------|--------|
| Volume | volume, ml | Number + mL |
| Concentration | concentration, 10^6/mL | Number |
| Progressive motility | pr, progressive | Percentage |
| Non-progressive motility | np | Percentage |
| Morphology | morphology, % | Percentage |
| pH | ph | 7.0-8.0 |

### Hormone Recognition

| Hormone | Keywords | Unit |
|---------|----------|------|
| Testosterone | testosterone, T | nmol/L |
| LH | LH | IU/L |
| FSH | FSH | IU/L |
| Prolactin | PRL | ng/mL |
| Estradiol | E2 | pg/mL |

## Step 2: Check Information Completeness

### Semen Analysis (semen)
- **Required**: At least one parameter value
- **Optional**: Abstinence period, test date

### Hormone Levels (hormone)
- **Required**: Hormone type and value
- **Optional**: Measurement time, test date

### Varicocele (varicocele)
- **Required**: Presence and location
- **Optional**: Grade, confirmation method

### Reproductive Tract Infection (infection)
- **Required**: Pathogen and result
- **Optional**: Test date

## Step 3: Interactive Prompts (If Needed)

Use consultation-style dialogue, friendly and natural questioning for missing information.

### Question Scenarios

#### Scenario A: Semen Analysis Missing Parameters
```
Please provide specific semen analysis parameters, such as:
- Volume (mL)
- Concentration (10^6/mL)
- Motility (PR/NP percentage)
- Morphology (normal形态%)
```

#### Scenario B: Hormone Test Missing Type
```
Which hormone test result is this?
Options: Testosterone, LH, FSH, Prolactin, Estradiol
```

## Step 4: Generate JSON

### Semen Analysis Data Structure

```json
{
  "record_type": "semen_analysis",
  "date": "2025-06-20",
  "abstinence_period": "3_days",
  "volume": {
    "value": 2.5,
    "unit": "mL",
    "reference": ">=1.5",
    "result": "normal"
  },
  "concentration": {
    "value": 45,
    "unit": "10^6/mL",
    "reference": ">=15",
    "result": "normal"
  },
  "total_count": {
    "value": 112.5,
    "unit": "10^6",
    "reference": ">=39",
    "result": "normal"
  },
  "motility": {
    "pr": {"value": 35, "reference": ">=32", "result": "normal"},
    "np": {"value": 20, "reference": ">=40", "result": "normal"}
  },
  "morphology": {
    "value": 4,
    "unit": "%",
    "reference": ">=4",
    "result": "normal"
  },
  "ph": {
    "value": 7.5,
    "reference": "7.2-8.0",
    "result": "normal"
  },
  "liquefaction": {
    "value": 30,
    "unit": "minutes",
    "reference": "<=60",
    "result": "normal"
  },
  "diagnosis": "normospermia"
}
```

### Hormone Data Structure

```json
{
  "record_type": "hormone_test",
  "date": "2025-06-15",
  "testosterone": {
    "total": 15.5,
    "reference": "10-35",
    "unit": "nmol/L",
    "result": "normal"
  },
  "lh": {
    "value": 5.2,
    "reference": "1.7-8.6",
    "unit": "IU/L",
    "result": "normal"
  },
  "fsh": {
    "value": 8.1,
    "reference": "1.5-12.4",
    "unit": "IU/L",
    "result": "normal"
  },
  "prl": {
    "value": 12.5,
    "reference": "<15",
    "unit": "ng/mL",
    "result": "normal"
  },
  "e2": {
    "value": 35,
    "reference": "<70",
    "unit": "pg/mL",
    "result": "normal"
  }
}
```

Complete schema definition: see [schema.json](schema.json).

## Step 5: Save Data

1. Generate record ID: `fertility_YYYYMMDD_XXX`
2. Save to `data/生育记录/YYYY-MM/YYYY-MM-DD_精液分析.json`
3. Update `data/fertility-tracker.json`
4. Update `data/index.json`

## Semen Analysis Standards (WHO 2021)

| Parameter | Normal | Abnormal |
|-----------|--------|----------|
| Volume | >= 1.5 mL | < 1.5 mL (hypospermia) |
| Concentration | >= 15 x 10^6/mL | < 15 (oligozoospermia) |
| Total count | >= 39 x 10^6 | < 39 |
| PR (progressive) | >= 32% | < 32% (asthenozoospermia) |
| NP (total) | >= 40% | < 40% |
| Normal morphology | >= 4% | < 4% (teratozoospermia) |
| pH | 7.2-8.0 | < 7.2 or > 8.0 |
| Liquefaction time | <= 60 minutes | > 60 minutes |

## Diagnosis Classification

| Result | Diagnosis |
|--------|----------|
| All parameters normal | Normal semen (normospermia) |
| Concentration < 15 | Oligozoospermia |
| Concentration = 0 | Azoospermia |
| PR < 32% | Asthenozoospermia |
| Normal morphology < 4% | Teratozoospermia |
| Volume < 1.5mL | Hypospermia |
| Multiple abnormalities | Mixed abnormalities |

## Execution Instructions

```
1. Identify operation type (semen/hormone/varicocele/infection/status/diagnosis)
2. Parse input parameters, extract all available information
3. Check required fields, ask user if missing
4. Evaluate results against WHO standards
5. Generate JSON compliant with schema.json
6. Save to appropriate file path
7. Confirm save to user and display summary and recommendations
```

## Example Interactions

### Example 1: Record Semen Analysis
```
User: 精液分析 精液量2.5ml 密度45 前向35% 形态4%
AI: 解析中...
    Volume: 2.5 mL ✓ Normal
    Concentration: 45 x 10^6/mL ✓ Normal
    Progressive motility: 35% ✓ Normal
    Morphology: 4% ✓ Normal

    Diagnosis: Normospermia

    Saved to: data/生育记录/2025-06/2025-06-20_精液分析.json
```

### Example 2: Record Hormone Levels
```
User: 激素检测 睾酮15.5 LH5.2 FSH8.1
AI: Record hormone test results:

    Testosterone: 15.5 nmol/L ✓ Normal (reference: 10-35)
    LH: 5.2 IU/L ✓ Normal (reference: 1.7-8.6)
    FSH: 8.1 IU/L ✓ Normal (reference: 1.5-12.4)

    Assessment: Hormone levels normal, HPTA axis function normal

    Saved to: data/生育记录/2025-06/2025-06-15_激素检测.json
```

### Example 3: View Status
```
User: 生育状态
AI: Male fertility health status

    Semen analysis: Normal (last test: 2025-06-20)
    Hormone levels: Normal (last test: 2025-06-15)
    Varicocele: None
    Reproductive tract infection: Negative

    Comprehensive Assessment: Normal fertility function

    Recommendation: Continue trying natural conception, maintain healthy lifestyle
```

For more examples, see [examples.md](examples.md).

## Important Notice

- This system is for fertility health tracking only, cannot replace professional medical diagnosis
- Semen analysis requires 2-3 confirmations
- Abstinence 3-7 days before testing
- Infertility assessment requires both partners to be checked
- All data is stored locally only

## Seek Immediate Medical Care For

- Azoospermia
- Significantly abnormal hormones
- Grade III varicocele
- Positive reproductive tract infection
