---
name: allergy
description: Manage allergy records including drug, food, and environmental allergies with severity tracking and medical alert integration.
argument-hint: <operation_type(add/list/update/delete) allergy_information_natural_language_description>
allowed-tools: Read, Write
schema: allergy/schema.json
---

# Allergy History Management Skill

Record and manage allergy history, including drug allergies, food allergies, environmental allergies, etc., with quick query and update support.

## Core Flow

```
User Input -> Parse Operation Type -> [add] Parse Allergy Info -> Medical Standardization -> Generate JSON -> Save
                             -> [list] Filter and Display
                             -> [update] Find and Update -> Save
                             -> [delete] Confirm Deletion
```

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation |
|----------------|-----------|
| add | add |
| list | list |
| update | update |
| delete | delete |

## Step 2: Add Allergy Record (add)

### Allergy Information Parsing

Extract from natural language:

**Basic Information (Auto Extracted):**
- **Allergen Name**: Specific substance name causing allergy
- **Allergy Type**: Drug, food, environmental, other
- **Severity Level**: Mild, moderate, severe, anaphylaxis
- **Reaction Symptoms**: Specific allergic reaction manifestations

**Detailed Information (Extract or Ask):**
- **Discovery Time**: When allergy was first discovered
- **Discovery Circumstances**: Situation and context at the time
- **Confirmation Method**: Doctor diagnosis, self-observation, test confirmed
- **Current Status**: Still allergic or resolved

### Medical Standardization Conversion

| Colloquial Description | Medical Term | Type |
|------------------------|-------------|------|
| Penicillin | Penicillin | Drug allergy |
| Peanut | Peanut | Food allergy |
| Pollen | Pollen | Environmental allergy |
| Iodine contrast | Iodine contrast | Drug allergy |
| Hymenoptera venom | Hymenoptera venom | Other allergy |

### Allergy Type Classification

- **Drug Allergies**: Antibiotics (penicillin, cephalosporin, etc.), painkillers (aspirin, etc.), contrast agents, vaccines, TCM, etc.
- **Food Allergies**: Seafood (shrimp, crab, shellfish), nuts (peanut, walnut), eggs, dairy, gluten, fruits, etc.
- **Environmental Allergies**: Pollen, dust mites, animal dander, mold, latex, etc.
- **Other Allergies**: Insect bites, chemicals, metals, etc.

### Automatic Severity Determination

**Keyword Mapping:**
- "Shock", "Anaphylaxis", "Unconscious", "Coma" → Level 4 (anaphylaxis)
- "Severe", "Systemic", "Unbearable", "BP drop" → Level 3 (severe)
- "Obvious", "Moderate", "Needs treatment", "Swelling" → Level 2 (moderate)
- "Mild", "Occasional", "Local" → Level 1 (mild) |

### Reaction Symptom Recognition

**Skin symptoms:** Rash, hives, itching, redness, erythema
**Respiratory symptoms:** Dyspnea, wheezing, laryngeal edema, chest tightness
**Digestive symptoms:** Nausea, vomiting, diarrhea, abdominal pain
**Systemic symptoms:** Shock, blood pressure drop, syncope, loss of consciousness, systemic urticaria

## Step 3: Generate JSON

```json
{
  "allergies": [
    {
      "id": "allergy_20251231123456789",
      "allergen": {
        "name": "Penicillin",
        "type": "drug",
        "type_category": "Drug allergy",
        "synonyms": ["Penicillin", "盘尼西林"]
      },
      "severity": {
        "level": "severe",
        "level_code": 3,
        "description": "Severe allergic reaction"
      },
      "reactions": [
        {
          "reaction": "Rash",
          "onset_time": "Within 30 minutes of exposure",
          "severity": "moderate"
        }
      ],
      "discovery": {
        "date": "2010-05-15",
        "age_at_discovery": "8 years old",
        "circumstances": "Appeared after penicillin injection during pneumonia treatment"
      },
      "confirmation": {
        "method": "doctor_confirmed",
        "method_name": "Doctor diagnosis",
        "confirmed_by": "XX Hospital Pediatrics"
      },
      "current_status": {
        "status": "active",
        "status_name": "Active"
      },
      "management": {
        "avoidance_strategy": "Strictly avoid penicillin-class medications",
        "emergency_plan": "Seek immediate medical attention if accidentally used, carry allergy information",
        "medical_alert": true
      },
      "notes": "Must proactively inform medical staff during all medical visits"
    }
  ]
}
```

## Step 4: Save Data

File path: `data/allergies.json`

## Step 5: View Allergy Records (list)

**Filter Parameters:**
- No parameters: Display all allergies
- `active`: Display only active allergies
- `drug`: Display only drug allergies
- `food`: Display only food allergies
- `severe`: Display only severe and above allergies

## Step 6: Update/Delete Allergy Records

**Supported Fields:**
- `severity`: Severity level (mild/moderate/severe/anaphylaxis)
- `status`: Current status (active/resolved)
- `notes`: Notes

## Execution Instructions

```
1. Parse operation type (add/list/update/delete)
2. [add] Parse allergy info, medical standardization, generate JSON, save
3. [list] Read allergies.json, filter and display
4. [update] Find allergen, update fields, save
5. [delete] Confirm deletion, remove record
```

## Example Interactions

### Add Allergy Record
```
User: Penicillin severe allergy from childhood injection caused difficulty breathing
-> Save drug allergy record, severity level 3
```

### View All Allergies
```
User: View all allergies
-> Display all allergy records grouped by type
```

### View Severe Allergies
```
User: View severe allergies
-> Display only level 3 and above allergy records
```

### Update Status
```
User: Peanut status changed to resolved
-> Update current status to resolved
```

### Delete Record
```
User: Delete penicillin allergy
-> Confirm then delete record
```
