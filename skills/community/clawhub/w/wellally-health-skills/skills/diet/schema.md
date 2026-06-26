# DietRecord Schema

Complete data structure definition for diet and nutrition records.

## Field Quick Reference

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Record unique ID |
| `record_date` | string | Record date (YYYY-MM-DD) |
| `meal_time` | string | Meal time (HH:mm) |
| `meal_type` | enum | Meal type |
| `nutrition` | object | Nutritional content |

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `image_path` | string | Food image path |
| `foods` | array | List of identified foods |
| `health_score` | object | Health score |
| `suggestions` | string[] | Dietary recommendations |

## Enum Values

### meal_type
`Breakfast` | `Lunch` | `Afternoon Tea` | `Dinner` | `Late Night Snack`

## nutrition Object Structure

### calories
- `value`: Calorie value
- `unit`: "kcal"
- `breakdown`: Calorie source breakdown

### macronutrients
- `protein`: Protein { value, unit: "g" }
- `fat`: Fat { value, unit: "g" }
- `carbohydrate`: Carbohydrates { value, unit: "g" }
- `fiber`: Dietary Fiber { value, unit: "g" }

### vitamins
- `vitamin_a`: Vitamin A { value, unit: "μg" }
- `vitamin_b1`: Vitamin B1 { value, unit: "mg" }
- `vitamin_b2`: Vitamin B2 { value, unit: "mg" }
- `vitamin_b3`: Vitamin B3 { value, unit: "mg" }
- `vitamin_b6`: Vitamin B6 { value, unit: "mg" }
- `vitamin_b12`: Vitamin B12 { value, unit: "μg" }
- `vitamin_c`: Vitamin C { value, unit: "mg" }
- `vitamin_d`: Vitamin D { value, unit: "μg" }
- `vitamin_e`: Vitamin E { value, unit: "mg" }
- `vitamin_k`: Vitamin K { value, unit: "μg" }
- `folate`: Folate { value, unit: "μg" }

### minerals
- `calcium`: Calcium { value, unit: "mg" }
- `iron`: Iron { value, unit: "mg" }
- `zinc`: Zinc { value, unit: "mg" }
- `potassium`: Potassium { value, unit: "mg" }
- `sodium`: Sodium { value, unit: "mg" }
- `magnesium`: Magnesium { value, unit: "mg" }
- `phosphorus`: Phosphorus { value, unit: "mg" }

### other
- `cholesterol`: Cholesterol { value, unit: "mg" }
- `water`: Water { value, unit: "g" }

## health_score Object

| Field | Range | Description |
|-------|-------|-------------|
| `overall` | 0-10 | Overall score |
| `balance` | 0-10 | Balance |
| `variety` | 0-10 | Variety |
| `nutrition_density` | 0-10 | Nutrition density |

## Data Storage

- Location: `data/diet-records/YYYY-MM/YYYY-MM-DD_HHMM.json`
- Index: `data/index.json`
