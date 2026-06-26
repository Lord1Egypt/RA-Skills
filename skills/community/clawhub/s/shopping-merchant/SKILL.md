---
name: shopping-merchant
description: Evaluate which merchant type a shopper should trust on Chinese ecommerce platforms
version: 1.0.0
tags: shopping, ecommerce, trust, platform-comparison, china, consumer-protection
---

# Shopping Merchant

Evaluate which merchant type a shopper should trust on Taobao, JD, Tmall, PDD, Douyin, Xiaohongshu, and other Chinese ecommerce platforms. Use when choosing between flagship store, authorized store, self-operated retail, third-party seller, factory-direct shop, discount outlet, or marketplace shop, and weighing authenticity, after-sales, warranty, shipping reliability, and price risk.

## Usage Scenarios

### Scenario 1: Brand vs Third-Party for Electronics
**User input:** "同一款耳机，京东自营贵 80，第三方便宜，怎么选？"
**Expected output:** The skill classifies the product (electronics, high risk), compares merchant types (self-operated retail vs marketplace third-party), and recommends: for high-value electronics, the self-operated retailer's warranty and return policy are worth the ￥80 premium. Explains what risks the cheaper seller carries (counterfeit risk, harder returns, inconsistent warranty) and when the third-party might still be acceptable (verified flagship store, high ratings, good return policy).

### Scenario 2: Skincare Merchant Selection
**User input:** "护肤品买旗舰店、授权店还是普通店？"
**Expected output:** The skill categorizes cosmetics as high risk due to authenticity sensitivity. Recommends official flagship store as the strongest choice. Explains that authorized stores are acceptable if verified, but ordinary marketplace stores carry significant counterfeit risk for this category. Provides trust-adjusted recommendation with clear risk tiers.

### Scenario 3: Platform Price Gap Assessment
**User input:** "拼多多工厂店比天猫旗舰店便宜很多，风险在哪里？"
**Expected output:** The skill explains the difference between factory-direct (PDD) and official flagship store (Tmall). Identifies risks: authenticity guarantee differences, after-sales support, return policy, warranty coverage. Evaluates based on product category and value. Gives a final recommendation: for low-risk items (household goods, accessories), the lower price may be acceptable; for high-risk items, the premium for trust is justified.
### Scenario 4: 夜市摆摊选品
**User input:** "打算去大学城夜市摆摊卖点吃的，夏天到了，卖什么好？启动资金只有两三千。"
**Expected output:** 推荐低成本高利润的夜市小吃品类：冰粉/手搓冰粉（成本3元卖12元）、暴打柠檬茶（成本2元卖10元）、烤肠/淀粉肠（成本1元卖4元）。建议先去目标夜市蹲点两周，记录人流量和现有摊位品类，避免直接竞争。推荐1688或义乌购进原料。强调食品经营许可证和卫生要求。

## Best Use Cases

- Decide whether to buy from 旗舰店, 专卖店, 专营店, 自营, 第三方, 工厂店, or outlet
- Compare merchant trust when two stores sell the same item at different prices
- Decide whether the cheaper seller is acceptable for low-risk products
- Choose safer merchant types for electronics, cosmetics, baby products, medicine-adjacent products, luxury goods, and high-value appliances
- Explain after-sales and warranty trade-offs before checkout
- Build a shopper-facing trust-adjusted recommendation, not a seller onboarding plan

## Workflow

1. Identify the purchase context.
   - Understand what the user is buying and how risky the purchase is.
   - If needed, ask one short clarifying question about product value, authenticity sensitivity, or after-sales importance.

2. Classify the merchant decision.
   Common merchant choices include:
   - official flagship store
   - brand-authorized store
   - self-operated retail
   - marketplace third-party seller
   - factory-direct or wholesale-style seller
   - discount outlet or clearance channel

3. Judge the trade-off.
   Weigh:
   - authenticity confidence
   - return and warranty expectations
   - shipping and fulfillment stability
   - seller quality consistency
   - price gap versus risk gap
   - category risk and product value
   - whether the buyer can inspect or return the item easily

4. Give a merchant recommendation.
   - Say which merchant type is the strongest fit.
   - Explain when paying more for a stronger merchant is justified.
   - Explain when a lower-trust merchant is still acceptable.

## Risk Tiers

- **Low risk**: household consumables, simple accessories, low-price repeat purchases
- **Medium risk**: clothing, small appliances, hobby gear, gifts, imported snacks
- **High risk**: electronics, cosmetics, baby goods, health-adjacent products, luxury goods, expensive appliances

For high-risk products, prefer authenticity and after-sales reliability over small price differences. For low-risk products, a cheaper third-party or factory-direct merchant may be reasonable if ratings, return policy, and product details look consistent.

## Output

Use this structure unless the user asks for something shorter:

### Best Merchant Type
State the strongest default choice.

### Why
List the main reasons.

### When a Cheaper Seller Is Still Fine
Explain when lower-trust sellers may still be acceptable.

### When to Pay More for Safety
Explain when stronger merchant trust is worth the premium.

### Final Advice
Give a direct merchant-selection recommendation.

## Quick Examples

```text
同一款耳机，京东自营贵 80，第三方便宜，怎么选？
```

```text
护肤品买旗舰店、授权店还是普通店？
```

```text
拼多多工厂店比天猫旗舰店便宜很多，风险在哪里？
```

## Quality bar

Do:
- optimize for trust-adjusted value, not raw price alone
- distinguish product-risk level from seller-risk level
- explain when stronger after-sales support matters
- be explicit about authenticity-sensitive purchases

Do not:
- treat all third-party sellers as equally risky
- assume the cheapest merchant is the best choice
- pretend to verify live store pages or account-only information
