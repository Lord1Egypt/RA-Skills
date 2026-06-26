# Pre-Submission Checklist — Complete Reference

Use this checklist before every App Store submission to ensure first-submission approval.

---

## Quick Pre-Flight Check

### Critical Items (Must Pass)

| Check | Status | Notes |
|-------|--------|-------|
| App tested on real device | ☐ | Not just simulator |
| No crashes during testing | ☐ | Test all flows |
| Demo account provided (if needed) | ☐ | Test credentials work |
| Backend services live | ☐ | All APIs accessible |
| Privacy manifest included | ☐ | PrivacyInfo.xcprivacy |
| Privacy labels accurate | ☐ | Match actual data collection |
| Privacy policy linked | ☐ | In app and App Store listing |
| Screenshots show app in use | ☐ | Not splash screens |
| Built with Xcode 16+ / iOS 18 SDK | ☐ | Current requirements |

---

## Detailed Checklist by Category

## 1. Technical Requirements

### Build Configuration
- [ ] Using Xcode 16 or later
- [ ] Built against iOS 18 SDK
- [ ] Release build configuration (not Debug)
- [ ] arm64 architecture only (no simulator slices)
- [ ] dSYM symbols uploaded for crash reporting

### Info.plist
- [ ] All required keys present
- [ ] Permission description strings for all used permissions
- [ ] Bundle ID matches App Store Connect
- [ ] Version number updated
- [ ] Build number incremented

### Code Quality
- [ ] No deprecated API warnings
- [ ] No private API usage
- [ ] Xcode validation passes
- [ ] No memory leaks (tested with Instruments)

### Compatibility
- [ ] Tested on minimum supported iOS version
- [ ] Tested on current iOS version
- [ ] Tested on multiple device sizes
- [ ] Tested on iPad (if Universal app)
- [ ] Dark Mode supported (if applicable)
- [ ] Dynamic Type supported

---

## 2. Privacy Compliance

### Privacy Manifest (PrivacyInfo.xcprivacy)
- [ ] File exists at bundle root
- [ ] NSPrivacyTracking set correctly (true/false)
- [ ] NSPrivacyTrackingDomains listed (if tracking)
- [ ] NSPrivacyCollectedDataTypes complete
- [ ] NSPrivacyAccessedAPITypes with reasons

### Privacy Labels (App Store Connect)
- [ ] All data types identified
- [ ] Uses accurately described
- [ ] "Linked to User" marked correctly
- [ ] "Used to Track User" marked correctly
- [ ] Labels match actual code behavior

### Privacy Policy
- [ ] Link in App Store listing
- [ ] Link accessible from within app
- [ ] Covers all data collection
- [ ] Explains user rights
- [ ] Contact information included

### Third-Party SDKs
- [ ] All SDKs updated to latest versions
- [ ] All SDKs have privacy manifests
- [ ] All SDKs are signed
- [ ] SDK data collection included in privacy labels

### ATT (if tracking)
- [ ] ATT prompt implemented
- [ ] Prompt shown before tracking
- [ ] User choice respected
- [ ] Fallback for denied permission

---

## 3. App Store Connect Metadata

### App Identity
- [ ] App name under 30 characters
- [ ] App name unique and not trademarked
- [ ] Subtitle under 30 characters (if using)
- [ ] Keywords optimized (100 characters)

### Screenshots
- [ ] 6.9" iPhone screenshots provided
- [ ] 6.5" iPhone screenshots provided
- [ ] 6.3"/6.1" iPhone screenshots provided
- [ ] iPad screenshots (if iPad supported)
- [ ] All screenshots show app in use
- [ ] No splash screens or login pages
- [ ] Correct resolutions and formats
- [ ] Localized for each market (if applicable)

### App Preview Videos (if using)
- [ ] 15-30 seconds length
- [ ] Screen recordings only (no pre-rendered)
- [ ] Correct resolutions
- [ ] Accurate representation of app

### Description
- [ ] Accurately describes app
- [ ] No competitor mentions
- [ ] No unverifiable claims
- [ ] Privacy Policy link included
- [ ] Terms of Service link included

### What's New
- [ ] Describes actual changes
- [ ] Not just marketing copy
- [ ] Useful to users

### Age Rating
- [ ] All questions answered honestly
- [ ] Rating reflects actual content
- [ ] UGC warning set (if applicable)

### Category
- [ ] Primary category appropriate
- [ ] Secondary category (if applicable)

### Support & Contact
- [ ] Support URL valid and accessible
- [ ] Support URL tested
- [ ] Contact information accurate

---

## 4. App Functionality

### Demo Account (if login required)
- [ ] Demo credentials provided in review notes
- [ ] Demo account tested and working
- [ ] Demo has full access to all features
- [ ] Demo doesn't require 2FA (or code provided)
- [ ] Demo doesn't expire during review period

### Core Functionality
- [ ] All features work as described
- [ ] No placeholder content
- [ ] No "coming soon" features
- [ ] No hidden functionality

### User Flows
- [ ] Complete user journey tested
- [ ] Edge cases handled
- [ ] Error states graceful
- [ ] Loading states present

### Network
- [ ] Works with slow connection
- [ ] Handles no connection gracefully
- [ ] Backend services live and stable
- [ ] API rate limits won't affect review

---

## 5. Design Compliance

### Human Interface Guidelines
- [ ] iOS design patterns followed
- [ ] Touch targets ≥44pt
- [ ] Navigation patterns standard
- [ ] Tab bar used correctly (not for actions)

### Accessibility
- [ ] VoiceOver compatible
- [ ] Dynamic Type supported
- [ ] Color contrast meets standards
- [ ] Reduce Motion respected

### Dark Mode
- [ ] Dark Mode supported
- [ ] All screens look correct
- [ ] Images and icons adapt

---

## 6. Monetization (if applicable)

### In-App Purchases
- [ ] IAP used for digital goods (if applicable)
- [ ] Products created in App Store Connect
- [ ] Sandbox testing complete
- [ ] Restore purchases implemented
- [ ] Receipt validation implemented

### Subscriptions
- [ ] Sign-up screen meets requirements
- [ ] Price most prominent element
- [ ] Free trial clearly explained
- [ ] Cancellation info displayed
- [ ] Terms of Service linked
- [ ] Privacy Policy linked
- [ ] Restore purchases available

### Pricing Display
- [ ] Full price shown (not per-day)
- [ ] Localized for user's currency
- [ ] No hidden fees

---

## 7. Content Compliance

### User-Generated Content (if applicable)
- [ ] Content filtering implemented
- [ ] Report mechanism available
- [ ] Block user capability
- [ ] Contact information published
- [ ] Timely moderation

### Kids Category (if applicable)
- [ ] No external links (unless parental gated)
- [ ] No purchases (unless parental gated)
- [ ] No third-party advertising
- [ ] No analytics collecting PII
- [ ] COPPA compliant

### General Content
- [ ] No objectionable content
- [ ] No violence/hate speech
- [ ] Age-appropriate for rating
- [ ] No misleading claims

---

## 8. Review Notes

### Information to Include
- [ ] Demo account credentials
- [ ] Special instructions for testing
- [ ] Explanation of non-obvious features
- [ ] Hardware requirements (if any)
- [ ] Testing conditions (if specific)

### Example Review Notes

```
Demo Account:
Username: demo@yourapp.com
Password: AppReview2025!
Access: Full access to all premium features

Testing Notes:
• The "Scan Document" feature requires pointing the camera at a document
• Location features can be tested by granting location permission
• Push notifications require device token registration

Special Features:
• Dark Mode is fully supported
• App works offline with limited functionality
• Widget available on iOS 17+
```

---

## 9. Final Steps

### Before Clicking Submit
- [ ] All checklist items above completed
- [ ] Test app one final time on device
- [ ] Review all metadata for typos
- [ ] Verify screenshots are current
- [ ] Confirm demo account still works
- [ ] Check backend services are stable

### App Store Connect
- [ ] All required fields completed
- [ ] Export compliance answered
- [ ] Content rights confirmed
- [ ] Advertising identifier (if applicable)
- [ ] App pricing set

### Post-Submission
- [ ] Monitor App Store Connect for status
- [ ] Check email for any messages
- [ ] Be available to respond quickly
- [ ] Have fixes ready for common issues

---

## Quick Reference: By Rejection Risk

### High Risk (Most Common Rejections)

| Issue | Prevention |
|-------|------------|
| Privacy violations | Complete privacy manifest, accurate labels |
| Crashes | Test on real devices |
| Inaccurate metadata | Update screenshots, honest description |
| Broken demo account | Test before submission |
| Missing functionality | Ensure app provides real utility |

### Medium Risk

| Issue | Prevention |
|-------|------------|
| UGC without moderation | Add filtering, reporting, blocking |
| Payment issues | Use IAP correctly |
| Performance problems | Profile with Instruments |
| Design violations | Follow HIG |

### Lower Risk (But Still Possible)

| Issue | Prevention |
|-------|------------|
| Age rating incorrect | Answer honestly |
| Wrong category | Choose primary function |
| Support URL broken | Test before submission |

---

## Emergency Contacts

### Apple Resources

| Resource | URL |
|----------|-----|
| App Review Guidelines | https://developer.apple.com/app-store/review/guidelines/ |
| App Store Connect | https://appstoreconnect.apple.com |
| Developer Support | https://developer.apple.com/contact/ |
| Expedited Review Request | App Store Connect → Contact Us |

### When You're Rejected

1. Read rejection message carefully
2. Identify specific guideline cited
3. Determine fix vs appeal
4. Make changes or draft appeal
5. Resubmit promptly

---

*Use this checklist before every submission. Customize for your specific app.*
