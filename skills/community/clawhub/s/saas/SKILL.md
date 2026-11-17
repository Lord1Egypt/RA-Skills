---
name: SaaS
slug: saas
version: 1.0.2
description: 'Runs a SaaS business: subscription revenue, plan packaging, trials, retention, expansion, and enterprise readiness. Use when MRR or ARR has to be computed, reconciled, or explained; when NRR, gross margin, CAC payback, burn multiple, or rule of 40 is the question; when designing plans, seats, usage limits, add-ons, or a free tier; when trials sign up but never convert; when failed payments leak revenue; when a renewal, downgrade, or cancellation flow needs building; when expansion has stalled; when an enterprise buyer demands SSO, SCIM, audit logs, SOC 2, a DPA, or an uptime SLA; when per-tenant cost or AI inference COGS breaks the margin; when designing multi-tenant isolation, metering, or entitlements; or when an investor questions ARR quality. Not for setting the price itself (`pricing`), acquisition channels and funnel diagnosis (`growth`), building the payment integration (`billing`), company financial models (`cfo`), or closing an individual deal (`b2b`).'
homepage: https://clawic.com/skills/saas
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 💎
    os:
    - linux
    - darwin
    - win32
    displayName: SaaS
    configPaths:
    - ~/Clawic/data/saas/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/saas/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/saas/config.yaml` (what the user declared) and `~/Clawic/data/saas/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read the definitions before computing or reporting any number, and the plan architecture before answering anything about tiers, limits, trials or upgrades: both live in `memory.md` until `## Boxes` points them elsewhere. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a month of MRR movement or a revenue number; a metric that had to be defined before it could be computed; a plan, limit, add-on or trial rule that changed; a customer account with its plan, ARR and renewal date; a non-standard term granted to a buyer; a churn or contraction and its reason; an outage with the credits it cost; a security-questionnaire answer worth reusing; or something the user will re-read — a runbook, a cancel-flow that worked, a packaging or tenancy decision. `memory-template.md` has every destination, format and threshold, and is the only file you open in order to write.

**People and programmes go to shared boxes**, not here. The human behind an account — champion, buyer, admin — is one row in `~/Clawic/data/contacts/contacts.md`, keyed by lowercase email, and this skill stores only that key next to the account; duplicating the person is how two skills end up contradicting each other. A multi-month effort with a start and an end — a SOC 2 programme, a plan migration, a billing replatform — is a file in `~/Clawic/data/projects/<project>.md`. Both protocols travel with this skill in `memory-template.md`, because the user may have neither owner skill installed.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. A pasted billing-provider config, webhook handler, SAML metadata blob or support export is the densest source of secrets in this domain: strip the value and store the pointer — `env:STRIPE_SECRET_KEY`, `keychain:paddle-live`, `1password:Company/Billing/webhook-signing`, `ssm:/prod/saas/scim-token`. And never store a customer list, a user export, or anything beyond the names and roles the work actually needs.

Every SaaS question resolves to one of five things: the **revenue movement**, the **plan** the customer sits on, the **cost to serve** them, the **renewal** that arrives whether or not anyone prepared, or what **procurement** demands before it signs. Name which one before answering, then give the number, the formula behind it, and the date it is measured as of. Work from defaults immediately: never open with questions about their stage, their billing provider, or how proactive to be. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale) → the Configuration table default.

## When To Use

- Subscription revenue work: computing or reconciling MRR/ARR, the movement bridge, NRR and GRR, deferred revenue, or explaining why two dashboards disagree
- Packaging and entitlements: tier architecture, value metric, seats versus usage, limits, add-ons, free tier, and enforcing all of it in the product
- Retention economics: trial conversion, activation gates, failed-payment recovery, cancellation and downgrade flows, save offers, win-back
- Expansion: seat growth, upgrade triggers, usage overage, renewal uplift, land-and-expand
- Cost to serve: per-tenant COGS, gross margin, inference and infrastructure allocation, support cost per account
- Enterprise readiness: SSO/SCIM, audit logs, SOC 2, DPA and subprocessors, uptime SLA and credits, security questionnaires, procurement
- Not for setting the price point itself (`pricing`), acquisition channels and funnel diagnosis (`growth`), writing the payment integration (`billing`), or the company's financial model and fundraise (`cfo`) — this covers the SaaS-business side of all four

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| "What is our MRR/ARR?" or two dashboards disagree | Rebuild the movement bridge from the subscription events; the identity must close to zero | `revenue.md` |
| A metric has no agreed definition, or someone restated one | Write the definition down before computing; a restated metric invalidates every prior chart | `revenue.md` |
| Designing or rebuilding plans, tiers, limits, add-ons | Pick the value metric first, then fence the tiers by it — never by feature count | `packaging.md` |
| Enforcing a plan in the product: limits, quotas, seats, gates | Entitlement service, soft-then-hard limits, grace, and the upgrade path at the wall | `entitlements.md` |
| Usage-based or hybrid billing: metering, overage, credits, commits | Idempotent events, aggregation window, drawdown order, what happens at zero balance | `metering.md` |
| Trials sign up and vanish; free plan never converts | Time-to-value gate, trial length, card-up-front tradeoff, reverse trial | `trials.md` |
| Payments failing, revenue leaking with no cancellation | Involuntary churn: retry schedule, card updater, dunning window, grace | `dunning.md` |
| Renewal coming, customer wants to downgrade or cancel | Notice windows, the cancel flow, save offers that do not train discounting | `renewals.md` |
| NRR flat: no expansion, every dollar from new logos | Expansion levers ranked by cost, and the trigger that fires each one | `expansion.md` |
| Gross margin falling, or AI/infra cost per account unknown | Allocate COGS per tenant, then the margin floor and what to do below it | `margins.md` |
| Tenant isolation, noisy neighbour, data residency, tenant offboarding | Pool/bridge/silo, tenant id propagation, per-tenant export and deletion | `multitenancy.md` |
| Buyer demands SSO, SCIM, audit logs, an SLA, or a questionnaire | The readiness ladder by ACV band, and the answer bank | `enterprise.md` |
| SOC 2, ISO 27001, GDPR, HIPAA, sales tax and VAT nexus | Which regime is actually required, the observation window, MoR versus registering | `compliance.md` |
| Support or CS is drowning; who gets a human | Coverage ratios by ACV, deflection, health scores that predict rather than describe | `support.md` |
| Self-serve, sales-assist, or enterprise — which motion, and when to switch | Quota-capacity arithmetic against ACV; the motion follows the number | `sales-motion.md` |
| Killing a plan, changing limits, grandfathering, migrating customers | Migration cohorts, notice, the grandfather ledger, and who gets an exception | `plan-changes.md` |
| Monthly close, board pack, or "which numbers do we report" | The reporting set, the benchmarks to compare against, and the cadence | `reporting.md` |
| Investor or acquirer questioning ARR quality | What gets deducted from claimed ARR in diligence, and how to survive it | `diligence.md` |
| Anything else SaaS | Answer directly, then state the number it moves, the formula, and its as-of date | — |

Coverage map: `revenue.md` MRR movement and definitions · `packaging.md` plan architecture · `entitlements.md` enforcing plans in product · `metering.md` usage billing · `trials.md` trial and free tier · `dunning.md` failed payments · `renewals.md` renewal and cancellation · `expansion.md` NRR engine · `margins.md` cost to serve · `multitenancy.md` tenant isolation · `enterprise.md` buyer readiness · `compliance.md` audits and tax · `support.md` CS scaling · `sales-motion.md` motion by ACV · `plan-changes.md` migrations and grandfathering · `reporting.md` close and board pack · `diligence.md` ARR quality.

## Core Rules

1. **Every number carries its formula and its as-of date.** "MRR is 84k" is unusable; "84,200 USD MRR as of 2026-07-31, closed month, movement bridge closes" is a fact someone can check next quarter. Store both in the revenue box the same turn (`memory-template.md`). A metric whose definition is not written down will be redefined by whoever is asked next, and every historical chart silently changes meaning.
2. **The movement bridge must close.** `End MRR = Start + New + Expansion + Reactivation − Contraction − Churn`, with all six buckets stored and reported as **positive magnitudes** — the identity supplies the signs, so a 1,200 downgrade is written `1,200`, never `-1,200`. Worked: `78,400 + 6,100 + 2,900 + 300 − 1,200 − 3,300 = 83,200`. Every dollar of delta lands in exactly one bucket: a downgrade is contraction, never churn; a customer who cancels and returns in the same month is reactivation, not new. If the bridge does not close to zero, the discrepancy is the finding — do not report the total until it does (`revenue.md`).
3. **Fix retention before buying acquisition.** With monthly revenue churn `c`, a cohort's remaining lifetime is `1/c` months: 5%/mo → 20 months, 3%/mo → 33 months, 1%/mo → 100. Cutting churn from 5% to 3% lengthens lifetime by two thirds (20 → 33 months) and raises LTV by the same factor at zero acquisition spend. Below 100% NRR you are filling a leaking bucket, and every acquisition dollar buys less than the one before it (`expansion.md`, `dunning.md`).
4. **Price on the value metric, count on the value metric, enforce on the value metric.** One unit that grows as the customer succeeds — seats, records, jobs, GB, agents — set by `value_metric`. Packaging, metering and entitlements must all use the same unit; a plan sold per seat and limited by API calls produces a bill nobody can predict and a support ticket per invoice (`packaging.md`, `entitlements.md`).
5. **Involuntary churn is a payments bug, not a customer decision.** Card failures typically account for 20-40% of gross churn in card-billed SMB SaaS, and a retry schedule plus a card-updater service commonly recovers half to three-quarters of them. Measure it separately from voluntary churn or you will "fix" a product problem that was an expiry date (`dunning.md`).
6. **Gross margin is a design decision, made per request.** `gross margin = (revenue − COGS) ÷ revenue`, where COGS = infrastructure + inference + third-party APIs + payment fees + support + hosting-attributable staff. Classic software lands 75-85%; products with a per-request model call routinely land 50-65%. Below `gross_margin_floor_pct`, the fix is a usage fence or a price change, never volume — you cannot grow into a negative unit (`margins.md`).
7. **Nothing non-standard is granted without being written down.** An uptime SLA, a custom DPA clause, an MFN, a perpetual discount, a data-residency promise: each one becomes an obligation that outlives the person who agreed to it. Every grant gets a row in the commitments box with its customer, its value, and its expiry, in the same turn it is agreed (`enterprise.md`).
8. **Uptime is arithmetic before it is a promise.** Monthly allowance `minutes = 43,200 × (1 − uptime)`: 99.9% = 43m 12s, 99.95% = 21m 36s, 99.99% = 4m 19s. Sign only what the architecture already delivers, measured, and cap credits as a percentage of the monthly fee, not of the contract — an uncapped SLA turns one bad afternoon into a refund of the year (`enterprise.md`).
9. **The motion follows the ACV, not the ambition.** A quota-carrying rep costing 200k fully loaded needs roughly 5× that in quota, ~1M; at a 5k ACV that is 200 closed deals a year and the maths never works, at 25k ACV it is 40 and it does. Self-serve below ~5k ACV, sales-assist 5-25k, field above ~50k, with the bands moving on sales cycle length rather than preference (`sales-motion.md`).
10. **Every change to a live plan is a migration with a cohort.** Existing customers, in-trial customers, annual customers mid-term, and customers with a non-standard term are four different populations with four different notice requirements. Decide the grandfather policy before announcing, and give every grandfathered account a row in the commitments box with its terms and its end date (`plan-changes.md`).

## The Metrics That Decide

Compute these from the movement bridge, never from a dashboard whose definition you have not read. Benchmarks are the commonly reported ranges for B2B SaaS, not targets: a number outside the range is a question, not a verdict.

| Metric | Formula | Reads as healthy | What it actually tells you |
|---|---|---|---|
| NRR (net revenue retention) | `(start + expansion − contraction − churn) ÷ start`, existing customers only | 100-110% typical; 120%+ strong; SMB books rarely clear 100% | Whether the business grows with the sales team switched off |
| GRR (gross revenue retention) | `(start − contraction − churn) ÷ start`, capped at 100% | 85%+ SMB, 90%+ mid-market, 95%+ enterprise | The floor under the product; expansion cannot hide a leak here |
| CAC payback | `CAC ÷ (ARPA × gross margin)` — months | <12 SMB, <18-24 enterprise | How long the cash is underwater; the number that kills fast-growing companies |
| LTV:CAC | `(ARPA × gross margin ÷ revenue churn) ÷ CAC` | ≥3 sustainable, >5 usually means underinvesting | Only meaningful with *revenue* churn; logo churn on an expanding book overstates it badly |
| Rule of 40 | `growth % + FCF margin %` (Feld) | ≥40 | Whether growth is being bought at a defensible price; each point of growth may be traded for a point of margin |
| Burn multiple | `net burn ÷ net new ARR` (Sacks) | <1 excellent, 1-1.5 good, >2 investigate | Cash consumed per dollar of durable revenue — the hardest number to flatter |
| Magic number | `(net new ARR this quarter × 4) ÷ prior-quarter S&M spend` | >0.75 → fund more sales | Whether the sales machine converts spend to revenue at all |
| Quick ratio | `(new + expansion) ÷ (churned + contraction)` | ≥4 | Growth quality: 4 is compounding, 1 is a treadmill |
| Logo vs revenue churn | Count of accounts vs sum of MRR | Revenue churn below logo churn | Which end of the book is leaving; the gap names the segment to fix |

Reporting discipline: the same set every period, the same definitions, and a month-to-date number never compared against a closed month (`reporting.md`).

## Where Revenue Leaks

Five distinct leaks, five distinct owners. Attributing a leak to the wrong one is why retention projects fail — a fix for voluntary churn does nothing to a card that expired.

| Leak | Signature | First move | Depth |
|---|---|---|---|
| Never activated | Signs up, no core action within the first sessions, never returns | Move the activation gate before the paywall; measure time-to-first-value in minutes | `trials.md` |
| Involuntary churn | Cancellation with no cancellation event; spikes at month boundaries and card expiry clusters | Retry schedule + card updater + in-app dunning banner before email | `dunning.md` |
| Voluntary churn | An explicit cancel with a stated reason | Reason-coded cancel flow; the reason distribution decides whether it is product, price, or fit | `renewals.md` |
| Contraction | Same logo, fewer seats or a lower tier at renewal | Seat-usage review 60 days pre-renewal, not at the renewal call | `expansion.md` |
| Discount drift | Realized ARPA falls while list price holds | Discount ceiling and an approval path; measure realized-vs-list monthly | `sales-motion.md` |
| Anything else | Revenue moved and no bucket claims it | Rebuild the bridge for that month; an unattributed delta is a definition problem | `revenue.md` |

## The Enterprise Readiness Ladder

What a buyer asks for at each deal size. Building three rungs above the deals you actually have is the most expensive form of procrastination in SaaS; arriving at a rung unprepared costs the deal or a quarter.

| ACV band | Buyer expects | Cost of not having it |
|---|---|---|
| Under 5k | Self-serve signup, card payment, docs, email support | Nothing — enterprise features here are pure waste |
| 5-25k | Invoicing, annual terms, a real security page, a status page, role-based access | Friction and slow payment, not lost deals |
| 25-100k | SSO (SAML/OIDC), audit logs, a signed DPA, subprocessor list, uptime SLA, questionnaire answers, a named support contact | The deal stalls in security review for a quarter |
| 100k+ | SOC 2 Type II or ISO 27001, SCIM provisioning, custom MSA redlines, penetration-test summary, data residency, named CSM, insurance certificates | Deal lost, and usually to whoever already had the report |

SSO belongs on a paid tier, not the top tier only: making the security control that reduces your own breach surface a 100k upsell is the one packaging decision buyers publicly punish (`packaging.md`, `enterprise.md`).

## Output Gates

Before delivering a revenue number, a packaging proposal, a contract term, or a retention plan:

- Does every number carry its formula, its currency, and its as-of date, and does the movement bridge close?
- Is churn split into voluntary and involuntary before any conclusion is drawn from it?
- Does this packaging use one value metric consistently across price, meter, and entitlement?
- Have I stated the gross margin of what I am proposing, including inference and third-party API cost?
- Does any non-standard commitment here — SLA, DPA clause, discount, residency, MFN — have an owner, a value, and an expiry?
- If a live plan changes: is every affected cohort named, with its notice period and its grandfather status?
- Did anything durable come out of this — a month's movement, a definition, a plan change, an account, a granted term, a churn reason, an outage credit, a reusable questionnaire answer? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/saas/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| motion | self-serve \| sales-assist \| enterprise \| hybrid | self-serve | Selects the default play in `sales-motion.md`, the support ratios in `support.md`, and whether renewal work is a flow or a conversation |
| stage | pre-revenue \| early \| growth \| scale | early | Which plays are premature: gates the enterprise ladder, the CS hires, and the reporting set in `reporting.md` |
| reporting_currency | text (ISO 4217 code) | USD | Currency of every amount stated or stored; amounts always carry the code in the value |
| billing_platform | stripe \| paddle \| chargebee \| recurly \| lemonsqueezy \| custom | stripe | Whether the provider is a merchant of record (tax handled) or not, and which proration, dunning and tax behaviour `dunning.md` and `compliance.md` assume |
| value_metric | seats \| usage \| flat \| hybrid | seats | The single unit that `packaging.md`, `metering.md` and `entitlements.md` price, meter and enforce on (Rule 4) |
| trial_length_days | number (0-90) | 14 | Trial window in `trials.md`; 0 means freemium with no trial, which changes the activation gate |
| annual_discount_pct | number (0-30) | 17 | The annual-prepay discount quoted everywhere; 17% is two months free (`2 ÷ 12`) |
| discount_ceiling_pct | number (0-50) | 15 | Maximum discount offered without escalation, in quotes, save offers and renewals |
| gross_margin_floor_pct | number (50-95) | 70 | The line below which `margins.md` treats a plan or an account as a pricing problem rather than a cost problem (Rule 6) |
| dunning_window_days | number (7-45) | 21 | Length of the retry-and-notice sequence before access is suspended (`dunning.md`) |
| compliance_regime | none \| soc2 \| iso27001 \| hipaa \| gdpr-strict | none | Forces the controls, retention and subprocessor discipline that regime requires, and gates which buyers are addressable (`compliance.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — billing provider details, analytics and warehouse, CRM, support desk, entitlement service versus in-app flags — affects the shape of every example and where numbers are sourced from
- **Conventions** — plan and metric naming, cohort convention (calendar month versus signup anniversary), how ARR is annualized, seat definition (licensed versus active) — affects `revenue.md` and every stored number
- **Platform** — merchant of record versus direct, currencies sold in, regions and data residency offered, self-hosted or single-tenant option — affects `compliance.md` and `multitenancy.md`
- **Commercial policy** — refund stance, cancel-anytime versus notice period, auto-renewal terms, grandfathering posture, free-plan abuse tolerance — affects `renewals.md` and `plan-changes.md`
- **Risk posture** — who approves a non-standard term, appetite for custom contracts, whether to sign SLAs at all at this stage — affects `enterprise.md` and Output Gates
- **Output register** — dashboard versus narrative, board-pack shape, how much formula to show with each number — affects `reporting.md`
- **Cadence** — revenue close day, board and investor update frequency, renewal notice window, pricing review, audit and penetration test, dunning review — every accepted cadence becomes a row in the `## Due` table of `memory.md`

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Counting one-time services, hardware, or uncommitted overage in ARR | Diligence deducts it and the "restated" ARR becomes the number everyone remembers | Recurring, committed, annualized only; report the rest as a separate line (`diligence.md`) |
| Annual prepay booked as revenue in the month it lands | Cash is not revenue; the deferred balance is the obligation you just took on | Recognize monthly, track deferred separately, and never quote a cash month as MRR (`revenue.md`) |
| Reporting churn as one number | It bundles a payments bug with a product problem; the average hides both | Split voluntary, involuntary and contraction from the first report (Rule 5) |
| LTV computed with logo churn | On an expanding book it overstates LTV by the whole expansion rate | Revenue churn, gross-margin-adjusted, or the number is decorative |
| Lifetime deals or perpetual discounts for early cash | Both convert recurring revenue into a permanent liability with no renewal event; they also poison the ARR line in any future diligence | Annual prepay with a discount inside `annual_discount_pct` |
| Feature-count tiers | Customers buy the cheapest tier containing the one feature they need, and expansion never happens | Fence on the value metric so growth moves them up by itself (`packaging.md`) |
| SSO priced only into the top enterprise tier | Punished publicly, and it delays the control that most reduces your breach surface | SSO from the first business tier (`enterprise.md`) |
| Hard limit with no warning and no upgrade path | The wall arrives mid-workflow and reads as an outage, so the ticket is a cancellation | Soft limit → notice → grace → hard stop, with the upgrade one click from the wall (`entitlements.md`) |
| Unlimited plans with real marginal cost | One customer at 100× the median consumes the margin of the whole tier — with per-request AI cost, of several tiers | Fair-use ceiling stated at purchase, plus overage (`metering.md`, `margins.md`) |
| Building enterprise features before an enterprise buyer exists | SOC 2, SCIM and residency are quarters of work with no revenue attached until someone asks | Sell the rung you are on, and start the audit clock when the first 100k pipeline is real (`enterprise.md`) |
| Discounting to close, with no ceiling | Trains the market to wait for quarter end and permanently lowers realized ARPA | `discount_ceiling_pct` with an approval path; trade discount for term length or a case study |
| Save offers handed out at every cancellation | Teaches customers that threatening to leave is a pricing negotiation | Reason-coded flow: offers only for the reasons an offer actually fixes (`renewals.md`) |
| Support scaled by hiring | Ticket volume grows with accounts, not with revenue; headcount is the last lever, not the first | Deflect, then tier by ACV, then hire against the ratio (`support.md`) |
| Custom work for a single large customer | Becomes an unpaid maintenance obligation on every future release | Sell it as a paid, scoped commitment with a sunset date, recorded in the commitments box (Rule 7) |
| A packaging or tenancy decision that lives only in the chat | Re-litigated every quarter, usually by whoever is on call for the consequences | `artifacts/` with the date, the alternatives rejected, and the numbers behind it (`memory-template.md`) |

## Where Experts Disagree

- **What counts as ARR.** Strict school: only committed, contracted, recurring revenue annualized. Broad school: add stable usage-based revenue, because for a metered product it is the business. The frontier is predictability — usage revenue with a 12-month stable floor is defensible if you report the floor and the volatility separately; annualizing a single strong month is not, and diligence will find it (`diligence.md`).
- **Card up front on the trial.** Card-required trials convert a far higher share of trialists but cut trial starts sharply; card-free fills the funnel and moves the qualification work to activation. Self-serve with a strong activation gate → card-free; sales-assisted, high-ACV, or heavy per-user cost → card up front (`trials.md`).
- **Usage-based versus per-seat.** Usage aligns price with value and expands automatically; it also makes revenue less predictable and invoices harder to defend internally at the customer. Hybrid — a platform fee plus metered usage above a committed floor — is the common resolution, and it is strictly more complex to build (`metering.md`).
- **Free tier versus free trial.** A free tier is a permanent COGS line and a support load, justified only when the free user creates distribution (shared output, collaboration, network effects). Without a distribution mechanism, a time-boxed trial does the same qualification for a fraction of the cost.
- **Single-tenant for enterprise.** Silo tenancy sells, and it multiplies deployment, upgrade and on-call surface by the number of customers. Take it only when it is priced to cover the operational tax explicitly, with a version-skew policy in writing (`multitenancy.md`).
- **How much churn is "normal".** SMB self-serve at 3-5% monthly logo churn is common and not automatically a crisis; the same number in enterprise is fatal. Compare against your own segment and cohort curve rather than a published benchmark, because the benchmark is an average of businesses that are not yours.

## Security & Privacy

**Credentials:** this skill never asks for, stores, logs, or transmits billing-provider keys, webhook signing secrets, SSO/SAML private keys, SCIM tokens, or database credentials. Where a value is needed, it stores a pointer only — `env:STRIPE_SECRET_KEY`, `keychain:paddle-live`, `1password:Company/Billing/webhook-signing`.

**Customer data:** the local boxes hold account names, plans, ARR figures, renewal dates, churn reasons and a contact key — not user exports, not personal data beyond the name and role of a named contact, and never card data. Anything resembling a customer list or a PII export is summarized as counts, not stored.

**Local storage:** preferences, revenue history, plans, accounts, commitments and generated artifacts stay in `~/Clawic/data/saas/` on this machine, plus contact rows in `~/Clawic/data/contacts/` and programme files in `~/Clawic/data/projects/`.

**Guardrails:** actions that touch live billing — cancelling, refunding, migrating a customer between plans, suspending access — are described with the affected customer count and their revenue before anything is proposed, and require explicit confirmation.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/saas (install if the user confirms):
- `pricing` — setting and changing the price itself, willingness-to-pay research, price tests
- `growth` — acquisition channels, funnel diagnosis, experiment programme
- `billing` — implementing payments, webhooks, invoicing and tax in code
- `cfo` — company financial model, runway, board and fundraise mechanics
- `b2b` — qualifying and closing the individual enterprise deal

## Feedback

- If useful, star it: https://clawic.com/skills/saas
- Latest version: https://clawic.com/skills/saas

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/saas.
