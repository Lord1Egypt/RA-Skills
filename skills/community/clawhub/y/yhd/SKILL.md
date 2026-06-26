---
name: yhd
version: 2.0.0
description: "Shop YHD.com (1号店) with browser automation for search, daily flash sales, fresh grocery selection, cart operations, and membership benefits. Supports logged-in workflows for browsing, adding to cart, and order preview while keeping checkout/payment for user control. Use when the user wants help shopping on 1号店, comparing grocery deals, timing flash sales, or choosing fresh-food purchasing strategies."
metadata:
  clawdbot:
    emoji: "🛒"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

## When to Use

User wants to shop on YHD.com (1号店). Agent helps with daily deals, fresh grocery shopping, 1号店会员 benefits, price comparison, and finding the best deals on China's leading membership-based shopping platform.

## Capabilities

### v2.0 - Browser Automation Support

| Operation | Auth Required | Description |
|-----------|---------------|-------------|
| **Search** | Optional | Search products, filter by category/deals |
| **Flash Sales** | Optional | Browse daily rotating flash sales (每日秒杀) |
| **Product Detail** | Optional | View specs, prices, member prices |
| **Fresh Produce** | Optional | Check harvest dates, origin, traceability |
| **Price Compare** | Optional | Compare regular vs 1号店会员 prices |
| **Add to Cart** | ✅ Required | Add items to shopping cart |
| **View Cart** | ✅ Required | Review cart contents, quantities |
| **Apply Coupons** | ✅ Required | Check and apply 免邮券, 满减 |
| **Delivery Slot** | ✅ Required | View available 2-hour delivery windows |
| **Generate Order Preview** | ✅ Required | Calculate total with member discounts |
| **Payment** | ❌ Blocked | User must complete payment manually |

**Safety Rule**: Agent stops before payment. User retains full control over final purchase.

### Legacy: Guidance-Only Mode (No Browser)

- Daily flash sale timing strategies
- Fresh grocery selection tips
- 1号店会员 benefits guidance
- Price comparison advice
- Smart cart building tips

## Quick Reference

| Topic | File |
|-------|------|
| Daily deals timing | `timing.md` |
| Fresh grocery guide | `fresh.md` |
| Membership benefits | `membership.md` |
| Price comparison | `pricing.md` |
| Browser automation | `browser-workflow.md` |

## Workflow

### Phase 1: Discovery (Agent-Assisted)
1. **Search** - Agent searches YHD for target products
2. **Flash Sales** - Browse daily rotating deals (每日秒杀)
3. **Filter & Sort** - Apply filters (category, price, member deals)
4. **Compare** - Agent compares regular vs 1号店会员 prices
5. **Freshness Check** - Check harvest dates, origin info, 产地直发 status

### Phase 2: Selection (Agent-Assisted)
1. **Product Detail** - Agent opens selected product page
2. **Price Analysis** - Compare current vs member price vs flash sale price
3. **Quality Check** - Verify 溯源码, grade (A级/B级), origin
4. **Quantity Selection** - Confirm amount for fresh items

### Phase 3: Cart & Pre-Order (Agent-Assisted with Login)
1. **Add to Cart** - Agent adds item to cart (requires login)
2. **Cart Review** - Agent shows cart contents, quantities, subtotal
3. **Coupon Application** - Agent checks 免邮券, 满减, member discounts
4. **Delivery Slot** - Agent checks available 2-hour delivery windows
5. **Address Selection** - Agent confirms delivery address
6. **Order Summary** - Agent generates complete order preview

### Phase 4: Checkout (User-Controlled)
1. **Handoff** - Agent presents final order details
2. **User Review** - User confirms all details are correct
3. **Payment** - ⚠️ **User completes payment manually**
4. **Confirmation** - User shares order confirmation with agent if desired

**Agent Boundary**: Stops at Phase 3. Never executes payment or final order submission.

### Legacy: Guidance-Only Mode (No Browser)

Follow the Core Rules below for decision support without automation.

## Core Rules

### 1. Daily Flash Sale Timing

YHD operates on **daily rotating flash sales** (每日秒杀):

| Sale Type | Timing | Best For |
|-----------|--------|----------|
| Morning Fresh | 8:00 AM - 10:00 AM | Fresh produce, dairy, bakery |
| Midday Essentials | 12:00 PM - 2:00 PM | Daily necessities, snacks |
| Afternoon Deals | 3:00 PM - 5:00 PM | Home goods, personal care |
| Evening Rush | 8:00 PM - 10:00 PM | Premium items, restocks |
| Midnight Clearance | 12:00 AM - 2:00 AM | Last chance deals, limited stock |

**Strategy:**
- Check tomorrow's preview at 8:00 PM daily
- Set reminders for high-demand categories
- Popular fresh items sell out within 30 minutes
- 1号店会员 get 30-minute early access

### 2. Fresh Grocery Navigation

YHD's strength is **fresh food and groceries**:

| Category | Best Time to Buy | Quality Indicators |
|----------|------------------|-------------------|
| Fresh Produce | Morning 8-10 AM | Harvest date, origin label |
| Meat & Seafood | Morning 8-10 AM | Slaughter/delivery date |
| Dairy & Eggs | Any time | Check expiration dates |
| Bakery & Bread | Morning 8-10 AM | Bake time stamp |
| Frozen Foods | Evening restocks | Temperature indicator |

**Pro Tip:**
- 产地直发 (Direct from origin) = fresher, better prices
- 今日特惠 (Today's special) updates hourly
- 买1赠1 (Buy 1 Get 1) common on produce

### 3. 1号店会员 Benefits

**Membership Tiers:**

| Tier | Annual Fee | Key Benefits |
|------|------------|--------------|
| Regular | Free | Basic deals, standard shipping |
| 1号店会员 | ¥198/year | Free shipping, member prices, early access |
| 1号店PLUS | ¥298/year | All above + cashback + priority support |

**Member-Exclusive Features:**
- 会员价 (Member prices): 5-20% off regular prices
- 会员日 (Member day): 8th of every month, extra discounts
- 免邮券 (Free shipping coupons): Monthly allowance
- 专属客服 (Priority support): Faster response

**Break-Even Analysis:**
- Shop >¥200/month → membership pays for itself
- Heavy fresh grocery buyers → highly recommended

### 4. Price Intelligence

**Price Comparison Strategy:**
- YHD prices vs Tmall/JD: Often competitive on groceries
- 1号店会员价 vs regular: Always check both
- Bundle deals: "满99减20" (Spend ¥99, save ¥20) common
- Flash sale prices: Can be 30-50% off regular

**Price Tracking:**
- 降价通知 (Price drop alerts): Set on wishlist items
- 历史价格 (Price history): Check before buying
- Seasonal patterns: Fresh produce cheaper in harvest season

### 5. Quality Assessment for Fresh Items

**Fresh Produce Grading:**

| Grade | Indicator | Recommendation |
|-------|-----------|----------------|
| A级/A Grade | Premium select | Best quality, higher price |
| B级/B Grade | Standard | Good value, everyday choice |
| 产地直发 | Direct from farm | Freshest, seasonal |
| 进口/Imported | International | Check origin, premium pricing |

**Red Flags:**
- No harvest/pack date listed
- Vague origin description
- Reviews mentioning spoilage
- Photos don't match description

**Green Signals:**
- 溯源码 (Traceability code)
- Same-day or next-day delivery
- High repeat purchase rate
- Detailed farm/region information

### 6. Shipping & Delivery

| Aspect | Details |
|--------|---------|
| Standard Delivery | Same-day or next-day (major cities) |
| Delivery Windows | 2-hour slots, 8:00 AM - 10:00 PM |
| Free Shipping Threshold | ¥99 for non-members, free for 1号店会员 |
| Cold Chain | Available for fresh/frozen items |
| Delivery Fee | ¥6-15 depending on distance/time |

**Delivery Optimization:**
- Choose morning slots for freshest produce
- Evening slots often have more availability
- Combine orders to hit free shipping threshold
- Cold chain items delivered in insulated packaging

### 7. Smart Cart Building

**Timing Strategies:**
1. **Early Morning Shopping:** Best selection of fresh items
2. **Flash Sale Stacking:** Combine multiple concurrent deals
3. **Member Day Shopping:** 8th of month for extra discounts
4. **Coupon Hunting:** Check app banners for stackable coupons

**Category Bundling:**
- Fresh + Pantry = Free shipping easier to reach
- Seasonal items + Regular items = Better overall value
- Bulk buying on non-perishables = Lower unit cost

**Payment Optimization:**
- 1号店钱包: Occasional extra discounts
- Bank partnerships: Check for card-specific deals
- First-order: Usually has welcome discount
- Referral codes: Share with friends for mutual benefits

## Common Traps

- **Overbuying perishables** → Fresh items have limited shelf life
- **Ignoring delivery windows** → Missing your slot means next-day delivery
- **Not checking expiration** → Especially on dairy and packaged foods
- **Missing member benefits** → Non-members pay more and shipping fees
- **Flash sale FOMO** → Compare with regular prices, not all "deals" are deals
- **Ignoring minimum order** → Factor in delivery fees if under threshold

## YHD-Specific Features to Leverage

### 1. 今日特惠 (Today's Deals)
- Updates hourly with new flash sales
- Limited quantity, first-come-first-served
- Set notifications for favorite categories

### 2. 产地直发 (Direct from Origin)
- Farm-to-table produce
- Better prices, fresher quality
- Seasonal availability

### 3. 1号店会员日 (Member Day)
- 8th of every month
- Extra discounts on top of member prices
- Exclusive product launches

### 4. 预售 (Pre-sale)
- Lock in prices for upcoming seasonal items
- Pay deposit, pay balance on delivery
- Common for imported fruits, seafood

## Agent Execution Guide

### When User Says "帮我买..." / "帮我下单..."

```
User: "帮我买1号店的牛奶"
  ↓
Step 1: Confirm Intent
  "我来帮你搜索1号店的牛奶，对比价格和会员优惠，加入购物车。
   最后需要你确认订单并完成支付。可以吗？"
  ↓
Step 2: Discovery Phase (No login required)
  - Search YHD for "牛奶"
  - Check daily flash sales (每日秒杀)
  - Filter: 1号店会员价, 产地直发
  - Compare top 3 options
  - Check if member price is better
  ↓
Step 3: Selection Phase (No login required)
  - User picks one option
  - Agent opens product page
  - Confirm quantity, expiration date
  - Show final price (1号店会员价 if applicable)
  ↓
Step 4: Cart Phase (⚠️ Requires login)
  "接下来需要登录你的1号店账号才能加入购物车，
   请确认是否继续？"
  - If yes: proceed with browser automation
  - If no: provide manual instructions
  ↓
Step 5: Order Generation (Requires login)
  - Add to cart
  - Apply 免邮券, 满减 coupons
  - Select 2-hour delivery slot
  - Calculate final price
  - Generate order preview
  ↓
Step 6: Handoff (User-controlled)
  "订单已准备好，请检查：
   [订单详情摘要]
   
   👉 请手动完成支付：
   1. 打开1号店 App
   2. 进入购物车
   3. 点击结算
   4. 确认地址和配送时段
   5. 提交订单并支付"
```

### Browser Automation Rules

**Always announce before action:**
- "正在搜索..."
- "正在查看今日特惠..."
- "正在对比会员价格..."
- "正在加入购物车..."

**Snapshot key information:**
- Product name, regular price, 1号店会员 price
- Flash sale countdown and stock
- Origin info (产地直发)
- Harvest/pack dates for fresh items
- Available delivery windows
- Cart subtotal and applicable coupons

**Stop conditions:**
- Before any payment screen
- When CAPTCHA appears (hand to user)
- When login is required (ask first)
- When flash sale item sells out

### Login Handling

**Option A: User already logged in (Chrome profile)**
```
browser navigates to YHD
If user profile has active session → proceed
If session expired → prompt user to login manually first
```

**Option B: Manual mode (no login)**
```
Agent provides:
- Exact search keywords
- Flash sale timing tips
- Member price comparison
- Step-by-step manual instructions
User executes manually
```

## Quality Bar

### Do:
- ✅ Focus on flash sale timing and member benefits
- ✅ Explain fresh produce selection criteria
- ✅ Use browser automation for search/cart
- ✅ Add to cart and apply coupons (with user consent)
- ✅ Generate order preview with delivery slot selection
- ✅ Stay honest about not doing payment operations

### Do Not:
- ❌ Pretend to log in (ask first)
- ❌ Claim to confirm live inventory without checking
- ❌ Store user data persistently
- ❌ **Execute payment or final order submission**
- ❌ Guarantee flash sale availability

## Related Skills

Install with `clawhub install <slug>` if user confirms:
- `vip` — VIP.com flash sale shopping
- `taobao` — Taobao marketplace guidance
- `jd-shopping` — JD.com shopping with automation
- `jingdong` — Alternative JD shopping guide
- `freshippo` — Freshippo fresh grocery shopping
- `shopping` — general shopping assistance
- `grocery` — grocery shopping optimization

## Feedback

- If useful: `clawhub star yhd`
- Stay updated: `clawhub sync`
