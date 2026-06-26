# App Review Guidelines -- In-App Purchases and Subscriptions

Use this as a StoreKit implementation guardrail for App Review payment issues.
For full submission, privacy, metadata, entitlement, or rejection-risk audits,
use the sibling `app-store-review` skill and re-check Apple's current App
Review Guidelines.

## Contents

- [Guideline 3.1.1 Baseline](#guideline-311-baseline)
- [What Generally Requires IAP](#what-generally-requires-iap)
- [What Generally Does Not Require IAP](#what-generally-does-not-require-iap)
- [External Purchase Links and Reader Apps](#external-purchase-links-and-reader-apps)
- [Subscription Display Requirements](#subscription-display-requirements)
- [StoreKit Implementation Checklist](#storekit-implementation-checklist)
- [Common IAP Rejection Risks](#common-iap-rejection-risks)
- [Pre-Submission Payments Checklist](#pre-submission-payments-checklist)
- [References](#references)

## Guideline 3.1.1 Baseline

Digital content, app features, subscriptions, virtual goods, and services
unlocked in the app generally must use Apple's In-App Purchase system unless a
specific App Review guideline exception, storefront-specific rule, or approved
entitlement applies.

Do not present this as a universal ban on every external purchase link. The
rules differ by storefront, entitlement, and app type, and they change over
time. For a release audit, quote the current guidelines directly.

## What Generally Requires IAP

- Premium features or content unlocks
- Subscriptions to app functionality
- Virtual currency, coins, gems, or other digital goods
- Ad removal
- Digital tips or donations
- Digital gift cards, certificates, vouchers, or coupons for digital goods

## What Generally Does Not Require IAP

- Physical products and e-commerce
- Ride-sharing, food delivery, and real-world services
- One-to-one services such as tutoring or consulting booked through the app
- Enterprise or B2B apps distributed through Apple Business Manager

## External Purchase Links and Reader Apps

- Remove external purchase links, buttons, calls to action, and purchase paths
  for digital goods unless the current storefront rules or an approved
  entitlement explicitly allow them.
- Reader apps may access content purchased elsewhere. Account-management or
  sign-up links depend on current reader-app rules, storefront, and entitlement
  status.
- U.S. storefront behavior and some regional external-purchase entitlements are
  different from the old blanket prohibition. Do not hardcode old guidance into
  product or review advice.

## Subscription Display Requirements

- Clearly display price, duration, billing frequency, renewal behavior, and
  cancellation terms before purchase.
- Free trials must clearly state trial duration, post-trial price, billing
  frequency, auto-renewal, and cancellation terms.
- Subscriptions should provide ongoing value and be available across a user's
  devices where the app supports them.

## StoreKit Implementation Checklist

- Categorize consumables, non-consumables, non-renewing subscriptions, and
  auto-renewable subscriptions correctly in App Store Connect.
- Provide working restore purchases for restorable products. StoreKit views can
  expose this with `.storeButton(.visible, for: .restorePurchases)`.
- Verify transactions with StoreKit 2 `VerificationResult`, current
  entitlements, and server-side JWS validation when the business model requires
  server authority.
- Handle interrupted purchases, `.pending` Ask to Buy approvals, refunds,
  revocations, Family Sharing changes, grace period, and billing retry.

## Common IAP Rejection Risks

1. **Unauthorized external purchase path.** The app links or directs users to
   buy digital goods outside IAP without a current rule or entitlement allowing
   that path.
2. **Missing restore path.** Restorable products cannot be restored from the
   paywall or store surface.
3. **Unclear subscription terms.** Price, duration, renewal behavior, trial
   conversion price, and cancellation terms are missing or hidden before
   purchase.
4. **Incorrect product categorization.** Consumables, non-consumables, and
   auto-renewable subscriptions do not match the App Store Connect product
   setup or the app's entitlement logic.

## Pre-Submission Payments Checklist

- [ ] Digital goods and app-unlocked features use IAP unless a current exception or approved entitlement applies
- [ ] Subscription terms are visible before purchase
- [ ] Free trial copy states post-trial price and billing frequency
- [ ] External purchase links and CTAs are either removed or justified by a current storefront rule or approved entitlement
- [ ] Restore purchases path is visible and functional for restorable products
- [ ] Product types match App Store Connect configuration
- [ ] Transaction verification uses StoreKit 2 APIs and server validation where needed
- [ ] Ask to Buy, deferred approvals, refunds, and revocations are handled

## References

- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) -- use the original Apple URL because this guidelines page is not reliably available through Sosumi.
- [StoreKit External Purchase Link Entitlement](https://sosumi.ai/documentation/bundleresources/entitlements/com_apple_developer_storekit_external-purchase-link)
- [StoreKit External Purchase](https://sosumi.ai/documentation/storekit/external-purchase)
