---
name: taobao-shopping
slug: taobao-shopping
version: 2.0.0
homepage: https://clawic.com/skills/taobao-shopping
description: Navigate Taobao (淘宝) with expert shopping strategies, seller verification, public product search, reviews, price comparison, SKU risk checks, and cart-ready guidance. Safe default: public visible information only; login, address, checkout, order submission, and payment stay user-controlled.
metadata:
  clawdbot:
    emoji: "🛍️"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

# Taobao Shopping

Help users shop smarter on Taobao with expert strategies, seller verification, public product search, reviews, price comparison, SKU risk checks, and cart-ready guidance.

## When to Use

User wants to shop on Taobao (淘宝), China's largest C2C/B2C marketplace. Agent helps with product discovery, seller verification, price negotiation, and leveraging Taobao's vast variety while managing quality risks.

## Quick Reference

| Topic | File |
|-------|------|
| Marketplace guide | `references/marketplace-guide.md` |
| Output patterns | `references/output-patterns.md` |
| Browser workflow | `references/browser-workflow.md` |

## Capabilities

### Supported Operations (v2.0)

| Operation | Auth Required | Description |
|-----------|---------------|-------------|
| **Search** | Optional | Search products, filter by price/rating/brand |
| **Browse** | Optional | Browse categories, trending items, recommendations |
| **Product Detail** | Optional | View specs, images, pricing, promotions |
| **Compare** | Optional | Compare prices across sellers/variants |
| **Cart Guidance** | User-controlled | Explain how to add the confirmed SKU manually or stop before changing cart state. |
| **Visible Coupon Notes** | No | Summarize visible coupon/promo terms; account-only coupons are user-only. |
| **Address / Checkout / Order Preview** | User-only | Do not select address, enter checkout, submit order, or generate private order state. |
| **Payment** | User-only | User must complete payment manually. |

**Important**: Default operation stops before login, cart changes, checkout, address selection, order submission, and payment. User retains full control over private account state and purchase execution.

## Workflow

### Phase 1: Discovery (Agent-Assisted)
1. **Search** - Agent searches Taobao for target product
2. **Filter & Sort** - Apply filters (price range, rating, brand, 天猫优先)
3. **Compare** - Agent compares top 3-5 options across sellers
4. **Reviews** - Agent reads user reviews, extracts common pros/cons
5. **Price Analysis** - Agent checks current price, promotions, coupon availability

### Phase 2: Selection (Agent-Assisted)
1. **Product Detail** - Agent opens selected product page
2. **Variant Selection** - Confirm color, size, configuration
3. **Seller Verification** - Confirm 天猫/企业店/个人店 status
4. **Final Price Check** - Calculate 到手价 after all discounts

### Phase 3: User Handoff
1. **Cart-ready guidance** - Agent summarizes the confirmed SKU, visible price, seller risk, and promo caveats.
2. **Manual checks** - User verifies final payable amount, address-based delivery, coupon eligibility, stock, return policy, invoice/warranty, checkout, order submission, and payment.

**Agent Boundary**: Stops before login-required account state, address selection, checkout, final order submission, and payment.

## Core Rules

### 1. Taobao Store Types Decoded

Understanding Taobao's ecosystem is crucial for safe shopping:

| Store Badge | Chinese | Trust Level | Best For |
|-------------|---------|-------------|----------|
| **Tmall** | 天猫/天猫旗舰店 | ⭐⭐⭐⭐⭐ | Brand authenticity |
| **Tmall Global** | 天猫国际 | ⭐⭐⭐⭐⭐ | Imported goods |
| **Enterprise** | 企业店铺 | ⭐⭐⭐⭐☆ | Verified business |
| **Personal Crown** | 个人皇冠店 | ⭐⭐⭐☆☆ | Experienced seller |
| **Personal Regular** | 普通个人店 | ⭐⭐☆☆☆ | Price hunting |

**Priority Order:** 天猫旗舰店 > 天猫 > 企业店 > 皇冠店 > 普通店

### 2. The Tmall Advantage

**Why Tmall Wins:**

| Factor | Tmall | Personal Store |
|--------|-------|----------------|
| Authenticity | Brand direct/authorized | Varies |
| Return service | 7-day no-reason | Varies by seller |
| Customer service | Brand handles | Seller handles |
| Fees transparency | Clear | May have hidden costs |
| Price protection | Available | Rare |

**识别天猫:**
- Look for "天猫" red badge
- URL contains "tmall.com"
- Higher commission = better service

### 3. Price Optimization

**Understanding Taobao Pricing:**

| Price Label | Meaning | Strategy |
|-------------|---------|----------|
| **原价** | Listed "original" | Often inflated |
| **券后价** | After coupon | Real baseline |
| **满减价** | After threshold discount | Stack with coupons |
| **到手价** | Final after all discounts | Real cost |

**Best Deal Formula:**
```
Final Price = 标价 - 店铺券 - 平台券 - 满减 - 淘金币 - 支付优惠
```

**Timing for Best Prices:**
- **618** (June 1-18) - Mid-year mega sale
- **双11** (Nov 11) - Singles Day
- **双12** (Dec 12) - Year-end clearance
- **38女王节** (Mar 8) - Women's categories
- **99划算节** (Sep 9) - Autumn sale

### 4. Seller Verification

**Check Before Buying:**

| Metric | Green Flag | Red Flag |
|--------|------------|----------|
| **Rating** | 4.8+ | Below 4.6 |
| **Reviews** | Recent positive | Old or negative |
| **Sales** | High volume | Zero or low |
| **Store Age** | 3+ years | New store |
| **Return Rate** | Low | High |
| **Description** | Detailed | Vague/copy-paste |

### 5. Returns & Protection

**Taobao Consumer Protection:**

| Feature | Coverage | Notes |
|---------|----------|-------|
| 7-day return | Most items | Unused, tags on |
| 运费险 | Optional | Buy for return shipping |
| 假一赔四 | Tmall | Counterfeit protection |
| 极速退款 | High credit | Instant refund |
| 晚到必赔 | Some items | Late delivery compensation |

## Agent Execution Guide

### When User Says "帮我买..."

Follow this escalation path:

```
User: "帮我买 iPhone 手机壳"
  ↓
Step 1: Confirm Intent
  "我来帮你搜索 iPhone 手机壳，对比选项，核对店铺和规格。
   登录、加购、结算、提交订单和支付需要你手动完成。"
  ↓
Step 2: Discovery Phase (No login required)
  - Search Taobao for "iPhone 手机壳"
  - Filter: 天猫优先, sort by sales
  - Compare top 3 options
  - Read reviews for each
  - Present comparison table
  ↓
Step 3: Selection Phase (No login required)
  - User picks one option
  - Agent opens product page
  - Confirm variant/specs
  - Show final price
  ↓
Step 4: Handoff (User-controlled)
  "我已经整理好下单前检查项：
   [商品/SKU/店铺/价格/风险摘要]
   
   👉 请手动完成：
   1. 打开淘宝 App
   2. 核对规格、券后价和库存
   3. 核对地址、运费、退换和发票/保修
   4. 自行决定是否加入购物车、结算、提交订单并支付"
```

### Browser Automation Rules

**Always announce before action:**
- "正在搜索..."
- "正在打开商品页面..."
- "正在读取用户评价..."
- "正在加入购物车..."

**Snapshot key information:**
- Product title, price, promotions
- Store type badge
- Rating and review count
- Available variants
- Visible coupon information
- Delivery estimate

**Stop conditions:**
- Before any payment screen
- When CAPTCHA appears (hand to user)
- When login or account state is required
- When price differs significantly from expected

### Login Handling

**Manual mode (default, no login)**
```
Agent provides:
- Exact search keywords
- Product links
- Visible coupon/promo notes
- Step-by-step manual instructions
User executes manually
```

## Quality Bar

### Do:
- Focus on seller verification and store type
- Explain trade-offs clearly (variety vs. consistency)
- Stay honest about not doing account-state operations
- Always announce before browser actions
- Snapshot key information for user review
- Stop before any payment screen
- Stop when login, cart, address, checkout, order, or payment appears

### Do Not:
- Pretend to log in or use account-state data
- Claim to retrieve orders, coupons, or account data without login
- Store cookies or user data
- Present heuristics as guaranteed outcomes
- Complete payment for user
- Enter checkout, address, final order, or payment flows

## Common Traps

- **Assuming low price = best deal** → Check seller rating first
- **Ignoring store type** → 天猫 vs. personal store matters
- **Not checking reviews** → Photos reveal quality issues
- **Missing coupon stacking** → Multiple discounts available
- **Buying from new sellers** → Higher risk, less protection
- **Forgetting 运费险** → Cheap insurance for returns
- **Rushing without comparison** → Same item, different prices
- **Agent overstepping** → Never complete payment for user

## Taobao vs Competitors

| Factor | Taobao | JD | Tmall |
|--------|--------|-----|--------|
| Variety | Best | Good | Good |
| Price | Lowest | Higher | Medium |
| Authenticity | Varies | Best | Good |
| Shipping | Varies | Fastest | Good |
| Electronics | Riskier | Best | Good |
| Fashion | Best choice | Limited | Good |

**When to Choose Taobao:**
- Fashion and accessories
- Hard-to-find items
- Price-sensitive purchases
- Custom/handmade goods
- When variety matters most

## Related Skills

Install with `clawhub install <slug>` if user confirms:
- `jingdong` - JD.com shopping
- `jd-shopping` - Alternative JD guide
- `tianmao` - Tmall shopping
- `pdd` - Pinduoduo shopping
- `vip` - VIP flash sales

## Feedback

- If useful: `clawhub star taobao-shopping`
- Stay updated: `clawhub sync`
