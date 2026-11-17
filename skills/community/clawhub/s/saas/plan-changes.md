# Plan Changes — Migrations, Grandfathering and Sunsetting

Scope: changing what already-paying customers are on — repackaging, limit changes, plan retirement, forced migrations. Designing the new packaging is `packaging.md`; the price level is `pricing`; the renewal conversation is `renewals.md`.

**Before announcing anything**, read `## Plans` in `~/Clawic/data/saas/memory.md` (or `plans.md`) for what exists today, `## Commitments` for every customer with a contractual price, feature or term that a change would breach, and `## Accounts` for who sits on the affected plans and what their renewal dates are. A migration announced before that inventory exists produces an exception list assembled under time pressure, which is how contracts get broken.

## Every Change Is a Cohort Problem

Four populations, four different obligations. Name each one and its treatment before writing a single announcement.

| Cohort | Constraint | Default treatment |
|---|---|---|
| Monthly self-serve on a public plan | Terms usually allow change with notice | Notice period, then the new plan at the next billing date |
| In-trial or mid-signup | Was shown the old plan | Honour what they were shown for their first term |
| Annual, mid-term | Paid for a defined package | No change until renewal, without exception |
| Contractual / grandfathered / enterprise | `## Commitments` says what was promised | Change only by agreement; unilateral change is a breach |

The exception nobody plans for: customers on a plan that no longer exists because it was retired years ago and never migrated. They are in the data, they are paying, and they will be the loudest. Find them with a query, not with memory.

## The Migration Decision

Three options for existing customers, and the choice is a business decision that should be made explicitly rather than by drift.

| Option | Cost | Right when |
|---|---|---|
| Grandfather indefinitely | Permanent engineering and support complexity; the old plan must be maintained forever | The affected population is tiny and loyal, or a contract requires it |
| Grandfather for a period, then migrate | One-off migration work at a known date | The default: a stated window — commonly one renewal cycle or a year — is generous enough to be accepted and bounded enough to end |
| Migrate immediately with notice | Churn risk concentrated in one moment | The old plan is loss-making or a security liability, and the notice period is real |

- **Grandfathering has a cost that compounds.** Every legacy plan is a branch in entitlements, billing, support answers and every future packaging analysis (`entitlements.md`). Three legacy plans is manageable; a decade of them means nobody can answer what the product costs.
- **Record every grandfathered account** with the plan, the terms and the end date in `## Commitments`. "Grandfathered" with no end date is permanent, whatever anyone intended.
- **Never change two variables at once.** Price and packaging in the same announcement means the customer cannot evaluate either, and will assume the worst about both (`expansion.md`).

## Notice and Sequencing

Working backwards from the effective date:

| Before effective date | Action |
|---|---|
| Internally, before anything | Model the revenue impact per cohort: expected uplift, expected churn, net. Decide the acceptable churn budget in advance |
| 90 days | Brief support and sales with the reasoning, the exception rules and the answers to the obvious objections. A support agent improvising an exception sets policy |
| 60 days | Direct notice to affected customers — email plus in-product — with what changes for *them* specifically, not a generic announcement |
| 30 days | Reminder, with the comparison of their current usage against the new plan and the resulting price |
| 14 days | Final reminder; open a path to talk for anyone who has not responded |
| 0 | Effective. Old plan disabled for new signups long before this, not on this day |
| +30 days | Measure: actual churn and contraction against the budget, in `## Churn Reasons` and `## Revenue` |

Personalized notice outperforms a generic one by a wide margin: a customer who reads "your plan changes from X to Y, your price changes from A to B, your usage last month was Z" has nothing to fear or misinterpret. A blog post is not notice.

## Sunsetting a Plan or a Feature

- **Close it to new signups first**, months before retiring it for existing customers. The population then only shrinks.
- **State the replacement** and make the path to it one click. A sunset with no destination reads as a removal of value.
- **Migrate the data.** If the replacement cannot hold what the old plan held, it is not a replacement and the sunset is not ready.
- **Feature removal follows the same discipline as plan removal**, and is more emotive: usage data showing near-zero adoption is what makes it defensible, and the handful of heavy users of a dead feature deserve a personal conversation rather than an email.
- **Deprecation for APIs specifically**: an announced date, a documented alternative, per-customer usage reporting so heavy callers are contacted directly, and a sunset window measured in quarters. Breaking an integration silently is a churn event with a long tail (`enterprise.md`).

## Handling Exceptions Without Destroying the Policy

- **Decide the exception rule before announcing**, not per email. A written rule — for example, one extension of a stated length, granted once, for any account that asks before the effective date — is fair, defensible and finite.
- **One named approver** beyond the rule. Exceptions granted by whoever received the email produce a book nobody can describe.
- **Every exception is a row in `## Commitments`** with its expiry. Exceptions are how permanent obligations are created accidentally.
- **A migration that generates exceptions for a large share of the affected accounts is a badly designed migration.** Stop and redesign rather than processing them one at a time.

## Measuring the Change

Set the success criteria before the announcement, then measure at 30 and 90 days:

- Churn and contraction against the pre-agreed budget, split by cohort. A single blended number hides which cohort revolted.
- Realized ARPA before and after, on the affected population only.
- Support volume attributable to the change, and how long it took to decay.
- Migration completion rate: the percentage on the new plan by the effective date, and who is still stranded.
- Net revenue impact against the model, with the variance explained. A migration that beat the model is as important to understand as one that missed.

Write these into `## Revenue` and `## Churn Reasons` with the change named in the notes; a year later, the next repackaging is planned from this record or from nothing.

## Price Increases on Existing Customers

The pricing skill owns the price level and how to test it. What belongs here is the operational side:

- New customers first, existing at renewal with notice. Applying a rise to a mid-term annual contract is a breach of what they bought.
- Exempt at-risk accounts identified in `## Accounts`; a rise on a red-health account is a scheduled churn.
- Communicate the increase with what changed in the product, not with cost inflation alone. Customers accept paying more for more; they resent paying more for the same.
- Budget for churn explicitly and measure against the budget — the actual departures as rows in `## Churn Reasons`, the revenue delta in `## Revenue`. A rise that produces no churn was probably too small: write that outcome into the `Notes` of the `## Revenue` row, naming the rise, or the next pricing decision repeats the same undershoot.

**After any plan change, migration or sunset**, write the new plan state to `## Plans` with a `## Retired Plans` entry for anything sunset (date, replacement, who was grandfathered), every grandfather or exception to `## Commitments` with its expiry, the measured churn and revenue impact to `## Churn Reasons` and `## Revenue`, and the migration plan with its cohort model to `artifacts/<kebab-name>.md` with its `## Boxes` line (`memory-template.md`). Track the migration itself as a programme in the shared `~/Clawic/data/projects/<project>.md` when it spans more than a few weeks.
