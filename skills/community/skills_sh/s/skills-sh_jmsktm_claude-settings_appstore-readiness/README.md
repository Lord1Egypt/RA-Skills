# iOS App Store Readiness Skill

Expert iOS App Store submission and approval system with 9 specialized agents to ensure first-submission approval.

## Overview

This skill provides comprehensive App Store compliance checking, drawing from Apple's official guidelines to help iOS apps pass App Review on the first attempt. It integrates with the ID8Pipeline as a **hard gate at Stage 9** (Launch Prep).

## Quick Start

```bash
# Full audit before submission
/appstore-readiness

# Quick compliance check during development
/appstore-review

# Step-by-step submission guide
/appstore-submit
```

## Agent Roster

| Agent | Role | When to Use |
|-------|------|-------------|
| **REVIEWER** | Compliance Auditor | "Will this pass review?", "Check my app" |
| **DESIGNER** | HIG Expert | UI/UX review, design compliance |
| **PRIVACY** | Data Guardian | ATT, privacy labels, privacy manifest |
| **COMMERCE** | IAP Strategist | Payments, subscriptions, commissions |
| **METADATA** | ASO Specialist | Screenshots, descriptions, keywords |
| **TECHNICAL** | Build Engineer | SDK requirements, performance, crashes |
| **SENTINEL** | Deadline Tracker | Submission timing, expedited reviews |
| **FIXER** | Rejection Recovery | Appeals, rejection responses |
| **MENTOR** | Teaching Partner | Explains why rules exist |

## Trigger Keywords

The skill activates automatically when discussing:
- `app store`, `iOS submission`, `apple review`, `app rejection`
- `aso`, `app store optimization`, `screenshots`
- `privacy manifest`, `privacy labels`, `ATT`, `app tracking`
- `iap`, `in-app purchase`, `subscription`, `storekit`
- `review guidelines`, `HIG`, `human interface`
- `testflight`, `app store connect`

## ID8Pipeline Integration

### Stage 9: Launch Prep (Hard Gate)

Before advancing to Stage 10 (Ship), projects must pass the App Store readiness audit:

```
/appstore-readiness
```

**Required checkpoints:**
- [ ] Privacy audit passed (PRIVACY agent)
- [ ] HIG compliance verified (DESIGNER agent)
- [ ] Technical requirements met (TECHNICAL agent)
- [ ] Metadata validated (METADATA agent)
- [ ] Full review simulation passed (REVIEWER agent)

### Stage 10: Ship

- SENTINEL tracks submission and review status
- FIXER handles any rejection
- METADATA optimizes based on performance

## Reference Documentation

The `references/` folder contains comprehensive guidelines (~100KB total):

| Document | Contents |
|----------|----------|
| `app-store-review-guidelines.md` | All 5 guideline sections with rule numbers |
| `human-interface-guidelines.md` | iOS HIG essentials |
| `privacy-requirements.md` | ATT, labels, manifests, third-party SDKs |
| `in-app-purchase-rules.md` | When IAP is required, 7 exceptions |
| `subscription-guidelines.md` | Auto-renewable subscription rules |
| `screenshot-metadata-specs.md` | Device sizes, metadata requirements |
| `common-rejection-reasons.md` | Top 10 rejections with prevention |
| `technical-requirements.md` | SDK, Xcode, performance standards |
| `pre-submission-checklist.md` | Final checklist before submission |

## Current Requirements (as of 2025)

| Requirement | Value |
|-------------|-------|
| **Xcode** | Version 16+ |
| **iOS SDK** | iOS 18 |
| **Privacy Manifest** | Required (since May 2024) |
| **SDK Signatures** | Required for all third-party SDKs |

## Example Audit Output

```
┌─────────────────────────────────────────────────────┐
│            APP STORE READINESS AUDIT                │
├─────────────────────────────────────────────────────┤
│ App: MyApp                                          │
│ Date: 2025-01-15                                    │
│ Pipeline Stage: 9 - Launch Prep                    │
├─────────────────────────────────────────────────────┤
│ OVERALL STATUS: READY                               │
│ Approval Probability: HIGH                          │
└─────────────────────────────────────────────────────┘

TECHNICAL       ✅ PASS
PRIVACY         ✅ PASS
DESIGN          ⚠️ WARNINGS
MONETIZATION    ✅ PASS
METADATA        ✅ PASS
REVIEW SIM      ✅ PASS
```

## File Structure

```
~/.claude/skills/appstore-readiness/
├── README.md              # This file
├── CLAUDE.md              # Quick reference & dispatch patterns
├── SKILL.md               # Complete agent specifications
└── references/
    ├── app-store-review-guidelines.md
    ├── human-interface-guidelines.md
    ├── privacy-requirements.md
    ├── in-app-purchase-rules.md
    ├── subscription-guidelines.md
    ├── screenshot-metadata-specs.md
    ├── common-rejection-reasons.md
    ├── technical-requirements.md
    └── pre-submission-checklist.md
```

## Related Commands

```bash
~/.claude/commands/
├── appstore-readiness.md  # Full audit workflow
├── appstore-review.md     # Quick check
└── appstore-submit.md     # Submission guide
```

## Contributing

This skill is maintained as part of the ID8Labs Claude settings. To update:

1. Edit reference docs when Apple updates guidelines
2. Update SKILL.md for agent behavior changes
3. Test with `/appstore-readiness` on a real project
4. Commit and push to `claude-settings` repo

## Official Apple Resources

- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [App Store Connect Help](https://developer.apple.com/help/app-store-connect/)
- [Privacy Requirements](https://developer.apple.com/app-store/app-privacy-details/)

---

*Built for ID8Labs to achieve first-submission App Store approval.*
