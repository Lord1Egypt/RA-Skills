# Child Nutrition Data Structure

## Data File
`data/child-nutrition-tracker.json`

## Main Structure

### dietary_records (Dietary Records)

| Field | Type | Description |
|------|------|-------------|
| date | string | Record date |
| age | string | Age representation |
| age_months | integer | Age in months |

### meals (Meals)

Includes breakfast, lunch, dinner, snacks

| Field | Type | Description |
|------|------|-------------|
| time | string | Meal time |
| foods | array | Food list |
| name | string | Food name |
| amount | string | Food amount |
| category | string | Food category |

### Food Categories (category)

| Value | Description |
|-------|-------------|
| grain | Grains and tubers |
| protein | Meat, eggs, fish, poultry |
| vegetable | Vegetables |
| fruit | Fruits |
| dairy | Milk and dairy products |
| nuts | Soybeans and nuts |
| other | Other |

### water_intake (Water Intake Record)

| Field | Type | Description |
|------|------|-------------|
| amount_ml | integer | Water intake (ml) |
| recommended_min | integer | Recommended minimum |
| recommended_max | integer | Recommended maximum |
| adequate | boolean | Whether adequate |

### nutrition_assessment (Nutrition Assessment)

| Field | Type | Possible Values |
|------|------|----------------|
| calories | string | adequate/insufficient/excessive |
| protein | string | adequate/insufficient |
| calcium | string | adequate/insufficient/supplement_recommended |
| iron | string | adequate/insufficient |
| vitamin_d | string | adequate/insufficient/supplement_recommended |
| overall | string | good/fair/poor |

### picky_eating (Picky Eating)

| Field | Type | Description |
|------|------|-------------|
| level | string | Picky level: none/mild/moderate/severe |
| refused_foods | array | List of refused foods |
| preferred_foods | array | List of preferred foods |
| strategies_tried | array | Improvement strategies tried |
| improvement_notes | string | Improvement notes |

### nutritional_assessment (Comprehensive Nutrition Assessment)

| Field | Possible Values | Description |
|------|-----------------|-------------|
| protein_status | adequate/insufficient | Protein status |
| calcium_status | adequate/insufficient | Calcium status |
| iron_status | adequate/insufficient | Iron status |
| zinc_status | adequate/insufficient | Zinc status |
| vitamin_d_status | adequate/insufficient/supplement_recommended | Vitamin D status |
| overall_status | good/fair/poor | Overall status |

## Age-Group Nutrition Recommendations

| Age | Energy | Protein | Calcium | Iron |
|-----|--------|---------|---------|------|
| 1-3 years | 1000-1400 | 25-30 | 600 | 9 |
| 4-6 years | 1400-1600 | 30-35 | 800 | 10 |
| 7-10 years | 1600-2000 | 35-40 | 1000 | 13 |
| 11-14 years | 2000-2500 | 50-60 | 1200 | 15-18(M)/12-15(F) |
