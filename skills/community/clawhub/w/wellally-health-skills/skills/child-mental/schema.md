# Child Mental Health Data Structure

## Data File
`data/child-mental-tracker.json`

## Main Structure

### assessments (Assessment Records)

| Field | Type | Description |
|------|------|-------------|
| date | string | Assessment date |
| age | string | Age representation |
| age_months | integer | Age in months |

### mood_assessment (Mood Assessment)

| Field | Type | Description |
|------|------|-------------|
| overall_mood | string | Overall mood: stable/fluctuating/unstable |
| mood_rating | integer | Mood rating 1-10 |
| mood_range | string | Rating range |
| emotional_expression | string | Emotional expression: appropriate/over/limited |
| emotional_regulation | string | Emotional regulation: good/fair/poor |
| dominant_mood | string | Dominant mood: happy/calm/sad/angry/excited |

### behavior_assessment (Behavior Assessment)

| Field | Type | Description |
|------|------|-------------|
| overall_behavior | string | Overall behavior: normal/attention_needed/concerning |
| activity_level | string | Activity level: low/appropriate/high |
| attention_span | string | Attention: age_appropriate/short/very_short |
| compliance | string | Compliance: good/fair/poor |
| aggression | string | Aggressive behavior: none/occasional/frequent |
| oppositional | string | Oppositional behavior: none/occasional/frequent |

### anxiety_screening (Anxiety Screening)

| Field | Type | Description |
|------|------|-------------|
| separation_anxiety | string | Separation anxiety: none/mild/moderate/severe |
| social_anxiety | string | Social anxiety: none/mild/moderate/severe |
| generalized_anxiety | string | Generalized anxiety: none/mild/moderate/severe |
| specific_phobias | string | Specific phobias: none/mild/moderate/severe |
| overall_anxiety | string | Overall anxiety: low_risk/moderate_risk/high_risk |

### attention_screening (Attention Screening)

| Field | Type | Description |
|------|------|-------------|
| inattention_score | integer | Inattention score (0-27) |
| hyperactivity_score | integer | Hyperactivity-impulsivity score (0-27) |
| total_score | integer | Total score (0-54) |
| interpretation | string | Interpretation: below_clinical_range/possible/likely |
| recommendation | string | Recommendation: monitoring/professional_eval |

### overall_assessment (Overall Assessment)

| Value | Description |
|-------|-------------|
| normal | Normal |
| attention_needed | Needs attention |
| professional_eval_recommended | Professional evaluation recommended |

### mood_tracking (Mood Tracking)

| Field | Type | Description |
|------|------|-------------|
| date | string | Date |
| time | string | Time |
| mood | string | Mood: happy/calm/sad/angry/excited/anxious |
| mood_rating | integer | Rating 1-10 |
| context | string | Background/context |
| notes | string | Notes |
