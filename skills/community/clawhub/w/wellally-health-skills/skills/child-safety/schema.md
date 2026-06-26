# Child Safety Data Structure

## Data File
`data/child-safety-tracker.json`

## Main Structure

### safety_assessments (Safety Assessments)

| Field | Type | Description |
|------|------|-------------|
| date | string | Assessment date |
| age | string | Age representation |
| age_months | integer | Age in months |
| area | string | Assessment area: home/car/water/food/outdoor |
| area_name | string | Area name |

### checklist (Checklist)

| Field | Type | Description |
|------|------|-------------|
| window_protection | boolean | Window protection |
| outlet_covers | boolean | Outlet covers |
| corner_guards | boolean | Corner guards |
| chemical_storage | boolean | Chemical storage |
| bathroom_safety | boolean | Bathroom safety |
| stair_gates | boolean? | Stair gates (nullable) |
| car_seat | boolean? | Car seat (nullable) |
| water_supervision | boolean? | Water supervision (nullable) |

### score (Score)

| Field | Type | Description |
|------|------|-------------|
| total_items | integer | Total checklist items |
| safe_items | integer | Safe items |
| percentage | integer | Safety percentage |
| level | string | Safety level |

### Safety Levels (level)

| Value | Description |
|-------|-------------|
| excellent | Excellent (>=90 points) |
| good | Good (70-89 points) |
| needs_attention | Needs attention (50-69 points) |
| high_risk | High risk (<50 points) |

### risks_identified (Identified Risks)

| Field | Type | Description |
|------|------|-------------|
| item | string | Risk item |
| risk_level | string | Risk level: low/medium/high/critical |
| description | string | Description |

### emergency_contacts (Emergency Contacts)

| Field | Type | Description |
|------|------|-------------|
| name | string | Name |
| phone | string | Phone |
| relationship | string | Relationship: father/mother/hospital, etc. |

### statistics (Statistics)

| Field | Type | Description |
|------|------|-------------|
| total_assessments | integer | Total assessments |
| last_assessment_date | string | Last assessment date |
| average_score | integer | Average score |
| areas_assessed | array | Areas assessed |

## Area-Specific Checklist Items

### home (Home Safety)
- window_protection
- outlet_covers
- corner_guards
- chemical_storage
- bathroom_safety
- stair_gates

### car (Car Safety)
- car_seat
- car_seat_installation
- back_seat_only
- window_locks

### water (Water Safety)
- water_supervision
- pool_fence
- bath_water_level
- life_jacket

### food (Food/Eating Safety)
- food_cutting
- no_choking_hazards
- supervised_eating
- allergy_awareness
