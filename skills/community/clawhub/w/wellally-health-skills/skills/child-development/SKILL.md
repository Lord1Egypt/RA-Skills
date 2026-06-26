---
name: child-development
description: Track and assess child developmental milestones based on ASQ-3 and Denver II standards. Use when user mentions development, milestones, motor skills, language, social skills, or cognitive development.
argument-hint: <operation_type: record/check/milestone/delay/history, e.g.: record gross, check 12 months, milestone all>
allowed-tools: Read, Write
schema: child-development/schema.json
---

# Child Developmental Milestone Tracking Skill

Child developmental milestone tracking and assessment based on ASQ-3 and Denver II standards, providing early warning for developmental delays.

## Core Flow

```
User Input → Parse Operation Type → Read Child Information → Calculate Age → Determine Assessment Items → Generate Assessment Report → Save Data
```

## Step 1: Parse User Input

### Operation Type Mapping

| Input | action | domain |
|------|--------|--------|
| record | record | all(default)/gross/fine/language/social/cognitive |
| check | check | - |
| milestone | milestone | Optional: specify domain |
| delay | delay | - |
| history | history | - |

### Developmental Domain Mapping

| Input Keywords | domain |
|----------------|--------|
| gross motor | gross |
| fine motor | fine |
| language | language |
| social | social |
| cognitive | cognitive |

## Step 2: Check Information Completeness

### Required (prompt to set if missing):
- Child name (from data/profile.json)
- Birth date (from data/profile.json)
- Gender (from data/profile.json)
- Prematurity status (from data/profile.json)

### Prompt when child profile missing:
```
Child profile not found

Please set child basic information first:
/profile child-name Xiaoming
/profile child-birth-date 2020-01-01
/profile child-gender male
```

## Step 3: Calculate Age and Months

```javascript
birthDate = profile.child_birth_date
today = new Date()

ageMonths = (today - birthDate) / (30.44 * 24 * 60 * 60 * 1000)

// Prematurity correction (<37 weeks, correct until 2 years)
if gestational_age < 37 && ageMonths <= 24:
  correctedAgeMonths = ageMonths - (40 - gestational_age) * 4
else:
  correctedAgeMonths = ageMonths
```

## Step 4: Generate Assessment Questions

### Determine Key Milestones by Age

**6-Month Assessment Example:**
```
Please assess whether milestones are achieved (yes/no):

Gross Motor (6 months)
  Can sit briefly without support
  Can support self on hands during tummy time
  Can roll from back to tummy

Fine Motor (6 months)
  Can reach for objects
  Can transfer items between hands
  Can pinch with thumb and finger

Language (6 months)
  Can make single syllable sounds (ma/ba etc.)
  Responds to sounds
  Can turn toward sound source

Social (6 months)
  Shows stranger anxiety
  Laughs out loud
  Can express happiness/anger

Cognitive (6 months)
  Looks for dropped objects
  Can distinguish familiar/stranger faces
```

## Step 5: Generate Assessment Report

### Developmental Assessment Grading

| Assessment Result | Condition |
|-------------------|-----------|
| Normal | All domains meet age standards |
| Possible delay | 1-2 months behind |
| Significant delay | 3+ months behind |

### Normal Assessment Report Example:
```
Developmental Assessment - Normal

Assessment Information:
Child: Xiaoming
Age: 6 months
Corrected age: 6 months
Assessment date: July 1, 2025

Gross Motor Development:
  Sitting alone: Achieved (at 5 months)
  Rolling over: Achieved (at 4 months)
  Tummy time support: Achieved
  Assessment: Normal

Fine Motor:
  Reaching for objects: Achieved
  Transferring between hands: Achieved
  Pincer grasp: Not achieved (normal, ~9 months)
  Assessment: Normal

Comprehensive Assessment:
  Normal development
  All developmental domains within normal range, no significant delays detected.

Recommendations:
  Continue observation and recording
  Provide rich environmental stimulation
  Interact and communicate with child frequently
  Regular developmental assessments
```

## Step 6: Save Data

Save to `data/child-development-tracker.json`, including:
- child_profile: Child basic information
- developmental_tracking.assessments: Assessment records
- milestone_achievement: Milestone achievement statistics
- alerts: Developmental warnings
- statistics: Statistical information

## Key Milestones by Age

### 0-3 Months (Early Infancy)
| Age | Gross Motor | Fine Motor | Language | Social |
|-----|-------------|------------|----------|--------|
| 1 month | Lift head briefly | Eyes follow | Cooing | Gaze at faces |
| 2 months | Lift head 45° during tummy time | Hands together | Laugh | Social smile |
| 3 months | Lift head 90° during tummy time | Grab rattle | Smile at face | Smile at face |

### 4-6 Months (Mid Infancy)
| Age | Gross Motor | Fine Motor | Language | Social |
|-----|-------------|------------|----------|--------|
| 4 months | Head steady, roll | Reach for objects | Squeal | Laugh aloud |
| 5 months | Sit with support | Pincer grasp | Turn to sound | Recognize strangers |
| 6 months | Sit briefly | Transfer objects | Single syllables | Stranger anxiety |

### Developmental Delay Standards

| Domain | Mild Delay | Significant Delay | Severe Delay |
|--------|------------|------------------|---------------|
| Gross motor | 1-2 months behind | 3-4 months behind | >4 months behind |
| Fine motor | 1-2 months behind | 3-4 months behind | >4 months behind |
| Language | 1-2 months behind | 3-4 months behind | >4 months behind |
| Social/Cognitive | 1-2 months behind | 3-4 months behind | >4 months behind |

## Execution Instructions

1. Read data/profile.json for child information
2. Calculate age and corrected age (if applicable)
3. Execute corresponding function based on operation type
4. Generate assessment report
5. Save to data/child-development-tracker.json

## Medical Safety Principles

### Safety Boundaries
- No developmental disability diagnosis
- No future developmental level prediction
- No substitute for professional developmental assessment
- No intervention training program recommendations

### System Can
- Developmental milestone tracking
- Developmental delay screening
- Early warning alerts
- Assessment history records

## Important Notice

This system is for developmental milestone recording and reference only, **cannot replace professional medical diagnosis**.

Development has individual variations; being 1-2 months behind may be normal variation.

If significant developmental delay is found or you have concerns about development, **please consult a child health specialist or developmental behavioral pediatrician promptly**.
