# App Store Review Checklists

## Contents
- App Review Information Checklist
- Privacy Manifest Checklist
- In-App Purchase Checklist
- Screenshot and App Preview Checklist
- HIG Compliance Checklist
- Pre-Submission Checklist

## App Review Information Checklist

Use this to avoid Guideline 2.1 rejections:

- [ ] Demo credentials provided in App Review Information notes (if login required)
- [ ] Demo mode available if credentials are impractical or account state is hard to reproduce
- [ ] Demo account works and has access to all features
- [ ] App Review notes explain login-gated, role-gated, region-gated, hardware-gated, or otherwise non-obvious features
- [ ] All screens have real content (no placeholders or Lorem Ipsum)
- [ ] No broken links or dead-end flows
- [ ] All hardware-required features have fallback or reviewer instructions

## Privacy Manifest Checklist

Verify PrivacyInfo.xcprivacy completeness:

- [ ] `PrivacyInfo.xcprivacy` exists where app code, SDK code, executables, or dynamic libraries need it
- [ ] All required-reason API categories in app and bundled SDK code are declared with approved reason codes
- [ ] `NSPrivacyTracking` is true only if tracking occurs
- [ ] Third-party SDK manifests present and up to date when SDKs collect data, use required-reason APIs, enable data collection, or contact tracking domains
- [ ] Privacy nutrition labels match actual data collection
- [ ] Audit runtime network traffic and SDK transmissions; observed behavior must match privacy labels, manifests, privacy policy, and ATT state

## In-App Purchase Checklist

- [ ] Digital goods and subscriptions use StoreKit IAP unless current storefront rules or approved entitlements allow otherwise
- [ ] Subscription price, duration, billing frequency, auto-renewal terms, and any trial duration/post-trial price shown before purchase
- [ ] Restore purchases button present and functional
- [ ] No external purchase path, link, button, or call to action for digital goods unless current rules or approved entitlements allow it
- [ ] Ask-to-buy and interrupted purchases handled
- [ ] Transaction verification uses StoreKit 2 or server-side verification

## Screenshot and App Preview Checklist

- [ ] 1-10 screenshots uploaded for each required platform and localization
- [ ] iPhone screenshots use current App Store Connect accepted sizes; 6.9-inch iPhone screenshots are the primary set as of May 2026
- [ ] 6.5-inch iPhone screenshots provided only when 6.9-inch iPhone screenshots are not provided or when manually optimizing that fallback
- [ ] 13-inch iPad screenshots provided if the app runs on iPad
- [ ] Screenshots and preview videos show actual app UI and do not misrepresent unavailable features
- [ ] App previews are 30 seconds or shorter, with a poster frame that works without autoplay

## HIG Compliance Checklist

### Navigation
- [ ] `NavigationStack` used (not `NavigationView`)
- [ ] System back chevron used; no custom back icons
- [ ] Tab bar uses <= 5 tabs; use More tab if needed
- [ ] Avoid hamburger menus

### Modals and Sheets
- [ ] Sheets have a visible dismiss control
- [ ] Full-screen modals have close/done button
- [ ] Alerts use system alert styles

### System Feature Support
- [ ] Dark Mode renders correctly
- [ ] Dynamic Type supported throughout
- [ ] iPad multitasking supported (Slide Over, Split View)
- [ ] Dynamic Island / Live Activities render correctly when used
- [ ] System gestures not disabled

### Widgets and Live Activities
- [ ] Widgets show real content (not placeholders)
- [ ] Timelines update meaningfully
- [ ] Live Activities show time-sensitive info
- [ ] Lock Screen widgets are legible at small sizes

## Pre-Submission Checklist

### Completeness
- [ ] No placeholder or test content
- [ ] All features functional without special hardware
- [ ] Demo credentials or demo mode provided, with App Review notes for gated or non-obvious features
- [ ] No dead-end screens

### Metadata
- [ ] App name matches functionality
- [ ] Screenshots are real app screenshots using current required platform sizes, including 6.9-inch iPhone and 13-inch iPad when applicable
- [ ] Description contains no prices or competitor mentions
- [ ] Category is correct

### Privacy
- [ ] Privacy manifest present where required, with approved reason codes
- [ ] Third-party SDK manifests verified
- [ ] Privacy policy URL present and accessible
- [ ] Audit runtime network traffic and SDK transmissions; nutrition labels, privacy manifest declarations, privacy policy, and observed behavior match actual data collection
- [ ] ATT prompt only if tracking occurs

### Payments
- [ ] Digital content uses StoreKit IAP unless current rules or approved entitlements allow otherwise
- [ ] Subscription price, duration, billing frequency, auto-renewal terms, and any trial duration/post-trial price visible before purchase
- [ ] No external purchase paths, payment links, buttons, or calls to action unless current storefront rules or approved entitlements allow them
- [ ] Free trial terms clear
- [ ] Restore purchases implemented

### Design
- [ ] Standard navigation patterns used
- [ ] Dark Mode supported
- [ ] Dynamic Type supported
- [ ] No custom alerts mimicking system alerts
- [ ] Launch screen not an ad
- [ ] Empty states provide guidance

### Technical
- [ ] Built with Xcode 26 or later and relevant platform SDK 26 or later for uploads after April 28, 2026
- [ ] No private API usage
- [ ] No dynamic code execution
- [ ] Entitlements justified with usage descriptions
- [ ] Background modes justified and used
- [ ] Deployment target is intentionally chosen and tested
