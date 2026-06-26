---
name: child-nutrition
description: Track child diet, nutrition assessment, picky eating management, and dietary advice. Use when user mentions child eating, meals, nutrition, vitamins, or feeding issues.
argument-hint: <operation_type: record/pickyeater/growth/deficiency/advice/history, e.g.: record breakfast milk eggs, pickyeater, deficiency, advice>
allowed-tools: Read, Write
schema: child-nutrition/schema.json
---

# Child Nutrition Assessment Skill

Child diet recording, nutrition assessment and picky eating management, providing age-specific nutritional needs and dietary recommendations.

## Core Flow

```
User Input → Identify Operation Type → Read Child Information → Determine Nutritional Needs by Age → Generate Assessment Report → Save Data
```

## Step 1: Parse User Input

### Operation Type Mapping

| Input | action | Description |
|------|--------|-------------|
| record | record | Log diet |
| pickyeater | pickyeater | Picky eating assessment |
| growth | growth | Growth nutrition assessment |
| deficiency | deficiency | Nutritional deficiency screening |
| advice | advice | Dietary recommendations |
| history | history | Historical records |

### Food Category Recognition

| Keywords | category |
|----------|----------|
| rice, noodles, bread, porridge, 米饭, 面条 | grain |
| beef, pork, chicken, fish, eggs, 牛肉, 猪肉, 鸡肉, 鱼, 蛋 | protein |
| milk, yogurt, cheese, 牛奶, 酸奶, 奶酪 | dairy |
| vegetables, 青菜, 白菜, 菠菜, 胡萝卜, 黄瓜 | vegetable |
| apple, banana, orange, pear, 苹果, 香蕉, 橙子, 梨 | fruit |
| nuts, peanuts, 坚果, 花生 | nuts |

## Step 2: Check Information Completeness

### record Operation:
- Diet information (can infer from user input)

### Other Operations:
- Only require child basic information

## Step 3: Determine Nutritional Needs by Age

| Age | Energy(kcal/day) | Protein(g/day) | Calcium(mg/day) | Iron(mg/day) |
|-----|------------------|----------------|-----------------|--------------|
| 1-3 years | 1000-1400 | 25-30 | 600 | 9 |
| 4-6 years | 1400-1600 | 30-35 | 800 | 10 |
| 7-10 years | 1600-2000 | 35-40 | 1000 | 13 |
| 11-14 years | 2000-2500 | 50-60 | 1200 | 15-18 (male) / 12-15 (female) |

## Step 4: Generate Assessment Report

### Nutritional Status Assessment

| Assessment Item | Standard |
|----------------|----------|
| Energy intake | 80-120% of recommended is normal |
| Protein | Daily sources: milk, eggs, meat |
| Calcium | Daily dairy products |
| Iron | Daily red meat, animal blood |
| Vitamin C | Daily fruits and vegetables |

### Diet Record Report Example:
```
Diet record saved

Diet Information:
Child: Xiaoming
Age: 2 years 5 months
Record date: January 14, 2025

Today's Diet:

Breakfast (08:00):
  Milk 200ml
  Egg 1
  Bread 1 slice
  Apple half

Lunch (12:00):
  Rice 1 small bowl
  Vegetables moderate
  Chicken 50g
  Tomato scrambled eggs

Dinner (18:00):
  Noodles 1 small bowl
  Tomato beef
  Cucumber

Nutrition Assessment:
  Energy intake: Adequate
  Protein: Adequate (milk, eggs, meat)
  Calcium: Adequate (dairy)
  Iron: Adequate (meat, eggs)
  Vitamin C: Adequate (fruits, vegetables)
  Dietary fiber: Adequate (vegetables, fruits)

Water Intake:
  Today's water: ~800ml
  Recommended: 1000-1300ml/day
  Assessment: Basically adequate

Overall Evaluation:
  Balanced diet, adequate nutrition

Recommendations:
  Continue current eating habits
  Increase water intake appropriately

Data saved
```

## Step 5: Save Data

Save to `data/child-nutrition-tracker.json`, including:
- child_profile: Child basic information
- dietary_records: Diet records
- picky_eating: Picky eating status
- nutritional_assessment: Nutrition assessment
- statistics: Statistical information

## Picky Eating Assessment Standard

| Picky Eating Degree | Condition |
|---------------------|-----------|
| None | Accepts all food types |
| Mild | Refuses 1-2 food types |
| Moderate | Refuses 3-5 food types, affects nutrition |
| Severe | Refuses >5 food types, nutrition affected |

## Nutritional Deficiency Symptoms

### Iron Deficiency
- Pale complexion
- Poor appetite
- Easy fatigue
- Poor concentration
- Pica (eating non-food items)

### Calcium Deficiency
- Teeth grinding at night
- Excessive sweating
- Night terrors
- Growth delay
- Multiple cavities

### Vitamin D Deficiency
- Occipital balding
- Night terrors/excessive sweating
- Delayed teething
- Square skull/pigeon chest
- Bow legs/X-legs

### Zinc Deficiency
- Poor appetite
- Diminished taste
- Slow wound healing
- White spots on nails
- Low immunity

## Nutrition Focus by Age

### 1-3 Years (Toddler)
- Milk volume: 400-500ml/day
- Main meals: 3 times
- Snacks: 2 times
- Food texture: Gradually transition to solid foods

### 3-6 Years (Preschool)
- Milk volume: 300-400ml/day
- Main meals: 3 times
- Snacks: 1-2 times
- Note: Food variety, prevent picky eating

### 6-12 Years (School Age)
- Milk volume: 300ml/day
- Main meals: 3 times
- Snacks: 1 time
- Note: Important breakfast, balanced nutrition

## Common Nutrient Sources

| Nutrient | Sources |
|----------|---------|
| Protein | Meat, fish, eggs, milk, beans |
| Calcium | Dairy, soy products, leafy greens |
| Iron | Red meat, animal blood, liver |
| Zinc | Shellfish, lean meat, nuts |
| Vitamin A | Animal liver, carrots, dark vegetables |
| Vitamin C | Citrus, kiwi, bell peppers |
| Vitamin D | Sunlight, cod liver oil, fortified foods |
| Dietary fiber | Whole grains, vegetables, fruits |

## Execution Instructions

1. Read data/profile.json for child information
2. Determine nutritional needs based on age
3. Analyze diet information or generate recommendations
4. Save to data/child-nutrition-tracker.json

## Medical Safety Principles

### Safety Boundaries
- No malnutrition diagnosis
- No nutritional supplement brand recommendations
- No prescribing
- No severe malnutrition handling

### System Can
- Diet recording and tracking
- Nutritional intake assessment
- Picky eating management recommendations
- Nutritional deficiency screening
- Dietary recommendation education

## Important Notice

This system is for diet recording and nutrition reference only, **cannot replace professional nutritional assessment and diagnosis**.

If following conditions occur, **please consult pediatrician or nutritionist**:
- Growth delay
- Significant underweight or overweight
- Severe picky eating affecting growth
- Suspected nutritional deficiency symptoms
