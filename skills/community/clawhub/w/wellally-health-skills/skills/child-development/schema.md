# Child Development Tracking Data Structure

## Data File
`data/child-development-tracker.json`

## Main Structure

### child_profile (Child Basic Information)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| child_id | string | Yes | Child unique identifier, format: child_20200101 |
| name | string | Yes | Child name |
| birth_date | string | Yes | Birth date, format YYYY-MM-DD |
| gender | string | Yes | Gender: male/female |
| premature | boolean | No | Premature birth (<37 weeks) |
| gestational_age | integer | No | Gestational age, required for premature babies |

### assessments (Assessment Records)

| Field | Type | Description |
|------|------|-------------|
| date | string | Assessment date, format YYYY-MM-DD |
| age | string | Age representation, e.g., 6m, 2y5m |
| age_months | integer | Age in months |
| corrected_age | integer | Corrected age (for premature babies) |

### domain_assessment (Domain Assessment)

Each developmental domain (gross_motor, fine_motor, language, social, cognitive) contains:

| Field | Type | Description |
|------|------|-------------|
| achieved | boolean | Whether achieved |
| age_achieved | integer | Age achieved in months (if achieved) |
| status | string | Assessment status: normal/delay_suspected/delay_confirmed |

### milestone_achievement (Milestone Statistics)

| Field | Type | Description |
|------|------|-------------|
| total_milestones | integer | Total milestones in this domain |
| achieved | integer | Number achieved |
| percentage | integer | Completion percentage |

## Developmental Domains

- **gross_motor**: Gross motor skills (head control, rolling, sitting, crawling, walking, etc.)
- **fine_motor**: Fine motor skills (grasping, pinching, using tools, etc.)
- **language**: Language (babbling, words, sentences, etc.)
- **social**: Social (smiling, stranger anxiety, interaction, etc.)
- **cognitive**: Cognitive (object permanence, problem-solving, etc.)

## Developmental Delay Criteria

| Assessment Result | Condition |
|-------------------|-----------|
| normal | All milestones achieved within normal age range |
| delay_suspected | Behind by 1-2 months |
| delay_confirmed | Behind by 3+ months |
