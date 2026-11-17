# Support and Customer Success at Scale

Scope: serving customers without headcount growing with the customer count — deflection, tiering, coverage ratios, health scores. The support commitments in an enterprise contract are `enterprise.md`; the cost side is `margins.md`.

**Before proposing a support or CS structure**, read `## Accounts` in `~/Clawic/data/saas/memory.md` (or `accounts.md`) for the ARR distribution — a book of many small accounts and a book of a few large ones need opposite structures — and `## Commitments` for response-time targets already contracted.

## Support and Success Are Different Jobs

| | Support | Customer success |
|---|---|---|
| Trigger | The customer contacts you | You contact the customer |
| Measures | Time to first response, resolution time, satisfaction | Retention, expansion, health |
| Scales with | Ticket volume, which tracks account count | Revenue concentration |
| Cost line | COGS | COGS if it is required to run the service; sales cost if it is an upsell motion (`margins.md`) |

Merging them produces a team that is reactive by day and never does the proactive work, because tickets always win the priority argument. Separate the queues, even inside one person's calendar.

## Coverage Ratios

Coverage follows revenue concentration, not headcount ambition. The commonly used shape, to be calibrated against your own ticket data rather than adopted blind:

| Segment | Model | Rough coverage |
|---|---|---|
| Self-serve, low ACV | Pooled / tech-touch: docs, in-app guidance, email queue, community | No named owner; measured by deflection rate |
| Mid-market | Pooled CS with proactive plays triggered by health signals | One CSM per roughly one to two million in ARR |
| Enterprise | Named CSM, scheduled reviews, escalation path | One CSM per roughly three hundred thousand to a million in ARR, depending on complexity |

Sanity check before hiring: **fully loaded cost of the hire ÷ ARR they would own** should be a small single-digit percentage. If a named CSM would cost a fifth of the revenue they cover, the segment needs tech-touch, not a person.

Support headcount is driven by tickets per account per month, which is a **product** number: the fix is almost always upstream. Hiring against a rising ticket rate treats the symptom and locks in the cost permanently.

## Deflection Before Headcount

In order of return:

1. **Fix the top ticket driver.** Tag every ticket with a cause, sort by volume monthly, and route the leader to the product backlog. The top three causes are usually a meaningful share of all volume, and each fix removes tickets forever rather than answering them faster.
2. **In-product answers at the point of confusion**, not a help centre the customer has to leave to find. Contextual help against the screen where the question arises deflects more than any documentation reorganization.
3. **Documentation that matches the current product.** Stale docs generate tickets and destroy trust in every other page.
4. **Self-serve actions for the top request types**: change plan, add seats, update card, export data, reset access, cancel. Each one that requires a human is a permanent tax and, for cancellation, a chargeback risk (`renewals.md`).
5. **Status page and proactive incident communication.** An unannounced outage generates a ticket from a large share of active accounts at once (`incidents/<year>.md`).
6. **Automation and assistants last**, on top of good documentation. Deployed over bad docs they produce confident wrong answers, which cost more than the ticket did.

## Tiering by Plan

Response-time targets belong to plans and are worth real money on enterprise tiers.

| Severity | Definition | Typical target on a paid tier |
|---|---|---|
| S1 | Production down or unusable for the account | Response in an hour or less, contracted, with an escalation path |
| S2 | Major function broken, workaround exists | Same business day |
| S3 | Minor issue, question | One to two business days |
| S4 | Feature request, feedback | Acknowledged, then routed to product |

- **Response time is the commitment; resolution time is not.** Committing to a resolution time for a defect you have not seen is a promise you cannot keep.
- Define business hours and the coverage regions explicitly. "24/7" without a follow-the-sun team or a paid rota is a commitment to burn someone out.
- Measure against the target and publish the achievement internally. A contracted response target with no measurement is a breach nobody has noticed yet (`enterprise.md`).

## Health Scores That Predict Rather Than Describe

Most health scores are a coloured restatement of last month's usage. A useful one is built from signals that lead churn:

| Signal | Weight it deserves | Why |
|---|---|---|
| Champion departure or admin change | Highest | The strongest single churn predictor in B2B SaaS |
| Trend in usage of the core workflow | High | Direction matters more than level |
| Seat utilization against licensed seats | High | Predicts contraction at renewal (`expansion.md`) |
| Breadth of adoption (users, teams, integrations) | Medium | Narrow adoption is fragile whatever the volume |
| Support sentiment and unresolved escalations | Medium | A pattern of complaints, not a single ticket |
| Payment failures | Medium | Sometimes a card, sometimes a company in trouble (`dunning.md`) |
| Login count alone | Low | Present in every scoring model and predictive of almost nothing on its own |

Rules: validate the score against actual churn before trusting it (does last quarter's red cohort actually churn more?); every red must generate an action with an owner; and score changes, not levels, are what deserve attention.

## The Proactive Plays

- **Onboarding to first value**, with a checklist per segment and a completion measure. The strongest determinant of a first renewal is what happened in the first weeks (`trials.md`).
- **Adoption review at 90 days**, comparing actual use against what they bought.
- **Pre-renewal usage review at 90 days out**, which is where uplift or contraction is decided (`renewals.md`).
- **Executive business review** for enterprise: outcomes delivered, benchmarks against similar accounts, roadmap alignment. Quarterly is common and often too frequent to be substantive; twice a year with real content beats four thin sessions.
- **Champion-change play**, triggered the moment the signal fires: re-establish the relationship with the successor within days, not at the next renewal.

## Feedback Into Product

Support is the highest-volume, most biased research channel in the company. Use it accordingly.

- Tag every ticket by cause and route the aggregate — never individual anecdotes — to product. The count is the signal; the loudest customer is not.
- Weight by revenue and by segment, and check whether a request is concentrated in one account before building it (SKILL.md Traps).
- Close the loop publicly: shipping something a customer asked for and telling them is a retention act with no marginal cost.
- Silence is data too. An account with zero tickets and falling usage is disengaged, not self-sufficient.

**After any support or CS structural decision**, write the coverage model, ratios and response targets to `artifacts/<kebab-name>.md` with its `## Boxes` line, contracted response targets to `## Commitments`, and health-score changes that led to a save or a loss to `## Accounts` and `## Churn Reasons` respectively (`memory-template.md`). Add the ticket-driver review to `## Due` as a monthly row: the top driver changes, and a list from last quarter directs the fix at a problem already solved.
