---
name: postpartum
description: Track postpartum recovery, newborn care, EPDS screening, and maternal health monitoring
argument-hint: <operation_type+description, e.g.: start 2025-10-08 vaginal, lochia rubra moderate, epds 8>
allowed-tools: Read, Write
schema: postpartum/schema.json
---

# Postpartum Care Management Skill

Comprehensive postpartum recovery tracking and newborn care management, from delivery to postpartum recovery period, providing professional postpartum health monitoring and guidance.

## Core Flow

```
User Input → Parse Operation Type → Execute Operation → Generate/Update Data → Save → Output Result
```

## Supported Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| start | Start postpartum record | /postpartum start 2025-10-08 vaginal |
| lochia | Log lochia | /postpartum lochia rubra moderate |
| pain | Log pain | /postpartum pain uterine 6 |
| breastfeeding | Breastfeeding record | /postpartum breastfeeding exclusive |
| epds | EPDS mental screening | /postpartum epds 8 |
| mood | Log mood | /postpartum mood anxious |
| weight | Log weight | /postpartum weight 65.0 |
| pelvic-floor | Pelvic floor record | /postpartum pelvic-floor kegel-exercises 20 |
| baby | Baby record | /postpartum baby A feeding breastfeeding left 15min |
| status | View status | /postpartum status |
| recovery-summary | Recovery summary | /postpartum recovery-summary |
| extend | Extend tracking | /postpartum extend 1year |

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation |
|----------------|-----------|
| start | start |
| lochia | lochia |
| pain | pain |
| breastfeeding | breastfeeding |
| EPDS, epds | epds |
| mood | mood |
| weight | weight |
| pelvic-floor | pelvic-floor |
| baby | baby |
| status | status |
| recovery-summary | recovery-summary |
| extend | extend |

### Delivery Mode Recognition

| Keywords | Type |
|----------|------|
| vaginal | vaginal |
| c-section, cesarean | c-section |

### Postpartum Stage Calculation

```javascript
days_postpartum = today - delivery_date

if (days_postpartum <= 2) {
  stage = "immediate" // Acute phase (0-2 days)
} else if (days_postpartum <= 14) {
  stage = "early" // Early phase (3-14 days)
} else if (days_postpartum <= 42) {
  stage = "subacute" // Subacute phase (15-42 days)
} else {
  stage = "late" // Recovery phase (43 days+)
}
```

### Lochia Stage Recognition

| Keywords | Stage | Time | Color |
|----------|-------|------|-------|
| rubra | rubra | 0-3 days | Bright red |
| serosa | serosa | 4-9 days | Pink/brown |
| alba | alba | 10+ days | Yellow-white |

### Pain Location Recognition

| Keywords | Location |
|----------|----------|
| uterine | uterine |
| incision | incision |
| breast | breast |
| head | head |
| back | back |

### Pain Severity Recognition

| Keywords | Level |
|----------|-------|
| mild | Mild |
| moderate | Moderate |
| severe | Severe |

### Breastfeeding Mode Recognition

| Keywords | Type |
|----------|------|
| exclusive | exclusive |
| mixed | mixed |
| formula | formula |

### Breastfeeding Issues Recognition

| Keywords | Issue |
|----------|-------|
| engorgement | engorgement |
| mastitis | mastitis |
| low-supply | low-supply |
| cracked-nipples | cracked-nipples |

### Mood Recognition

| Keywords | Mood |
|----------|------|
| happy | happy |
| anxious | anxious |
| sad | sad |
| irritable | irritable |
| overwhelmed | overwhelmed |

## Step 2: Check Information Completeness

### start Operation Required:
- delivery_date: Delivery date
- delivery_type: Delivery mode

### start Operation Recommended:
- baby_count: Number of babies (default 1)
- tracking_period: Tracking period (default 6months)

### epds Operation Required:
- score: EPDS total score (0-30)

### baby Operation Required:
- baby_id: Baby identifier (A/B/C/D)
- info_type: Information type (feeding/sleep/weight/diaper)

## Step 3: Interactive Prompts (If Needed)

### Scenario A: Missing Delivery Date
```
Please provide delivery date:
(Format: YYYY-MM-DD)
```

### Scenario B: Missing Delivery Mode
```
Delivery mode?
• Vaginal birth (vaginal)
• C-section (c-section)
```

### Scenario C: Missing Baby Count
```
Number of babies?
(Enter 1 for single or leave blank, 2 for twins)
```

### Scenario D: EPDS Question 10 Positive
```
EMERGENCY WARNING

Question 10 score: 2-3 points
(Thoughts of self-harm)

IMMEDIATE ACTION REQUIRED:
Step 1: Tell someone close to you immediately
Step 2: Seek professional help immediately
Step 3: Ensure baby's safety

24-hour Help Lines:
• National Mental Health Hotline: 400-161-9995
• Life Line: 400-821-1215
```

## Step 4: Generate JSON

### Postpartum Record Data Structure

```json
{
  "postpartum_id": "postpartum_20251008",
  "delivery_date": "2025-10-08",
  "delivery_type": "vaginal",
  "baby_count": 1,
  "tracking_period": "6months",
  "tracking_end_date": "2026-04-06",

  "current_status": {
    "days_postpartum": 0,
    "stage": "immediate",
    "progress_percentage": 0
  },

  "recovery_tracking": {
    "lochia": {
      "stage": "rubra",
      "amount": "moderate",
      "last_updated": null
    },
    "perineal_care": {
      "healing": "good",
      "pain_level": 3,
      "incision_type": null,
      "notes": ""
    },
    "breastfeeding": {
      "status": "establishing",
      "challenges": [],
      "last_updated": null
    },
    "pain": {
      "uterine_contractions": {
        "present": true,
        "severity": "moderate"
      }
    }
  },

  "mental_health": {
    "epds": {
      "last_screened": null,
      "total_score": null,
      "risk_level": "not_screened",
      "q10_positive": false,
      "last_updated": null
    },
    "mood_log": []
  },

  "physical_recovery": {
    "pelvic_floor": {
      "status": "recovering",
      "exercises": "not_started",
      "notes": ""
    },
    "diastasis_recti": {
      "present": null,
      "severity": null,
      "assessed": false
    },
    "weight_tracking": [],
    "sleep_tracking": []
  },

  "babies": [
    {
      "baby_id": "A",
      "name": null,
      "gender": null,
      "birth_weight": null,
      "current_weight": null,
      "feeding": {
        "method": "establishing",
        "pattern": "on_demand",
        "last_feed": null,
        "feeds_log": []
      },
      "sleep": {
        "pattern": "newborn",
        "last_sleep": null,
        "sleep_log": []
      },
      "diapers": {
        "count": 0,
        "last_change": null,
        "diaper_log": []
      },
      "notes": ""
    }
  ],

  "red_flags": {
    "active": [],
    "resolved": [],
    "last_assessment": null
  },

  "metadata": {
    "created_at": "2025-10-08T00:00:00.000Z",
    "last_updated": "2025-10-08T00:00:00.000Z"
  }
}
```

Complete schema definition: see [schema.json](schema.json).

## Step 5: Save Data

1. Read `data/postpartum-tracker.json`
2. Update corresponding data
3. Write back to file
4. If detailed records exist, save to `data/postpartum-records/YYYY-MM/YYYY-MM-DD_postpartum-record.json`

## Execution Instructions

```
1. Parse user input and determine operation type
2. Execute corresponding logic based on operation type
3. Validate input data and state
4. Generate JSON compliant with schema.json
5. Save to data/postpartum-tracker.json
6. Output operation result and summary to user
```

## Example Interactions

### Example 1: Start Postpartum Record
```
User: /postpartum start 2025-10-08 vaginal

System:
Postpartum record created

Delivery Information:
Delivery date: October 8, 2025
Delivery mode: Vaginal birth
Baby count: 1
Current postpartum day: 0

Tracking Settings:
Tracking period: 6 months
Tracking end: April 6, 2026

Postpartum stage: Acute phase (0-2 days)

RED FLAGS (seek immediate medical care if present):
• Postpartum hemorrhage (>1 pad/hour)
• Fever > 100.4°F (38°C)
• Severe headache
• Blurred vision
• Difficulty breathing
• Chest pain

Data saved to: data/postpartum-records/2025-10/2025-10-08_postpartum-record.json
```

### Example 2: EPDS Screening
```
User: /postpartum epds 8

System:
EPDS mental health screening completed

EPDS Results:
Screening date: November 15, 2025
Postpartum days: 35
EPDS total score: 8

Risk Assessment: Low risk

Recommendations:
• Maintain positive mindset
• Adequate rest and sleep
• Communicate with family and friends
• Moderate exercise (such as walking)

Next screening:
3 months postpartum (around January 2026)

Rescreen anytime if:
• Persistent low mood
• Unable to care for baby
• Thoughts of hopelessness or self-harm
```

### Example 3: Baby Feeding Record
```
User: /postpartum baby A feeding breastfeeding left 15min

System:
Baby feeding recorded

Baby A Feeding Information:
Time: October 15, 2025 14:30
Method: Breastfeeding (left side)
Duration: 15 minutes

Today's feeding count: 8 times
Feeding pattern: On demand

Assessment:
Feeding frequency normal (newborn 8-12 times/24 hours)
```

For more examples, see [examples.md](examples.md).
