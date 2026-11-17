---
name: restaurant-meal-nutrition-planner
description: "Build a restaurant meal that fits the user's calorie, protein, sodium and allergen goals. Totals calories, protein, carbs, fat and sodium from the restaurant's published nutrition figures, flags any item with a missing figure instead of guessing, checks listed allergens, and suggests swaps that close the gap. Uses the BJ's Restaurant & Brewhouse menu as the worked example. Use when someone asks what to order to stay under a calorie or sodium limit, how many calories or how much protein a restaurant meal has, or which menu items avoid an allergen."
version: 1.0.1
metadata:
  openclaw:
    emoji: "🍽️"
    homepage: https://bjsmenus.com/
---

# Restaurant meal nutrition planner

Instruction-only: no commands, installs or network access. Work from the nutrition figures the user gives you or pastes from the restaurant's published nutrition guide, and do the arithmetic yourself.

## When to use

- "I'm going to BJ's tonight. What can I get for under 800 calories with at least 40 g of protein?"
- "Total up a Wagyu burger, fries and a root beer for me."
- "I'm allergic to shellfish and watching sodium. Build me a dinner."

## 1. Collect the goals

Ask only for what is missing. Defaults are in brackets.

- Calorie ceiling for this meal (none). If they give a daily target instead, suggest about one third of it for a main meal and say that is a rule of thumb.
- Protein floor in grams (none)
- Sodium ceiling in mg (none). For reference, the US Dietary Guidelines and the FDA Daily Value use 2,300 mg for a whole day. A single restaurant entree often passes that.
- Optional carb or fat ceilings in grams (none)
- Allergens to avoid (none). Use the restaurant's own allergen list names.
- Courses wanted: main, side, drink, dessert (main + side + drink)

## 2. Get the figures

Use only published per-item numbers: the restaurant's nutrition guide, or figures the user supplies. Never estimate a missing value from a similar dish.

For each item record: name, serving as listed, calories, protein g, carbs g, fat g, sodium mg, listed allergens.

Watch for these traps:

- **Per-slice or per-piece items.** Pizza and flatbread figures are often per slice. Ask how many slices they will eat and multiply every number by that count. If they don't know, show the per-slice figure and leave the item out of the total.
- **Ranges or "with dressing" values** (e.g. "80 plain / 240-320 with dressing"). Ask which version they will order. If they want the range, carry a low and a high total.
- **Not listed.** If any figure is missing, the total for that nutrient is **incomplete**. Say so and name the item. Never treat a missing value as zero.
- **Combos.** A "with fries" item already includes the side. Don't add fries again.

Sanity check each item: protein × 4 + carbs × 4 + fat × 9 should land within about 10% of the listed calories. If it is far off, the user may have copied a wrong row. Ask them to check it, but keep the published calorie figure.

## 3. Total and compare

1. Add each nutrient across all items.
2. Put each total next to its goal: calories and sodium must be at or under the ceiling; protein at or over the floor.
3. Check every item's allergen list against the avoid list. An item with no allergen listed is not the same as allergen-free. Say "none of the tracked allergens listed".
4. Mark each goal **met**, **missed by X**, or **incomplete**.

Output a table:

| Item | kcal | Protein g | Carbs g | Fat g | Sodium mg | Allergens |
|---|---|---|---|---|---|---|

Then a **Total** row and a **Goal** row.

## 4. Suggest swaps

If a goal is missed, change the item that adds most to that nutrient first:

- Too many calories: swap the side for a vegetable side, then a sugary drink for water, unsweetened tea or diet soda, then look at a lighter main ("Enlightened", grilled or salad-based items).
- Too much sodium: look at the main first. Sauces, wings, burgers and soups are usually the biggest sources. Fries and loaded potatoes are next.
- Not enough protein: pick a main built on chicken breast, fish, shrimp or steak, or add a plain protein side.
- Allergen conflict: replace the item. Don't suggest "ask them to leave it off" as a fix for a real allergy.

Give at most three swaps, each with the new totals, so the user can choose.

## Example (BJ's)

Goal: 900 kcal or less, at least 45 g protein, 2,000 mg sodium or less, no shellfish. Figures are from BJ's published nutrition guide (June 2026).

First pick: Boneless Wings (870 kcal, 65 g protein, 59 g carbs, 41 g fat, 3,522 mg sodium) + Fries (350, 4, 40, 19, 921). Total: 1,220 kcal, 69 g protein, 99 g carbs, 60 g fat, 4,443 mg sodium. Calories are over by 320 and sodium by 2,443.

Swap to:

| Item | kcal | Protein g | Carbs g | Fat g | Sodium mg | Allergens |
|---|---|---|---|---|---|---|
| Enlightened Cherry Chipotle Glazed Salmon | 580 | 47 | 40 | 26 | 576 | Fish, Soy, Sulfites, Wheat |
| Broccoli | 40 | 3 | 6 | 0 | 30 | none of the tracked allergens listed |
| Lemonade | 180 | 0 | 44 | 0 | 17 | none of the tracked allergens listed |
| **Total** | **800** | **50** | **90** | **26** | **623** | no shellfish |
| Goal | ≤ 900 | ≥ 45 | – | – | ≤ 2,000 | no shellfish |

All goals met. Choosing water instead of lemonade brings it down to 620 kcal and 46 g of carbs.

## Notes

- Published figures are for the standard recipe and can vary by location, portion and any changes made when ordering.
- For a serious allergy, tell the user to confirm with the restaurant before ordering. Shared fryers and kitchens can cause cross-contact that the menu does not show.
- This is meal arithmetic, not medical or dietetic advice. Anyone on a prescribed diet should follow their clinician's targets.
- Never order or contact a restaurant for the user.

## Links

- Want to check a dish before adding it? Browse the full [BJ's menu](https://bjsmenus.com/) with prices and calories.
