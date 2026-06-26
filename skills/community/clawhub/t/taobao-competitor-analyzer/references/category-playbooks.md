# Category Playbooks

## Goal

Use these playbooks after normalizing the Taobao baseline and before making the final recommendation. The goal is to avoid one-size-fits-all price sorting. A lower price means different things for phones, skincare, baby goods, shoes, snacks, and paper towels.

## How To Use

1. Classify the product into the closest category.
2. Infer the user's buying posture: low price, trust/after-sales, delivery speed, exact variant, or research.
3. Apply the category's must-check attributes and risk gates.
4. Decide whether the price gap is large enough to overcome category risk.
5. State the playbook in the verdict as `品类策略`.

If the category is unclear, write the assumption and keep recommendation strength at `弱推荐` or lower.

## Buying Postures

### Low Price First

- Use normalized unit price after matching gates pass.
- Prefer unconditional visible prices over conditional coupon/member/group-buy prices.
- Strong recommendations still need high match and enough seller/channel evidence.

### Trust And After-Sales First

- Prefer official, self-operated, flagship, or authorized channels.
- Treat invoice, warranty, returns, and authenticity evidence as decision drivers.
- A cheaper weak-channel listing usually becomes `弱推荐` or `仅供参考`.

### Speed First

- Prefer visible delivery promise, local stock, self-operated logistics, and stable fulfillment.
- Downgrade group-buy, pre-sale, limited stock, and unclear shipping.
- If delivery is address-dependent and not visible, include it in `下单前核对`.

### Exact Variant First

- Prioritize exact model, color, size, flavor, version, pack count, batch, and bundle contents.
- Do not treat near matches as cheaper exact matches.
- For apparel, shoes, beauty, and electronics, variant mismatch usually blocks `强推荐`.

### Research First

- Include exact matches, near matches, and substitutes in separate groups.
- Do not rank substitutes against exact matches as if they are identical.
- Use this mode for marketplace research, category scans, and competitor mapping.

## Electronics And Appliances

Examples: phones, headphones, laptops, cameras, routers, appliances, smart devices.

Must check:
- exact model, generation, storage/capacity, color, region/version, bundle, and warranty
- new vs refurbished/open-box/parallel import
- official/self-operated/authorized channel
- invoice, warranty, installation, return policy, trade-in, and delivery timing

Platform fit:
- JD is often stronger when self-operated, official, invoice, warranty, fast delivery, or installation matters.
- PDD can be considered when subsidy/official evidence is visible and the SKU is exact.
- Vipshop is usually weaker for exact electronics coverage unless the listing is clearly official and exact.

Recommendation gate:
- Do not recommend a weaker channel for small savings.
- Require high match and clear warranty/channel evidence for `强推荐`.
- If savings are modest and JD/Taobao official support is stronger, recommend staying with the safer channel or waiting.

## Beauty And Personal Care

Examples: skincare, perfume, makeup, haircare, oral care, personal care devices.

Must check:
- exact product line, volume, shade, scent, set contents, version, and packaging
- official/flagship/authorized seller cues
- batch, expiry, sealed packaging, import/domestic version, sample/trial size
- return limits and authenticity guarantee

Platform fit:
- Tmall/Taobao flagship, JD official/self-operated, and brand official channels are stronger trust signals.
- Vipshop can be attractive for branded discount inventory when exact variant and channel confidence are visible.
- PDD low prices need extra caution unless official/subsidy/channel evidence is clear.

Recommendation gate:
- Do not let a low price override unclear authenticity, sample size, expiry, or seller trust.
- For branded skincare and perfume, weak-channel savings should usually be `仅供参考`.
- If exact shade/volume/set differs, mark as near match or substitute.

## Food And Daily Goods

Examples: snacks, drinks, rice/oil, tissue, detergent, pet food, household consumables.

Must check:
- unit count, weight, volume, flavor, pack count, expiration/shelf life, and packaging
- unit price basis such as per 100g, per bottle, per pack, per sheet, or per item
- shipping fee, free-shipping threshold, heavy-item delivery, and regional stock
- brand and seller reliability for food, pet food, and ingestible items

Platform fit:
- PDD can win on low-risk commodities when spec, count, and unit basis are clear.
- JD can win when speed, heavy-item delivery, after-sales, or self-operated reliability matters.
- Vipshop is less central unless it has exact branded inventory or bundle discounts.

Recommendation gate:
- A clear normalized unit-price win can justify switching for low-risk daily goods.
- For food, pet food, or anything ingested, expiry and seller reliability still matter.
- Do not compare different pack counts without unit price.

## Apparel, Shoes, And Bags

Examples: clothing, sneakers, sports shoes, bags, accessories.

Must check:
- brand, style code/model, size, color, gender, season/version, material, and bundle/accessories
- official/authorized seller when counterfeiting risk is meaningful
- return/exchange policy, size availability, stock, and authenticity guarantee

Platform fit:
- Vipshop can be strong for branded discount inventory when size/color/style code match exactly.
- JD/Tmall/official channels are stronger when authenticity and returns matter.
- PDD and generic Taobao listings require caution for branded goods unless evidence is strong.

Recommendation gate:
- Size/color mismatch usually means near match, not same item.
- If returns are unclear for apparel/shoes, downgrade recommendation strength.
- Do not recommend a cheaper listing for branded shoes/bags without strong authenticity evidence.

## Baby, Health, And Safety

Examples: infant formula, baby products, supplements, medicine-adjacent goods, helmets, batteries, chargers, appliances with safety implications, medical devices.

Must check:
- official/authorized seller, registration/approval where relevant, batch, expiry, standard/certification, warranty, and return policy
- exact model/spec and safety certification
- do not provide medical claims or health guarantees

Platform fit:
- Prefer official, self-operated, flagship, authorized, or brand channels.
- Treat very low prices from unclear sellers as risk signals.
- PDD or marketplace third-party listings need unusually strong evidence to be more than `仅供参考`.

Recommendation gate:
- Safety and authenticity override price.
- Do not issue `强推荐` for unclear-channel baby/health/safety goods.
- If evidence is weak, recommend official/self-operated channels or waiting.

## Books, Stationery, And Low-Risk Standard Goods

Examples: books, notebooks, pens, cables with low risk, small office supplies, simple accessories.

Must check:
- ISBN/model, edition, count, color, size, bundle contents, shipping, and seller reliability
- for books, distinguish正版,影印,二手,预售,套装, and different editions

Platform fit:
- PDD and Taobao can be reasonable for low-risk standard goods when listing details are clear.
- JD can be better for fast shipping, invoices, and standardized fulfillment.
- Vipshop is usually relevant only for branded stationery or limited discount inventory.

Recommendation gate:
- Price can matter more once edition/model/count are confirmed.
- Do not compare different editions, bundle counts, or used/new condition as exact matches.

## Unknown Or Mixed Category

Use this when the item does not fit cleanly.

Rules:
- State the assumed category.
- Use the strictest relevant risk gate among possible categories.
- Keep recommendation at `弱推荐` or lower unless evidence is very strong.
- Ask one short follow-up if the category would materially change the purchase advice.
