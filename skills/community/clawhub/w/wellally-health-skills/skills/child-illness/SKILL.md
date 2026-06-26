---
name: child-illness
description: Track child illness, symptoms, fever management, and medication records. Use when user mentions child sickness, fever, cough, cold, or disease.
argument-hint: <operation_type: record/symptom/fever/medicine/recovery/frequency/history, e.g.: record fever cough, fever 38.5, medicine ibuprofen 5ml>
allowed-tools: Read, Write
schema: child-illness/schema.json
---

# Child Illness Management Skill

Child common illness recording, symptom tracking and home care management, providing fever management, medication logging and recovery tracking.

## Core Flow

```
User Input → Identify Operation Type → Read Child Information → Collect Illness Information → Generate Report → Save Data
```

## Step 1: Parse User Input

### Operation Type Mapping

| Input | action | Description |
|------|--------|-------------|
| record | record | Log illness |
| symptom | symptom | Log symptoms |
| fever | fever | Fever management |
| medicine | medicine | Medication log |
| recovery | recovery | Recovery tracking |
| frequency | frequency | Illness frequency |
| history | history | Historical records |

### Illness Type Recognition

| Keywords | Illness Type | Common Symptoms |
|----------|--------------|-----------------|
| cold, 感冒, 上感, 流鼻涕, 鼻塞 | Acute upper respiratory infection | Fever, cough, runny nose, sore throat |
| bronchitis, 支气管炎 | Acute bronchitis | Cough, sputum, fever |
| pneumonia, 肺炎 | Pneumonia | High fever, cough, difficulty breathing |
| gastroenteritis, 肠炎, 拉肚子, 腹泻 | Acute gastroenteritis | Vomiting, diarrhea, fever |
| HFMD, 手足口 | Hand, foot and mouth disease | Rash, fever, oral ulcers |
| chickenpox, 水痘 | Chickenpox | Rash, fever, itching |
| flu, 流感 | Influenza | High fever, body aches, fatigue |
| otitis media, 中耳炎, 耳朵痛 | Acute otitis media | Ear pain, fever |
| allergic rhinitis, 过敏鼻炎 | Allergic rhinitis | Sneezing, runny nose, nasal itching |

## Step 2: Check Information Completeness

### record Operation Required:
- Symptom description (can infer from user input)
- Onset date (defaults to today)

### fever Operation Required:
- Temperature value

### medicine Operation Required:
- Medication name
- Dosage

## Step 3: Interactive Prompts (When Information Insufficient)

### When Missing Symptom Details:
```
Please provide following information (can skip):

1. Main symptoms: (e.g., fever, cough, runny nose)
2. Onset date: (defaults to today)
3. Severity: (mild/moderate/severe)
4. Medical consultation: (yes/no)

Enter /done to complete recording
```

### When Fever Recording Missing Temperature:
```
Please enter current temperature (e.g., 38.5)
```

## Step 4: Generate Assessment Report

### Temperature Grade Standard

| Temperature Grade | Standard Range |
|-------------------|----------------|
| Normal | < 37.3 |
| Low-grade fever | 37.3 - 38.0 |
| Moderate fever | 38.1 - 39.0 |
| High fever | 39.1 - 41.0 |
| Very high fever | > 41.0 |

### Illness Record Report Example:
```
Illness record saved

Illness Information:
Child: Xiaoming
Age: 2 years 5 months
Record date: January 14, 2025

Illness: Acute upper respiratory infection
Type: Viral cold
Severity: Mild

Symptoms:
  Fever (peak 38.5)
  Cough (dry)
  Runny nose (clear)
  Mild sore throat

Home Care Recommendations:

Fever Management:
  Use antipyretic when temperature > 38.5
  Plenty of water/milk
  Loose, breathable clothing
  Regular temperature monitoring

Warning Signs:
Seek immediate medical care if:
  Difficulty breathing or rapid breathing
  Persistent high fever > 3 days
  Poor mental status
  Refusing to eat or significantly reduced urine output

Data saved
```

## Step 5: Save Data

Save to `data/child-illness-tracker.json`, including:
- child_profile: Child basic information
- illness_records: Illness records
- symptom_history: Symptom history
- fever_tracking: Temperature tracking
- medication_log: Medication log
- statistics: Statistical information

## Common Illness Care Points

### Acute Upper Respiratory Infection (Cold)
- Cause: Viral infection
- Course: 7-10 days
- Care: Rest, plenty of fluids, symptomatic treatment
- Seek care indicators: Fever > 3 days, difficulty breathing, poor mental status

### Acute Gastroenteritis
- Symptoms: Vomiting, diarrhea
- Care focus: Prevent dehydration (oral rehydration solution)
- Diet: Bland, small frequent meals

### Hand, Foot and Mouth Disease
- Symptoms: Fever + rash (hands, feet, mouth)
- Contagious: High, requires isolation
- Course: 7-10 days

## Fever Management Principles

### Medication Fever Reduction
- Ibuprofen (>6 months): 5-10mg/kg, every 6-8 hours
- Acetaminophen (>3 months): 10-15mg/kg, every 4-6 hours
- Maximum 4 times daily

### Avoid Using
- Aspirin (contraindicated in children)
- Steroid fever reduction
- Alcohol sponge bath

### Warning Signs
- Temperature >= 39 for 24 hours
- Febrile seizures
- Poor mental status, drowsiness
- Difficulty breathing

## Execution Instructions

1. Read data/profile.json for child information
2. Execute corresponding function based on operation type
3. Generate care recommendation report
4. Save to data/child-illness-tracker.json

## Medical Safety Principles

### Safety Boundaries
- No illness diagnosis
- No specific medication brand recommendations
- No prescribing
- No emergency handling

### System Can
- Illness recording and tracking
- Symptom change monitoring
- Fever management recording
- Medication time logging
- Recovery progress tracking
- Illness frequency statistics

## Important Notice

This system is for illness recording and home care reference only, **cannot replace professional medical diagnosis and treatment**.

If following conditions occur, **seek immediate medical care**:
- Persistent high fever > 3 days
- Difficulty breathing or rapid breathing
- Poor mental status, drowsiness
- Persistent crying unable to be soothed
- Refusing to eat or significantly reduced urine output
- Rash or seizures

For emergencies, **immediately call 120**.
