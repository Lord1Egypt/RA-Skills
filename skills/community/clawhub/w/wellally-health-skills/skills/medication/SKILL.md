---
name: medication
description: Manage medication plans and track medication adherence with allergy checks, pregnancy safety warnings, and drug interaction detection.
argument-hint: <operation_type(add/log/list/history/status) medication_description_natural_language>
allowed-tools: Read, Write
schema: medication/schema.json
---

# Medication Management Skill

Manage medications and medication plans, record daily medication intake, and track medication adherence.

## Core Flow

```
User Input -> Parse Operation Type -> [add] Parse Medication Info -> Allergy Check -> Pregnancy Safety Check -> Drug Interaction Check -> Save
                             -> [log] Record Medication Status -> Save
                             -> [list] Display Medication List
                             -> [history] Display History
                             -> [status] Display Statistics
```

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation |
|----------------|-----------|
| add | add |
| log | log |
| list | list |
| history | history |
| status | status |

## Step 2: Add Medication (add)

### Medication Information Parsing

Extract from natural language:
- **Medication Name**: Generic name or brand name
- **Dosage**: Value + unit (mg, g, ml, IU, tablets, etc.)
- **Frequency**: Times per day, times per week, etc.
- **Medication Time**: Specific medication time points
- **Special Instructions**: Before meals, after meals, before bed, etc.

### Frequency Mapping Rules

| User Input | Frequency Type | Schedule Record Count |
|------------|----------------|----------------------|
| 每天1次, 每日1次 | daily | 7 entries |
| 每天2次, 早晚各一次 | daily | 14 entries |
| 每天3次, 一日三次 | daily | 21 entries |
| 每周1次 | weekly | 1 entry |
| 隔天1次 | every_other_day | 4 entries |
| 按需 | as_needed | 0 entries |

### Time Mapping Rules

| User Input | Standard Time |
|------------|---------------|
| 早餐前 | 07:00 |
| 早餐后 | 08:00 |
| 午餐前 | 11:30 |
| 午餐后 | 12:30 |
| 晚餐前 | 17:30 |
| 晚餐后 | 18:30 |
| 睡前 | 21:00 |
| 早晚 | 08:00, 20:00 |

## Step 3: Safety Checks

### 3.1 Medication Allergy Check

Check `data/allergies.json` for related allergies.

**Common Drug Family Mapping:**

| Drug Category | Includes Drugs |
|---------------|----------------|
| Penicillins | Penicillin, Amoxicillin, Ampicillin, Mezlocillin, etc. |
| Cephalosporins | Cefazolin, Cefixime, Ceftriaxone, etc. |
| Sulfonamides | Sulfamethoxazole, Sulfadiazine, etc. |
| NSAIDs | Aspirin, Ibuprofen, Diclofenac, etc. |

### 3.2 Pregnancy Safety Check

Check `data/pregnancy-tracker.json` and drug pregnancy categories.

| Pregnancy Category | Description | Risk |
|--------------------|-------------|------|
| A | Safe | Lowest |
| B | Relatively Safe | Low |
| C | Use with Caution | Moderate |
| D | Contraindicated | High |
| X | Absolutely Contraindicated | Very High |

### 3.3 Drug Interaction Check

Check for interactions with current medications, classified by severity (A/B/C/D/X).

## Step 4: Generate JSON

```json
{
  "id": "med_20251231123456789",
  "name": "Aspirin",
  "generic_name": "Aspirin",
  "dosage": {
    "value": 100,
    "unit": "mg"
  },
  "frequency": {
    "type": "daily",
    "times_per_day": 1
  },
  "schedule": [
    {
      "weekday": 1,
      "time": "08:00",
      "timing_label": "After Breakfast",
      "dose": {"value": 100, "unit": "mg"}
    }
  ],
  "instructions": "Take after breakfast",
  "active": true
}
```

## Step 5: Save Data

File path: `data/medications/medications.json`

## Step 6: Record Medication (log)

### Medication Status Recognition

| Taken Keywords | Missed Keywords |
|----------------|-----------------|
| 已服用, 已服, 服了 | 忘记, 漏服, 未服 |

### Record Data Structure

```json
{
  "date": "2025-12-31",
  "logs": [
    {
      "id": "log_20251231080000001",
      "medication_id": "med_xxx",
      "medication_name": "Aspirin",
      "scheduled_time": "08:00",
      "actual_time": "2025-12-31T08:15:00",
      "status": "taken",
      "dose": {"value": 100, "unit": "mg"}
    }
  ]
}
```

File path: `data/medication-logs/YYYY-MM/YYYY-MM-DD.json`

## Step 7: Adherence Calculation

**Adherence Percentage = (Actual Doses Taken / Planned Doses) x 100%**

| Grade | Range |
|-------|-------|
| Excellent | >= 90% |
| Good | 70-89% |
| Needs Improvement | < 70% |

## Execution Instructions

```
1. Parse operation type
2. [add] Parse medication info -> Safety checks -> Generate schedule -> Save
3. [log] Record medication status -> Save to log file
4. [list] Read medication list -> Format display
5. [history] Read log files -> Display by time
6. [status] Calculate adherence -> Display statistics
```

## Example Interactions

### Add Medication
```
User: Aspirin 100mg once daily after breakfast
-> Allergy check -> Safety check -> Save
```

### Record Medication
```
User: Already took Aspirin
-> Record status taken
```

### Missed Dose
```
User: Forgot to take Amlodipine
-> Record status missed, display make-up recommendation
```

### View List
```
User: View medication list
-> Display all active medications and schedules
```
