---
name: diet
description: Record and track daily nutrition intake through food photos. Analyze nutritional content including calories, protein, fat, carbohydrates, vitamins, and minerals. Use when user wants to log meals, track nutrition, or analyze dietary habits.
argument-hint: <operation_type image_path_or_meal_time, e.g.: add lunch.jpg 12:30>
allowed-tools: Read, Write
schema: diet/schema.json
---

# Diet and Nutrition Tracking Skill

Record daily meals through photos or uploads, automatically analyze nutritional content, and track nutritional intake.

## Core Flow

```
User Input → Identify Operation Type → [add] Analyze Image → Nutrition Analysis → Save Record
                              ↓
                         [history/status/summary] → Read Data → Display Report
```

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation Type |
|----------------|----------------|
| add | add - Add diet record |
| history | history - View history records |
| status | status - Nutrition statistics |
| summary | summary - Nutrition summary |

### Meal Classification (Based on Meal Time)

| Time Range | Meal Type |
|------------|-----------|
| 05:00 - 09:59 | Breakfast |
| 10:00 - 14:59 | Lunch |
| 15:00 - 16:59 | Afternoon Tea |
| 17:00 - 21:59 | Dinner |
| 22:00 - 04:59 | Late Night Snack |

## Step 2: Check Information Completeness

### For add operation, required:
- `image` - Food photo path

### For add operation, optional:
- `meal_time` - Meal time (defaults to current time)

### For history/status/summary operations:
- No parameters required, optional time range

## Step 3: Interactive Prompts (If Needed)

### Scenario A: No Image Provided
```
Please provide a food photo. You can drag and drop or specify the path.
```

### Scenario B: Invalid Image Path
```
Cannot read the image. Please check if the path is correct.
Supported formats: JPG, PNG, WebP
```

### Scenario C: Invalid Time Format
```
Invalid time format. Please use HH:mm or YYYY-MM-DD HH:mm format
Example: 12:30 or 2025-12-30 12:30
```

## Step 4: Generate JSON

### Diet Record Data Structure

```json
{
  "id": "20251231123456789",
  "record_date": "2025-12-31",
  "meal_time": "12:30",
  "meal_type": "Lunch",
  "image_path": "food.jpg",
  "foods": [
    {
      "name": "Rice",
      "portion": "1 bowl (about 150g)",
      "weight_estimate": 150,
      "cooking_method": "Steamed",
      "confidence": 0.95
    }
  ],
  "nutrition": {
    "calories": {
      "value": 485,
      "unit": "kcal"
    },
    "macronutrients": {
      "protein": { "value": 15.2, "unit": "g" },
      "fat": { "value": 18.5, "unit": "g" },
      "carbohydrate": { "value": 60.3, "unit": "g" },
      "fiber": { "value": 6.2, "unit": "g" }
    },
    "vitamins": {
      "vitamin_a": { "value": 245, "unit": "μg" },
      "vitamin_c": { "value": 35, "unit": "mg" }
    },
    "minerals": {
      "calcium": { "value": 45, "unit": "mg" },
      "iron": { "value": 2.8, "unit": "mg" }
    }
  },
  "health_score": {
    "overall": 7.5,
    "balance": 8.0,
    "variety": 7.0,
    "nutrition_density": 7.5
  }
}
```

## Step 5: Save Data

1. Generate file path: `data/diet-records/YYYY-MM/YYYY-MM-DD_HHMM.json`
2. Create month directory (if not exists)
3. Save JSON data file
4. Update global index `data/index.json`

## Execution Instructions

```
1. Parse user input, identify operation type
2. For add operation:
   a. Use Read tool to read image
   b. Analyze food types and portions
   c. Calculate nutritional content
   d. Save record to data/diet-records/
3. For history operation: Display diet history
4. For status operation: Display nutrition statistics
5. For summary operation: Display nutrition summary
```

## Nutrition Reference

### Common Staple Food Portions
- 1 bowl rice ≈ 150g (180 kcal)
- 1 bowl noodles ≈ 200g (220 kcal)
- 1 steamed bun ≈ 100g (220 kcal)

### Meat Portions
- Pork 100g ≈ 250 kcal
- Chicken 100g ≈ 130 kcal
- Fish 100g ≈ 100 kcal

### Vegetable Portions
- Leafy vegetables 1 serving ≈ 200g (40 kcal)
- Root vegetables 1 serving ≈ 200g (80 kcal)

## Adult Daily Nutrition Recommendations

### Macronutrients
- Calories: 1800-2400 kcal
- Protein: 55-75 g
- Fat: 55-75 g
- Carbohydrates: 250-350 g
- Dietary Fiber: 25-35 g

### Major Vitamins
- Vitamin A: 700-900 μg
- Vitamin C: 100 mg
- Vitamin D: 10-20 μg

### Major Minerals
- Calcium: 800-1000 mg
- Iron: 12-18 mg
- Zinc: 10-15 mg

For more examples, see [examples.md](examples.md).
