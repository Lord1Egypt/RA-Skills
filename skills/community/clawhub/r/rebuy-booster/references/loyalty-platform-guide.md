# Loyalty Platform Guide — Klaviyo, LoyaltyLion, Yotpo, Smile.io

## Overview

Loyalty and retention programs require tight integration between your ESP (email service provider) and your loyalty platform. This guide covers platform-specific configuration for the four most common ecommerce loyalty stacks. Always verify current platform behavior — feature sets and integration methods change frequently.

---

## Klaviyo (ESP + Retention Flows)

Klaviyo handles the communication layer for retention but is not a loyalty platform itself. It integrates with loyalty platforms via properties synced to customer profiles.

### Retention Flow Configuration

**Second-purchase trigger:**
- Trigger: "Placed Order" metric
- Flow filter: "Has placed order → exactly 1 time total" — ensures only first-time buyers enter the flow
- Alternative: Use a segment "Customers who have placed exactly 1 order" as the flow trigger for cleaner logic

**Re-order trigger:**
- Use "Placed Order" event + time delay matching product consumption cycle
- Flow filter: "Has placed order → zero times → since [X] days ago" — exits flow if customer re-orders before trigger fires
- Klaviyo's "Predictive Analytics" → "Expected Next Order Date" property can replace manual time delays for stores with sufficient order history

**VIP tier escalation:**
- Sync loyalty tier as a custom profile property (e.g., `loyalty_tier: "VIP"`) from your loyalty platform
- Build flow triggered by property change: "When loyalty_tier changes to VIP → enter VIP welcome flow"
- Conditional splits within flows: branch by `loyalty_tier` property to show different content to different tiers

**Lapsed buyer / win-back:**
- Klaviyo's built-in "Winback" flow template uses "Placed Order" with a long delay — customize trigger to fire at 90d / 180d based on your RFM thresholds
- Use "Predictive Analytics" → "Churn Risk" property to identify at-risk customers before they fully lapse — high-churn-risk customers can enter a proactive retention flow before they hit the win-back threshold

**Subscription flows:**
- If using Recharge, Bold, or Loop for subscriptions: these platforms have native Klaviyo integrations that sync subscription status as profile properties
- Build subscription-status conditional: show subscription upsell only to non-subscribers; show subscription management content to existing subscribers

---

## LoyaltyLion

LoyaltyLion is a mid-market loyalty platform with strong Klaviyo and Shopify integrations.

### Program Configuration

**Points structure setup:**
- Navigate to Program → Earning Rules → add rules for: purchase, account creation, review, referral, social follow, birthday
- Recommended earn rate: 1–5 points per $1 (calibrate based on redemption value you set)
- Redemption threshold: set at 2–3 orders' worth of points to drive frequency without immediate redemption

**Tier configuration:**
- Program → Tiers → create 2–3 tiers with entry thresholds by points earned (not current balance)
- Entry threshold by spend: Tier 1 = 0 points (all members), Tier 2 = 200 points (~$40–200 spend), Tier 3 = 1000 points (~$200–1000 spend)
- Benefits per tier: configure in "Perks" section — free shipping, early access, bonus multipliers

**Klaviyo integration:**
- Install LoyaltyLion Klaviyo integration from LoyaltyLion's integrations panel
- Properties synced: `loyalty_points_balance`, `loyalty_tier`, `loyalty_referral_url`, `loyalty_member_since`
- Events synced: points earned, tier upgrade, reward redeemed — use these as Klaviyo flow triggers

**Referral mechanics:**
- Program → Referrals → set referrer reward and friend reward separately
- Referrer reward on friend's first purchase (not on referral link click) — reduces fraud
- Use `loyalty_referral_url` property in email merge tags for personalized referral links

---

## Yotpo (Loyalty + Reviews + SMS)

Yotpo is an enterprise-grade platform combining loyalty, reviews, and SMS. Best for higher-volume stores ($2M+ GMV) that want a unified platform.

### Loyalty Module Setup

**Campaign types in Yotpo:**
- "VIP Tiers" — configure tier entry by total spend, order count, or custom properties
- "Loyalty Campaigns" — bonus points events for specific product purchases, limited-time multipliers, birthday bonus
- "Perks" — assign benefits to tiers: free shipping, early sale access, free products on milestone orders

**Review integration with loyalty:**
- Yotpo's native review request + loyalty integration: customers earn points for leaving reviews
- Configure "Earn points for verified purchase review" in Loyalty → Earning Rules
- Review reminder and loyalty point reminder can be combined in a single email (reduces email fatigue)

**Klaviyo integration:**
- Yotpo → Integrations → Klaviyo → sync customer loyalty data to Klaviyo profiles
- Properties synced: `yotpo_loyalty_points`, `yotpo_vip_tier`, `yotpo_referral_link`
- Use Yotpo's built-in email campaigns for loyalty-specific sends (points balance, tier upgrade) and Klaviyo for behavioral flows

**SMS + loyalty:**
- Yotpo SMS allows loyalty notifications via text: points earned, tier upgrade, reward expiring
- Segment SMS sends by tier: VIPs receive SMS for early access; standard members receive email only
- Consent requirements: SMS loyalty notifications require separate SMS opt-in from email opt-in

---

## Smile.io

Smile.io is the most common loyalty platform for Shopify stores under $5M GMV. Easy setup, native Shopify integration, limited customization at lower tiers.

### Program Configuration

**Points program:**
- Dashboard → Ways to Earn → add earning actions: order, account, review, birthday, social
- Smile's default earn rate: 1 point per $1 — adjust based on your margin profile
- Redemption: "Discount codes" are standard (X points = $Y off); "Free shipping" and "Free product" available on higher tiers

**Referrals:**
- Dashboard → Referrals → enable and set referrer + friend rewards
- Smile generates unique referral links per customer — accessible via their account page and Smile widget
- Limitation: Smile referral links are not easily injectable into email body copy (unlike LoyaltyLion) — use "Visit your account page for your referral link" as the CTA

**Klaviyo integration:**
- Install Smile Klaviyo integration from Smile's Integrations tab
- Synced properties: `smile_points_balance`, `smile_vip_tier_name`, `smile_referral_url`
- Synced events: "Points redeemed," "VIP tier change" — use as Klaviyo flow triggers
- Limitation: Smile's Klaviyo integration is one-directional (Smile → Klaviyo); you cannot trigger Smile actions from Klaviyo

**VIP tiers (available on Smile Plus+):**
- Dashboard → VIP Program → enable and configure tier thresholds
- Tier entry: by points earned (not balance) or by spend amount
- Tier benefits: multiplier points, free shipping, exclusive discounts
- Note: Smile's VIP tier notifications are handled by Smile's own email system by default — redirect to Klaviyo for consistent branding

---

## Cross-Platform Retention Stack Recommendations

| Store GMV | Recommended stack | Notes |
|---|---|---|
| Under $500K | Klaviyo + Smile.io | Simple, cost-effective, sufficient for early retention |
| $500K–$2M | Klaviyo + LoyaltyLion | Better Klaviyo integration, more customizable tier logic |
| $2M–$10M | Klaviyo + Yotpo or LoyaltyLion | Yotpo for unified platform; LoyaltyLion for Klaviyo-first stacks |
| $10M+ | Klaviyo + Yotpo or custom | Enterprise tier programs with dedicated account management |

**Critical integrations to verify before launch:**
- Loyalty tier property sync to Klaviyo (required for conditional email flows)
- Purchase event sync (loyalty platform must receive order data for accurate points calculation)
- Referral link injection into email copy (not all platforms support this natively)
- Subscription status sync (if using Recharge/Bold/Loop alongside loyalty)
