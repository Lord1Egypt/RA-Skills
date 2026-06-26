---
name: meal-planner
description: Plans the week's meals and shopping list based on preferences and learns over time. Use when a user wants to stop deciding what to eat every night.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🍽️"
  openclaw.user-invocable: "true"
  openclaw.category: daily-rhythm
  openclaw.tags: "meals,food,cooking,shopping,weekly-plan,nutrition,family"
  openclaw.triggers: "meal plan,what should we eat,plan dinners,shopping list,food for the week,what's for dinner"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/meal-planner


# Meal Planner

Answers the question "what are we having this week" before you have to ask it.

Sends a weekly meal plan Sunday evening. Generates a shopping list.
Remembers what worked and what didn't. Adjusts over time.

---

## File structure

```
meal-planner/
  SKILL.md
  preferences.md     ← who's eating, dietary needs, cuisine likes/dislikes, cooking time
  history.md         ← what's been made, ratings, notes
  config.md          ← schedule, delivery, shopping list format
```

---

## Setup flow

### Step 1 — Household

- How many people? Adults / children?
- Any dietary requirements? (vegetarian, vegan, gluten-free, allergies)
- Any strong dislikes? ("no fish", "not spicy", "kids won't eat anything green")

### Step 2 — Cooking reality

- How many nights per week do you actually cook? (vs takeaway, eating out, leftovers)
- What's the realistic time available on a weeknight? 20 minutes? 45 minutes?
- Is someone a more confident cook, or is quick and simple always better?
- Any nights that are always eating out or always easy (Friday = pizza, whatever)?

### Step 3 — Preferences

- Favourite cuisines?
- Any "classics" that always work (a pasta that everyone likes, a go-to curry)?
- Budget per week for food roughly?
- Do they want variety or is repeating good meals fine?

### Step 4 — Shopping

- Where do they shop? (affects whether to include store-specific links)
- Do they want a consolidated shopping list or grouped by meal?
- Anything always in the house that doesn't need listing?

### Step 5 — Write preferences.md

```md
# Meal Planner Preferences

## Household
adults: [N]
children: [N, ages if relevant]

## Dietary
requirements: [list]
dislikes: [list]
kids won't eat: [list if applicable]

## Cooking
nights per week: [N]
weeknight time: [minutes]
skill level: [quick and easy / comfortable / adventurous]
fixed nights: [e.g. "Friday = takeaway", "Wednesday = leftovers"]

## Preferences
favourite cuisines: [list]
go-to meals: [list of reliable ones]
budget per week: [range]
repeat meals: [fine / prefer variety]

## Shopping
store: [if relevant]
always in stock: [staples to exclude from list]
```

### Step 6 — Register cron job

Weekly, Sunday evening:

```json
{
  "name": "Meal Planner",
  "schedule": { "kind": "cron", "expr": "0 17 * * 0", "tz": "<USER_TIMEZONE>" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run meal-planner. Read {baseDir}/preferences.md, {baseDir}/history.md, and {baseDir}/config.md. Generate a meal plan for the coming week. Avoid meals made in the last 2 weeks (check history.md). Generate shopping list. Deliver to configured channel.",
    "lightContext": true
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL>", "to": "<TARGET>", "bestEffort": true }
}
```

---

## Runtime flow

### 1. Read preferences and history

Load household, dietary needs, preferences.
Check history.md for recent meals — don't repeat anything from the last 2 weeks.
Check for any meals that got poor ratings — don't suggest them again.

### 2. Check the week's calendar (if connected)

Are there any evenings where cooking won't happen?
Meetings running late, social events, nights out?
Adjust the plan accordingly.

### 3. Generate the meal plan

Rules:
- Match cooking time to weeknight reality
- At least one new meal per week (not from history.md)
- At least one proven favourite (from go-to meals in preferences.md or high-rated history)
- Balanced variety across the week — don't do Italian four nights in a row
- Account for fixed nights (Friday = takeaway, etc.)
- If cooking for family: at least 3 of 5 meals should be family-friendly

Format:

**🍽️ Meal Plan — Week of [DATE]**

**Monday** — [MEAL NAME]
[One line: cuisine type, rough time, why it works this week]

**Tuesday** — [MEAL NAME]
[One line]

**Wednesday** — [MEAL NAME / Leftovers from Monday]

**Thursday** — [MEAL NAME]
[One line]

**Friday** — [Takeaway / Easy / User's preference]

**Saturday** — [Something nicer — more time available]

**Sunday** — [Batch cook or something comforting]

For each meal: one practical note if relevant ("uses same base as Thursday — make extra").

### 4. Generate shopping list

Consolidated list of everything needed for the week's meals.
Exclude items marked as "always in stock" in preferences.md.
Group by: produce / meat & fish / dairy / store cupboard / other.

Remove duplicates — if three meals use the same ingredient, list it once with the combined quantity.

**🛒 Shopping List — Week of [DATE]**

**Produce**
• [item] — [quantity]
• [item]

**Meat & Fish**
• [item]

**Dairy**
• [item]

**Store cupboard**
• [item] — (check if you have)

### 5. Update history.md

Log this week's planned meals.
Add "planned" status — updates to "made" or "skipped" via commands.

---

## Rating and learning

After the week, the skill learns from feedback.

`/meal rate [meal name] [1-5] [optional note]`

> `/meal rate chicken traybake 4 "good but needed more seasoning"`
> `/meal rate lentil soup 2 "kids refused it"`

history.md stores all ratings. The next week's plan avoids low-rated meals and favours high-rated ones.

After 4 weeks the plan is noticeably better. After 8 weeks it knows the household.

---

## Mid-week adjustments

`/meal swap [day] [reason]` — suggest an alternative for a specific night
`/meal tonight` — what's planned for tonight + quick recipe link
`/meal skip [day]` — mark a meal as skipped (takeaway, eating out)

---

## Recipe handling

When user asks about a meal in the plan:
`/meal recipe [meal name]` — generate or find a recipe

The skill generates a recipe from memory or web_search.
Format: ingredient list, method in numbered steps, time required.
Calibrated to the household's cooking skill level from preferences.md.

---

## Management commands

- `/meal plan` — show this week's plan
- `/meal next` — generate next week's plan now
- `/meal rate [meal] [1-5] [note]` — rate a meal
- `/meal add [meal]` — add a meal to the favourites list
- `/meal remove [meal]` — remove from suggestions
- `/meal shop` — show shopping list
- `/meal swap [day]` — suggest alternative for a night
- `/meal recipe [meal]` — get the recipe
- `/meal history` — show what's been made recently

---

## Multi-profile integration

In a family or parent profile:
- Preferences.md includes kids' restrictions
- Weeknight meals default to family-friendly
- Saturday/Sunday can be more adventurous
- Shopping list can be sent to a shared family channel

---

## What makes it good

The learning loop is the product.
Week one it makes reasonable guesses.
Week four it knows that Monday needs to be under 30 minutes, that the kids won't eat fish,
and that the Saturday pasta always gets a 5.

The calendar integration prevents plans that don't fit the week.
A meal plan that ignores three busy evenings is useless.

The shopping list deduplication is genuinely useful at scale.
"Buy 400g chicken" across three recipes correctly surfaces as "buy 1.2kg chicken."
