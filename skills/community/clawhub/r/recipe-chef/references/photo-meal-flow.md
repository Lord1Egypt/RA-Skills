# Photo to meal plan flow

Use this reference when the user shares a fridge, bench, pantry, or grocery photo and wants dinner ideas.

## 1. Extract in layers
Build the ingredient picture in this order:
- proteins
- vegetables and fruit
- dairy and cheese
- sauces, condiments, and jars
- starches and obvious staples
- leftovers and ready-to-eat items
- visible cookware or appliances

Do not overclaim. If an item is fuzzy, label it as probable instead of certain.

## 2. Create confidence buckets
Organize findings into:
- definitely visible
- probably visible
- assumed pantry staples

This keeps the answer honest and makes substitutions easier.

## 3. Infer meal archetypes
Translate the visible items into realistic home-cooking categories. Common archetypes:
- wraps, tacos, quesadillas
- toasties, melts, sandwiches, burgers
- rice bowls or grain bowls
- pasta with add-ins or fridge-clear-out sauces
- salads with protein add-ons
- tray bakes or sheet-pan meals
- stir fries
- snack plates or picky-kid dinners

Prefer archetypes that match the visible mix of ingredients and sauces.

## 4. Score by realism
Rank higher when a dish:
- uses multiple clearly visible ingredients
- requires few extra purchases
- fits the likely effort level implied by the prompt
- suits children or mixed eaters when relevant
- works with common kitchen gear
- uses up perishable items first

Rank lower when a dish:
- depends on many unseen ingredients
- requires niche equipment
- sounds clever but is unrealistic for tonight

## 5. Return a mini meal plan
Default structure:
- Best tonight
- Second best
- Use-it-up next meal
- Optional upgrade with 1 to 2 extra ingredients

This is usually better than presenting isolated recipe links.

## 6. Ask one precision question if needed
Only ask a follow-up when it materially changes the best recommendation. Good examples:
- Do you have a protein not shown?
- Are we aiming for kid-safe or bold?
- Pan, oven, or air fryer?

## 7. Adapt the chosen dish
Once the user picks a direction, give:
- exact ingredients from the photo plus pantry assumptions
- missing ingredient callouts
- substitutions
- short step-by-step method
- kid tweaks
- healthy tweak or indulgent tweak when useful

## 8. Waste-reduction prompts
If the photo shows likely use-soon food, mention it naturally:
- soft herbs
- half-used dairy
- cut produce
- cooked leftovers
- wilting greens
- tomatoes, berries, mushrooms, or opened jars that should be used soon
