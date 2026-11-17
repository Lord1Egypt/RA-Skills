# Testing — Test Mode, Test Clocks, and What Cannot Be Rehearsed

**Read `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`** (or its box) before writing tests: which events the handlers rely on, and which flows already failed in production, are the test cases that matter. `incidents/<year>.md` is a list of tests you should already have.

**Contents:** [Two Universes](#two-universes) · [What to Test, in Priority Order](#what-to-test-in-priority-order) · [Test Cards](#test-cards) · [Test Clocks](#test-clocks) · [Testing Webhooks](#testing-webhooks) · [Testing Without Calling Stripe](#testing-without-calling-stripe) · [What Test Mode Cannot Prove](#what-test-mode-cannot-prove) · [Load and Migration Rehearsals](#load-and-migration-rehearsals)

## Two Universes

Test and live are separate datasets with separate keys, objects, webhooks and Dashboards. A test object id is meaningless against a live key and returns `resource_missing`, which is the most misdiagnosed error in this domain (`debug.md`).

- Never mix keys within one environment's configuration. One key resolution path, one mode, chosen by environment variable — a fallback default is how a live key ends up in a test run.
- Test data cannot be migrated to live. Products and prices are recreated; the ids differ; anything hardcoded breaks.
- Sandboxes give isolated test environments per developer or per branch, which is how parallel work stops overwriting the same test customer.
- Test mode is free and unlimited; there is no reason for a shared "staging" that points at live.

## What to Test, in Priority Order

Payment code is judged on failure paths, so test them first — the happy path is the one that gets manually clicked anyway.

1. **Webhook handler idempotency**: deliver the same `event.id` twice and assert one side effect. This is the test that prevents duplicate fulfillment.
2. **Signature verification**: a bad signature returns 4xx, and the handler never runs. Verify against raw bytes.
3. **Declines**: each `decline_code` your retry logic branches on produces the branch you expect (`dunning.md`).
4. **Authentication required**: an off-session charge that needs 3DS produces the recovery path, not a retry loop (`sca-3ds.md`).
5. **Out-of-order and late events**: a subscription update arriving after the invoice it precedes must not corrupt state.
6. **Renewals, trial ends and retries**: with a test clock, below.
7. **Proration**: the preview matches the invoice you assert against, for both upgrade and downgrade.
8. **Refunds, partial refunds and credit notes**, including their tax effect.
9. **Currency exponents**: at least one zero-decimal currency in the test matrix, or Rule 2 is untested.
10. **The happy path**, once, end to end.

## Test Cards

Stripe publishes card numbers that force specific outcomes; the ones worth having in a fixtures file:

| Purpose | Card |
|---|---|
| Success | `4242 4242 4242 4242` |
| Generic decline | `4000 0000 0000 0002` |
| Insufficient funds | `4000 0000 0000 9995` |
| 3DS authentication required | `4000 0025 0000 3155` |
| Dispute (fraudulent) after charge | `4000 0000 0000 0259` |

Any future expiry and any CVC work. There are numbers for incorrect CVC, expired card, processing errors, per-country behavior and specific dispute reasons — check the current test-card list rather than memorizing it, because it grows.

The trap: test cards simulate the *outcome*, not the issuer. A card that forces a 3DS challenge tells you your redirect handling works; it tells you nothing about how often real issuers will challenge.

## Test Clocks

A test clock is a simulated present that a set of test customers lives in. Advance it and Stripe evaluates renewals, trial ends, retries and cancellations as if that time had passed — in seconds.

Use it whenever the behavior depends on time:

- The first renewal of a new plan, and the invoice it produces.
- Trial end with a payment method, and trial end without one.
- The complete dunning schedule: every retry, the terminal behavior, the emails.
- A proration on a mid-cycle upgrade, then the next full invoice.
- Cancellation at period end, and what the last invoice contains.
- A scheduled price migration landing on the right cycle (`pricing-models.md`).

Working rules: create the customer *inside* the clock — an existing customer cannot be moved into one. Advance forward only, in the steps the scenario needs, and assert the objects and events after each step rather than only at the end. Clocks are test mode only, and there are limits on how far and how fast they can advance.

Any change to a retry schedule, trial length or price migration that ships without a clock rehearsal is a change validated by reading it.

## Testing Webhooks

- **Locally**: if the Stripe CLI is already available, `stripe listen --forward-to <local-url>` forwards real test events to a local server and prints a signing secret for that session, and `stripe trigger <event>` produces one on demand. Neither is required — the Dashboard can resend any event to a deployed endpoint.
- **Triggered events are synthetic**: they carry plausible but unrelated objects. Assertions that depend on your own metadata need events produced by your own test flows, not by `trigger`.
- **In CI**: do not call Stripe. Store real event payloads captured once as fixtures and post them to the handler with a signature computed from a test secret. That tests your handler, deterministically, in milliseconds.
- **Resend from the Dashboard** to reproduce a production failure against a fixed handler — the same event, the same payload, the real shape.
- Test that the handler acks fast: a handler that does its work before responding is a handler that will be retried into duplicates under load.

## Testing Without Calling Stripe

- Unit-test your own logic — amount arithmetic, retry decisions, state transitions, entitlement — against fixtures, with no network. These are the tests that run on every commit.
- Integration-test against test mode for the flows where Stripe's behavior is the thing under test: proration, tax calculation, Checkout Session shape.
- Do not mock the Stripe SDK deeply. A mock that returns what you assume is a test of your assumption; capture real test-mode responses as fixtures instead.
- Keep a fixtures file of ids and payloads regenerated deliberately, not scraped from a live account.

## What Test Mode Cannot Prove

| Not provable in test | Why it matters | Where it is handled |
|---|---|---|
| Radar behavior on real traffic | Live rules block payments that always passed | `advanced.md` |
| Which payment methods this account can charge | Availability is per account, country and currency | `payment-methods.md` |
| Real issuer 3DS rates | Conversion impact is a live measurement | `sca-3ds.md` |
| Payout timing, reserves, first-payout delay | Cash-flow planning breaks on it | `reconciliation.md` |
| Tax registrations and real rates | No registration means no tax calculated | `tax.md` |
| Wallet buttons on real devices and domains | Domain verification and device support | `payment-methods.md` |
| Rate limits under real bursts | Test traffic is not bursty | `api-mechanics.md` |
| Dispute outcomes | Issuers decide, and only in live | `disputes.md` |

The launch consequence: the first live transactions are part of the test plan (`go-live.md`).

## Load and Migration Rehearsals

- Rehearse a backfill against test mode at the concurrency you plan to use, and watch for 429s — the migration that breaks checkout is a migration nobody rehearsed.
- Import a representative slice of production shapes, not ten clean rows: the customers with three subscriptions, the ones mid-dunning, the ones with a coupon that expired.
- Rehearse rollback too. "We will just recreate the objects" is not a rollback when the objects have live money attached.

---

**When a test-mode rehearsal reveals a real defect** — a duplicate side effect, a broken proration, a dunning path that never recovers — write the finding to `incidents/<year>.md` in `~/Clawic/data/stripe-api-integration/` even though no customer was hit, and if the rehearsal produced a reusable procedure (a clock scenario, a migration runbook), save it as `artifacts/procedure-<name>.md` with its `## Boxes` line in the same turn.
