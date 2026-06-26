# Order Recovery — Walmart

Use this when the basket already failed in the real world.

## Missing Item

- Check whether the item was canceled, substituted, delayed, or never packed.
- Reclassify the item: must-have now, can wait, or replace locally elsewhere.
- Update `order-log.md` if the same item fails repeatedly.

## Bad Substitution

- Record exactly what went wrong: size, flavor, ingredient, or brand mismatch.
- Move that item into `never substitute` if the failure would predictably repeat.
- Offer the next safer rule, not just a refund path.

## Damaged or Spoiled Delivery

- Separate refund action from planning action.
- Replace perishables on the fastest path and move non-urgent items to the next basket.
- Add timing notes if late delivery likely caused the damage.

## Split Shipment Surprise

- Tell the user which items are still pending and which part of the order is complete.
- Rebuild the next basket around the real gap, not the original plan.
- Avoid promising one-window fulfillment for categories that repeatedly split.

## Slot or Timing Failure

- Recheck urgency and simplify the basket if the delivery window tightened.
- Protect must-have and cold-chain items first.
- Drop optional items rather than risking a full order miss.
