# Auto-Renewable Subscription Guidelines — Complete Reference

**Official URL:** https://developer.apple.com/app-store/subscriptions/

This document covers all requirements for implementing auto-renewable subscriptions in iOS apps.

---

## Subscription Groups

### Purpose

Subscription groups organize your subscriptions and determine upgrade/downgrade behavior.

### Rules

| Rule | Details |
|------|---------|
| **One per group** | Users can only have one active subscription per group |
| **Upgrade/downgrade** | Moving between subscriptions in same group |
| **Single group recommended** | Most apps should have one group only |
| **Multiple groups** | Only when users would want multiple active subscriptions |

### When to Use Multiple Groups

| Scenario | Recommendation |
|----------|----------------|
| Single product with tiers | **One group** (e.g., Basic, Pro, Enterprise) |
| Separate products | **Multiple groups** (e.g., Photo Editing + Cloud Storage) |
| Add-on features | **Separate group** if user wants both simultaneously |

### Example: Single Group

```
Group: Premium Access
├── Level 1: Annual Premium ($99.99/year) - Most features
├── Level 2: Monthly Premium ($12.99/month) - Most features
└── Level 3: Basic ($4.99/month) - Limited features
```

---

## Subscription Levels (Ranking)

### How Ranking Works

| Level | Meaning |
|-------|---------|
| **Level 1** | Highest value, most features |
| **Level 2** | Second highest |
| **Level 3** | Third highest |
| **...** | Continue ranking |

### Upgrade Behavior

**When user moves to HIGHER level (upgrade):**
- Takes effect immediately
- User receives prorated refund for unused portion of previous subscription
- New billing cycle starts

### Downgrade Behavior

**When user moves to LOWER level (downgrade):**
- Takes effect at end of current billing period
- User retains current access until renewal
- New subscription starts at next renewal

### Crossgrade Behavior

**When user moves to SAME level (crossgrade):**
- If same duration: Immediate, with prorated refund
- If different duration: Depends on configuration

---

## Pricing

### Price Points

| Feature | Details |
|---------|---------|
| **Available points** | 800 standard price points |
| **Higher tiers** | Additional 100 points available on request |
| **Currency** | All supported App Store currencies |
| **Territory** | Can set different prices per region |

### Pricing Best Practices

| Practice | Details |
|----------|---------|
| **Anchor pricing** | Show annual savings vs monthly |
| **Clear value** | Price reflects perceived value |
| **Competitive** | Research category pricing |
| **Localized** | Consider purchasing power parity |

### Price Changes

| Rule | Details |
|------|---------|
| **Scheduling** | Can schedule one future change per territory |
| **Notice** | Apple notifies existing subscribers |
| **Consent** | Required for price increases |
| **Timing** | Takes effect at next renewal |

---

## Introductory Offers

### Types

| Offer Type | Description |
|------------|-------------|
| **Free Trial** | Free for specific duration, then auto-bill |
| **Pay As You Go** | Discounted price per billing period for duration |
| **Pay Up Front** | One-time discounted price for duration |

### Eligibility

| Rule | Details |
|------|---------|
| **New subscribers only** | Never had subscription in this group |
| **One per group** | Each user gets one intro offer per subscription group |
| **Verify eligibility** | Use StoreKit to check before displaying |

### Configuration

```swift
// Check eligibility
let isEligible = await product.subscription?.isEligibleForIntroOffer
```

### Display Requirements

| Requirement | Details |
|-------------|---------|
| **Trial duration** | Clearly state length (e.g., "7-day free trial") |
| **Price after trial** | Show exact price charged when trial ends |
| **Auto-billing** | Explain automatic renewal |
| **Cancellation** | How to cancel before being charged |

---

## Promotional Offers

### Purpose

Win back churned users or reward existing subscribers.

### Eligibility

| Who | Details |
|-----|---------|
| **Existing subscribers** | Currently subscribed users |
| **Former subscribers** | Previously subscribed, now lapsed |
| **NOT new users** | New users use introductory offers |

### Configuration

| Setting | Details |
|---------|---------|
| **Limit** | Up to 10 promotional offers per subscription |
| **Discount types** | Free, pay-as-you-go, pay-up-front |
| **Duration** | Configurable periods |
| **Signature** | Requires server-side signature for redemption |

### Implementation

```swift
// Promotional offer requires signature from your server
let offer = Product.PurchaseOption.promotionalOffer(
    offerID: "promo_offer_1",
    keyID: "ABC123",
    nonce: UUID(),
    signature: serverGeneratedSignature,
    timestamp: Date()
)
```

---

## Offer Codes

### Types

| Type | Details |
|------|---------|
| **One-time codes** | Single-use, unique codes |
| **Custom codes** | Reusable codes you define |

### Use Cases

| Use Case | Code Type |
|----------|-----------|
| Influencer partnerships | One-time codes |
| Marketing campaigns | Custom codes |
| Event promotions | One-time codes |
| Broad promotions | Custom codes |

### Redemption

Users can redeem codes:
- In your app (StoreKit API)
- In App Store
- Via URL link

---

## Win-Back Offers

### Purpose

Automatically target subscribers who have churned.

### Configuration

| Setting | Details |
|---------|---------|
| **Location** | App Store Connect |
| **Targeting** | Automatic based on subscription history |
| **Display** | Shown on App Store product page |

---

## Billing Grace Period

### Purpose

Retain subscribers when payment fails temporarily.

### Configuration

| Duration | When to Use |
|----------|-------------|
| **No grace period** | Default, immediate expiration |
| **3 days** | Short buffer for payment issues |
| **16 days** | Standard recommendation |
| **28 days** | Maximum retention effort |

### Behavior

| State | User Access | Your Action |
|-------|-------------|-------------|
| **Grace period** | Maintains access | Apple retries payment |
| **Billing retry** | Access depends on config | Apple continues retries |
| **Churned** | Access revoked | Consider win-back offer |

---

## Revenue Share Timeline

### Commission Rates

| Period | Apple | Developer |
|--------|-------|-----------|
| **Year 1** | 30% | 70% |
| **Year 2+** | 15% | 85% |

### Calculating Year 1

| Counts | Doesn't Count |
|--------|---------------|
| Days of paid service | Free trial days |
| Paid introductory periods | Paused periods |
| Paid promotional periods | Grace period days |

### Retention to 15%

**Threshold:** 340 days of paid service (approximately)
- Then commission drops to 15%
- Resets if subscription lapses >60 days

---

## Sign-Up Screen Requirements

### Required Elements

**MUST display on subscription sign-up:**

| Element | Requirement |
|---------|-------------|
| **Subscription name** | Clear, accurate name |
| **Duration** | Monthly, yearly, etc. |
| **Content/services** | What's included |
| **Full renewal price** | **MOST PROMINENT ELEMENT** |
| **Localized pricing** | User's local currency |
| **Restore purchases** | Sign in or restore option |
| **Terms of Service** | Link required |
| **Privacy Policy** | Link required |

### Free Trial Display

| Element | Requirement |
|---------|-------------|
| **Trial duration** | "7-day free trial" |
| **Price after trial** | "$9.99/month after trial" |
| **Auto-billing notice** | "Subscription auto-renews unless cancelled" |
| **Cancellation info** | "Cancel anytime in Settings" |

### Example Layout

```
┌─────────────────────────────────────────┐
│            Premium Access               │
│                                         │
│     [Feature 1] [Feature 2]             │
│     [Feature 3] [Feature 4]             │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │        7-day Free Trial         │   │
│   │   then $9.99/month              │   │
│   │   Cancel anytime                │   │
│   └─────────────────────────────────┘   │
│                                         │
│   Already a subscriber? Restore         │
│                                         │
│   Terms of Service | Privacy Policy     │
└─────────────────────────────────────────┘
```

---

## Cancellation Requirements

### User Rights

| Right | Implementation |
|-------|----------------|
| **Easy access** | Cancellation must be findable |
| **Clear process** | User understands consequences |
| **No barriers** | Cannot require phone call or excessive steps |
| **Continued access** | Access until end of paid period |

### Allowed Retention Tactics

| Tactic | Allowed? |
|--------|----------|
| Show what user will lose | ✅ Yes |
| Offer discounted rate | ✅ Yes |
| Offer pause instead | ✅ Yes |
| Survey for feedback | ✅ Yes |
| Hide cancellation option | ❌ No |
| Require phone call | ❌ No |
| Add excessive steps | ❌ No |
| Guilt/shame user | ❌ No |

### System Management UI

Consider using Apple's system-provided management interface:
- `manageSubscriptionsSheet(isPresented:)`
- Takes user to system subscription management
- Consistent, trusted experience

---

## Subscription States

### Server-Side States

| State | Meaning | Action |
|-------|---------|--------|
| **Active** | Currently subscribed | Full access |
| **Expired** | Subscription ended | Revoke access |
| **In Grace Period** | Payment failed, retrying | Maintain access |
| **In Billing Retry** | Continued payment attempts | Depends on config |
| **Revoked** | Refunded or revoked | Revoke access |
| **Pending Price Consent** | Price increase pending | Notify user |

### Client-Side Verification

```swift
// Check subscription status
for await result in Transaction.currentEntitlements {
    if case .verified(let transaction) = result {
        // User has active entitlement
    }
}
```

---

## Testing

### Sandbox Environment

| Feature | Sandbox Behavior |
|---------|------------------|
| **Subscription duration** | Accelerated (1 month = 5 minutes) |
| **Renewal limit** | 6 renewals per subscription |
| **Payment** | Not charged |
| **Account** | Sandbox Apple ID required |

### Subscription Durations in Sandbox

| Production | Sandbox |
|------------|---------|
| 1 week | 3 minutes |
| 1 month | 5 minutes |
| 2 months | 10 minutes |
| 3 months | 15 minutes |
| 6 months | 30 minutes |
| 1 year | 1 hour |

### TestFlight

| Feature | Details |
|---------|---------|
| **Billing** | Not charged |
| **Behavior** | Mirrors sandbox |
| **Users** | TestFlight testers only |

---

## Family Sharing

### Configuration

| Setting | Details |
|---------|---------|
| **Enable** | In App Store Connect |
| **Sharing** | Up to 5 family members |
| **Irreversible** | Cannot disable once enabled |

### Naming Convention

Highlight family plan in subscription name:
- "Premium Family Plan"
- "Family Subscription"
- "Household Access"

### Revenue Consideration

| Impact | Details |
|--------|---------|
| **Revenue per user** | May decrease |
| **User satisfaction** | May increase |
| **Competitive advantage** | Important for families |

---

## Common Subscription Mistakes

| Mistake | Fix |
|---------|-----|
| Price not prominent | Make price the largest text |
| Missing trial details | Clearly state duration and post-trial price |
| Hard to cancel | Provide easy cancellation path |
| Wrong subscription group | Users getting both when they want one |
| Not handling all states | Handle grace period, expired, revoked |
| Missing restore purchases | Always provide restore option |
| Sandbox not tested | Test all flows in sandbox |

---

## Subscription Checklist

### App Store Connect
- [ ] Subscription group created
- [ ] Subscriptions configured with correct levels
- [ ] Pricing set for all territories
- [ ] Introductory offers configured (if using)
- [ ] Promotional offers configured (if using)
- [ ] Family Sharing decision made

### App Implementation
- [ ] Sign-up screen meets all requirements
- [ ] Price is most prominent element
- [ ] Free trial clearly explained
- [ ] Restore purchases implemented
- [ ] Terms of Service linked
- [ ] Privacy Policy linked
- [ ] Cancellation easy to find
- [ ] All subscription states handled

### Testing
- [ ] Sandbox testing complete
- [ ] Upgrade/downgrade tested
- [ ] Cancellation tested
- [ ] Restore tested
- [ ] Grace period behavior verified
- [ ] Edge cases handled

---

*Subscription requirements evolve. Always verify against current Apple documentation.*
