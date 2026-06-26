# Site Notes

## Goal

Use browser-visible marketplace pages to collect price evidence for the same or closest-matching product on JD, Pinduoduo, and Vipshop, then turn that evidence into a purchase decision against the Taobao baseline when available.

## Common Reminders

- Prefer visible desktop web pages.
- Use exact product names first, then a lightly simplified query if results are sparse.
- Compare like-for-like products only.
- Keep the evidence chain simple: search page -> listing -> visible title/price/spec.
- Do not use APIs, hidden JSON endpoints, or scraping shortcuts outside the browser tool.
- Price is not enough; capture trust, conditions, and caveats.
- The final answer should help the user choose, not just browse.
- Read `category-playbooks.md` when the product category changes how much price should matter.

## Baseline Discipline

- Treat Taobao as the baseline only when a Taobao price, URL, screenshot, or user-provided listing detail exists.
- If the user provides only a Taobao title, search against that identity but write `淘宝基准价未提供`.
- Do not claim the user should switch away from Taobao unless Taobao's visible or user-provided price is known.
- When the user provides the Taobao price, label it as user-provided unless verified in browser.

## Matching Score Reminders

Use the 100-point score from `SKILL.md`:
- brand: 25
- model / line / generation: 25
- variant and must-match specs: 20
- size / weight / count / packaging: 15
- seller or channel trust: 10
- evidence completeness: 5

Interpretation:
- 85-100: high, can drive recommendation
- 65-84: medium, caveated recommendation only
- below 65: low, reference/near-match only

Downgrade to low when the result has a critical mismatch such as different generation, capacity, count, refurbished status, unclear warranty, trial size, or unverified authenticity in a risk-sensitive category.

## Price Normalization Reminders

Before ranking, separate:
- headline/list price
- visible final or coupon-after price
- coupon/member/subsidy/group-buy/payment/region conditions
- unit basis such as per pack, per sheet, per 100g, per ml, per pair, or per item
- shipping, free-shipping threshold, installation, warranty, invoice, or delivery constraints

Use conservative comparison:
- Prefer unconditional visible price when promo eligibility is unclear.
- Treat member-only, group-buy, payment, and regional subsidy prices as conditional.
- For multi-pack daily goods, compare unit price and total quantity.
- For electronics, beauty, apparel, infant goods, medical/safety goods, and branded products, keep authenticity, warranty, and channel trust ahead of headline price.

## Category Shortcut

Use `references/category-playbooks.md` to decide which risk dominates:
- warranty and invoice for electronics/appliances
- authenticity, batch, and expiry for beauty/personal care
- unit price, pack count, and freshness for food/daily goods
- size, color, style code, and return policy for apparel/shoes/bags
- official authorization and safety evidence for baby/health/safety products
- ISBN/model/count and shipping for books/stationery/low-risk standard goods

When category risk and headline price disagree, mention the conflict and let category risk control recommendation strength.

## JD

- Usually supports standard web search and listing pages well.
- Prefer self-operated or official flagship listings when multiple near-identical results exist.
- Watch for coupon text, plus/member pricing, trade-in, bank/payment offers, and promotional banners.
- Distinguish list price from final promo price if both are shown.
- Treat 京东自营 and official flagship stores as stronger trust signals when prices are close.
- For electronics, appliances, beauty, infant goods, and regulated products, do not recommend a weaker channel solely because it is cheaper.

## Pinduoduo

- Web results may be noisier than JD.
- Watch for subsidy labels, group-buy wording, coupon claims, and strong promo framing.
- Matching confidence should be reduced when the seller, spec, or packaging is unclear.
- If the browser experience is limited, use a public search engine with site restriction, then open the visible result page.
- If the low price depends on 拼团 or 百亿补贴, call that out explicitly in the final recommendation.
- Reduce recommendation strength when seller trust is unclear, even if the price looks excellent.
- A very low PDD price should be treated as a lead to verify, not as a conclusion, unless match and seller evidence are strong.

## Vipshop

- Results may lean toward branded discount inventory and variant-specific listings.
- Pay attention to size/color/version because discount channels often surface adjacent variants.
- If the exact match is missing, mark the result as `近似款` instead of treating it as the same SKU.
- Vipshop often wins on branded discounts but loses on exact spec coverage; do not overstate comparability.
- Treat limited stock, size gaps, color mismatch, and flash-sale timing as decision caveats.

## Evidence Standard

For each platform, aim to capture:
- title
- displayed price
- visible final price or promo condition
- variant/specification
- seller/store if visible
- URL
- matching score and reason
- a short matching note

When visible, also capture:
- official / self-operated / flagship status
- coupon or membership dependency
- subsidy / group-buy dependency
- shipping promise
- return / warranty / invoice / authenticity guarantee

Evidence quality gate:
- A listing should have title, price, spec/version, and URL before it can support a strong recommendation.
- If two or more of those are missing, downgrade confidence to low.
- Low-confidence candidates can be included, but they should not determine the final answer alone.

## Output Discipline

Use short, decision-friendly language.

Recommended summary fields:
- Taobao baseline status
- category strategy and buying posture
- lowest visible raw price
- lowest visible comparable price
- whether the comparison is apples-to-apples
- major caveats: variant mismatch, coupon dependency, seller difference, shipping difference, warranty/invoice difference, regional limitation
- recommended platform
- recommendation strength: strong / weak / reference only / cannot judge
- one-sentence reason the user should or should not switch away from Taobao
- final checks before buying: final payable price, address-based delivery, coupon eligibility, stock, warranty, and return policy
