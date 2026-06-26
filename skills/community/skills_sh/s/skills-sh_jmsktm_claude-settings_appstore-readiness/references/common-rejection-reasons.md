# Common Rejection Reasons — Complete Reference

This document covers the most common App Store rejection reasons and how to prevent them.

---

## Top 10 Rejection Categories

### 1. Privacy Violations (Most Common)

**Guidelines:** 5.1.1, 5.1.2

| Issue | Description | Prevention |
|-------|-------------|------------|
| **Missing privacy policy** | No privacy policy link | Add link to app and App Store listing |
| **Incomplete policy** | Policy doesn't cover all data | Review all data collection points |
| **Inaccurate nutrition labels** | Labels don't match actual collection | Audit code and SDK data practices |
| **Missing privacy manifest** | No PrivacyInfo.xcprivacy | Create manifest with all declarations |
| **ATT not implemented** | Tracking without permission | Implement ATT prompt if tracking |
| **SDK privacy issues** | Third-party SDKs not compliant | Verify all SDKs have manifests |

**Fix Priority:** CRITICAL — Privacy is the #1 rejection reason since 2024.

---

### 2. Crashes and Bugs

**Guideline:** 2.1

| Issue | Description | Prevention |
|-------|-------------|------------|
| **Crash on launch** | App crashes during reviewer testing | Test on all device types |
| **Crash on specific action** | Feature causes crash | Test all user flows |
| **Crash on specific device** | Device-specific crash | Test on older devices too |
| **Memory issues** | App runs out of memory | Profile memory usage |
| **Network-related crash** | Crash without internet | Test offline scenarios |

**Fix Actions:**
1. Test on real devices (not just simulator)
2. Test on oldest supported iOS version
3. Test with poor network conditions
4. Use Xcode Instruments for profiling
5. Review crash logs from TestFlight

---

### 3. Performance Issues

**Guideline:** 2.4

| Issue | Description | Prevention |
|-------|-------------|------------|
| **Slow launch** | Takes too long to start | Optimize startup code |
| **Battery drain** | Excessive power usage | Audit background processes |
| **Excessive heat** | Device gets hot | Check CPU usage |
| **Unresponsive UI** | Interface freezes | Move work off main thread |
| **Large app size** | App too big for download | Optimize assets, use on-demand resources |

**Fix Actions:**
1. Profile with Xcode Instruments
2. Test on oldest supported device
3. Optimize images and assets
4. Use lazy loading where appropriate
5. Monitor background activity

---

### 4. Inaccurate Metadata

**Guideline:** 2.3

| Issue | Description | Prevention |
|-------|-------------|------------|
| **Screenshots don't match** | Screenshots show different UI | Update screenshots with each release |
| **Misleading description** | Claims features that don't exist | Only describe actual features |
| **Wrong category** | App in inappropriate category | Choose primary function category |
| **Hidden features** | Undocumented functionality | Describe all features in review notes |
| **Incorrect age rating** | Content rating too low | Answer questions honestly |
| **Name too long** | Exceeds 30 characters | Shorten app name |
| **Keyword stuffing** | "Best Photo Editor Camera Filter App" | Use clean, descriptive name |

**Fix Actions:**
1. Review all metadata before submission
2. Update screenshots with every UI change
3. Be honest about features and ratings
4. Use review notes for non-obvious features

---

### 5. Broken Login/Demo Account

**Guideline:** 2.1

| Issue | Description | Prevention |
|-------|-------------|------------|
| **No demo account** | Login required but no test credentials | Provide working demo account |
| **Demo account broken** | Credentials don't work | Test demo account before submission |
| **Limited demo access** | Demo can't access all features | Ensure demo has full access |
| **Demo expired** | Account timed out during review | Use account that doesn't expire |
| **Demo needs verification** | 2FA or email verification required | Disable for demo or provide all info |

**Demo Account Best Practices:**
```
Username: demo@yourapp.com
Password: AppReview2025!
Notes: Full access, no 2FA required
       If 2FA required, verification code: 123456
```

---

### 6. Payment System Violations

**Guideline:** 3.1.1, 3.1.2

| Issue | Description | Prevention |
|-------|-------------|------------|
| **External payment for digital** | Using Stripe/PayPal for in-app content | Use IAP for digital goods |
| **Linking to external purchase** | "Buy on our website" links | Remove external payment links |
| **Wrong IAP type** | Using consumable for permanent feature | Use correct IAP type |
| **No restore purchases** | Can't recover previous purchases | Implement restore functionality |
| **Subscription UI issues** | Price not prominent, missing disclosures | Follow HIG subscription requirements |
| **Misleading pricing** | Per-day pricing for monthly subscription | Show actual billing price |

**Note:** Some apps qualify for exceptions (see in-app-purchase-rules.md for exceptions).

---

### 7. Incomplete Information

**Guideline:** 2.1

| Issue | Description | Prevention |
|-------|-------------|------------|
| **Missing support URL** | No way to contact developer | Provide valid support URL |
| **Broken support URL** | URL doesn't work | Test URL before submission |
| **Placeholder content** | Lorem ipsum, TBD text | Complete all content |
| **Missing review notes** | No explanation for reviewers | Explain non-obvious features |
| **Backend not accessible** | Server down during review | Ensure backend is live |

**Review Notes Best Practices:**
- Explain any non-obvious features
- Provide demo account credentials
- Explain any special hardware requirements
- Note if app requires specific conditions to test
- Mention any features that might seem unusual

---

### 8. Design Issues

**Guideline:** 4.2

| Issue | Description | Prevention |
|-------|-------------|------------|
| **Minimum functionality** | App is just a website wrapper | Add native functionality |
| **Too simple** | App lacks adequate utility | Ensure meaningful features |
| **Copycat** | Too similar to existing app | Create original experience |
| **Marketing app** | App is just a catalog/brochure | Add interactive functionality |
| **Web-only content** | Could just be a website | Leverage native capabilities |

**Minimum Functionality Requirements:**
- Must do more than display web content
- Must provide lasting entertainment or utility
- Must not be primarily marketing material
- Must not be a simple repackaged website

---

### 9. UGC Without Moderation

**Guideline:** 1.2

| Issue | Description | Prevention |
|-------|-------------|------------|
| **No content filtering** | UGC posted without review | Implement filtering |
| **No reporting mechanism** | Users can't report content | Add report functionality |
| **No blocking capability** | Users can't block others | Add block functionality |
| **No contact information** | No way to report issues | Publish contact info |
| **Slow moderation** | Reports not addressed | Implement timely response |

**UGC Requirements Checklist:**
- [ ] Content filtering before posting
- [ ] Report button on all user content
- [ ] Block user functionality
- [ ] Published contact information
- [ ] Timely response to reports
- [ ] Age verification for mature content

---

### 10. Kids Category Violations

**Guideline:** 1.3

| Issue | Description | Prevention |
|-------|-------------|------------|
| **External links** | Links leaving app | Remove or put behind parental gate |
| **In-app purchases exposed** | Purchase without parental gate | Add parental gate |
| **Third-party advertising** | Ads from ad networks | Remove third-party ads |
| **Analytics tracking** | Collecting identifying info | Use privacy-safe analytics |
| **Account creation** | Email/password signup for children | Follow COPPA requirements |

**Kids Category Rules:**
- No links out of app (unless parental gated)
- No purchasing (unless parental gated)
- No third-party analytics collecting PII
- No third-party advertising
- Must comply with COPPA, GDPR-K

---

## Rejection Response Guide

### When You're Rejected

1. **Read carefully** — Understand exact rejection reason
2. **Don't panic** — Most rejections are fixable
3. **Identify guideline** — Know which rule was violated
4. **Plan fix** — Determine fastest path to approval
5. **Respond or resubmit** — Choose appropriate action

### When to Fix and Resubmit

| Scenario | Action |
|----------|--------|
| Valid rejection | Fix issue and resubmit |
| Clear mistake | Fix immediately |
| Simple fix | Faster to fix than appeal |
| Multiple issues | Fix all before resubmitting |

### When to Appeal

| Scenario | Action |
|----------|--------|
| Rejection seems incorrect | Appeal with evidence |
| Guideline misapplied | Explain why it doesn't apply |
| Need clarification | Ask for specific guidance |
| Have documentation | Show compliance evidence |

### How to Communicate with App Review

**DO:**
- Be professional and polite
- Reference specific guideline numbers
- Explain exactly what you changed
- Provide additional context if helpful
- Ask clarifying questions if confused

**DON'T:**
- Be argumentative or hostile
- Blame the reviewer
- Resubmit without changes
- Ignore the stated reason
- Submit multiple appeals for same issue

### Response Template

```
Hi App Review Team,

Thank you for your feedback regarding [App Name] (Version X.X).

I understand the rejection was related to Guideline [X.X.X] concerning [issue].

I have made the following changes to address this:
1. [Specific change made]
2. [Specific change made]
3. [Specific change made]

[If applicable: Here is additional context that may be helpful: ...]

Please let me know if you need any additional information.

Best regards,
[Your Name]
```

---

## Prevention Strategies

### Pre-Submission Testing

| Test | Details |
|------|---------|
| **Device testing** | Test on multiple real devices |
| **iOS version testing** | Test on minimum and current iOS |
| **Network testing** | Test with poor/no connectivity |
| **Edge case testing** | Test unusual user flows |
| **Accessibility testing** | Test with VoiceOver, Dynamic Type |

### Metadata Review

| Check | Details |
|-------|---------|
| **Screenshots current** | Match actual app UI |
| **Description accurate** | All claims are true |
| **Age rating honest** | Answered truthfully |
| **Support URL works** | Tested and accessible |
| **Demo account works** | Tested before submission |

### Privacy Audit

| Check | Details |
|-------|---------|
| **Privacy manifest** | Complete and accurate |
| **Privacy labels** | Match actual collection |
| **Privacy policy** | Comprehensive and accessible |
| **ATT implemented** | If tracking users |
| **SDK compliance** | All SDKs have manifests |

### Business Model Review

| Check | Details |
|-------|---------|
| **IAP required** | Using IAP for digital goods |
| **Exceptions apply** | If not using IAP, have valid exception |
| **Subscription UI** | Meets all HIG requirements |
| **Pricing clear** | No misleading pricing |

---

## Quick Reference: Rejection → Fix

| Rejection Reason | Fix |
|------------------|-----|
| Privacy policy missing | Add link to app and listing |
| Privacy manifest missing | Create PrivacyInfo.xcprivacy |
| Privacy labels incorrect | Audit code, update labels |
| App crashes | Debug, fix, test on real devices |
| Slow performance | Profile with Instruments, optimize |
| Screenshots don't match | Update screenshots |
| No demo account | Provide working credentials |
| External payment | Switch to IAP |
| No restore purchases | Implement restore functionality |
| Support URL broken | Fix URL, test accessibility |
| Minimum functionality | Add meaningful features |
| UGC without moderation | Add filtering/reporting/blocking |
| Kids category violation | Remove ads, links, or add parental gate |

---

*Rejection patterns evolve. Always verify against current Apple documentation.*
