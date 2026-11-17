# Dunning — Failed Payments and Involuntary Churn

Involuntary churn is a payments problem wearing a retention costume. In card-billed SMB SaaS it commonly accounts for 20-40% of gross churn, and a competent recovery sequence typically recovers half to three-quarters of failed payments — making it the highest-return retention work available, because the customer never decided to leave.

**Before any retention analysis**, read `## Churn Reasons` in `~/Clawic/data/saas/memory.md` (or `churn-log.md` if `## Boxes` points there) and confirm churn is split into `voluntary`, `involuntary` and `contraction`. A single blended churn number cannot tell you whether you have a product problem or an expiry date problem (SKILL.md Rule 5).

## Know Why the Charge Failed

The decline reason decides the entire response. Retrying the wrong category burns retry attempts and, at volume, damages the merchant account's authorization rate.

| Category | Typical reasons | Retry? | Response |
|---|---|---|---|
| Soft, transient | Insufficient funds, issuer unavailable, do-not-honour | Yes | Scheduled retries; most recovery lives here |
| Soft, timing | Card expired, expired but updatable | Yes, after update | Card-updater service, then in-app prompt |
| Hard | Stolen, lost, closed account, revoked authorization | No | Ask for a new payment method immediately; retrying is a compliance and reputation cost |
| Authentication | 3-D Secure / SCA challenge required | Not blind | Requires customer action in the session; a silent retry always fails |
| Risk block | Fraud rule on your side or the issuer's | No | Manual review; often a legitimate customer with an unusual pattern |

Store the raw decline code per attempt. "Payment failed" as a category makes every recovery number uninterpretable, and the codes are what reveal a systematic issue — one issuer, one country, one BIN range — rather than a diffuse one.

## The Retry Schedule

Attempts spread over the dunning window (`dunning_window_days`, default 21), not bunched:

- Day 0 initial charge fails → in-app banner immediately. **In-app precedes email**: the admin is often already logged in, and the banner is seen when the email is not.
- Retries at roughly day 1, day 3, day 7. Recovery probability falls steeply after the first week; attempts beyond four rarely add recovery and do add processor cost.
- **Avoid weekends and the 1st of the month** for retries where the failure was insufficient funds: the deposit-cycle argument is why the payday-aligned retry recovers more than the calendar-spaced one.
- Escalate the recipient, not the frequency: admin → billing contact on file → any other admin on the account. The commonest cause of unrecovered soft declines is that the only email on file belongs to someone who left the company.
- Exponential fatigue is real. Four emails over three weeks is a sequence; eight is a spam complaint.

## Prevention Beats Recovery

Recovery is repair work. These reduce the failures themselves:

- **Card-updater / account-updater networks** (offered by the major card networks through most providers) refresh expiring and reissued cards automatically. It is usually a switch, and it removes a meaningful share of expiry failures before they happen.
- **Pre-expiry notice** for cards expiring before the next renewal — a short in-app prompt weeks ahead recovers far more cheaply than a decline does.
- **Backup payment method** on file for annual and enterprise accounts, used automatically when the primary fails.
- **Retry the annual renewal earlier than the term end** so there is runway inside the paid period; a failure discovered on the last day has no room.
- **Offer bank transfer / invoice above a threshold ACV.** Card limits are a common and invisible cause of large-invoice failure, and above roughly five figures annually most buyers prefer invoicing anyway (`sales-motion.md`).
- **Local payment methods where you sell.** Card penetration varies enormously by country; SEPA direct debit, iDEAL, boleto and similar remove failures no retry schedule can (`compliance.md`).
- **Update SCA-exempt setup properly**: subscriptions set up with the correct off-session merchant-initiated flag avoid a per-renewal authentication challenge that would otherwise fail silently.

## What Happens to Access

| Phase | Access | Message |
|---|---|---|
| Day 0 to window end | Full (`past_due`) | Banner naming the card and the date access changes |
| Window end | Suspended: read and export only | Email stating the data-retention period |
| Retention period after suspension | Data held, account restorable in one click | Reminder at the midpoint and shortly before deletion |
| After retention period | Deletion per policy | Notice sent before, never after |

Suspending on the first decline is the classic own goal: it converts a temporary card problem into a support incident and often into a real cancellation. Full access through the window costs a few weeks of service and recovers a customer.

## Measuring It

Four numbers, monthly, in `## Revenue` alongside the movement bridge:

- **Failure rate** = failed charges ÷ charges attempted. A step change means a processor, rule or configuration change, not customer behaviour.
- **Recovery rate** = accounts recovered within the window ÷ accounts that entered dunning. This is the number the sequence is tuned against.
- **Involuntary share of gross churn** = involuntary churned MRR ÷ total churned MRR. Above roughly a third, dunning is the highest-value project in the company.
- **Days to recovery**, median. Rising means the sequence is reaching people too late.

Compare only against your own history. Published benchmarks mix card-heavy consumer books with invoice-heavy enterprise ones and mean nothing across that gap.

## Chargebacks

A chargeback is worse than a failed payment: the money reverses, a fee applies, and a rising ratio threatens the payment account itself.

- The commonest cause is an unrecognized descriptor. Set the billing descriptor to the brand the customer knows, not the legal entity.
- Renewal notice before charging — required in several jurisdictions for auto-renewal, and independently the cheapest chargeback prevention there is (`compliance.md`).
- Frictionless self-serve cancellation. A customer who cannot find the cancel button disputes the charge instead, and the dispute costs the fee plus the relationship.
- Respond to disputes with evidence assembled automatically: signup record, terms acceptance, usage log, invoice, and the cancellation-policy text as displayed at purchase.
- Watch the ratio against the processor's threshold, not against your comfort. Crossing it means monitoring programmes, reserves and, eventually, account termination.

**After any dunning change or review**, write the recovery and failure rates for the period to `## Revenue`, every involuntary loss to `## Churn Reasons` with its decline category, and the sequence itself — timings, channels, escalation, retention period — to `artifacts/<kebab-name>.md` with its `## Boxes` line, in the same turn (`memory-template.md`). Add the dunning review to `## Due` as a monthly row: a sequence that is never re-measured degrades quietly as card mix and processor rules change.
