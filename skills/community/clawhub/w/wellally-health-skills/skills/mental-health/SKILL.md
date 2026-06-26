---
name: mental-health
description: Mental health tracking - psychological assessments (PHQ-9, GAD-7), mood diary, therapy progress, and crisis management planning
argument-hint: <operation_type+info, e.g.: assess phq9, mood anxious 7, therapy session 24, crisis plan create>
allowed-tools: Read, Write
schema: mental-health/schema.json
---

# Mental Health Management Skill

Mental health assessment and tracking, including standardized scales, mood diary, therapy records, and crisis management.

## Core Flow

```
User Input -> Identify Operation Type -> Extract Parameter Info -> Check Completeness -> [Need Supplement] Ask User
                                                      |
                                                   [Information Complete]
                                                      |
                                              Generate JSON -> Save Data -> Output Confirmation
```

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation Type | Description |
|----------------|----------------|-------------|
| assess, assessment | psychological_assessment | Psychological assessment |
| phq9, phq-9 | phq9_assessment | PHQ-9 depression screening |
| gad7, gad-7 | gad7_assessment | GAD-7 anxiety screening |
| psqi | psqi_assessment | PSQI sleep quality assessment |
| gds | gds_assessment | GDS geriatric depression screening |
| epds | epds_assessment | EPDS postpartum depression screening |
| mood | mood_diary | Mood diary |
| trigger | mood_trigger | Trigger factors |
| coping | coping_strategy | Coping strategies |
| diary | mood_diary_view | View mood diary |
| pattern | pattern_analysis | Mood pattern analysis |
| therapy | therapy_record | Therapy record |
| crisis | crisis_management | Crisis management |
| progress | therapy_progress | Therapy progress |
| goals | therapy_goals | Therapy goals |

### Mood Type Keywords

| Input Keywords | Mood Value |
|----------------|------------|
| happy | happy |
| calm | calm |
| anxious | anxious |
| sad | sad |
| angry | angry |
| tired | tired |
| frustrated | frustrated |
| excited | excited |
| depressed | depressed |
| irritable | irritable |
| nervous | nervous |

### Mood Intensity
- Numbers 1-10

### Trigger Factor Keywords

| Input Keywords | Trigger Factor |
|----------------|----------------|
| work | work_deadline, work_pressure |
| sleep | lack_of_sleep |
| pain | chronic_pain |
| relationship | relationship_issue |
| family | family_conflict |
| money, financial | financial_stress |
| crowd | crowd |
| weather | weather |

### Coping Strategy Keywords

| Input Keywords | Coping Strategy |
|----------------|-----------------|
| deep_breathing | deep_breathing |
| meditation | meditation |
| exercise | exercise |
| walk | walk |
| journaling | journaling |
| socializing | socializing |
| music | music |
| reading | reading |

### Effectiveness Keywords

| Input Keywords | Effect |
|----------------|--------|
| very_helpful | very_helpful |
| helpful | helpful |
| somewhat_helpful | somewhat_helpful |
| not_helpful | not_helpful |

### Therapy Type Keywords

| Input Keywords | Therapy Type |
|----------------|--------------|
| cbt | CBT |
| psychodynamic | psychodynamic |
| humanistic | humanistic |
| family | family |
| group | group |
| dbt | DBT |
| emdr | EMDR |

### Crisis Warning Signs

| Input Keywords | Signal |
|----------------|--------|
| hopelessness | hopelessness |
| withdrawal | social_withdrawal |
| mood_swings | extreme_mood_swings |
| death | talk_of_death |
| self_harm | self_harm |
| suicidal | suicidal_thoughts |

### Risk Level

| Input Keywords | Risk |
|----------------|------|
| low | low |
| medium | medium |
| high | high |

## Step 2: Check Information Completeness

### Mood Diary Required:
- Mood type
- Mood intensity (1-10)

### Psychological Assessment Required:
- Assessment type
- Total score

### Therapy Record Required:
- Session number
- Session date

### Crisis Plan Required:
- Plan type (create/update/view)

## Step 3: Interactive Prompts (If Needed)

### Scenario A: Missing Mood Intensity
```
How intense is this mood?
Rate on a scale of 1-10 (1 being mildest, 10 being most intense)
```

### Scenario B: PHQ-9 Assessment
```
Please answer the following questions (In the past 2 weeks, how often have you been bothered by the following problems?)

1. Little interest or pleasure in doing things
2. Feeling down, depressed, or hopeless
3. Trouble falling or staying asleep, or sleeping too much
4. Feeling tired or having little energy
5. Poor appetite or overeating
6. Feeling bad about yourself - or that you are a failure
7. Trouble concentrating on things
8. Moving or speaking slowly, or being fidgety/restless
9. Thoughts that you would be better off dead or of hurting yourself

Each question scoring: 0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day
```

### Scenario C: Crisis Risk Assessment
```
If you have any of the following, please seek professional help immediately:

1. Having thoughts or plans of self-harm or suicide
   - Call psychological crisis hotline: 400-xxx-xxxx
   - Go to the nearest psychiatric emergency
   - Call emergency number: 120

2. Hallucinations, delusions
3. Completely out of control emotions
4. Severely impaired functioning

What is your current situation?
```

## Step 4: Generate JSON

### Mood Diary
```json
{
  "id": "mood_20250620083000001",
  "date": "2025-06-20",
  "time": "08:30",
  "mood": "anxious",
  "intensity": 7,
  "triggers": ["work_deadline"],
  "coping_strategies": ["deep_breathing"],
  "effectiveness": "somewhat_helpful",
  "notes": "Work pressure causing anxiety"
}
```

### PHQ-9 Assessment
```json
{
  "assessment_date": "2025-06-20",
  "scale": "phq9",
  "total_score": 8,
  "max_score": 27,
  "severity": "Mild depression",
  "items": [0, 1, 1, 2, 1, 0, 1, 1, 1],
  "recommendation": "Observe for two weeks, seek medical help if no improvement"
}
```

### GAD-7 Assessment
```json
{
  "assessment_date": "2025-06-20",
  "scale": "gad7",
  "total_score": 12,
  "max_score": 21,
  "severity": "Moderate anxiety",
  "items": [2, 2, 2, 1, 2, 2, 1],
  "recommendation": "Recommend medical consultation, consider psychotherapy"
}
```

### Therapy Record
```json
{
  "session_number": 24,
  "date": "2025-06-20",
  "duration_minutes": 50,
  "therapy_type": "CBT",
  "topics_discussed": ["anxiety", "work_stress"],
  "mood_before": "anxious",
  "mood_after": "calmer",
  "homework_assigned": "thought_record"
}
```

### Crisis Plan
```json
{
  "created_date": "2025-06-20",
  "warning_signs": ["hopelessness", "social_withdrawal"],
  "emergency_contacts": [
    {"type": "spouse", "phone": "***-****-1234", "availability": "24/7"}
  ],
  "coping_strategies": ["deep_breathing", "grounding_technique"],
  "current_risk_level": "low"
}
```

Complete schema definition: see [schema.json](schema.json).

## Step 5: Save Data

1. Read `data/mental-health-tracker.json`
2. Update corresponding sections based on operation type
3. Update statistics
4. Write back to file

## Execution Instructions

```
1. Identify operation type
2. Extract parameter information
3. Check required field completeness
4. If missing, ask user to supplement
5. Generate JSON compliant with schema.json
6. Save to data/mental-health-tracker.json
7. Output confirmation and recommendations
```

## Example Interactions

### Example 1: Record Mood
```
User: mood anxious 7 work stress

AI: Mood diary recorded
Time: 2025-06-20 08:30
Mood: Anxious
Intensity: 7/10 (High intensity)
Triggers: Work stress

Recommendation: Try deep breathing or meditation to relieve anxiety
```

### Example 2: PHQ-9 Assessment
```
User: assess phq9 score 8

AI: PHQ-9 assessment result recorded
Total score: 8/27
Severity: Mild depression

Assessment: Mild depressive symptoms
Recommendations:
- Increase exercise
- Improve sleep
- Reduce stress
- Observe for two weeks, seek medical help if no improvement

Note: If item 9 (self-harm thoughts) score >= 1, recommend medical consultation
```

### Example 3: Therapy Record
```
User: therapy session 24 cbt anxiety work_stress

AI: Therapy session recorded
Session number: 24
Therapy type: Cognitive Behavioral Therapy (CBT)
Topics discussed: Anxiety, Work stress

Next therapy reminder: Please record this week's thought diary
```

### Example 4: Crisis Plan
```
User: crisis plan create

AI: Let's build your crisis intervention plan together

1. Warning Sign Identification
   What signals indicate you might need help?
   - Feelings of hopelessness
   - Social withdrawal
   - Extreme mood swings

2. Emergency Contacts
   Please add reachable family or friends or therapist

3. Coping Strategies
   What methods help when warning signs appear?

4. Professional Resources
   - Psychological crisis hotline: 400-xxx-xxxx (24 hours)
   - Psychiatric emergency: Nearest Grade-A tertiary hospital
   - Emergency number: 120

Crisis plan created. You can update with:
- /crisis sign add [warning sign]
- /crisis contact add [contact] [phone]
- /crisis strategy add [coping strategy]
```

For more examples, see [examples.md](examples.md).

## Medical Safety Boundaries

### Cannot Do:
- Make psychological diagnoses (mental illness diagnosis must be done by a psychiatrist)
- Prescribe psychiatric medications
- Predict suicide risk or self-harm behavior
- Replace professional psychotherapy
- Handle acute psychiatric crises
- Provide specific psychotherapy plans

### Can Do:
- Mental health screening and assessment (using standardized scales)
- Mood pattern identification and trend tracking
- Crisis warning sign reminders
- Coping strategy recommendations (non-therapeutic)
- Therapy progress recording and tracking
- Emergency resource information provision

### Emergency Situation Handling:
If any of the following, seek professional help immediately:
1. Thoughts or plans of self-harm or suicide
2. Hallucinations, delusions
3. Completely out of control emotions
4. Severely impaired functioning

Emergency resources:
- National psychological crisis hotline: 400-xxx-xxxx (24 hours)
- Psychiatric emergency: Nearest Grade-A tertiary hospital psychiatry department
- Emergency number: 120
