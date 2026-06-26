# Publishing Scenario Reference

Use this reference when the requirement belongs to game publishing, growth, official website, recharge, SDK, or admin configuration scenarios.

## Scenario Selection

Choose the nearest scenario. If multiple scenarios apply, combine only the relevant modules.

| Scenario | Use When |
| --- | --- |
| Website campaign | Campaign page, reservation, reward claim, lottery, share activity, event landing page |
| Recharge center | Payment, top-up packages, bonus, rebate, order, refund, reconciliation |
| User acquisition | Ad landing page, channel link, campaign attribution, A/B test, conversion tracking |
| SDK | Login, payment, real-name verification, user agreement, data report, version compatibility |
| Admin configuration | Activity config, reward config, permission, publish workflow, query page, operation log |

## Website Campaign

Typical modules:

- Campaign landing page
- Login or account binding
- Reservation or registration
- Reward claim
- Lottery or draw
- Share invitation
- Campaign rule display
- Result page
- Admin campaign configuration
- Data dashboard

Key rules:

- Campaign status: not started, ongoing, ended, paused, offline
- Timezone and effective time
- User eligibility
- Claim limit per account, device, role, or server
- Reward inventory
- Anti-abuse strategy
- Display differences by platform or region

Common edge cases:

- User opens the page before campaign starts
- Campaign ends while the user is on the page
- Reward inventory runs out
- User claims repeatedly
- Login expires during claim
- Backend returns success but frontend times out
- Sharing source is missing or invalid

## Recharge Center

Typical modules:

- Recharge package list
- Payment method selection
- Order creation
- Payment confirmation
- Payment result
- Order history
- First-purchase bonus
- Accumulated recharge reward
- Refund or failed payment handling
- Admin package configuration
- Reconciliation report

Key rules:

- Currency and region
- Price display
- Payment channel availability
- Order status: created, pending, paid, failed, canceled, refunded, timeout
- Payment callback
- Reissue or compensation rule
- Risk control
- Invoice or receipt rules when applicable

Common edge cases:

- Payment succeeds but callback is delayed
- User closes the page during payment
- User pays an expired order
- Duplicate callback
- Currency mismatch
- User is in an unsupported region
- Payment channel maintenance

## User Acquisition

Typical modules:

- Ad landing page
- Download or store redirect
- Channel parameter recognition
- Campaign material configuration
- Conversion event tracking
- Attribution callback
- A/B test
- Data dashboard

Key rules:

- Channel source
- Campaign ID and creative ID
- Link parameter preservation
- Deep link and fallback link
- Device and platform detection
- Landing page variant assignment
- Conversion event definition
- Attribution window

Common edge cases:

- Missing channel parameter
- Invalid campaign link
- User switches browser or device
- Store redirect fails
- Attribution callback fails
- Duplicate conversion event
- A/B test traffic split mismatch

## SDK

Typical modules:

- Login
- Account binding
- Payment
- Real-name verification
- User agreement and privacy agreement
- Data report
- Error code handling
- Version compatibility
- Integration documentation

Key rules:

- Supported platform and version
- API request and response contract
- Callback format
- Error code mapping
- Signature and security verification
- Backward compatibility
- Upgrade path
- Sandbox and production environment

Common edge cases:

- SDK version too low
- Callback missing or duplicated
- Host app handles callback incorrectly
- Network retry causes duplicate request
- User cancels authorization
- Payment result is unknown
- Signature verification fails

## Admin Configuration

Typical modules:

- Create and edit configuration
- Preview
- Save draft
- Submit for review
- Publish
- Pause, resume, and offline
- Copy existing configuration
- Permission control
- Operation log
- Data query

Key rules:

- Field type and validation
- Required field
- Default value
- Effective time
- Review status
- Publish status
- Role permission
- Conflict detection
- Rollback rule

Common edge cases:

- Required configuration missing
- Time range conflict
- Reward inventory less than issued amount
- Admin changes config during campaign
- Publish fails
- Unauthorized operator attempts a change
- Data query returns too many results
