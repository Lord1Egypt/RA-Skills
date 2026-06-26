# Allergy Skill Examples

## I. Add Allergy Record

### Example 1: Drug Allergy
```
User: Penicillin severe allergy from childhood injection caused difficulty breathing

Save:
{
  "allergen": {
    "name": "Penicillin",
    "type": "drug",
    "type_category": "Drug allergy"
  },
  "severity": {
    "level": "severe",
    "level_code": 3
  },
  "reactions": [
    {"reaction": "Difficulty breathing", "severity": "Severe"}
  ]
}
```

### Example 2: Food Allergy
```
User: Peanut moderate allergy lips swell after eating

Save:
{
  "allergen": {
    "name": "Peanut",
    "type": "food",
    "type_category": "Food allergy"
  },
  "severity": {
    "level": "moderate",
    "level_code": 2
  },
  "reactions": [
    {"reaction": "Lip swelling", "severity": "Moderate"}
  ]
}
```

### Example 3: Anaphylaxis
```
User: Bee sting anaphylactic shock whole body rash throat swelling

Save:
{
  "allergen": {
    "name": "Hymenoptera venom",
    "type": "other",
    "type_category": "Other allergy"
  },
  "severity": {
    "level": "anaphylaxis",
    "level_code": 4
  },
  "reactions": [
    {"reaction": "Systemic urticaria"},
    {"reaction": "Laryngeal edema"}
  ]
}
```

## II. View Allergy Records

### Example 4: View All Allergies
```
User: View all allergies

Output:
📋 Allergy History List
Total 5 allergy records (4 active)

Drug Allergies (2):
1. Penicillin 🔴 Severe
2. Iodine contrast 🟠 Severe
...
```

### Example 5: View Drug Allergies
```
User: View drug allergies

Output:
📋 Drug Allergy List
Total 2 drug allergy records
...
```

### Example 6: View Severe Allergies
```
User: View severe allergies

Output:
📋 Severe Allergy List
Total 3 severe allergy records
...
```

## III. Update Allergy Records

### Example 7: Update Severity Level
```
User: Penicillin severity changed to moderate

Update: severity.level = "moderate", level_code = 2
```

### Example 8: Mark as Resolved
```
User: Peanut status changed to resolved

Update: current_status.status = "resolved"
```

## IV. Delete Allergy Record

### Example 9: Delete Record
```
User: Delete penicillin allergy

Confirm then delete the allergy record
```
