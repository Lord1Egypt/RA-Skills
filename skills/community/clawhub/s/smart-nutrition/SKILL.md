---
name: smart-nutrition
description: Smart Nutrition Customizer. Input height, weight, age, gender, and activity level to calculate BMR and macronutrient needs, then generate a full-day meal plan with recipes, calorie counts, and nutrition labels. 
---

# Smart Nutrition Customizer 👩‍🍳

Calculate metabolic rate and nutritional needs from body data, then generate a personalized full-day meal plan.

## Use Cases

Use when the user needs "nutrition planning", "meal plan", "calorie calculation", "weight loss meals", "muscle gain meals", "dietitian", "healthy recipes", or "calorie counting".

## Workflow

### Step 1: Collect Information

Gather the following data from the user (ask only for what's missing, not all at once):

| Parameter | Description |
|-----------|-------------|
| Gender | Male / Female |
| Age | Years |
| Height | cm |
| Weight | kg |
| Activity Level | Sedentary / Lightly active (1-3 days/week) / Moderately active (3-5 days/week) / Very active (6-7 days/week) / Extremely active (athlete/manual labor) |
| Goal | Weight loss / Maintenance / Muscle gain (optional, defaults to maintenance) |

### Step 2: Calculate Metabolism & Nutritional Needs

#### Basal Metabolic Rate (BMR) — Mifflin-St Jeor Equation

```
Male:   BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age - 161 + 166  → i.e. 10W + 6.25H - 5A + 5
Female: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age - 161
```

#### Total Daily Energy Expenditure (TDEE) = BMR × Activity Multiplier

| Activity Level | Multiplier |
|----------------|------------|
| Sedentary | 1.2 |
| Lightly active | 1.375 |
| Moderately active | 1.55 |
| Very active | 1.725 |
| Extremely active | 1.9 |

#### Goal-Based Calorie Adjustment

| Goal | Adjustment |
|------|------------|
| Weight loss | TDEE - 300~500 kcal |
| Maintenance | TDEE (unchanged) |
| Muscle gain | TDEE + 300~500 kcal |

#### Macronutrient Distribution

| Goal | Protein | Fat | Carbs |
|------|---------|-----|-------|
| Weight loss | 30-35% | 25-30% | 35-45% |
| Maintenance | 20-25% | 25-30% | 45-55% |
| Muscle gain | 25-30% | 20-25% | 45-55% |

Conversion: Protein 4 kcal/g, Carbs 4 kcal/g, Fat 9 kcal/g.

### Step 3: Generate Full-Day Meal Plan

Output in the following format, covering breakfast, lunch, dinner, plus 1-2 optional snacks:

```
## 📊 Your Data Overview

| Item | Value |
|------|-------|
| BMR | xxx kcal |
| TDEE | xxx kcal |
| Target Calories | xxx kcal |
| Protein | xx g (xx%) |
| Fat | xx g (xx%) |
| Carbs | xx g (xx%) |

---

## 🍳 Breakfast (~xxx kcal)

### Dish Name

**Ingredients** (x servings):
- Ingredient 1 — xx g
- Ingredient 2 — xx g

**Instructions**:
1. Step one
2. Step two

**Nutrition**: Calories xx kcal | Protein xx g | Fat xx g | Carbs xx g

---

(Repeat same format for lunch, dinner, and snacks)

---

## 📋 Daily Summary

| Meal | Calories | Protein | Fat | Carbs |
|------|----------|---------|-----|-------|
| Breakfast | xx | xx | xx | xx |
| Lunch | xx | xx | xx | xx |
| Dinner | xx | xx | xx | xx |
| Snack | xx | xx | xx | xx |
| **Total** | **xx** | **xx** | **xx** | **xx** |
| Target | xx | xx | xx | xx |
```

### Meal Design Principles

- **Chinese cuisine first**, aligned with local eating habits; can intersperse Western/Japanese simple dishes
- Label specific gram amounts for each meal for practical execution
- Keep instructions concise and practical, 3-5 steps, suitable for home kitchens
- Use common, easy-to-buy ingredients
- Keep total daily calorie error within ±50 kcal of target
- Prioritize protein from quality sources: eggs, chicken breast, fish/shrimp, tofu, milk
- Weight loss plans: more vegetables, high protein, controlled oil and sugar; muscle gain plans: moderately increase carbs and protein
- If the user has food allergies or dietary restrictions, proactively ask and avoid

### Additional Services

After generating the plan, proactively ask if the user needs:
- 🔄 A new menu for another day
- 📅 A weekly meal plan
- 🛒 A shopping list
- 📉 Calorie target adjustment
