# Taobao Competitor Analyzer

Cross-platform shopping decision skill for Taobao users.

This skill checks the same or closest-matching product on:
- JD.com
- Pinduoduo
- Vipshop

Then it answers the question users actually care about:

`Should I keep buying this on Taobao, switch platforms, wait, or avoid this deal?`

## What It Does

- Compares visible prices across major Chinese marketplaces
- Uses Taobao as the baseline when a Taobao price, link, screenshot, or visible listing is available
- Matches brand, model, spec, count, and packaging before comparing price
- Scores same-item confidence so near matches do not masquerade as cheaper exact matches
- Normalizes headline price, coupon-after price, member price, subsidy price, group-buy price, shipping, and unit price
- Applies category playbooks so phones, skincare, baby goods, shoes, snacks, and paper towels are judged differently
- Flags near-match risk instead of pretending similar items are identical
- Weighs seller trust, shipping, warranty, invoice, and after-sales guarantees
- Returns a recommendation strength: strong, weak, reference-only, or cannot judge

## v1.1.0 Highlights

- Taobao baseline handling: no baseline price means no unsupported "switch away from Taobao" claim
- 100-point match scoring across brand, model, specs, quantity, channel trust, and evidence completeness
- Price normalization for unit price, coupon dependency, membership, subsidy, group-buy, and shipping caveats
- Evidence quality gate for title, price, spec/version, and URL before a listing can drive a strong recommendation
- Expanded verdict block with recommendation strength, lowest comparable price, risks, and final checks before purchase

## v1.2.0 Highlights

- Category-aware playbooks for electronics/appliances, beauty/personal care, food/daily goods, apparel/shoes/bags, baby/health/safety, and low-risk standard goods
- Buying-posture routing for lowest price, authenticity/after-sales, delivery speed, exact variant, and research-first workflows
- Platform-fit judgment so JD, PDD, and Vipshop are weighed differently by category instead of by headline price alone
- Category-specific price-delta thresholds: low-risk commodities can switch on unit-price wins, while warranty/authenticity categories need stronger evidence
- New `品类策略` and `购买偏好` fields in the verdict block

## Best Use Cases

- Compare a Taobao listing with JD / PDD / Vipshop
- Check whether a "cheaper" result is actually the same SKU
- Decide if it is worth switching platforms
- Do fast competitor research for consumer products
- Find the lowest visible comparable price with caveats
- Separate normal price from coupon, member, subsidy, and group-buy conditions
- Decide whether a low price is worth the category-specific risk

## Example Prompts

- `帮我查这个淘宝商品在京东、拼多多、唯品会有没有同款`
- `淘宝价 129，这个商品换到京东买值不值`
- `这款护肤品拼多多便宜很多，风险大不大`
- `这双鞋唯品会有近似款，能不能买`
- `别只比价，告诉我哪个平台更值得买`
- `Compare this Taobao product with JD, PDD, and Vipshop and recommend where to buy`

## Output Style

The skill is optimized to return:
- Taobao baseline status
- recommended platform
- recommendation strength
- lowest visible comparable price
- normalized unit/condition basis
- category strategy and inferred buying priority
- whether the comparison is apples-to-apples
- major risks and caveats
- a direct buy / wait / avoid recommendation

## Positioning

This is not a generic shopping browser helper.

It is a focused purchase-decision skill for users who want:
- faster price comparison
- fewer fake "cheap" matches
- clearer marketplace tradeoff analysis
- conservative recommendations when evidence is incomplete
- category-aware buying advice rather than one-size-fits-all price sorting
