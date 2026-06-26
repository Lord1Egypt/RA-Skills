# In-App Purchase Rules — Complete Reference

**Official URLs:**
- https://developer.apple.com/app-store/review/guidelines/#3.1
- https://developer.apple.com/in-app-purchase/
- https://developer.apple.com/design/human-interface-guidelines/in-app-purchase

This document covers when In-App Purchase is required, exceptions, implementation requirements, and commission structure.

---

## When In-App Purchase is REQUIRED

**Guideline 3.1.1:** Apps may not use their own mechanisms to unlock content or functionality.

### Digital Goods Requiring IAP

| Category | Examples |
|----------|----------|
| **Premium content** | Articles, tutorials, courses |
| **Subscriptions** | Digital content access, features |
| **Game currencies** | Gems, coins, gold |
| **Game levels** | Additional stages, worlds |
| **Full versions** | Upgrading from "lite" version |
| **Features** | Unlocking functionality |
| **Ad removal** | Removing advertisements |
| **Social boosts** | Profile visibility, post promotion |
| **Virtual goods** | Stickers, emojis, avatars |
| **Tips/donations** | In-app tipping for creators |

### Key Principle

**If the content is consumed within the app = IAP required**

---

## When IAP is NOT Required (Exceptions)

**Guideline 3.1.3** defines specific exceptions where other payment methods are allowed:

### Exception (a): Reader Apps

**Applies to:** Apps that allow users to access previously purchased content.

| Allowed | Details |
|---------|---------|
| Magazines | Previously subscribed publications |
| Newspapers | Previously purchased subscriptions |
| Books | Previously purchased e-books |
| Audio | Previously purchased audiobooks, music |
| Video | Previously purchased movies, shows |

**Requirements:**
- Cannot sell new content in-app
- Cannot include purchase links
- Can provide "create account" information
- Must not disadvantage IAP users

### Exception (b): Multiplatform Services

**Applies to:** Content purchased on other platforms (web, Android, etc.)

| Allowed | Details |
|---------|---------|
| Web purchases | Content bought on website can be accessed in app |
| Cross-platform | Content from Android/Windows can be used |
| Existing libraries | User's existing content library |

**Requirements:**
- Cannot link to external purchase
- Must work for users who purchased via IAP too
- Cannot disadvantage IAP users

### Exception (c): Enterprise Services

**Applies to:** B2B apps sold to organizations

| Allowed | Details |
|---------|---------|
| Enterprise subscriptions | Bulk licensing to companies |
| B2B services | Business tools sold to organizations |
| Team plans | Organization-wide access |

**Requirements:**
- Not for individual consumer purchase
- Must be organization deployment

### Exception (d): Person-to-Person Services

**Applies to:** Real-time 1:1 services between people

| Allowed | Details |
|---------|---------|
| Tutoring | Live one-on-one tutoring sessions |
| Medical consultations | Real-time doctor visits |
| Legal consultations | Live attorney consultations |
| Personal training | Real-time fitness coaching |
| Real estate tours | Live property showings |

**Requirements:**
- Must be real-time, live services
- Must be one-on-one
- Scheduled/recorded content needs IAP

### Exception (e): Physical Goods/Services

**Applies to:** Items consumed outside the app

| Allowed | Details |
|---------|---------|
| Physical products | Clothing, electronics, food |
| In-person services | Haircuts, cleaning, repair |
| Transportation | Ride sharing, delivery |
| Event tickets | Concerts, sports, theater |
| Travel | Hotels, flights, car rentals |

**Requirements:**
- Must be consumed outside the app
- Cannot be purely digital

### Exception (f): Free Stand-alone Companions

**Applies to:** Free apps that complement paid web-based tools

| Allowed | Details |
|---------|---------|
| Web tool companions | Free app for paid web service |
| Feature subset | Limited functionality, full on web |

**Requirements:**
- Must be genuinely free
- Cannot offer purchases in-app
- Web tool must be the primary product

### Exception (g): Advertising Management

**Applies to:** Apps for managing advertising campaigns

| Allowed | Details |
|---------|---------|
| Ad purchases | Buying ads for campaigns |
| Campaign management | Managing ad spend |

**Requirements:**
- For advertising purposes only
- Not for content consumption

---

## Commission Structure

### Standard Rates

| Scenario | Apple Commission | Developer Share |
|----------|-----------------|-----------------|
| **Standard rate** | 30% | 70% |
| **After 1 year subscriber** | 15% | 85% |
| **Small Business Program** | 15% | 85% |

### Small Business Program

**Eligibility:**
- Earned <$1M in App Store proceeds in prior calendar year
- Must apply each year

**Benefits:**
- 15% commission from day one (instead of 30%)
- Applies to all app revenue

**Reset:**
- If you exceed $1M, revert to standard 30%
- Can re-qualify next year if under $1M again

### Subscriber Retention Discount

**After subscriber paid for 1+ year:**
- Commission drops from 30% to 15%
- 85% to developer
- Calculated per subscriber

**Days count toward 1 year:**
- Days of paid service accumulate
- Free trials don't count
- Introductory offers with paid portion count

---

## In-App Purchase Types

### Consumables

| Characteristic | Details |
|----------------|---------|
| **Definition** | Depletes with use |
| **Examples** | Game currency, lives, boosts |
| **Restoration** | Cannot be restored |
| **Multiple purchase** | Can buy repeatedly |

### Non-Consumables

| Characteristic | Details |
|----------------|---------|
| **Definition** | Permanent, one-time purchase |
| **Examples** | Premium features, ad removal, full version |
| **Restoration** | Must support restore purchases |
| **Multiple purchase** | Cannot buy again once owned |

### Auto-Renewable Subscriptions

| Characteristic | Details |
|----------------|---------|
| **Definition** | Recurring until cancelled |
| **Examples** | Premium access, content subscriptions |
| **Billing** | Automatic renewal |
| **Requirements** | Must display cancellation, sign-up requirements |

### Non-Renewing Subscriptions

| Characteristic | Details |
|----------------|---------|
| **Definition** | Fixed duration, no auto-renewal |
| **Examples** | Season pass, limited time access |
| **Renewal** | User must manually repurchase |
| **Restoration** | App must track expiration |

---

## StoreKit Implementation Requirements

### Required Functionality

| Feature | Requirement |
|---------|-------------|
| **Restore purchases** | Must provide way to restore non-consumables and subscriptions |
| **Receipt validation** | Verify purchases are legitimate |
| **Error handling** | Graceful handling of purchase failures |
| **Transaction observation** | Handle interrupted transactions on app launch |

### Sign-Up Screen Requirements

**For subscriptions, the sign-up screen must display:**

| Element | Requirement |
|---------|-------------|
| **Subscription name** | Clear product name |
| **Duration** | Monthly, yearly, etc. |
| **Content/services** | What's included |
| **Renewal price** | **MOST PROMINENT ELEMENT** |
| **Localized pricing** | All available currencies |
| **Restore purchases** | Option to sign in or restore |
| **Terms of Service** | Link required |
| **Privacy Policy** | Link required |

### Free Trial Requirements

| Requirement | Details |
|-------------|---------|
| **Duration** | Clearly state trial length |
| **Price after trial** | Show what user will be billed |
| **Automatic billing** | Cannot mislead about auto-charge |
| **Cancellation** | Explain how to cancel before charge |

---

## Price Display Guidelines

### Requirements

| Rule | Details |
|------|---------|
| **Full price** | Show complete price, not per-day calculations |
| **Prominence** | Price must be most prominent element |
| **Localization** | Show user's local currency |
| **Clarity** | No hidden fees or conditions |

### What NOT to Do

| Violation | Example |
|-----------|---------|
| **Per-day pricing** | "Only $0.50/day!" for $14.99/month |
| **Hidden pricing** | Price in small text or hard to find |
| **Misleading savings** | Fake "was $X, now $Y" claims |
| **Currency confusion** | Showing USD to non-US users |

---

## Cancellation Requirements

### User Rights

| Requirement | Details |
|-------------|---------|
| **Easy to find** | Cancellation option must be accessible |
| **No barriers** | Cannot require calling support |
| **Clear process** | User understands what happens when cancelled |
| **Service continuation** | Access until end of paid period |

### Retention Best Practices

| Allowed | Not Allowed |
|---------|-------------|
| Offer pause instead of cancel | Hide cancellation |
| Show what will be lost | Add excessive steps |
| Offer discount to stay | Require phone call |
| Survey about reasons | Guilt users into staying |

---

## Family Sharing

### Configuration

| Setting | Details |
|---------|---------|
| **Enable** | Can enable for auto-renewable subscriptions |
| **Sharing limit** | Up to 5 family members |
| **Irreversible** | Cannot disable once enabled |
| **Naming** | Highlight in subscription name (e.g., "Family Plan") |

### Considerations

- Revenue per user may decrease
- User satisfaction may increase
- Cannot undo Family Sharing after enabling
- Consider offering individual and family tiers

---

## Offer Types

### Introductory Offers

| Type | Details |
|------|---------|
| **Who** | New subscribers only |
| **Limit** | One per subscription group |
| **Types** | Free trial, pay-as-you-go, pay-up-front |

### Promotional Offers

| Type | Details |
|------|---------|
| **Who** | Existing or former subscribers |
| **Limit** | Up to 10 per subscription |
| **Use** | Win back churned users, reward loyalty |

### Offer Codes

| Type | Details |
|------|---------|
| **Who** | Anyone with a code |
| **Types** | One-time or custom codes |
| **Use** | Marketing, partnerships, promotions |

### Win-back Offers

| Type | Details |
|------|---------|
| **Who** | Previous subscribers |
| **Configuration** | In App Store Connect |
| **Use** | Automatically target lapsed users |

---

## Common IAP Violations

| Violation | Guideline | Fix |
|-----------|-----------|-----|
| External payment for digital goods | 3.1.1 | Switch to IAP |
| Linking to external purchase | 3.1.1 | Remove links |
| Price not prominent | HIG | Make price most visible |
| No restore purchases | 3.1.1 | Add restore functionality |
| Misleading subscription UI | 3.1.2 | Follow sign-up requirements |
| Hidden cancellation | 3.1.2 | Make cancellation easy |
| Wrong IAP type | 3.1.1 | Use appropriate type |

---

## Implementation Checklist

### Setup
- [ ] Products created in App Store Connect
- [ ] StoreKit configured in Xcode
- [ ] Sandbox testing completed
- [ ] Receipt validation implemented

### UI Requirements
- [ ] Price prominently displayed
- [ ] Subscription terms clear
- [ ] Restore purchases available
- [ ] Terms of Service linked
- [ ] Privacy Policy linked

### Subscription Specifics
- [ ] Sign-up screen requirements met
- [ ] Free trial clearly explained
- [ ] Cancellation easy to find
- [ ] Renewal terms displayed

### Testing
- [ ] Purchase flow tested in sandbox
- [ ] Restore purchases tested
- [ ] Edge cases handled (failed purchase, interrupted transaction)
- [ ] Subscription states handled (active, expired, grace period)

---

*IAP requirements evolve. Always verify against current Apple documentation.*
