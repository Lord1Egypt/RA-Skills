---
name: tianmao
version: 2.0.0
description: Help users decide when Tmall is the best choice for official-brand shopping, then assist with browser automation for search, flagship-store verification, reviews, coupons, and cart preparation. Use when the user wants to 买天猫、找官方旗舰店、看88VIP价、判断正品和值不值、比较品牌官方渠道, or needs a brand-authentic shopping workflow with stronger store-trust verification.
---

# Tianmao (天猫)

Help users shop smartly on Tmall, Alibaba's premium B2C platform with official flagship stores and brand authenticity guarantee.

What makes this skill useful:
- It is optimized for official flagship and brand-trust decisions.
- It helps the user answer whether Tmall is worth the premium over cheaper marketplaces.
- It is strongest when authenticity and official after-sales matter more than absolute lowest price.

## Commerce Matrix

This skill is the flagship-store and authenticity-first node in the shopping matrix.

Prefer nearby skills when the user's priority changes:
- `alibaba-shopping` when the user has not yet chosen between Taobao, Tmall, and 1688
- `taobao-shopping` when variety and flexible seller choice matter more than official stores
- `taobao-competitor-analyzer` for Taobao vs JD/PDD/Vipshop same-item comparison

## Capabilities

### v2.0 - Browser Automation Support

| Operation | Auth Required | Description |
|-----------|---------------|-------------|
| **Search** | Optional | Search products, filter by brand/store type |
| **Official Stores** | Optional | Browse 官方旗舰店, 品牌直营店 |
| **Product Detail** | Optional | View specs, prices, 88VIP prices |
| **Brand Verification** | Optional | Verify store authenticity badges |
| **Reviews** | Optional | Read user reviews, ratings, photos |
| **Add to Cart** | ✅ Required | Add items to shopping cart |
| **View Cart** | ✅ Required | Review cart contents |
| **Apply Coupons** | ✅ Required | Check and apply 店铺券, 平台券, 88VIP discounts |
| **Generate Order Preview** | ✅ Required | Calculate final price with all discounts |
| **Payment** | ❌ Blocked | User must complete payment manually |

**Safety Rule**: Agent stops before payment. User retains full control over final purchase.

### Legacy: Decision-Only Mode (No Browser)

- Platform suitability analysis
- Official store guidance
- Brand authenticity advice
- 88VIP benefits explanation
- Tmall vs other platforms comparison

Read these references as needed:
- `references/official-store-guide.md` for store guidance
- `references/output-patterns.md` for output patterns
- `references/browser-workflow.md` for automation guide

## Workflow

### Phase 1: Discovery (Agent-Assisted)
1. **Search** - Agent searches Tmall for target products
2. **Filter by Store Type** - Focus on 官方旗舰店, 品牌直营店
3. **Brand Verification** - Check store badges, authenticity indicators
4. **Compare** - Agent compares top options across official stores
5. **Reviews** - Read user reviews, ratings, photo reviews

### Phase 2: Selection (Agent-Assisted)
1. **Product Detail** - Agent opens selected product page
2. **Price Analysis** - Compare 原价 vs 活动价 vs 88VIP价
3. **Store Verification** - Confirm 官方旗舰店 status
4. **Service Check** - Verify 假一赔四, 七天无理由退换, 运费险

### Phase 3: Cart & Pre-Order (Agent-Assisted with Login)
1. **Add to Cart** - Agent adds item to cart (requires login)
2. **Cart Review** - Agent shows cart contents, quantities
3. **Coupon Application** - Agent checks 店铺券, 平台券, 88VIP discounts
4. **Address Selection** - Agent confirms delivery address
5. **Order Summary** - Agent generates complete order preview

### Phase 4: Checkout (User-Controlled)
1. **Handoff** - Agent presents final order details
2. **User Review** - User confirms all details are correct
3. **Payment** - ⚠️ **User completes payment manually**
4. **Confirmation** - User shares order confirmation if desired

**Agent Boundary**: Stops at Phase 3. Never executes payment or final order submission.

### Legacy: Decision-Only Mode (No Browser)

1. Identify the user's shopping need
2. Focus on public decision-relevant factors
3. Explain trade-offs
4. Give practical next-step advice

## Output

### For Shopping Assistance (v2.0)

#### Product Comparison
| # | 商品 | 价格 | 店铺类型 | 评分 | 服务保障 |
|---|------|------|---------|------|---------|
| 1 | ... | ... | 官方旗舰店 | ... | 假一赔四 |

#### Selected Product
- **名称**: 
- **原价 / 活动价 / 88VIP价**: 
- **店铺**: 官方旗舰店
- **服务保障**: 假一赔四, 七天无理由, 运费险
- **优惠券**: 

#### Cart Summary (if applicable)
- 商品小计: 
- 店铺券抵扣: 
- 平台券抵扣: 
- 88VIP折扣: 
- **应付总额**: 

#### Next Steps
1. [Agent completed] ...
2. [User action] 打开淘宝/天猫 App 完成支付

### For Decision-Only Mode (Legacy)

#### Best Option
State the strongest current choice.

#### Why
List the main reasons.

#### Caveats
List meaningful concerns or trade-offs.

#### Final Advice
Give a direct practical suggestion.

## Agent Execution Guide

### When User Says "帮我买..." / "帮我下单..."

```
User: "帮我买天猫的化妆品"
  ↓
Step 1: Confirm Intent
  "我来帮你搜索天猫的化妆品，筛选官方旗舰店，对比价格，加入购物车。
   最后需要你确认订单并完成支付。可以吗？"
  ↓
Step 2: Discovery Phase (No login required)
  - Search Tmall for "化妆品"
  - Filter: 官方旗舰店 only
  - Compare top 3 options
  - Check 假一赔四, 品牌授权 badges
  - Read reviews
  ↓
Step 3: Selection Phase (No login required)
  - User picks one option
  - Agent opens product page
  - Confirm 官方旗舰店 status
  - Check 88VIP price if applicable
  - Show final price
  ↓
Step 4: Cart Phase (⚠️ Requires login)
  "接下来需要登录你的淘宝/天猫账号才能加入购物车，
   请确认是否继续？"
  - If yes: proceed with browser automation
  - If no: provide manual instructions
  ↓
Step 5: Order Generation (Requires login)
  - Add to cart
  - Apply 店铺券, 平台券, 88VIP discounts
  - Select address
  - Calculate final price
  - Generate order preview
  ↓
Step 6: Handoff (User-controlled)
  "订单已准备好，请检查：
   [订单详情摘要]
   
   👉 请手动完成支付：
   1. 打开淘宝/天猫 App
   2. 进入购物车
   3. 点击结算
   4. 确认地址和优惠券
   5. 提交订单并支付"
```

### Browser Automation Rules

**Always announce before action:**
- "正在搜索..."
- "正在筛选官方旗舰店..."
- "正在验证品牌授权..."
- "正在加入购物车..."

**Snapshot key information:**
- Product title, 原价, 活动价, 88VIP价
- Store badge (官方旗舰店/品牌直营)
- Service guarantees (假一赔四/七天无理由/运费险)
- Rating and review count
- Available coupons
- Brand authorization info

**Stop conditions:**
- Before any payment screen
- When CAPTCHA appears (hand to user)
- When login is required (ask first)
- When store is not 官方旗舰店 (warn user)

### Login Handling

**Option A: User already logged in (Chrome profile)**
```
browser navigates to Tmall
If user profile has active session → proceed
If session expired → prompt user to login manually first
```

**Option B: Manual mode (no login)**
```
Agent provides:
- Exact search keywords
- Official store filter tips
- Brand verification checklist
- Step-by-step manual instructions
User executes manually
```

## Tmall Store Types

| Store Badge | Meaning | Trust Level |
|-------------|---------|-------------|
| **官方旗舰店** | Official flagship | ⭐⭐⭐⭐⭐ |
| **品牌直营店** | Brand direct | ⭐⭐⭐⭐⭐ |
| **专卖店** | Authorized specialty | ⭐⭐⭐⭐☆ |
| **专营店** | Category store | ⭐⭐⭐☆☆ |

**Priority**: 官方旗舰店 > 品牌直营店 > 专卖店 > 专营店

## Service Guarantees

| Badge | Meaning |
|-------|---------|
| **假一赔四** | Counterfeit = 4x compensation |
| **七天无理由退换** | 7-day no-reason return |
| **运费险** | Free return shipping insurance |
| **极速退款** | Fast refund processing |
| **正品保障** | Authenticity guarantee |

## 88VIP Benefits

- **Discount**: 9.5折 on most items
- **Coupons**: Monthly coupon allowance
- **Free Shipping**: Selected items
- **Priority**: Customer service priority

## Quality Bar

### Do:
- ✅ Focus on official flagship stores
- ✅ Verify brand authenticity
- ✅ Use browser automation for search/cart
- ✅ Add to cart and apply coupons (with consent)
- ✅ Generate order preview with all discounts
- ✅ Stay honest about not doing payment operations

### Do not:
- ❌ Pretend to log in (ask first)
- ❌ Recommend non-official stores for branded goods
- ❌ Store user data persistently
- ❌ **Execute payment or final order submission**
- ❌ Guarantee authenticity without verification
