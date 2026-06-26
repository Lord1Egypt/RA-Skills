# symptom Skill Examples

## Example 1: Record Headache

```
User: Headache

Parse:
{
  "main_symptom": "Headache",
  "category": "Nervous System",
  "body_part": "Head",
  "severity": "Mild",
  "severity_level": 1
}

Output:
✅ Symptom recorded
Main Symptom: Headache (Mild)
Recommendation: Rest adequately, seek medical attention if symptoms persist for more than 24 hours
```

## Example 2: Record Fever with Cough

```
User: Fever 38 degrees with cough and sore throat

Parse:
{
  "main_symptom": "Fever",
  "category": "Systemic",
  "severity": "Moderate",
  "associated_symptoms": [
    {"name": "Cough", "present": true},
    {"name": "Sore throat", "present": true}
  ]
}

Output:
✅ Symptom recorded
Main Symptom: Fever (Moderate)
Associated Symptoms: Cough, Sore throat
Recommendation: Monitor temperature, drink plenty of water, seek medical attention if fever persists for more than 3 days
```

## Example 3: Critical Symptom

```
User: Chest tightness and shortness of breath for half an hour

Parse:
{
  "main_symptom": "Chest tightness",
  "severity": "Critical",
  "severity_level": 4
}

Output:
⚠️ Possible critical symptom detected
Recommendation: Seek immediate medical attention rather than just recording symptoms
Please call 120 or go to the nearest hospital emergency room
```

## Example 4: View History

```
User: View symptom history

Output:
📋 Symptom History Records
December 2025 (3 records)
12-31  Headache (Mild)     Nervous System
12-30  Abdominal pain (Moderate)     Digestive System
12-28  Fever (Moderate)     Systemic
```

## Example 5: Symptom Statistics

```
User: Symptom statistics

Output:
📊 Symptom Statistics Analysis
Monthly Overview:
Records: 5 times
Most Common: Headache (2 times)
Main System: Nervous System

Severity:
Mild: 3 times
Moderate: 2 times
```
