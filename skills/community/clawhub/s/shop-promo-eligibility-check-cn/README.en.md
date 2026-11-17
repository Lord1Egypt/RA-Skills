# Promotion Eligibility Check

Provide confirmed promotion terms and a cart to receive a condition-by-condition eligible, ineligible, or needs-confirmation table, traceable calculation steps, and a payable draft only where the rules are explicit.

Each cart line needs a SKU, unit price, and positive integer quantity. Inputs cover validity period and timezone, threshold basis, eligible SKUs, stacking order, shipping, and current time. `percent` is the payable percentage: 90 means pay 90% (a 10% discount). It requires confirmed `rounding_mode: "total_half_up_2"`. A multi-line fixed or percentage discount that affects only part of a later promotion requires `allocation_rule: "cart_order"`, which deducts by cart-line order; it is not required when the later offer is definitely inapplicable, has no effect, or a confirmed full-scope intermediate offer clears the balance. A fixed amount above the applicable balance stays **needs confirmation** rather than being silently capped. A validity period whose start is after its end also stays **needs confirmation**. The Skill preserves decimal inputs and never guesses platform rounding or allocation rules. Missing shipping keeps the payable draft at **needs confirmation**. A pending earlier promotion does not by itself make a post-discount threshold pending when its confirmed lower bound already meets it: goods have a lower bound of zero, plus known shipping when shipping is confirmed as included. This Skill never fetches live prices, claims coupons, places orders, or claims the lowest price.

```bash
npx skills add xxjrq/shop-promo-eligibility-check-cn
python3 scripts/self_test.py
```

See [success input](fixtures/success.json) → [actual delivery](fixtures/success-delivery.json), and [missing-information input](fixtures/failure.json) → [actual delivery](fixtures/failure-delivery.json). Chinese documentation is in [README.md](README.md).

The public Saleor discount-domain material was consulted only for business context; this repository contains original documentation and code and imports no Saleor code. See [LICENSE](LICENSE).
