# Checkout Guardrails - Uber Eats

Treat these actions as increasingly sensitive:

## Browse Safe

- switching between merchant and category pages
- reading ETA, fees, promos, and ratings
- comparing merchants without changing the cart

## Draft Cart Only If Requested

- adding items to an empty cart
- editing quantities on a fresh draft
- testing notes or substitutions for a candidate order

If the cart already contains items, ask whether to preserve, replace, or merge before editing.

## Explicit Confirmation Required

Always stop and summarize before:
- changing the delivery address
- clearing a non-empty cart
- relying on a cancellation path after checkout
- confirming payment and placing the order

## Final Summary Format

Before live checkout, confirm:
- merchant name
- items and quantities
- substitutions or delivery notes
- active delivery address
- ETA
- delivery fee, service fee, tip, and total
- payment method shown by Uber Eats

If any one of those is unclear on screen, do not place the order.
