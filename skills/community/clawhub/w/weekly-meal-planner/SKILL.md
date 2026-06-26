---
name: meal-planner
description: Weekly meal planner - input people count, budget, taste preference → output 7-day menu with breakfast/lunch/dinner and shopping list
version: v1.0.0
tags: meal-planning, menu-generation, grocery-list, family-cooking
---

# Meal Planner

Weekly meal planning assistant for families.

## Usage Scenarios

### Scenario 1: Weekly Menu for Family
**User input:** "3个人，每人每天预算50元，口味偏清淡，帮我规划一周菜单。"

**Expected output:** 7-day menu with breakfast/lunch/dinner for each day, estimated cost per meal within ¥50/person/day budget, consolidated shopping list with quantities and estimated prices, and budget summary.

### Scenario 2: Spicy Menu with Fixed Budget
**User input:** "这周想吃辣的，两个人，总预算700元，给个菜单。"

**Expected output:** Spicy-themed weekly menu for 2 people, total budget ¥700, with per-day cost breakdown (avg ¥100/day), daily meals, and categorized shopping list.

### Scenario 3: Single Person Sweet Preference
**User input:** "一个人吃饭，喜欢甜食，每天预算100，帮我规划。"

**Expected output:** Balanced 7-day menu incorporating sweet elements while maintaining nutrition, single-person portions to avoid waste, daily budget tracking within ¥100, and efficient shopping list.
### Scenario 4: 双职工带娃家庭一周晚餐安排
**User input:** "两口子都要上班，下班都快7点了，还要给娃做饭，每天发愁吃什么，帮我做个一周菜单。"
**Expected output:** 制定'懒人高效版'一周晚餐计划，原则：周末备菜、工作日20分钟上桌。推荐预制菜包（盒马工坊/叮咚买菜预制菜）+快手菜组合。周一至周五菜单示例：周一番茄牛腩（周末炖好）+凉拌黄瓜；周二盒马预制咖喱鸡+蒸米饭+烫青菜。搭配叮咚买菜/美团买菜下单清单，一次下单覆盖3天食材。

## Input
- Number of people
- Daily budget (per person or total)
- Taste preference (light/spicy/sweet/balanced)

## Output
- 7-day menu (breakfast/lunch/dinner)
- Shopping list with estimated prices
- Budget summary

## Constraints
- ❌ No detailed recipe steps
- ❌ No food delivery recommendations
- ❌ No allergy detection

## Usage
```bash
python3 scripts/meal-planner.py --people 3 --budget 50 --taste light
```
