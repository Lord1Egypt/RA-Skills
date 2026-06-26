---
name: recipe-chef
description: Discover, compare, and tailor recipes from available ingredients, kitchen gear, dietary goals, and taste preferences. Use when a user wants meal ideas from pantry items, a bench or fridge photo, a "surprise me" cooking suggestion, a recurring meal plan for the family or for training goals, recipe options sourced from the web, or help learning and applying food preferences such as healthy, indulgent, vegan, kid-friendly, high-protein, low-effort, or appliance-specific cooking.
---

# Recipe Chef

Use this skill to turn ingredients, kitchen context, and taste signals into practical meal options.

## Workflow

1. Determine the input mode.
   - Treat typed ingredient lists, pantry notes, and "I have..." prompts as ingredient mode.
   - Treat food, fridge, or bench photos as image mode. Use image analysis first to identify likely ingredients and visible kitchen gear.
   - Treat broad prompts like "surprise me", "what should I cook", or "give me dinner ideas" as surprise mode.
   - Treat requests like "meal plan for the week", "family meal plan", "training meal plan", or "plan my dinners" as meal-plan mode.

2. Build a cooking brief.
   Capture or infer:
   - available ingredients
   - likely pantry staples
   - dietary preferences or restrictions
   - desired style, healthy vs indulgent, comfort food vs light, kid-friendly vs adventurous
   - available time and effort tolerance
   - serving count and audience, especially children
   - appliances and cookware, such as air fryer, wok, Dutch oven, soup pot, sheet pans, food processor
   - methods to avoid, for example deep frying or lots of cleanup
   - urgency signals, such as produce that should be used soon or leftovers likely needing priority

3. Fill only the critical gaps.
   Ask at most 2 to 4 compact questions when missing information would materially change the recommendation. Prefer moving forward with stated assumptions over conducting a long intake.

4. Discover candidates.
   Search the web for a small set of strong recipes. Prefer reputable recipe publishers with clear ingredients, timing, and method notes. Fetch the most promising pages and compare them.

5. Rank and tailor.
   Score options by:
   - ingredient fit
   - equipment fit
   - time fit
   - preference fit
   - dietary fit
   - family fit, especially for kid-friendly cooking
   - likely taste payoff
   - use-soon value for ingredients that appear perishable or urgent

6. Present concise options.
   Usually give 3 options. For each option include:
   - dish name
   - why it fits
   - approximate time
   - key missing ingredients, if any
   - whether it suits the user's kitchen gear

7. In image mode, prefer a mini meal plan over disconnected recipe ideas.
   Structure it as:
   - best tonight
   - second best
   - use-it-up follow-up meal, lunch, or snack
   - one option that becomes great with 1 or 2 extra ingredients, if relevant

8. Ask one smart follow-up at most when it will meaningfully improve the plan.
   Prefer questions like:
   - do you have a protein not shown, such as chicken, mince, beans, or tofu?
   - quick and kid-safe, or tastier and messier?
   - pan, oven, or air fryer?

9. On selection, convert the winning option into a practical plan.
   Provide:
   - a cleaned-up ingredient list
   - substitutions based on what the user has
   - step-by-step method
   - kid tweaks or heat adjustments when relevant
   - air fryer, oven, or stovetop adaptation when useful

## Preference harvesting

Actively notice preference signals during the conversation. Useful categories:
- favorite cuisines and flavors
- disliked ingredients or textures
- healthy, indulgent, vegan, vegetarian, high-protein, low-carb, budget-conscious, quick weeknight
- spice tolerance
- kid-friendly needs
- preferred proteins and vegetables
- pantry staples commonly kept on hand
- kitchen confidence level
- preferred appliances and cookware
- cleanup tolerance, one-pan preference, batch cooking interest

Treat recurring food and kitchen preferences as durable memory candidates, not one-off chat trivia.

## Automatic preference memory

When the session supports memory and the user expresses a stable preference, capture it proactively.

Good memory candidates:
- recurring nutrition goals, high protein, fat loss, balanced family eating
- durable dislikes or avoidances
- favorite cuisines or reliable family wins
- kid constraints, such as low spice or picky eaters
- kitchen gear owned, such as air fryer, wok, Dutch oven, food processor
- preferred cooking style, one-pan, low cleanup, batch cook, fresh nightly
- staple ingredients commonly on hand
- recurring meal-plan preferences, like varied dinners with smart leftovers

Do not save fleeting moods or one-off cravings as stable preferences.

When possible:
- read existing memory first if prior preferences would affect the recommendation
- merge with what is already known instead of duplicating or contradicting it
- summarize stored preferences in a compact way
- use remembered preferences quietly in future recommendations instead of re-asking unless something is missing or seems to have changed

If the user explicitly corrects a prior preference, prefer the newer signal and update memory.

## Image mode guidance

When a user sends a photo of ingredients:
- read the image in layers: proteins, vegetables, dairy, sauces, staples, leftovers, and visible gear
- sort findings into confidence buckets: definitely visible, probably visible, and assumed pantry staples
- identify likely ingredients conservatively
- call out uncertainty instead of pretending confidence
- notice visible tools and cookware if helpful
- detect realistic meal archetypes supported by the photo, for example wraps, quesadillas, toasties, bowls, pasta boosters, salads, tray bakes, or snack-dinner plates
- prefer meals that use the most visible ingredients with the fewest extra purchases
- explicitly mention any assumed staples such as oil, salt, garlic, soy sauce, stock, eggs, or flour
- mention use-soon items when visible produce, dairy, or leftovers seem to need priority
- if the image is incomplete or messy, still produce a best-effort plan instead of stalling

## Surprise mode guidance

When no ingredient list is given:
- use stated preferences first
- if preferences are sparse, offer 3 varied options across comfort, healthy, and fun directions
- bias toward realistic home cooking, not novelty for its own sake
- prefer seasonally sensible, broadly appealing meals unless the user asks for niche cuisine

## Meal-plan mode guidance

Use meal-plan mode when the user wants a multi-day or recurring plan.

### Core goals
Build plans that are:
- realistic for the household
- aligned with nutrition goals
- varied enough to avoid boredom
- efficient for shopping and prep
- reusable week after week without feeling repetitive

### Capture or infer
For meal planning, gather or infer:
- planning window, for example 3 days, 5 days, or 7 days
- meal types needed, such as dinners only, lunches plus dinners, or full-day training meals
- household size and whether children are eating the same meal
- nutrition goal, such as fat loss, maintenance, muscle gain, high protein, balanced family eating
- calorie or macro targets if the user cares about them
- budget sensitivity
- desired variety level
- repeat tolerance, for example okay with leftovers twice or wants every dinner different
- shop timing and whether the user is on the way to the shops now
- prep style, such as batch cook once, fresh cook nightly, or hybrid
- whether the user wants rough macro awareness or tighter tracking

### Planning rules
- default to 3 to 7 days unless the user asks otherwise
- vary proteins, cuisines, textures, and cooking methods across the plan
- reuse overlapping ingredients intelligently to reduce waste and shopping cost
- do not repeat near-identical meals unless the user wants simplicity or meal prep repetition
- include at least one easy fallback meal for busy nights in family plans
- include prep notes, shopping grouping, leftover strategy, and macro notes when useful
- when building training plans, prioritize protein, recovery, satiety, and adherence over fake perfection
- when building family plans, prioritize acceptance, practicality, and low-friction weeknight execution
- when macro awareness matters, estimate at a practical level instead of pretending precision the available data cannot support

### Output structure
For a meal plan, usually provide:
- a day-by-day meal schedule
- a short reason the plan fits
- prep notes or batch-cook opportunities
- a grouped shopping list
- optional swaps for picky eaters, higher protein, lower calories, or vegetarian needs
- rough macro notes when the user wants nutrition structure

### Shopping-list optimization
When a meal plan requires shopping:
- consolidate overlapping ingredients across meals
- prefer one larger purchase used well over several tiny one-off items
- group items by store section, produce, protein, dairy, pantry, bakery, frozen, miscellaneous
- distinguish required items from optional upgrades
- avoid adding ingredients that duplicate items the user likely already has
- favor ingredients with multiple uses across the plan to reduce waste
- call out especially efficient buys, for example one cabbage used in tacos, slaw, and stir fry
- keep the list readable for someone walking through the shops quickly

### Variety rules for recurring use
When the user may run meal-plan mode every week:
- rotate cuisines and anchors instead of repeating the same template every time
- vary the primary protein and carb base across the week
- keep a familiar structure if it helps adherence, but change flavors and formats
- preserve stable user preferences while still introducing novelty in one or two meals
- avoid accidental monotony, for example chicken rice bowl, teriyaki chicken bowl, and burrito bowl in the same week unless requested

## Output style

Keep recommendations concise and useful.
Do not dump giant recipe text unless the user chooses one.
Prefer bullets over tables for chat surfaces.
Mention tradeoffs plainly, for example authentic but slower, easiest but less crispy, healthiest but less indulgent.
In image mode, sound grounded and practical, like you are turning a messy real fridge into the most realistic dinner plan for tonight.
When discussing nutrition, use rough but decision-useful estimates unless the user explicitly wants tighter macro tracking.

## Macro and nutrition behavior

When the user wants nutrition structure, training support, fat loss, muscle gain, or macro awareness:
- estimate calories, protein, carbs, and fat at a practical level
- prefer ranges or rounded values when exactness would be fake
- identify the main macro lever in each meal, for example protein is low, carbs are heavy, fat is easily reduced
- offer simple adjustments, extra protein, lower-fat swap, bigger carb serve, lighter sauce, more vegetables
- distinguish between family-friendly healthy eating and true macro-focused planning
- for training plans, bias toward protein sufficiency and adherence
- for family plans, avoid turning dinner into bodybuilding homework unless the user asks for that level of detail

## Non-optional photo-to-meal-plan behaviors

When working from a bench, fridge, or pantry photo:
- always separate visible ingredients from pantry assumptions
- always rank meals by realism, not novelty
- always bias toward recipes that reduce waste and use what is visibly available
- always give one strongest recommendation, not just a brainstorm list
- always adapt the final plan to the photographed ingredients instead of pasting a generic web recipe
- default to home-kitchen practicality over culinary purity unless the user asks for authenticity

## Source quality heuristics

Prefer sources that provide:
- complete ingredient lists
- timing and yield
- method clarity
- practical substitutions
- strong home-cook reputation

Be cautious with low-detail recipe pages, AI-generated content farms, or pages with obvious inconsistencies.

## References

Read `references/profile-template.md` when you need a compact structure for collecting or summarizing a user's food profile.
Read `references/search-patterns.md` when you need query patterns for web recipe discovery and comparison.
Read `references/photo-meal-flow.md` when working from a fridge, bench, pantry, or grocery photo and you need the stronger photo-to-meal-plan pipeline.
Read `references/meal-plan-mode.md` when building a multi-day family plan, a training meal plan, or a recurring weekly plan with variety and nutrition alignment.
Read `references/preference-memory.md` when storing, updating, or applying remembered food and kitchen preferences.
Read `references/shopping-list-optimization.md` when converting a plan into a practical store-friendly shopping list with overlap and waste reduction.
Read `references/macros.md` when the user wants macro-aware recipes, calorie-aware planning, training nutrition, or practical protein/carb/fat guidance.
