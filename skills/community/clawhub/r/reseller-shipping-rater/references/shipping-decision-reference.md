# Reseller Shipping Reference

## Dimensional weight — the actual formulas
- **UPS / FedEx (daily rates)**: `billable = max(actual_lb, L×W×H/139)`. Negotiated accounts often use 139-166; retail sites compute 139.
- **USPS**: dim pricing applies to packages over 1 cu ft for Priority Mail Express, Priority Mail, and Ground Advantage (divisor 166) — under 1 cu ft, you pay actual weight.
- **Cubic Ground Advantage**: if volume ≤ 0.5 cu ft AND weight ≤ 20 lb, price by volume TIER (T1-T5), not weight. Zone-based. This is the single most underused discount in small-parcel shipping: a 19-lb dense item in a 0.4 cu ft box can ship for near the 1-lb rate.
- **Boxing down 1 inch on each side** can drop you a cubic tier or under the 1-cu-ft dim threshold: that inch is money.

## Flat rate decision table (dense items, zone 5+)
| Situation | Winner |
|---|---|
| >10 lb, fits Medium/Large FR, zone 6-8 | Flat rate, almost always |
| Books/media ONLY, any weight | Media Mail (~$4-7 for lbs of books) — but USPS may inspect; no ads, invoices ok |
| 1-2 lb clothing, zone 1-5 | Poly bag + Ground Advantage weight/cubic |
| Light + bulky (>1 cu ft, <3 lb) | Smallest possible box; NEVER flat rate (you'd pay density you don't have) |
| Fragile + heavy | FR Box + padding — flat rate caps your risk on zone 8 |

## Platform fee mechanics (fees hit shipping too)
- **eBay**: final value fee ~13.25% (most categories) applied to item price + shipping charged + taxes. "Free shipping" = you pay 13.25% on the shipping money you embedded in the price.
- **Etsy**: ~6.5% transaction on item+shipping + payment processing (~3%+$0.25) + $0.20 listing.
- **Poshmark/Mercari**: higher take (~20% / ~10%+processing) — for these, shipping is often subsidized flat by the platform; your only lever is box size within the prepaid label's weight cap.
- Rule: compute profit AFTER (fees on gross incl. shipping) + label + packaging + COGS. The `profit` command does exactly this stack.

## Packaging cost reality (per shipment)
- Free: reused boxes (condition matters for fragile), grocery-store produce boxes, newspaper.
- Poly mailers ~$0.15-0.30 ea in bulk; corrugated 12×10×6 ~$0.60-1.10; bubble 12" roll ~$0.25/ft; fragile double-box adds a full second box.
- Insurance: first $100 included with some services; declared-value over that adds ~$1-2/$100. Price high-value items' insurance INTO the margin.

## Zone math (why the destination changes the answer)
Zones 1-2 = close (~150-300 mi), zone 8 = farthest continental. Ground rates roughly double zone 1→8; flat-rate is constant. A 6-lb box: weight-based wins zone 3, flat-rate wins zone 8. Same item, different buyer → different right answer. This is why "calculated shipping" beats flat fees for mid-density items.

## The pre-listing 60-second flow
1. Box it the way you'd actually ship it (padding included) → measure, weigh.
2. `rate` + `flatrate` with the real zone range of your typical buyers (run zone 3 and zone 8 if nationwide).
3. Take the WORSE of the two as your shipping price basis (or use calculated shipping).
4. `profit` at your sale price — if under 15% margin, fix the box or the price BEFORE listing.
5. Confirm winner label price live (platform rates often 20-40% under retail print).

## When NOT to ship at all
- Sale price − (worst-case label + fees + packaging) < 2× your hourly rate / handling time.
- Dim weight > 20 lb equivalent on a sub-$25 sale.
- Zone 8 + oversize (any dim > 22") + fragile: damage-claim roulette; local pickup is a listing option, not a failure.
