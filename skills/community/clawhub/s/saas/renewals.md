# Renewals, Downgrades and Cancellation

Scope: keeping revenue that already exists — the renewal event, the cancel flow, save offers, win-back. Growing existing revenue is `expansion.md`; failed payments are `dunning.md`.

**Before any renewal or save conversation**, read `## Accounts` in `~/Clawic/data/saas/memory.md` (or `accounts.md`) for the plan, ARR, seats and renewal date, `## Commitments` for anything non-standard already granted to this customer, and `## Churn Reasons` for whether this reason is a pattern or a one-off. Granting the same concession twice at different values, to two customers with the same problem, is how a discount policy dies.

## The Renewal Is Won Before the Renewal Call

The renewal date is a deadline, not an event. Work backwards from it:

| Days before term end | Action |
|---|---|
| 90 | Usage and seat review: is consumption up, flat or down against last year? Down is the signal, and it is visible nowhere else this early |
| 60 | Renewal notice window opens for auto-renewing contracts (`renewal_notice_days`); confirm the billing contact still works there |
| 45 | Value recap with the numbers the buyer will need internally — usage, outcomes, tickets resolved, uptime achieved |
| 30 | Commercial conversation: uplift, term, seat true-up, any change to the package |
| 14 | Paperwork; a renewal still unsigned here is at risk, not late |
| 0 | Term ends. Churn is recorded in this month, not in the month notice was given (`revenue.md`) |

A renewal first discussed in its final fortnight is a price negotiation. The same renewal opened at 90 days is a usage conversation, and usage conversations produce uplift rather than discounts.

## Notice and Auto-Renewal Terms

- **Auto-renewal is the default worth having**, and it comes with obligations: advance notice before each renewal charge, clear cancellation instructions, and the renewal price stated. Several jurisdictions require some of this, and where it is not required it still prevents chargebacks (`compliance.md`, `dunning.md`).
- **Notice periods cut both ways.** A 60-day cancellation notice protects revenue and, in a buyer's procurement review, reads as a trap; a 30-day notice on an annual term is the common compromise.
- **Never rely on a silent renewal at a higher price.** An uplift applied without a stated notice is the single most reliable way to convert a renewal into a dispute and a public complaint.
- **Multi-year contracts**: price the uplift into the contract as a stated annual step, not as a surprise at each anniversary. A fixed multi-year price is a discount you have not measured.

## The Cancel Flow

The cancel flow's job is to route accurately, not to obstruct. Obstruction produces chargebacks and reviews; accurate routing produces both saves and a reason distribution worth having.

1. **Self-serve, findable, always.** A cancellation that requires an email is a chargeback in waiting and in some jurisdictions an outright violation.
2. **Reason first, from a fixed list**, with a free-text field second. The fixed list is what makes the distribution countable — a synonym invented per session makes the whole log useless (`memory-template.md`).
3. **Route by reason.** An offer only where an offer actually fixes the reason:

| Stated reason | Offer that works | Offer that backfires |
|---|---|---|
| Too expensive | Downgrade to a smaller plan, or annual at the standard discount | A bespoke discount: it prices the whole book |
| Missing a feature | Roadmap date if it is real, otherwise let them go cleanly | A vague "it's coming" — they return angrier |
| Not using it | Pause, or a smaller plan; ask what changed | A discount on something they do not use |
| Project ended / company changed | Pause with data retained, and a named contact for the return | Anything at all; this is not a product loss |
| Switched to a competitor | One honest question about what decided it | Matching the competitor's price |
| Bad experience / bugs | A person, today, and a specific fix | An offer instead of a fix |

4. **Confirm what happens next** on the confirmation screen: access until the paid term ends, data retention period, how to export, how to come back.
5. **No dark patterns.** Hidden buttons, forced calls, multi-step interrogation. Every one converts a churn into a chargeback plus a review, and the review outlives the MRR.

## Pause Instead of Cancel

The most underused retention mechanism. A pause offer — a bounded window with no charge, data retained, one-click resume — converts a share of cancellations that would otherwise be permanent, at no marginal cost for products with low per-account infrastructure cost.

- Bound it: a defined number of months maximum, with an automatic resume or cancellation at the end. Unbounded pause is a free tier with extra steps.
- Treat paused MRR as churn in the bridge (MRR is zero) and record the pause in `## Accounts` — otherwise a wave of pauses looks like a recovery that never arrives.
- Do not offer pause to accounts whose stated reason is a missing feature or a bad experience: it postpones the same conversation.

## Downgrades

A downgrade is contraction and a retained relationship. Treat it as a win compared to the alternative.

- Make it as self-serve as the upgrade. Forcing a call to downgrade produces cancellations instead.
- Handle the excess: seats, projects and data above the new limit become read-only, never deleted, with the admin choosing what to keep (`entitlements.md`).
- Record it as `contraction` in `## Churn Reasons` with the reason. Contraction reasons predict next year's churn better than churn reasons do, because the account is still there to be asked.
- Re-open the conversation on a schedule rather than at the next renewal: an account that shrank for budget reasons has a new budget cycle.

## Win-Back

- The window is short. Reach out within a few weeks while the alternative is still being set up; after a quarter the switching cost is theirs, not yours.
- Win-back works when the reason was fixable and got fixed: "the thing you left over now exists" with the specifics. It fails as a generic discount.
- A churned account is a warmer lead than a stranger — they know the product and the buying process. Keep them in `## Accounts` with their churn reason rather than deleting the row.
- Returning customers are reactivation in the bridge, never new (`revenue.md`).

## Save Discipline

- Every save offer comes from a fixed menu bounded by `discount_ceiling_pct`, and anything beyond it needs the approval path defined in the risk-posture preference area.
- A permanent discount granted to save an account is a permanent obligation: it goes in `## Commitments` with a revisit date, or it becomes invisible and forever.
- Trade concessions for something: a longer term, a case study, a reference call, annual prepay. A concession given for nothing sets the price of the next renewal.
- Measure save rate by reason. A high overall save rate driven entirely by discounts is not retention, it is a slow price cut.

**After any renewal, downgrade, cancellation, pause or save**, write the outcome to `## Accounts` (new plan, ARR, next renewal date) and the event to `## Churn Reasons` with its type — `voluntary`, `involuntary` or `contraction` — and the exact reason string reused from the existing list, in the same turn. Any concession granted goes to `## Commitments` with its value and expiry; a cancel flow or renewal sequence that measurably worked belongs in `artifacts/<kebab-name>.md` with its `## Boxes` line (`memory-template.md`).
