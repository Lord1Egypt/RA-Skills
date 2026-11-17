# Go Live — Launch, Key Management, and Migrating From Another Processor

**Read `## Integration Shape`, `## Webhook Endpoints` and `## Due` in `~/Clawic/data/stripe-api-integration/memory.md`** (or their boxes) before a launch or a key rotation: what is deployed, what is pinned, and what is already scheduled decide the plan.

**Contents:** [Account Activation Is Not Instant](#account-activation-is-not-instant) · [Key Management](#key-management) · [Rotating a Key](#rotating-a-key) · [A Key Leaked](#a-key-leaked) · [Launch Checklist](#launch-checklist) · [The First Live Transactions](#the-first-live-transactions) · [Migrating From Another Processor](#migrating-from-another-processor) · [Migrating Subscriptions](#migrating-subscriptions) · [After Launch](#after-launch)

## Account Activation Is Not Instant

Live mode requires an activated account: business details, ownership and identity verification, and bank details. Verification can ask for documents, and it can ask again after launch when volume or business description changes.

- Start activation before the integration is finished. Teams routinely discover on launch day that payouts are blocked pending a document.
- The business description and website you submit have to match what you actually sell. A mismatch is the usual cause of a post-launch restriction, and restrictions pause payouts, not charges — money accumulates where you cannot reach it.
- The first payout takes substantially longer than the steady-state schedule, commonly one to two weeks. Launch cash flow plans around that number (`reconciliation.md`).
- Some categories require extra review or are not supported at all. Confirm before building, not after.

## Key Management

| Key | Where it may live | Never |
|---|---|---|
| Publishable (`pk_…`) | Client-side code, public HTML | — (it is public by design) |
| Secret (`sk_…`) | Server environment, resolved from a secrets manager at boot | Repository, client bundle, log line, `~/Clawic/data/`, a chat message |
| Restricted (`rk_…`) | Same as secret, scoped per workload | Same as secret |
| Webhook signing (`whsec_…`) | Server environment, one per endpoint | Shared across endpoints or environments |

- One key per workload, not one key for the company: the API worker, the analytics job and the support tool get separate restricted keys with the minimum resources each needs. Revoking one then does not take down the others.
- Never construct a key from parts, never accept one from a request, never echo one in an error message. Redact by prefix in logs (`sk_live_…`) if you must log anything at all.
- Anywhere a key would be written down — notes, runbooks, an architecture document, this skill's own storage — the pointer goes instead: `keychain:stripe-live`, `1password:Work/Stripe/live`, `ssm:/prod/stripe/api-key` (`memory-template.md`).

## Rotating a Key

Rotation is roll-forward, not delete-and-hope. The old key keeps working until revoked, and the old key is the one that leaked.

1. Create the new key with the same scope.
2. Write it to the secrets manager under the same name and version it.
3. Deploy so every consumer reads the new value; restart everything that caches it at boot.
4. Verify traffic on the new key in the Dashboard logs — by key, not by "it seems fine".
5. Revoke the old key.
6. Watch for `authentication_error` for a full cycle, including nightly jobs, which are the last consumer anyone remembers.

Webhook secrets rotate the same way, per endpoint, with the handler accepting both the old and the new secret during the overlap window.

Put the rotation interval in the `## Due` table, and rotate immediately on any departure or suspected exposure regardless of the schedule.

## A Key Leaked

1. **Roll the key first.** Revoke it before investigating; investigation with a live key in the wild is a decision to keep bleeding.
2. Deploy the replacement, verify traffic, confirm the old key is dead.
3. Review the Dashboard logs filtered by that key for calls you did not make: charges, refunds, transfers, payout destination changes, new keys, new webhook endpoints pointing somewhere you do not own.
4. Check the payout bank details specifically — redirecting payouts is the highest-value abuse of a stolen key.
5. Purge the key from wherever it leaked: git history, CI logs, an issue tracker, a chat thread. A revoked key in a public repository is still a signal about how the team handles keys.
6. Contact Stripe if anything moved.
7. Write the incident to `incidents/<year>.md` with what changed as a result.

## Launch Checklist

Everything unchecked here outranks the feature that is waiting.

- [ ] Account activated, bank details verified, business description matches the site
- [ ] Live keys resolved from a secrets manager, no key anywhere in the repository or the client bundle
- [ ] `api_version` pinned in code and matching every webhook endpoint (`api-mechanics.md`)
- [ ] Live webhook endpoints created, each with its own secret and an explicit event list
- [ ] Handler verifies signatures against raw bytes, acks fast, deduplicates by `event.id`
- [ ] Fulfillment and revocation hang off events, never off API responses
- [ ] Idempotency keys derived from business identifiers on every money-moving write
- [ ] Amounts integer, per-currency exponent, no floats anywhere in the path
- [ ] `metadata` carries your primary key on every created object
- [ ] Statement descriptor set to something the cardholder recognizes (`disputes.md`)
- [ ] Receipts and renewal notices enabled and readable
- [ ] Cancellation works in one click, in the product and in the portal
- [ ] Retry schedule and terminal behavior chosen deliberately (`dunning.md`)
- [ ] Tax registrations in place for where you sell, behavior inclusive or exclusive per market (`tax.md`)
- [ ] Radar rules reviewed rather than left entirely at defaults (`advanced.md`)
- [ ] Alerting on failed webhook deliveries, spikes in declines, and disputes
- [ ] Refund and dispute process has a named owner and a runbook in `artifacts/`
- [ ] Reconciliation scheduled with a `## Due` row (`reconciliation.md`)
- [ ] Rollback plan: what happens if the first hour goes wrong

## The First Live Transactions

Test mode cannot prove the live-only list (`testing.md`), so the first live transactions are part of the plan.

- Charge yourself a real, small amount on a real card, in each payment method you enabled, and refund it. This is the only way to see the descriptor, the receipt, the email and the timing exactly as a customer does.
- Watch the first live events arrive at the real endpoint, and confirm the handler ran and did the right thing.
- Verify the first payout lands in the right account for the right amount.
- Launch to a small cohort before a campaign. Declines, wallet availability and Radar behavior are all live-only measurements.

## Migrating From Another Processor

The hard part is not the code, it is the cards.

- **Card data migrates processor to processor, never through you.** Stripe has a data migration process; the previous processor exports the encrypted PANs directly. Requesting the numbers yourself is a PCI catastrophe and most processors will refuse anyway.
- **Plan the timeline in weeks.** Export, transfer, import and verification each take real time, and the old processor is rarely in a hurry.
- **Tokens do not transfer** — the ids from the old system are meaningless in Stripe. Your database needs a mapping column, populated during import, before anything charges.
- **Run both in parallel** during the cutover: new customers on Stripe, existing ones on the old processor until their tokens are imported and verified. A big-bang cutover on billing is a decision to explain a lost month.
- **Refunds stay where the charge happened.** Keep the old account open, with access, for at least the refund and dispute window — that is months, not days.
- **Reconcile across both** for every month of the overlap, or the numbers will never close (`reconciliation.md`).
- Verify a sample of imported cards with a zero-amount authorization or a small charge before relying on the whole import.

## Migrating Subscriptions

- Recreate products and prices in Stripe first, and record the mapping in `## Catalog` (`pricing-models.md`).
- Preserve billing anchors so customers are charged on the day they expect. A migration that resets everyone's renewal to today produces a month of double-billing complaints and disputes.
- Preserve trial ends and discounts explicitly; they do not come along with a card token.
- Import with `backdate_start_date` and the correct anchor rather than creating fresh subscriptions that immediately invoice.
- Rehearse the whole import in test mode with a representative slice, including mid-dunning and discounted customers (`testing.md`).
- Tell customers before the descriptor on their statement changes — an unrecognized descriptor after a silent migration is a wave of `unrecognized` disputes.

## After Launch

Schedule the recurring work now, while someone cares: reconciliation monthly, dispute-rate review monthly, webhook endpoint audit and API version review quarterly, key rotation annually or on any departure. Each of those is a row in `## Due`, checked at the start of a session and stated when overdue.

---

**On launch, write** the live account context, the pinned API version and the integration shape to `## Account Context` and `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`, every live endpoint to `## Webhook Endpoints` with a pointer for its secret, the recurring work to `## Due`, and the payout account to `~/Clawic/data/finances/accounts.md`. A migration plan or a rotation procedure is `artifacts/<name>.md` with its `## Boxes` line in the same turn; a leak or a failed cutover is a row in `incidents/<year>.md`.
