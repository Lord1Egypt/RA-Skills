---
name: profile
description: Set and view user basic medical parameters including gender, height, weight, birth date with calculated BMI and body surface area.
argument-hint: <operation_type(set/view) gender height weight birth_date(YYYY-MM-DD)>
allowed-tools: Read, Write
schema: profile/schema.json
---

# User Basic Parameters Skill

Set or view user's basic medical parameters, including gender, height, weight, and birth date.

## Core Flow

```
User Input -> Parse Operation Type -> [set] Validate Input -> Calculate Derivatives -> Save -> Confirm
                                -> [view] Read Data -> Format Display
```

## Step 1: Parse Operation Type

| Input Keywords | Operation |
|----------------|-----------|
| set | set |
| view | view |

## Step 2: Set Parameters (set)

### Validate Input Data

| Parameter | Format | Range |
|-----------|--------|-------|
| gender | M/F | - |
| height | number | 50-250 cm |
| weight | number | 2-300 kg |
| birth_date | YYYY-MM-DD | Not later than today |

### Calculate Derived Indicators

**BMI Calculation:**
```
BMI = weight(kg) / height(m)²
```

**BMI Classification:**
| Range | Status |
|-------|--------|
| < 18.5 | Underweight |
| 18.5 - 23.9 | Normal |
| 24 - 27.9 | Overweight |
| >= 28 | Obese |

**Body Surface Area Calculation (Mosteller Formula):**
```
BSA = √(height_cm × weight_kg / 3600)
```

**Age Calculation:**
```
Age = Current Year - Birth Year
```

## Step 3: Generate JSON

```json
{
  "created_at": "2025-12-31",
  "last_updated": "2025-12-31",
  "basic_info": {
    "gender": "F",
    "height": 175,
    "height_unit": "cm",
    "weight": 70,
    "weight_unit": "kg",
    "birth_date": "1990-01-01"
  },
  "calculated": {
    "age": 35,
    "age_years": 35,
    "bmi": 22.9,
    "bmi_status": "Normal",
    "body_surface_area": 1.85,
    "bsa_unit": "m²"
  }
}
```

## Step 4: Save Data

File path: `data/profile.json`

## Step 5: View Parameters (view)

Read `data/profile.json` and format for display.

## Execution Instructions

```
1. Parse operation type
2. [set] Validate input -> Calculate BMI/BSA/Age -> Save -> Confirm
3. [view] Read data -> Format display
```

## Example Interactions

### Complete Setup
```
User: F 175 70 1990-01-01

Save:
{
  "basic_info": {
    "gender": "F",
    "height": 175,
    "weight": 70,
    "birth_date": "1990-01-01"
  },
  "calculated": {
    "age": 35,
    "bmi": 22.9,
    "body_surface_area": 1.85
  }
}
```

### View Parameters
```
User: view basic parameters

Output:
Basic Information:
Gender: F (Female)
Height: 175 cm
Weight: 70 kg
Age: 35 years

Calculated Indicators:
BMI: 22.9 (Normal)
Body Surface Area: 1.85 m²
```
