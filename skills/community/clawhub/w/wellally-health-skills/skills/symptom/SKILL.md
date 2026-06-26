---
name: symptom
description: Record physical symptoms and discomfort with automatic medical term conversion, severity assessment, and medical advice generation.
argument-hint: <operation_type(record/history/status) symptom_description_natural_language>
allowed-tools: Read, Write
schema: symptom/schema.json
---

# Physical Discomfort Recording Skill

Record daily physical discomfort and symptoms, automatically convert to standard medical records, and provide medical advice.

## Core Flow

```
User Input -> Parse Operation Type -> [add] Parse Symptoms -> Medical Standardization -> Severity Assessment -> Medical Advice -> Save
                              -> [history] Display History Records
                              -> [status] Display Statistical Analysis
```

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation |
|----------------|-----------|
| add | add |
| history | history |
| status | status |

## Step 2: Record Symptoms (add)

### Symptom Information Parsing

Extract from natural language:

**Basic Information (Auto Extracted):**
- **Symptom Name**: Standard medical term
- **Onset Time**: Specific time point or time period
- **Duration**: How long the symptom has persisted
- **Severity**: Mild/Moderate/Severe
- **Body Part**: Specific location of the symptom

**Associated Symptoms (Identified):**
- List of related symptoms
- Systemic symptoms (fever, fatigue, etc.)

**Triggers and Relieving Factors:**
- Triggering factors: exercise, diet, emotions, environment, etc.
- Relieving factors: rest, medication, position change, etc.

### Medical Standardization Conversion

| Colloquial Description | Medical Term |
|------------------------|--------------|
| 头疼 | Headache |
| 胃疼 | Gastric pain/Upper abdominal pain |
| 心慌 | Palpitations |
| 气短 | Shortness of breath |
| 拉肚子 | Diarrhea |
| 便秘 | Constipation |

### Symptom Classification

- **Respiratory System**: Cough, sputum, dyspnea, chest pain, etc.
- **Cardiovascular System**: Palpitations, chest tightness, edema, etc.
- **Digestive System**: Abdominal pain, nausea, vomiting, diarrhea, etc.
- **Nervous System**: Headache, dizziness, insomnia, etc.
- **Urinary System**: Urinary frequency, urgency, dysuria, etc.
- **Endocrine System**: Polydipsia, polyuria, weight changes, etc.
- **Musculoskeletal**: Joint pain, muscle pain, etc.
- **Systemic Symptoms**: Fever, fatigue, weight loss, etc.

### Severity Assessment

| Level | Description | Medical Advice |
|-------|-------------|----------------|
| Grade 1 Mild | Does not affect daily activities | Home observation |
| Grade 2 Moderate | Partially affects daily activities | Suggest observation or outpatient visit |
| Grade 3 Severe | Severely affects daily activities | Seek medical attention soon |
| Grade 4 Critical | Life-threatening | Seek immediate medical attention |

### Medical Advice Assessment

**Seek Immediate Medical Attention (Call 120):**
- Chest pain or chest tightness with sweating, dyspnea
- Sudden severe headache
- Dyspnea or suffocation
- Confusion or syncope

**Seek Medical Attention Soon (Today or Tomorrow):**
- Persistent high fever for more than 3 days
- Severe vomiting or diarrhea causing dehydration
- Persistently worsening pain

**Outpatient Visit (Within 1 Week):**
- Mild to moderate symptoms persisting for more than 1 week

## Step 3: Generate JSON

```json
{
  "id": "20251231123456789",
  "record_date": "2025-12-31",
  "symptom_date": "2025-12-31",
  "original_input": "User's original input",
  "standardized": {
    "main_symptom": "Headache",
    "category": "Nervous System",
    "body_part": "Head",
    "severity": "Mild",
    "severity_level": 1
  },
  "associated_symptoms": [
    {"name": "Nausea", "present": true}
  ],
  "medical_assessment": {
    "urgency": "observation",
    "recommendation": "Home observation",
    "advice": "Recommend adequate rest"
  }
}
```

## Step 4: Save Data

File path: `data/symptom-records/YYYY-MM/YYYY-MM-DD_MainSymptom.json`

## Execution Instructions

```
1. Parse operation type
2. [add] Parse symptoms -> Medical standardization -> Assess severity -> Generate recommendations -> Save
3. [history] Read records -> Display by time
4. [status] Statistical analysis -> Display report
```

## Example Interactions

### Record Headache
```
User: Headache
-> Parse as "Headache", mild, nervous system
-> Generate recommendation: Rest adequately, seek medical attention if persists for more than 24 hours
```

### Record Fever
```
User: Fever 38 degrees with cough
-> Parse as "Fever", moderate, systemic symptoms
-> Associated symptoms: Cough
-> Recommendation: Monitor temperature, drink plenty of water, seek medical attention if fever persists
```

### Record Chest Pain
```
User: Chest tightness and shortness of breath for half an hour
-> Critical symptom alert
-> Recommend immediate medical attention
```
