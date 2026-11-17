# Expansion — The NRR Engine

Scope: growing revenue inside accounts that already pay. Keeping them is `renewals.md`; the plan structure that makes expansion possible is `packaging.md`.

**Before designing an expansion play**, read `## Accounts` in `~/Clawic/data/saas/memory.md` (or `accounts.md`) for seats, ARR and renewal dates, `## Plans` for the current fences, and `## Revenue` for the expansion and contraction lines. Expansion work aimed at a book whose contraction exceeds its expansion is a leak repair, not a growth project.

## Why It Dominates Everything Else

Expansion revenue costs a fraction of new-logo revenue to acquire: no acquisition spend, no evaluation cycle, no security review, no onboarding. Above 100% NRR the business grows with the sales team switched off, and that compounding is what separates a durable SaaS from a treadmill.

The arithmetic worth carrying: at 100% NRR, a book of 1M ARR is 1M next year without new sales. At 115%, it is 1.15M — the equivalent of 150k in new ARR at zero CAC. That comparison decides most roadmap arguments about whether to build for new users or existing ones.

## The Levers, Ranked by Cost to Pull

| Lever | Marginal cost | Trigger that should fire it |
|---|---|---|
| Automatic seat growth | Near zero | The account adds a user; billing follows without a conversation |
| Usage crossing a tier ceiling | Near zero | 80% of the fenced metric, surfaced in product (`entitlements.md`) |
| Self-serve tier upgrade | Near zero | A gated feature is attempted repeatedly |
| Add-on purchase | Low | The specific need appears in usage — extra environment, storage, premium support |
| Renewal uplift | Low | Contract anniversary with usage grown |
| Cross-sell of a second product | Medium | Adoption depth in the first product, not calendar time |
| New department or region | High | An internal champion who will introduce you (`sales-motion.md`) |

Work top-down. Teams routinely build a cross-sell motion while the seat-add flow still requires an email to support, which is expansion revenue being refused.

## Make Expansion Automatic

- **Self-serve seat addition, always.** An admin adding a colleague at 11pm must not need anyone. Prorate the addition, show the resulting charge before confirming, and bill it in the same period.
- **Show consumption against the ceiling continuously**, not at 100%. The upgrade decision needs runway; a wall discovered mid-workflow produces a ticket, not a purchase (`entitlements.md`).
- **Upgrade in one click from the point of friction**, with the recommended plan derived from observed usage and the price shown. A generic "contact sales" link at the wall loses the moment.
- **Prorate honestly** and show the arithmetic. An unexplained mid-cycle charge is a support ticket and a trust cost that outlives the revenue.
- **Never require a call to spend more money.** Whatever the motion, the path to giving you more must be shorter than the path to leaving.

## Expansion Triggers Worth Instrumenting

Each of these is a signal that should generate an in-product prompt or a task, depending on `motion`:

- Consumption at 80% of any fenced metric, with the trend implying a crossing within the period.
- Repeated attempts to use a gated feature — three attempts by two different users is intent, not curiosity.
- A new user domain appearing on the account (a different department signing up with the same company domain).
- Seat utilization above roughly 90% of licensed seats: they are about to need more, and the conversation is easy.
- An integration connected that implies a workflow you charge for.
- Support tickets asking how to do something an upper tier does.
- Usage growth outpacing the account's own trailing average by a wide margin for two consecutive periods.

Instrument these as events with the account attached, so the trigger is queryable rather than anecdotal (`revenue.md`).

## Renewal Uplift

The annual price step applied to existing customers. Handled well it is the single most reliable expansion lever for contract-based books; handled badly it is a churn event.

- **State it in the contract** as an annual step. A pre-agreed uplift is administration; a surprise uplift is a negotiation you start from behind.
- **Size it against delivered value**, not against inflation alone: an account whose usage doubled can absorb a real step; one whose usage fell will treat any step as an insult.
- **Never apply an uplift and a packaging change in the same renewal.** Two changes at once means the customer cannot evaluate either and will assume the worst about both (`plan-changes.md`).
- **Exempt accounts already at risk.** An uplift on a red-health account is a churn you scheduled.
- The price level itself, and how to test it, is `pricing`.

## Contraction: The Other Half of NRR

NRR is a net number, and teams that only work expansion get surprised by it. Contraction is quieter than churn and almost always visible in advance.

| Contraction signal | Lead time | Response |
|---|---|---|
| Seat utilization falling below ~60% of licensed | Months | Seat review before they discover it themselves at renewal |
| Usage of the primary workflow declining two periods running | Months | Find out what changed; often a process change, not a product failure |
| Champion departure | Weeks | Re-establish with the successor immediately; champion loss is the strongest single churn predictor there is |
| Support tickets stopping entirely | Ambiguous | Either fully self-sufficient or fully disengaged; usage tells you which |
| Procurement asking for a cost breakdown | Weeks | A budget review is running; get the value recap in before it concludes |

Recording contraction with its reason in `## Churn Reasons` is more valuable than recording churn: the account is still there, so the hypothesis can be tested.

## Cross-Sell and Multi-Product

- The prerequisite is depth in the first product, not tenure. An account that has not adopted product one will not adopt product two, and pushing it damages the relationship that was working.
- Bundle pricing must beat the sum of the parts by enough to matter, or nobody moves; if it does not, sell them separately and stop calling it a suite.
- One invoice, one login, one admin surface. Multi-product companies that keep separate billing and identity per product create their own churn at every renewal.
- Attribute cross-sell revenue to expansion, not to new — it flatters new-logo performance otherwise and hides a slowing top of funnel (`revenue.md`).

**After any expansion, uplift, cross-sell or contraction**, write the new plan, seats and ARR to `## Accounts` and the movement to `## Revenue` in the correct bucket in the same turn; contraction gets its reason row in `## Churn Reasons`. An expansion play that worked — the trigger, the message, the observed conversion and its sample size — belongs in `artifacts/<kebab-name>.md` with its `## Boxes` line (`memory-template.md`).
