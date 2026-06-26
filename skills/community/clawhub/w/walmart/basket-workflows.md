# Basket Workflows — Walmart

Use the smallest workflow that matches the request.

## Weekly Stock-Up

- Start from household size, meal plan, and staple thresholds.
- Split the basket into `must-have`, `replaceable`, and `nice-to-have`.
- Mark items that can tolerate substitutions before checking value.
- Review unit value only after basket coverage is solid.

## Urgent Top-Off

- Optimize for speed and reliability, not perfect savings.
- Keep the basket short and protect items needed in the next 24 hours.
- Avoid mixed shipping items unless the user accepts split fulfillment.

## Repeat Reorder

- Pull from prior successful baskets and confirmed staple rules.
- Ask what changed since the last order: budget, schedule, guests, diet, or inventory.
- Revalidate any item with a history of bad substitutions or stock issues.

## Mixed Basket

- Flag grocery, general merchandise, and regulated items separately.
- Tell the user when the basket may split into pickup, shipping, or delayed components.
- Keep cold-chain and pharmacy-adjacent items on the tightest timing path.

## Output Shape

For every serious basket recommendation, return:
- basket mode and needed-by window
- must-have items
- replaceable items with fallback logic
- optional items that can drop if stock or budget breaks
- final warning list: split shipping, sensitive substitutions, timing risks
