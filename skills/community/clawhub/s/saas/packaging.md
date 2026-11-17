# Packaging — Plans, Tiers, Fences and the Value Metric

Scope: the architecture of what is sold — units, tiers, limits, add-ons. The price *level* and how to change it is `pricing`; enforcing the plan in the product is `entitlements.md`; migrating customers between plans is `plan-changes.md`.

**Before proposing any packaging change**, read `## Plans` in `~/Clawic/data/saas/memory.md` (or `plans.md` if `## Boxes` points there) and `## Commitments` — a customer with a grandfathered plan or a contractual feature promise is a constraint on the design, not an exception to handle later.

## Pick the Value Metric First

One unit that grows as the customer gets more value from the product. Everything else follows from it.

| Test | Passing looks like |
|---|---|
| Grows with customer success | More of the unit means the customer is winning, not just being charged |
| Predictable to the buyer | They can estimate next month's bill without a spreadsheet |
| Countable without argument | One agreed definition, visible in the product |
| Hard to game | Cannot be halved by sharing a login or batching requests |
| Costs you more as it grows | Otherwise margin drifts as accounts grow (`margins.md`) |

Common metrics and where they break: **seats** (breaks with shared logins and with products where one admin does the work for a hundred people); **usage events** (breaks on bill predictability); **records or objects stored** (breaks when the customer's data is imported once and never grows); **workflows or jobs run** (usually the strongest for automation products); **revenue processed** (aligns perfectly, and buyers resent it above a few percent); **AI credits** (predictable to you, opaque to them — publish the conversion or expect tickets).

Record the choice in `config.yaml` as `value_metric`. If price, meter and entitlement do not all use it, the invoice becomes unexplainable (SKILL.md Rule 4).

## Tier Architecture

Three paid tiers plus a quoted enterprise option is the default, and the reason is not aesthetics: with two, the cheap one anchors and nobody self-selects up; with five, the buyer's choice cost exceeds the price difference and conversion drops.

| Tier | Job | Fenced by |
|---|---|---|
| Entry | Convert an individual or a small team without a conversation | A low ceiling on the value metric |
| Core | Where the median paying customer belongs and stays | Value-metric ceiling plus the collaboration and admin features a team needs |
| Business | Capture the accounts whose usage or compliance needs justify multiples | SSO, audit logs, roles, higher ceilings, support response time |
| Enterprise (quoted) | Absorb everything non-standard: procurement, security, custom terms | Negotiated; never a published price (`sales-motion.md`) |

- **Fence on the value metric, not on feature count.** A feature-fenced ladder makes the buyer pick the cheapest tier containing the one feature they need, and they stay there forever. A metric-fenced ladder moves them up as they succeed, with no sales involvement.
- **The middle tier should hold the median account at the price you want.** If most customers sit on Entry, the fence is in the wrong place — move the ceiling, not the price.
- **Name tiers after who they are for** (Starter / Team / Business), never after their value judgement (Basic / Pro / Premium): the buyer who is not "pro" then buys Basic and undersizes.
- **Never publish more than one dimension of difference per row.** A pricing page that varies seats, usage and features across three tiers cannot be scanned in the fifteen seconds it gets.

## Good Fences, Bad Fences

| Fence | Verdict | Why |
|---|---|---|
| Value-metric ceiling (seats, jobs, records) | Best | Scales with success, upgrade feels earned |
| Collaboration and admin (roles, teams, permissions) | Good | Genuinely appears at team size, not before |
| Security and governance (SSO, audit log, retention) | Good on a mid tier, bad only at the top | Withholding SSO from everyone but 100k accounts is the one packaging choice buyers publicly punish |
| Support response time | Good | Real cost, and enterprises will pay for it (`support.md`) |
| API access | Depends | Fine as a ceiling on calls; blocking the API entirely on paid plans blocks integrations that create stickiness |
| Data export | Never | Holding a customer's own data hostage produces public complaints and, under GDPR portability, a compliance problem (`compliance.md`) |
| Core value of the product | Never | If the entry tier cannot deliver the outcome once, the trial cannot either (`trials.md`) |

## Add-Ons Versus Tiers

Make something an add-on when it is genuinely optional, has its own marginal cost, and is wanted by a minority across every tier — extra storage, additional environments, premium support, a compliance package. Make it a tier feature when wanting it correlates with company size, because then it is a fence that does work.

Add-ons discipline: no more than a handful, priced as a percentage of the base subscription rather than a flat fee so they scale with the account, and each one recorded in `## Plans` with what it includes. An add-on catalogue that grows past a page becomes a quoting problem and, eventually, an entitlement bug.

## Free, Trial, or Neither

Decision, in order:

1. **Does a free user create distribution?** Shared output, collaboration invites, public artifacts, network effects. Yes → a free tier can pay for itself. No → a time-boxed trial does the same qualification at a fraction of the cost (`trials.md`).
2. **What does a free user cost per month?** Infrastructure plus inference plus support. Multiply by the expected free population before, not after. A free tier is marketing spend and belongs in CAC (`margins.md`).
3. **What is the free ceiling?** Enough to reach value once, not enough to run a business on. The commonest error is a free tier so generous that the entry tier has no job.
4. **Abuse surface.** Free tiers with compute, email sending, storage or outbound network are abused within weeks — rate limits, verification, and a per-account cost cap are part of the design, not a later hardening pass.

## Seats: Counting Is a Packaging Decision

Licensed seats (billed regardless of use) versus active seats (billed on activity) is a revenue difference of 20-40% on typical B2B accounts, and it changes behaviour: licensed seats produce shelfware and painful renewals; active seats produce honest expansion and unpredictable bills.

- **Default: licensed seats with an active-seat report** shown to the admin. They see the waste, you keep the predictability, and the renewal conversation is about the report rather than a surprise.
- Define "active" once, in `## Definitions`, and show the same number in the product that appears on the invoice.
- Read-only or guest seats free (or heavily discounted) increase the account's surface without increasing its cost to serve much — and every free viewer is a candidate for an upgrade later.
- True-up rules belong in the contract: monthly automatic for self-serve, quarterly or annual true-up for enterprise (`renewals.md`).

## Pricing Page Structure

The page is the packaging made legible; it fails on structure far more often than on price.

- Three columns plus a contact-sales column; the recommended tier visually marked once.
- Each tier shows: who it is for, the value-metric allowance, price with the billing period explicit, and the three or four differences that matter — not a full feature matrix in the columns.
- Monthly and annual toggle with the annual saving stated as money, not only as a percentage.
- The full comparison table below the fold, for the buyer building an internal case.
- Currency, tax treatment (inclusive or plus VAT) and the auto-renewal terms stated on the page, because in several jurisdictions omitting them is a legal problem rather than a design choice (`compliance.md`).

**After any packaging decision**, write the new plan, tier, limit or add-on to `## Plans` and the reasoning — including what was rejected and the numbers behind it — to `artifacts/<kebab-name>.md` with its `## Boxes` line, in the same turn (`memory-template.md`). Packaging is re-litigated every few quarters; the file is what stops it being re-derived from scratch each time.
