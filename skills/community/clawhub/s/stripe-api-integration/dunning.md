# Dunning — Failed Renewals and Involuntary Churn

**Read `## Volume & Fees` and `## Catalog` in `~/Clawic/data/stripe-api-integration/memory.md`** (or their boxes) before designing a retry policy: the right number of attempts depends on the price point and the effective fee rate, not on a best practice.

**Contents:** [Involuntary Churn Is the Cheapest Revenue in the Building](#involuntary-churn-is-the-cheapest-revenue-in-the-building) · [Why Renewals Fail](#why-renewals-fail) · [The Subscription States That Matter](#the-subscription-states-that-matter) · [Retry Strategy](#retry-strategy) · [Prevention Beats Recovery](#prevention-beats-recovery) · [The Emails](#the-emails) · [What Happens at the End of Retries](#what-happens-at-the-end-of-retries) · [Measuring It](#measuring-it)

## Involuntary Churn Is the Cheapest Revenue in the Building

Voluntary churn is a customer deciding to leave. Involuntary churn is a customer who still wants the product and whose card failed. The second group has no objection to overcome — the only work is making the payment succeed, and a meaningful share of failed renewals recover with nothing more than a retry at a better time and a card-update prompt.

That makes dunning the highest-return billing work most teams have not done, and the reason it stays undone is that nobody owns it: it fails silently, in the background, to customers who never complain because they do not know.

## Why Renewals Fail

| Cause | Signal | Recoverable? |
|---|---|---|
| Insufficient funds | `decline_code: insufficient_funds` | Very — timing is the whole game |
| Expired card | `expired_card`, or a card whose `exp` has passed | Yes, with an updater or a customer prompt |
| Card replaced (lost, stolen, reissued) | `lost_card`, `stolen_card`, or a hard decline on a card that worked for a year | Only with a new card from the customer |
| Issuer risk decision | `do_not_honor`, `generic_decline` | Sometimes, later |
| Authentication required | `authentication_required` | Only on-session — never by retrying (`sca-3ds.md`) |
| Bank debit returned | Failure event days after "success" | Depends on the return reason; some rails charge you per failure |
| No default payment method | Invoice fails with nothing to charge | Always — this is a setup bug, not a decline |

The first two dominate. Designing for them — timing and card freshness — is most of the recoverable revenue.

## The Subscription States That Matter

```
active ──payment fails──> past_due ──retries exhausted──> unpaid | canceled
   ^                          |
   └──────invoice.paid────────┘
```

- `past_due`: retries are running. The customer usually still has access, and that is a business decision, not a Stripe default to accept blindly.
- `unpaid`: retries are done and Stripe left the subscription in place without collecting. Invoices keep being generated unless configured otherwise — a slow way to accumulate uncollectible debt.
- `canceled`: over. Reactivating means a new subscription; the old one does not come back.
- `incomplete` / `incomplete_expired`: the *first* payment never completed, and after roughly 23 hours it cannot. This is not dunning, it is a failed signup — different funnel, different fix (`subscriptions.md`).

Drive access from events, not from a nightly job reading your own table: `invoice.payment_failed` opens the grace period, `invoice.paid` closes it, `customer.subscription.deleted` revokes.

## Retry Strategy

Stripe retries automatically on a schedule you configure, and Smart Retries picks the times using signals from across the network rather than fixed intervals. The parameters you actually own:

- **Number of attempts.** More attempts recover more, with diminishing returns and, on bank rails, a per-failure cost. Stop when the expected recovery of the next attempt is below its cost: `expected_recovery = remaining_probability × price`, compared against the failure fee plus support load. For a 9 EUR plan that is a small number of attempts; for a 900 EUR plan it is worth more.
- **Spread, not clustering.** Retrying three times in 24 hours mostly re-hits the same empty balance. Spanning a couple of weeks crosses at least one payday, which is the single biggest lever on `insufficient_funds`.
- **Terminal behavior.** Cancel, mark unpaid, or leave it — decide deliberately (below).
- **Off-session declines that ask for authentication leave the schedule entirely.** They need the customer, so route them to the recovery loop instead of burning attempts (`sca-3ds.md`).
- Manual retries have their place: after the customer updates their card, retry the open invoice immediately instead of waiting for the next scheduled attempt.

## Prevention Beats Recovery

- **Card account updater**: networks push new card numbers and expiry dates for reissued cards, and Stripe applies them to saved payment methods. Enabling it removes a whole failure category before it happens.
- **Network tokens** survive card reissues for the same reason and generally authorize better than a stored PAN.
- **Ask for a backup payment method** on high-value plans; a SetupIntent costs one screen and saves the renewal.
- **Prompt before expiry, not after.** Cards expire on a date you already know; an email in the last month of validity converts far better than one sent after the failure.
- **Renew at a sane hour** in the customer's timezone, not at whatever minute the subscription was created.
- **Watch `customer.subscription.trial_will_end`** — it fires days before the trial ends and is the last cheap moment to fix a missing payment method.

## The Emails

Stripe can send them, or your app can. Either way the content decides the outcome.

- Say what happened in the customer's language: "your bank declined the payment" beats "invoice 4471 failed".
- One action, one link, straight to the hosted invoice page or the Billing Portal. A login wall between the customer and the payment is a churn generator.
- Distinguish the two cases: a card problem asks for a new card; an authentication request asks them to confirm with their bank. Sending the first message for the second case makes people replace a perfectly good card.
- Escalate the tone slowly and say when access ends. Surprise cut-off produces refund requests and disputes (`disputes.md`).
- Stop emailing the moment the invoice is paid — the most common complaint about dunning is a dunning email after payment.

## What Happens at the End of Retries

| Terminal behavior | Use when | Consequence |
|---|---|---|
| Cancel the subscription | Consumer plans, self-serve | Clean; the customer resubscribes if they come back |
| Mark the invoice uncollectible and leave the subscription | Enterprise with a human relationship | Keeps the relationship; the debt is visible instead of pretended away |
| Pause collection | Known temporary problem the customer told you about | Access decision is yours; invoices stop piling up |
| Keep charging forever | Never | Uncollectible invoices distort every revenue number you produce |

Whatever the choice, revoking access must be idempotent and reversible: the same customer will pay two days later, and the reactivation path has to work without a support ticket.

## Measuring It

- **Recovery rate** = recovered invoices ÷ failed invoices, over a window long enough to include the whole retry schedule. Measuring it weekly against a schedule that spans two weeks reports a number that is always wrong.
- **Involuntary share of churn** = failed-renewal cancellations ÷ all cancellations. If it is a large slice, dunning is the cheapest growth work available.
- **Cost per recovery**: failure fees plus support time, against recovered revenue. This is the number that decides attempt count.
- Rehearse every change with a test clock before shipping it — a retry schedule is a time-dependent system and cannot be validated by reading it (`testing.md`).

---

**When the retry schedule, grace period or terminal behavior is decided or changed**, write it to `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`, and save the reasoning — attempt count against price point, measured recovery rate — as `artifacts/decision-dunning.md` with its `## Boxes` line in the same turn. Record measured recovery rates alongside the month in `## Volume & Fees`, so the next change has a baseline instead of an opinion.
