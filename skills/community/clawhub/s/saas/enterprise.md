# Enterprise Readiness — What Procurement Demands Before It Signs

Scope: the capabilities and paperwork that unblock larger deals, and the SLA arithmetic behind them. The audit programmes themselves are `compliance.md`; qualifying and closing the deal is `b2b`; the motion decision is `sales-motion.md`.

**Before answering a questionnaire, quoting an SLA or agreeing a term**, read `security-answers.md` (the answer bank) and `## Commitments` in `~/Clawic/data/saas/memory.md` (or `commitments.md`) for what has already been conceded to other customers, and `incidents/<year>.md` for the uptime actually delivered. Promising an availability level the incident log contradicts is the most expensive sentence in this domain.

## Build the Rung You Are On

The readiness ladder by ACV band is in SKILL.md. The discipline it encodes: **start the work when the first real pipeline at that band exists, not before and not after.** A SOC 2 programme begun with no enterprise pipeline is two quarters of engineering with no revenue attached; begun after the deal appears, it costs the deal, because the observation window cannot be compressed (`compliance.md`).

The exception is anything with a long clock. Audit observation windows and penetration-test scheduling take months regardless of urgency, so the trigger is pipeline that is *credible*, not pipeline that is *signed*.

## Single Sign-On and Provisioning

- **SAML 2.0 and OIDC both**, because the buyer's identity provider decides, not you. Support IdP-initiated and SP-initiated flows; enterprises use both and will test both.
- **Per-tenant IdP configuration**, self-serve where possible: an admin uploading metadata beats a support ticket per customer, and it scales.
- **Domain verification before enforcement**, or one customer's SSO configuration captures another's users on a shared email domain.
- **Enforcement is a setting**: allow a break-glass local admin account, always. An SSO misconfiguration with no escape locks the customer out of their own tenant and generates a P1 that is entirely self-inflicted.
- **SCIM for provisioning and, more importantly, deprovisioning.** The reason enterprises want SCIM is the leaver process: an employee removed from the directory must lose access without anyone remembering to do it manually. Support user create, update, deactivate and group-to-role mapping.
- **Just-in-time provisioning** covers the create case without SCIM and is a legitimate stepping stone; it does not cover deprovisioning, which is the part that appears in the security review.
- **Price SSO onto the first business tier**, not the top one. Making the control that reduces breach risk a top-tier upsell is publicly criticized, and the deals it protects are not the ones it blocks (`packaging.md`).

## Audit Logs and Access Control

- **Audit log covers who did what to what, when, from where** — authentication, permission changes, data export, admin impersonation, configuration changes, and deletions. Immutable, exportable, and retained for a stated period.
- Retention is a packaging dimension: a short window on lower tiers, a longer one plus streaming to the customer's own SIEM on enterprise.
- **RBAC with roles the buyer recognizes**: at minimum owner, admin, member, read-only, plus billing as a separate permission. Custom roles are an enterprise-tier capability and a real engineering cost — do not promise them casually.
- Support impersonation appears in the customer's own audit log. Buyers ask whether your staff can see their data; the honest answer, plus a visible log, closes the question (`multitenancy.md`).

## Uptime SLA — Arithmetic First

Monthly allowance: `minutes = 43,200 × (1 − uptime)`.

| Target | Monthly downtime allowed | What it demands |
|---|---|---|
| 99.0% | 7h 12m | Nothing special |
| 99.5% | 3h 36m | Planned maintenance windows still fit |
| 99.9% | 43m 12s | Redundancy, no maintenance downtime, fast rollback |
| 99.95% | 21m 36s | Multi-AZ, automated failover, tested |
| 99.99% | 4m 19s | Multi-region active-active; almost no early-stage SaaS delivers this |

Rules that keep an SLA from becoming a refund programme:

- **Sign only what the incident log already shows**, with a margin. Read `incidents/<year>.md` before quoting a number.
- **Define availability precisely**: which endpoints, measured from where, at what interval, excluding what. An undefined "the service" includes every third-party dependency you do not control.
- **Exclusions, stated**: scheduled maintenance inside an announced window, customer-caused failures, force majeure, and beta or preview features.
- **Credits capped as a percentage of the monthly fee**, tiered by severity — a commonly used shape gives a small percentage for the first breach band and a larger one for severe breaches, capped well below the monthly fee. Never a percentage of contract value, and never uncapped.
- **Credits are customer-requested within a stated window**, not automatic. This is standard practice and it prevents a reconciliation burden on both sides.
- **Termination-for-repeated-breach** is the clause buyers actually want; conceding it is usually cheaper than a higher availability number, and it is a strong signal of confidence.
- Every SLA signed is a row in `## Commitments`, and every credit issued is a row in `incidents/<year>.md`.

## Security Questionnaires

A questionnaire is a repeated cost until it is turned into an asset.

- **Answer bank from the first one.** `security-answers.md` holds question, answer, evidence location and last-verified date. Most questionnaires overlap heavily; the second one should take a fraction of the first.
- **Publish a trust page** — subprocessors, certifications, architecture summary, uptime history, security contact. It deflects a share of questionnaires entirely and answers the rest faster.
- **A completed standard questionnaire** (an industry-standard self-assessment form) attached proactively often replaces a bespoke one.
- **Never answer aspirationally.** A "yes" that is not true today is discovered during the audit or after an incident, and both outcomes are worse than a "no, and here is the compensating control with a date".
- **Re-verify annually.** An answer bank is only reusable if every answer is true today; anything past its verification date is checked before reuse.

## Contracts and Procurement

| Artefact | What it is | Where the risk hides |
|---|---|---|
| MSA | The standing terms | Uncapped liability, unilateral termination, IP assignment overreach |
| Order form | The commercial specifics | Auto-renewal terms and uplift; contradicting the MSA |
| DPA | Data-processing terms under GDPR and similar | Subprocessor change notice, deletion timelines, audit rights |
| SLA | Availability commitment | Credit caps and the definition of downtime |
| Security exhibit | Controls promised | Commitments to future work with dates attached |
| Insurance certificate | Cyber and professional liability | Required minimums you do not currently carry |

- **Liability cap** is the clause that matters most: the common position is a cap at fees paid in the preceding twelve months, with narrow carve-outs. Accepting uncapped liability for a mid-sized contract is an existential trade for a routine deal.
- **MFN clauses** ("no customer gets a better price") are permanent constraints on the whole pricing surface and should be refused or tightly bounded. They belong in `## Commitments` if ever granted.
- **Redlines are a pattern, not a series of surprises.** After the first few enterprise deals, the same handful of clauses recur; a pre-approved fallback position for each turns weeks of legal review into a day.
- **Security review is a sales stage with a duration.** Forecast it into the cycle rather than treating it as a delay, and give the buyer everything unprompted at the start of it.
- Anything non-standard agreed — a clause, an SLA level, a residency promise, a feature commitment with a date — is written to `## Commitments` in the same turn, with its value and expiry (SKILL.md Rule 7).

## Support Expectations

Enterprise buyers price support explicitly: response-time targets by severity, escalation path, named contact, and a channel that is not a public form. Deliver it as a paid tier with the targets written down, and measure against them (`support.md`). A support commitment in a contract with no measurement behind it is a breach waiting for someone to notice.

**After any enterprise engagement**, write reusable answers to `security-answers.md` with their verification date, every non-standard term to `## Commitments`, and the account with its plan, ARR and renewal date to `## Accounts` — with the buyer and champion as rows in the shared `~/Clawic/data/contacts/contacts.md`, referenced here by key only. A negotiated position worth reusing (a fallback clause set, a completed questionnaire pack) belongs in `artifacts/<kebab-name>.md` with its `## Boxes` line (`memory-template.md`).
