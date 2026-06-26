---
name: taobao-competitor-analyzer
description: "Taobao price and competitor comparison assistant. Input a Taobao title/link or product need; compare JD, PDD, and Vipshop using browser-visible evidence, normalize prices, score same-item confidence, and output where to buy. Safe boundary: no login, no order submission, no payment."
---
# Taobao Competitor Analyzer

Compare a Taobao product with the same or closest-matching listings on 京东、拼多多、唯品会 using the browser tool only. Work from a product name, Taobao title, link, screenshot, or user-provided baseline details. Return a compact purchase decision with visible price evidence, normalized comparability, match score, category-aware platform fit, recommendation strength, and risk notes.

What makes this skill useful:
- It compares comparable items instead of chasing misleading low prices.
- It separates Taobao baseline price from competitor prices.
- It normalizes price by spec, quantity, shipping, and promo conditions before ranking.
- It scores same-item confidence before making a buying recommendation.
- It applies category-specific risk thresholds instead of treating shoes, phones, skincare, and paper towels the same way.
- It explains whether a lower price depends on coupons, membership, subsidy, or group-buy.
- It ends with a clear buy / wait / avoid recommendation instead of just a table.

## When To Use

Use this skill when the user is effectively asking:
- 这件淘宝商品别的平台多少钱
- 有没有同款或更划算的平台
- 京东 / 拼多多 / 唯品会 哪个更值得买
- 这几个平台价格差这么多正常吗
- 帮我做一个同款比价和购买建议
- 这个淘宝商品换平台买值不值
- 同样价差下哪个平台风险更低

The skill should optimize for purchase decisions, not raw data collection.

## Commerce Matrix

This skill is the cross-platform comparison node in the shopping matrix.

Prefer nearby skills when the task is narrower:
- `taobao-shopping` for Taobao-only listing and seller evaluation
- `jd-shopping` for trust-first self-operated buying
- `pdd-shopping` for low-price and subsidy-first buying
- `tianmao` for flagship-store and authenticity-first buying
- `vip` for branded discount and flash-sale buying
- `alibaba-shopping` when the user first needs to choose between Taobao, Tmall, and 1688

## Taobao Baseline Bridge

Use `taobao-shopping` first, or apply its same discipline yourself, when the Taobao side is not yet clear.

Before cross-platform comparison, establish the Taobao baseline:

- exact product identity
- selected SKU attributes
- visible or user-provided Taobao price
- store type and seller trust cue
- coupon / membership / threshold condition
- return, warranty, invoice, authenticity, or delivery caveat when relevant

If the user only provides a Taobao title with no price or listing evidence, this skill can compare competitor visible offers, but it must not claim the user should switch away from Taobao. Write `淘宝基准价未提供`.

If the user's real question is only "is this Taobao listing trustworthy?", stay in or route to `taobao-shopping` instead of broadening into JD/PDD/Vipshop.

## Workflow

1. Normalize the Taobao baseline.
   - Extract product identity: brand, model / series, variant, size / spec / count, color / flavor / version, packaging, and must-match attributes.
   - Record the Taobao price only if the user provides it or it is browser-visible.
   - If no Taobao price is available, write `淘宝基准价未提供` and do not imply whether switching platforms saves money versus Taobao.
2. Classify the product category and buying posture.
   - Pick the closest category from `references/category-playbooks.md`.
   - Infer whether the user is price-first, trust-first, speed-first, exact-variant-first, or research-first.
   - If the category or posture would change the recommendation and cannot be inferred, ask one short follow-up.
3. If the input is only a Taobao-style long title, compress it into the smallest searchable core:
   - brand
   - model / series
   - size / spec / count
   - key variant
4. Search the exact or lightly simplified keyword on:
   - 京东
   - 拼多多
   - 唯品会
5. Stay in browser-driven flows only. Do not call site APIs, hidden JSON endpoints, app-only interfaces, or unofficial scrapers.
6. Extract the top relevant visible results from each site.
7. Normalize each visible price into a comparable basis before ranking.
8. Score same-item comparability before judging price.
9. Apply category playbook gates before recommending a lower-price platform.
10. Decide with recommendation strength: `强推荐`, `弱推荐`, `仅供参考`, or `无法判断`.
11. End with a concrete recommendation: buy on which platform, stay with Taobao, wait, or avoid for now.

## Input Rules

Require a product identity as input.

Prefer one of these inputs:
- Taobao product link, screenshot, title, or visible listing details
- precise product name
- brand + model + spec
- product name plus intended use, if there are multiple variants
- Taobao visible price or expected Taobao budget, if the user wants a switch / stay decision
- category cue, such as phone, skincare, baby formula, shoes, snacks, tissue, appliance, or supplement
- buying priority, such as lowest price, official/authenticity, fast delivery, easy returns, warranty/invoice, exact color/size, or competitor research

If the product name is too broad, ask one short follow-up to narrow it, for example:
- brand
- model
- size/specification
- package count
- flavor/color/version
- whether the user prioritizes lowest price, authenticity/after-sales, or delivery speed

Good inputs:
- `Apple AirPods Pro 2`
- `维达抽纸 3层 100抽 24包`
- `耐克 Air Zoom Pegasus 41 男款`
- `这个淘宝价 129，帮我看看京东拼多多唯品会有没有更值的同款`

Weak inputs that need clarification:
- `纸巾`
- `耳机`
- `运动鞋`

If the user pastes a very long Taobao title, do not ask them to rewrite it unless it is truly ambiguous. You should clean and normalize it yourself first.

## Taobao Baseline Rules

Treat Taobao as the baseline only when baseline evidence exists.

Capture when visible or user-provided:
- Taobao title
- Taobao displayed price
- coupon-after, membership, or promo wording
- spec / version / count / packaging
- seller/store type
- shipping or delivery note
- URL or screenshot context

If the baseline is only a title:
- compare competitor platforms against the title identity
- say `淘宝基准价未提供，本次只比较竞品平台可见结果`
- avoid saying `值得从淘宝换平台` unless the user later provides Taobao price or visible Taobao evidence

If the user provides a Taobao price:
- call it `用户提供的淘宝基准价`
- compare it to normalized competitor prices
- flag that final payable price may change with address, coupon eligibility, account status, and stock

## Browser Execution Rules

- Prefer the isolated OpenClaw browser unless the user explicitly asks to use their Chrome tab.
- Start with one tab per site when practical.
- Re-snapshot after navigation or major DOM changes.
- If a site shows login walls, anti-bot interstitials, region prompts, or app-download overlays, use the visible web result if possible and mention the limitation.
- If a site blocks access completely, report it instead of trying to bypass it.
- Do not fabricate missing prices.
- Prefer visible search/listing pages over deep product pages when one platform is unstable.
- Capture enough evidence to justify the recommendation, not just enough to fill a table.

## Search Targets

Use the standard web search pages when possible:

- 京东: search for the product name on jd.com
- 拼多多: search for the product name on pinduoduo.com or the visible web listing/search experience available in browser
- 唯品会: search for the product name on vip.com

If direct site search is unstable in browser, use a public search engine query constrained to the site, then open the most relevant visible result. Example pattern:
- `site:jd.com 商品名`
- `site:pinduoduo.com 商品名`
- `site:vip.com 商品名`

Still use browser navigation for the actual evidence collection.

## Category And Preference Routing

Read `references/category-playbooks.md` when the product category is obvious or when price, trust, warranty, freshness, sizing, or authenticity can change the decision.

Classify the category before final recommendation:
- `数码/家电`: model, version, warranty, invoice, self-operated/official channel, installation, trade-in, refurbished/open-box risk.
- `美妆/个护`: official channel, batch/expiry, sample/trial size, authenticity, sealed packaging, return limits.
- `食品/日用品`: unit price, pack count, shelf life, shipping threshold, heavy-item delivery, commodity substitutability.
- `服饰/鞋包`: exact color/size/style code, season/version, authenticity, return convenience, stock by size.
- `母婴/健康/安全`: official/authorized channel, registration/approval when relevant, expiry, warranty, return policy, safety risk.
- `图书/文具/低风险标品`: ISBN/model/count, shipping, bundle contents, seller reliability, unit price.
- `不确定/混合`: say which playbook you used and why.

Infer buying posture:
- `低价优先`: maximize normalized savings, but only after match and risk gates pass.
- `正品/售后优先`: prefer official, self-operated, flagship, authorized, invoice, warranty, and return clarity.
- `速度优先`: prefer visible delivery promise and stable fulfillment even if not the cheapest.
- `精确款优先`: prioritize exact variant, size, color, model, batch, or package count.
- `研究优先`: broaden to near matches and substitutes, but clearly separate them from exact matches.

Use category-specific price-delta thresholds:
- For high-risk or warranty-heavy goods, require a meaningful saving before recommending a weaker channel.
- For low-risk commodities, a clear normalized unit-price win can justify switching more easily.
- If the category playbook conflicts with the lowest visible price, the playbook wins.

## Matching Score

Treat listings as comparable only when the core attributes align.

Score each candidate out of 100:
- Brand: 25
- Product line / model / generation: 25
- Variant and must-match specs: 20
- Size / weight / count / packaging: 15
- Seller/channel trust when relevant: 10
- Evidence completeness: 5

Use these match bands:
- `高` / 85-100: same item or same SKU-equivalent listing; price comparison can drive the recommendation.
- `中` / 65-84: near match with one explainable difference; include it with caveats, and make only a weak recommendation unless the tradeoff is obvious.
- `低` / below 65: reference or substitute only; do not call it cheaper than Taobao or cheaper than another exact match.

Force the match band to `低` when any critical mismatch appears:
- different model, generation, storage, capacity, size, flavor, color, or pack count
- refurbished / open-box / parallel import when the baseline is standard new domestic stock
- trial/sample size compared with regular size
- unclear warranty or authenticity for safety-sensitive or high-counterfeit-risk categories
- missing enough information to confirm the listing is the same item

Apply category overrides:
- For high-counterfeit, safety-sensitive, or warranty-heavy categories, reduce the score when official/self-operated/authorized evidence is missing.
- For low-risk commodities, do not over-penalize seller/channel differences when the spec, count, and unit basis are clear.
- For apparel and shoes, exact size, color, style code, and return policy can matter as much as headline model name.
- For beauty, baby, food, and supplements, expiry, batch, sealed packaging, and authenticity cues can be critical match evidence.

If there is no close match on a platform:
- say `未找到足够接近的同款`
- optionally include the nearest visible alternative, clearly labeled as `近似款` or `替代款`

## Price Normalization Rules

Do not rank prices until they are normalized.

For each candidate, separate these fields when visible:
- `标价`: the headline displayed price
- `可见到手价`: coupon-after, subsidy, member, or promo price, only when the condition is visible
- `优惠条件`: coupon, membership, group-buy, payment method, limited-time sale, regional subsidy, or account qualification
- `单位基准`: per item, per pack, per 100g, per ml, per sheet, per pair, or another meaningful unit
- `运费/门槛`: shipping fee, free-shipping threshold, installation fee, or delivery limitation

Use the most conservative comparable price:
- Prefer unconditional visible price when coupon eligibility is unclear.
- Use coupon-after price only when the page makes the condition visible and likely attainable.
- Keep member-only, group-buy, subsidy, bank-card, and region-dependent prices separate from normal prices.
- For multi-pack goods, compare unit price and total package value, not only headline price.
- For electronics, apparel, beauty, and branded goods, do not let a lower price override warranty, channel, authenticity, or version mismatch.
- Use the category playbook's preferred unit basis when available.

Never recommend a cheaper platform when the cheaper listing is only cheaper because of:
- lower specification
- different quantity or packaging
- unclear seller trust
- member-only or coupon-after price not available to most users
- group-buy requirement the user may not want
- missing shipping, installation, warranty, or invoice cost

## Decision Rules

Use this order of judgment:

1. Is the candidate the same item or only a near match
2. Is the visible price directly comparable after normalization
3. Does the category playbook allow price to dominate, or should trust/warranty/authenticity/freshness/sizing dominate
4. Is the seller/store trust level similar
5. Are coupon, membership, subsidy, or group-buy conditions required
6. Are shipping speed, warranty, invoice, return rights, and after-sales meaningfully different
7. Does the user's likely preference favor lowest price, trust, delivery speed, exact variant availability, or broad research

Recommendation strength:
- `强推荐`: high match, clear normalized price, trustworthy seller/channel, and the advantage is material.
- `弱推荐`: high or medium match, but with one meaningful caveat such as coupon dependency, seller difference, delivery uncertainty, category risk, or missing Taobao baseline price.
- `仅供参考`: partial evidence, noisy results, medium/low match, or blocked platform pages.
- `无法判断`: no comparable listings, missing baseline for the user question, or evidence too incomplete to support a purchase decision.

Do not use one universal price threshold:
- A 5-8% saving may be weak for a phone if warranty/channel is worse.
- A 10-20% normalized unit-price saving may matter for low-risk daily goods.
- Any saving can be irrelevant if the exact size, color, model, expiry, or warranty does not match.

If Taobao is not actually the best option, say so directly. If none of the results are truly comparable, explicitly say `当前不适合做强结论`.

## What To Capture Per Site

Capture only information visible on the page. Prefer the first 1-3 relevant results.

For each selected listing, collect when visible:
- platform
- title
- displayed price
- visible final/promo price and condition
- unit price or normalized price basis, when applicable
- package/specification
- store/seller name
- delivery or shipping note
- URL
- match score and band
- category and buying-posture note when it changes the conclusion
- confidence: high / medium / low
- note about why it matches or why it is only approximate

Also capture, when visible and relevant:
- official/self-operated/flagship indicator
- coupon or subsidy dependency
- group-buy requirement
- delivery speed or shipping promise
- return, warranty, invoice, or authenticity guarantee

Evidence quality gate:
- A candidate should include at least title, displayed price, spec/version, and URL to drive a recommendation.
- If two or more of those fields are missing, downgrade confidence to low.
- Low-confidence candidates can appear in the table but cannot be the sole basis for `强推荐`.

## Output Format

Return a decision first, then the evidence table.

Start with a short verdict block:

- `淘宝基准`: visible/user-provided price, or `淘宝基准价未提供`
- `品类策略`: category playbook used and why
- `购买偏好`: inferred or user-provided priority
- `推荐平台`: platform or `暂不建议换平台`
- `推荐强度`: `强推荐` / `弱推荐` / `仅供参考` / `无法判断`
- `最低可见可比价`: platform + normalized price basis, only among comparable items
- `值不值得换平台`: yes / no / depends, with one sentence
- `主要原因`
- `风险点`
- `核验时间`: include date/time or say browser-visible at time of checking

Then return a concise comparison table and short notes.

Use a table like this:

| 平台 | 商品标题 | 标价 | 可见到手价/条件 | 单位价/基准 | 规格/版本 | 店铺 | 匹配分 | 匹配度 | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|
| 淘宝 | ... | ¥... | ... | ... | ... | ... | 基准 | 基准 | 用户提供/页面可见 |
| 京东 | ... | ¥... | ... | ... | ... | ... | 92 | 高 | 同品牌同规格 |
| 拼多多 | ... | ¥... | ... | ... | ... | ... | 78 | 中 | 规格接近，包装不同 |
| 唯品会 | ... | ¥... | ... | ... | ... | ... | 52 | 低 | 仅找到近似款 |

Then add:
- `最低可见价`: platform and raw visible price
- `最低可比价`: platform and normalized comparable price
- `可比性判断`: high / medium / low, with reason
- `证据完整性`: state whether each recommendation-driving row has title, price, spec/version, and URL
- `品类判断`: why this category should prioritize price, trust, delivery, warranty, freshness, authenticity, or exact variant
- `风险提示`: differences in package, seller, promo timing, membership price, shipping, warranty, invoice, or coupon requirements
- `购买建议`: 直接买 / 可等等 / 只建议在某平台买 / 暂不建议下单
- `下单前核对`: final payable price, address-based delivery, coupon eligibility, stock, warranty, and return policy

## Interpretation Rules

- Do not claim a platform is cheaper unless the compared items are materially comparable.
- Separate `标价` from coupon-after price when the page makes that distinction.
- Mention when a price may depend on membership, flash sale, subsidy, payment method, group-buy, or region.
- If search results are noisy, prefer accuracy over completeness.
- If the Taobao baseline price is missing, do not say the user should switch away from Taobao; say which competitor has the best visible comparable offer.
- If the Taobao baseline is not actually the best option, say so directly.
- If category-specific risk outweighs the price difference, recommend staying with the safer channel or waiting.
- If none of the results are truly comparable, explicitly say `当前不适合做强结论`.
- Do not issue `强推荐` unless the recommendation-driving listing includes at least title, price, spec/version, URL, and enough seller/channel evidence for the category risk.
- If the user seems purchase-ready, optimize the answer for actionability: where to buy, what to verify before paying, and what tradeoff they are accepting.

## Example Requests

- `帮我查一下“德芙黑巧克力 84g”在京东、拼多多、唯品会的价格`
- `对比一下“iPhone 16 Pro 256GB”在几个平台上的可见报价`
- `把这个淘宝商品名拿去京东、拼多多、唯品会搜同款，做个价格表`
- `这个淘宝商品有没有更便宜但靠谱的平台`
- `帮我判断这件商品有没有必要从淘宝换到京东买`
- `淘宝价 129，这个商品换平台买值不值`
- `别只比价，也告诉我哪个平台更值得下单`

## Failure Handling

If one or more sites cannot be accessed or searched reliably, still return a partial result and list:
- which site failed
- what was attempted
- whether the failure was due to login wall, anti-bot page, timeout, app-only flow, or missing web search results

If evidence is partial, downgrade recommendation strength.

Do not fill missing evidence with guesses. Use:
- `未见明确价格`
- `未见规格`
- `未见店铺信息`
- `无法确认同款`

## Resource

- Read `references/site-notes.md` when you need execution reminders for JD, Pinduoduo, and Vipshop search behavior, evidence standards, normalized pricing, and recommendation gates.
- Read `references/category-playbooks.md` when category, user preference, authenticity, warranty, freshness, sizing, safety, or platform fit can change the recommendation.


## P1 Safety Boundaries

- Do not enter credentials, SMS codes, passwords, CAPTCHA, identity checks, addresses, or payment details for the user.
- Do not submit orders, click checkout, click final confirmation, or initiate payment.
- Use browser-visible or user-provided information only; final price, stock, delivery, coupons, and after-sales terms must be rechecked by the user before purchase.
