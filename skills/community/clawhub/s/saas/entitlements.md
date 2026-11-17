# Entitlements — Enforcing the Plan Inside the Product

Scope: turning a plan into behaviour — what a customer can do, how much, and what happens at the wall. Designing the plans themselves is `packaging.md`; counting billable usage is `metering.md`.

**Before changing any limit or gate**, read `## Plans` in `~/Clawic/data/saas/memory.md` (or `plans.md`) and `## Commitments` — a customer with a contractual feature promise must not be gated by a change made for everyone else.

## One Entitlement Service, Not Scattered Plan Checks

The failure mode is `if (plan === 'pro')` spread across the codebase. Six months later nobody can answer "what does Business include" without grepping, and a new tier requires touching forty files.

Shape that survives:

```
entitlements(account) → {
  features: { sso: true, audit_log: true, api: true },
  limits:   { seats: 25, projects: null, events_per_month: 100000 },
  state:    { status: "active", grace_until: null }
}
```

- One resolver, one cache, one place where plan → entitlements is defined. Product code asks `can(account, "sso")` or `limit(account, "seats")` and never names a plan.
- `null` means unlimited; absent means not entitled. Distinguishing the two prevents the bug where a missing key silently grants everything.
- Resolution order: contractual override for this account → plan defaults → global default. The override layer is what makes a negotiated enterprise term implementable without a bespoke plan (Rule 7 in SKILL.md).
- Cache with a short TTL and an explicit invalidation on subscription change. A customer who upgrades and still sees the paywall for ten minutes files a ticket that costs more than the cache saved.
- Entitlements resolve on the server. A flag checked only in the client is a UI hint, not a limit.

## Soft, Then Hard

A limit that arrives without warning reads as an outage, and the ticket that follows is a cancellation. The ladder, with the thresholds worth defaulting to:

| Stage | Trigger | Behaviour |
|---|---|---|
| Silent | Below 80% of the limit | Nothing |
| Notice | 80% | In-product indicator with the current count and the ceiling |
| Warning | 100% reached | Blocking modal that explains what stops next and offers the upgrade in one click |
| Grace | 100-120%, for a bounded window | Work continues, banner persists — protects the customer mid-workflow |
| Hard stop | Past grace | Creation of new units blocked; existing data readable and exportable, never deleted |

- **Never break reads.** Blocking a customer from seeing their own data converts an upgrade conversation into a data-portability complaint (`compliance.md`).
- **Never block in the middle of a job.** Enforce at the start of a unit of work, not halfway through one; a half-processed batch is a support ticket and a correctness problem.
- **Grace window is a business setting**, not a code constant: it interacts with `dunning_window_days` and should be at least long enough for an admin to get purchasing approval — a few working days at minimum for team plans.

## Which Limit Type to Use

| Type | Resets | Right for | Trap |
|---|---|---|---|
| Concurrent | Continuously | Seats, active sessions, running jobs | Needs release on crash, or the count drifts upward forever |
| Period quota | Monthly, on the billing anniversary | Events, API calls, credits | Resetting on the calendar month while billing on the anniversary creates a partial first period nobody can explain |
| Cumulative | Never | Total records, storage | Deleting data must decrement it, or the customer pays for what they removed |
| Rate | Per second or minute | API protection | Rate limiting is abuse protection; using it as a packaging fence produces intermittent failures that look like bugs |

Match the reset to the billing period, always. A quota that resets on the 1st for an account billed on the 17th means the first period is short, the customer hits the wall early, and no support explanation lands well.

## Downgrades and Expiry: Deciding What Happens to Excess

The situation packaging documents never cover: an account on 25 seats moves to a plan allowing 10.

- **Never delete.** Excess data and users become read-only or suspended, never removed. Deletion on downgrade is the single fastest way to a public complaint and, for user-generated content, potentially a data-protection breach.
- **Let the admin choose which to keep.** Auto-selecting the ten most recent users deactivates the CFO who logs in monthly.
- **Give a window** — the same grace pattern — before the restriction bites, and state it at the moment of downgrade, not in an email.
- **Reactivation must restore.** If they upgrade back within the retention window, everything returns exactly as it was; anything else makes downgrade a one-way door and turns a temporary budget cut into a churn.

## Trials and Failed Payments Are Entitlement States, Not Plans

`status` drives behaviour independently of the plan:

| State | Entitlements | Notes |
|---|---|---|
| `trialing` | Full target-tier access, or a deliberately reduced set | The choice is a trial design question (`trials.md`) |
| `active` | Plan entitlements | — |
| `past_due` | Full access during the dunning window | Suspending on the first failed card punishes a customer who did nothing wrong (`dunning.md`) |
| `suspended` | Read and export only | Data retained for a stated period |
| `cancelled` | Access until the end of the paid term, then read and export | Cutting access on the cancellation click is an unearned refund request |

Every one of these states must be enumerable in the entitlement resolver. A codebase that only knows `plan` cannot express "past_due but still working", which is exactly the state most revenue is recovered from.

## Testing the Matrix

The combinatorics get away from teams quickly: tiers × features × limit states × subscription states.

- Table-driven tests over the full plan × feature matrix, generated from the same definition the resolver uses — not hand-written per plan.
- One end-to-end test per boundary: at the limit, one over, in grace, past grace, downgraded with excess.
- An internal page showing the resolved entitlements for any account. Support answering "why can't they do X" by reading the resolver output rather than guessing is worth more than any documentation.
- A weekly reconciliation: accounts whose entitlements do not match their subscription. Drift comes from manual overrides, failed webhooks and abandoned migrations, and it always exists.

## Non-Standard Grants

An enterprise deal grants a feature outside the plan, or a limit above the tier. Two rules:

1. Implement it as an **account-level override** in the resolver, never as a private plan. A bespoke plan per customer becomes unmaintainable at about the fifth one and invisible in every packaging analysis.
2. Record it in `## Commitments` with the customer, exactly what was granted, its value, and its expiry — the same turn it is agreed. An override with no record is a permanent obligation that survives everyone who knew about it.

**After changing a limit, a gate or an override**, write the change to `## Plans` and any customer-specific grant to `## Commitments` in the same turn (`memory-template.md`). If the enforcement ladder itself was designed or revised, it is a decision worth `artifacts/<kebab-name>.md` with its `## Boxes` line — the thresholds get questioned every time a customer complains about a wall.
