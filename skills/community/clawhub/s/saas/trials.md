# Trials, Freemium and the First Session

Scope: turning a signup into a paying account — trial design, activation gate, free-tier boundary, and the abuse surface that comes with both. Acquisition and channel work is `growth`; enforcing the boundary in product is `entitlements.md`.

**Before changing a trial or free-tier rule**, read `## Plans` in `~/Clawic/data/saas/memory.md` (or `plans.md`) for the current allowances and `config.yaml` for `trial_length_days` — and check whether trial conversion is even the constraint: if `## Revenue` shows healthy new MRR and heavy churn, the leak is downstream (`dunning.md`, `renewals.md`).

## Trial Length Is Set by Time-to-Value, Not by Convention

The rule: **trial length = time to first value + one usage cycle + slack for one weekend**. A tool used daily needs days; a tool used at month-end close needs to span a month-end.

- 14 days is the default because most B2B tools reach value inside a week and a fortnight covers two working weeks. It is a default, not a finding.
- Extending a trial that is not converting rarely helps: trial usage concentrates in the first sessions, and an account that has done nothing by the midpoint almost never starts. Lengthening the window mostly lengthens the time to a `no`.
- **Extension on request converts well** and costs nothing — an account that asks for more time is engaged. Grant it once, automatically, with no justification asked and no approval step; only if extension-on-request becomes standing policy is there anything to write down, and then it is a trial rule and belongs in `## Plans`.
- Usage-based trials (a credit allowance rather than a clock) fit products with irregular cadence, and remove the "I was busy that week" objection. They need a spend ceiling and an expiry anyway, or they become a free tier by accident.

## Card Up Front: The Real Tradeoff

Requiring a card sharply reduces trial starts and sharply raises the conversion rate of those who start — the two effects partly cancel, so the decision is about which cost you prefer, not about which number is bigger.

| Choose card-required when | Choose card-free when |
|---|---|
| Each trial has real marginal cost (inference, compute, human onboarding) | Marginal cost per trial is near zero |
| The motion is sales-assisted and reps' time is the scarce resource | Self-serve, and volume feeds the funnel |
| Abuse is easy and expensive (sending, compute, storage) | The product cannot be abused profitably |
| Buyers are used to it in this category | The category is card-free and requiring one reads as a red flag |

Middle path, and often the best one: **reverse trial** — full access to the paid tier for the trial window, with an automatic drop to a limited free tier at the end rather than a wall. The customer experiences the ceiling from above, which is a far stronger upgrade motivation than being shown it from below, and no card is needed to start.

If a card is required: state the charge date and the amount before the field, send a reminder before the charge, and make cancellation self-serve. Every dark pattern here converts into a chargeback, and chargebacks threaten the payment account itself.

## The Activation Gate

Activation is the single action that predicts retention. Find it, then design everything before it away.

- **Identify it empirically**: compare the behaviour of accounts retained at day 90 against those that churned, in the first session. The action that separates them best is the activation event — not the one the team assumes.
- Common shapes: first successful integration connected, first record imported, second team member invited, first output shared outside the account.
- **Measure time-to-value in minutes for the first one**, then count how many of them happen in session one. A funnel where activation typically happens on day three has three days of opportunity to lose the account.
- **Remove every step before it**: no mandatory profile, no survey, no email verification blocking the first action (verify in parallel), no empty state without seeded example data. Each pre-value step costs a share of the funnel and buys nothing.
- The activation definition goes in `## Definitions` — if it drifts, so does every retention chart built on it.

## Trial Sequence

| Moment | Purpose | Common error |
|---|---|---|
| Signup → first action | Reach value once | A tour instead of the product; empty state with no data |
| Day 1 | Confirm they got there, offer the one next step | A feature list nobody asked for |
| Midpoint | Segment: activated → show the next-depth feature; not activated → single question offering help | Sending both groups the same email |
| Two days before expiry | State exactly what changes at expiry, with the plan that fits their usage | A generic upgrade prompt with no plan recommendation |
| Expiry day | The drop happens as described; upgrade in one click, data retained | Silent access cut with no notice |
| After expiry | One value-led follow-up, then stop; move to the win-back cadence | An indefinite drip that trains people to filter you |

Recommend the plan their **observed usage** fits, with the numbers visible: an account that used 40 seats and 80k events being pointed at the entry tier reads as inattention.

## Free Tier: Cost, Ceiling and Abuse

A free tier is a permanent COGS line and a permanent support load. Justify it with distribution, not with hope (`packaging.md`).

- **Model it as CAC**: `free tier monthly cost ÷ free-to-paid conversions per month` is the effective acquisition cost, comparable directly to paid channels. A free tier failing that comparison is a marketing channel that is losing.
- **Ceiling rule**: enough to reach value repeatedly, not enough to run a business on. If the free tier serves a real workload for a real team, the entry tier has no job.
- **Cost ceiling per free account**, enforced in code, especially with per-request model cost (`margins.md`).
- **Abuse surface** appears within weeks on anything with compute, sending, storage or outbound network. Countermeasures that work without wrecking the funnel: verified email plus a payment-card check only for the abusable feature, per-account rate limits, cost caps, and a manual review queue triggered by anomalous consumption rather than by signup.
- **Multi-account abuse** (one team, ten free accounts) is a fence problem: the collaboration features that make a team account worth buying are what make the workaround painful.

## Diagnosing a Trial Funnel

Take the stages in order; the first one below its band is the constraint and the only one worth working on.

| Stage | Question | If it is the constraint |
|---|---|---|
| Signup → first session | Do they arrive and start? | Onboarding friction, wrong expectation set by the landing page (`growth`) |
| First session → activation | Do they reach value once? | Empty state, setup steps, missing seed data |
| Activation → habit | Do they come back? | The value was one-off; the product has no recurring trigger |
| Habit → paid | Do they convert? | Price, packaging fit, or no buying authority in the account (`packaging.md`, `sales-motion.md`) |
| Paid → month 2 | Do they stay? | Not a trial problem (`renewals.md`, `dunning.md`) |

An account that activated and used the product daily but did not convert is almost never a pricing objection — it is usually that the user is not the buyer. That is a motion problem, and it is where sales-assist earns its cost.

**After changing a trial rule, a free-tier ceiling or the activation definition**, write it to `## Plans` and `## Definitions` in the same turn, and record the observed conversion rate with its date and sample size in `## Pain Points` if it drove the decision (`memory-template.md`). A trial sequence that finally worked belongs in `artifacts/<kebab-name>.md` with its `## Boxes` line — it is the asset most often rebuilt from memory by whoever inherits the funnel.
