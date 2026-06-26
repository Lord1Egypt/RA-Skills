---
name: sichuan-cuisine
description: >-
  Ultimate Sichuan cuisine (川菜) knowledge base with 45+ classic recipes spanning cold dishes, hot dishes, soups, snacks, hot pot/maocai/gan guo, and banquet dishes. Covers all 24 flavor profiles, complete ingredient encyclopedia, and comprehensive cooking techniques. Use when users ask about Sichuan recipes, cooking methods, flavor profiles, ingredient substitutions, meal planning, Sichuan food culture, or any 川菜-related questions. Triggers include keywords like 川菜, 回锅肉, 麻婆豆腐, 鱼香, 宫保, 水煮, 麻辣, 红油, 担担面, 酸辣粉, 口水鸡, 夫妻肺片, 灯影牛肉, 樟茶鸭, 东坡肘子, 火锅, 冒菜, 干锅, 开水白菜, 菜谱, 四川菜, 成都美食 etc.
---

# Sichuan Cuisine (川菜) Skill

Comprehensive skill for Sichuan cuisine — one of China's Eight Great Cuisines, known for "百菜百味" (100 dishes, 100 flavors) and 24 official flavor profiles.

## How to Use

1. Identify what user needs: recipe, technique explanation, flavor profile info, ingredient advice, meal recommendation
2. Load relevant reference file(s) based on need
3. Provide concise, actionable answer

## Reference Files

### Flavor Profiles → `references/flavor-profiles.md`
Load when user asks about: flavor types, taste profiles, "what flavor is X dish?", 24 flavor types, 味型, understanding Sichuan taste theory.
Contains: All 24 official flavor profiles with characteristics, core seasonings, representative dishes, key ratios.

### Recipe Database → `references/recipe-database.md`
Load when user asks about: specific recipes, how to cook a dish, cooking steps, ingredient amounts.
Contains **45+ classic recipes** across 6 categories:
- **凉菜 (11)**: 蒜泥白肉、口水鸡、红油耳片、姜汁豇豆、椒麻鸡片、夫妻肺片、灯影牛肉、棒棒鸡、怪味鸡丝、陈皮牛肉、泡椒凤爪、麻酱凤尾、芥末鸭掌、四川泡菜
- **热菜 (23)**: 回锅肉、盐煎肉、宫保鸡丁、鱼香肉丝、鱼香茄子、麻婆豆腐、水煮牛肉、水煮鱼、酸菜鱼、辣子鸡、毛血旺、干煸四季豆、家常豆腐、东坡肘子、粉蒸肉、粉蒸排骨、樟茶鸭、锅巴肉片、糖醋脆皮鱼、糖醋排骨、京酱肉丝、炝炒莲白、青椒肉丝、大蒜烧鳝段、火爆腰花、韭香腰花、干烧鱼、豆瓣鱼、豆豉鲫鱼、番茄炒蛋
- **汤羹 (6)**: 开水白菜、鸡豆花、酸辣汤、连锅汤、竹荪肝膏汤、酸萝卜老鸭汤
- **小吃 (8)**: 红油抄手、担担面、酸辣粉、钟水饺、赖汤圆、三大炮、宜宾燃面、蛋烘糕、冰粉、凉糕、川北凉粉
- **火锅/干锅/冒菜 (4)**: 麻辣火锅底料、冒菜、干锅鸡、干锅排骨
- **基本功 (6)**: 复制酱油、红油、刀口辣椒、郫县豆瓣铁律、清汤（顶汤）、猪油炼制

### Ingredients → `references/ingredients.md`
Load when user asks about: what ingredient to buy, substitutions, brand recommendations, kitchen stocking, "what is X ingredient?", 调料, 食材. Contains: Essential Sichuan seasonings, meat cuts, vegetable pairings, common mistakes, pantry checklist.

### Techniques → `references/techniques.md`
Load when user asks about: knife skills, heat control, seasoning order, starch slurry techniques, 火候, 刀工, 勾芡, cooking methods. Contains: Knife work, fire control levels, seasoning timing, starching methods, unique Sichuan techniques, cooking sequence templates.

## Workflow

### Recipe Request
1. Load `references/recipe-database.md`
2. If dish is not in database, synthesize with knowledge from `references/flavor-profiles.md` + `references/techniques.md`
3. Present recipe with: ingredients (主料→配料→调料), numbered steps, key tips (关键)

### Flavor/Method Question
1. Load `references/flavor-profiles.md` or `references/techniques.md` as needed
2. Explain with representative dishes as examples
3. Include practical ratios and tips

### Meal/Ingredient Recommendation
1. Load `references/ingredients.md`
2. Check `references/recipe-database.md` for dish suggestions
3. Consider seasonality and local availability (default: Chengdu context)

## Key Principles to Always Apply

1. 咸为基础 All Sichuan flavors build on saltiness
2. 糖提鲜 Small amount of sugar enhances umami in most dishes
3. 复合并重 Layer flavors, don't settle for single-note taste
4. 豆瓣必剁细 Pixian doubanjiang MUST be finely chopped before frying
5. 豆瓣必小火豆瓣 must be fried at low heat (<120°C) to release red oil without burning
6. 蒜要现捣 Garlic must be pounded fresh — never use pre-pounded

When user mentions a dish not in the database, apply these principles with your general Sichuan cuisine knowledge to provide useful guidance rather than refusing.
