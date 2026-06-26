# Diet Skill Examples

## 1. Add Diet Record

### Example 1: Quick Record (Using Current Time)
```
User: /diet add lunch.jpg

Save:
{
  "id": "20251231123456789",
  "record_date": "2025-12-31",
  "meal_time": "12:34",
  "meal_type": "Lunch",
  "image_path": "lunch.jpg",
  "foods": [
    {
      "name": "Rice",
      "portion": "1 bowl (about 150g)",
      "weight_estimate": 150,
      "cooking_method": "Steamed",
      "confidence": 0.95
    },
    {
      "name": "Stir-fried Vegetables",
      "portion": "1 serving (about 200g)",
      "weight_estimate": 200,
      "cooking_method": "Stir-fried",
      "confidence": 0.88
    }
  ],
  "nutrition": {
    "calories": { "value": 485, "unit": "kcal" },
    "macronutrients": {
      "protein": { "value": 15.2, "unit": "g" },
      "fat": { "value": 18.5, "unit": "g" },
      "carbohydrate": { "value": 60.3, "unit": "g" },
      "fiber": { "value": 6.2, "unit": "g" }
    }
  }
}
```

### Example 2: Record Breakfast (Specified Time)
```
User: /diet add breakfast.jpg 08:00

Save:
{
  "record_date": "2025-12-31",
  "meal_time": "08:00",
  "meal_type": "Breakfast",
  ...
}
```

### Example 3: Record Yesterday's Dinner
```
User: /diet add dinner.jpg 2025-12-30 18:30

Save:
{
  "record_date": "2025-12-30",
  "meal_time": "18:30",
  "meal_type": "Dinner",
  ...
}
```

## 2. View History Records

### Example 4: View Today's History
```
User: /diet history today

Output:
📋 Today's Diet Records

December 31, 2025
━━━━━━━━━━━━━━━━━━━━━━━━━━

🌅 Breakfast (08:30)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Foods: Milk, Whole wheat bread, Eggs
Calories: 420 kcal | Protein: 18g | Fat: 15g

🌞 Lunch (12:30)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Foods: Rice, Stir-fried vegetables, Braised pork
Calories: 785 kcal | Protein: 22g | Fat: 35g

🌙 Dinner (18:45)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Foods: Multigrain rice, Steamed fish, Garlic broccoli
Calories: 520 kcal | Protein: 28g | Fat: 12g

Today's Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Calories: 1725 kcal
Protein: 68g (15.8%)
Fat: 62g (32.3%)
Carbohydrates: 195g (45.2%)
Dietary Fiber: 18g
```

### Example 5: View Weekly History
```
User: /diet history week

Output:
Weekly Diet Records (December 25 - December 31)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total records: 21 meals
Average calories: 1850 kcal/day
...
```

## 3. Nutrition Statistics

### Example 6: View Nutrition Statistics
```
User: /diet status

Output:
📊 Nutrition Intake Statistics

Statistics Period: Today
━━━━━━━━━━━━━━━━━━━━━━━━━━

Calorie Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Today's Intake: 1725 kcal
Basal Metabolism: 1450 kcal
Recommended Intake: 2000 kcal
Completion: 86.3% ✅

Macronutrients:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Protein: 68g / 60g  (113.3%) ✅
Fat: 62g / 65g  (95.4%) ✅
Carbohydrates: 195g / 250g (78%) ⚠️
Dietary Fiber: 18g / 25g (72%) ⚠️
```

### Example 7: View Weekly Statistics
```
User: /diet stats week

Output:
Weekly Nutrition Statistics (7 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average calories: 1850 kcal/day
Protein achievement rate: 92%
Fruit and vegetable intake: Low
...
```

## 4. Nutrition Summary

### Example 8: Today's Nutrition Summary
```
User: /diet summary today

Output:
📈 Today's Nutrition Summary Report

Nutrition Achievement:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Calories: 86%
✅ Protein: 113%
✅ Fat: 95%
⚠️ Carbohydrates: 78%
⚠️ Dietary Fiber: 72%

Nutrition Gaps:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Need to increase:
• Dark leafy greens (carrots, spinach) - Supplement Vitamin A
• Whole grains (oats, brown rice) - Increase dietary fiber
• Nuts (walnuts, almonds) - Supplement Vitamin E and Zinc
```

## 5. Food Recognition Examples

### Staple Food Recognition
| Input | Recognition Result |
|-------|-------------------|
| Rice photo | name: "Rice", portion: "1 bowl (about 150g)", calories: 180 |
| Noodles photo | name: "Noodles", portion: "1 bowl (about 200g)", calories: 220 |

### Meat Recognition
| Input | Recognition Result |
|-------|-------------------|
| Braised pork | name: "Pork braised", portion: "100g", calories: 250 |
| Steamed fish | name: "Fish steamed", portion: "150g", calories: 150 |

### Vegetable Recognition
| Input | Recognition Result |
|-------|-------------------|
| Mixed vegetables | name: "Mixed vegetables", portion: "200g", calories: 40 |
| Broccoli | name: "Broccoli", portion: "150g", calories: 50 |
