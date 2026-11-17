# Debug — Symptom to Cause

**Before diagnosing anything**, read `## Integration Shape` and `## Webhook Endpoints` in `~/Clawic/data/stripe-api-integration/memory.md` — or whatever `## Boxes` points to — and check `incidents/<year>.md` for the same symptom. Most second occurrences are the first occurrence with a different customer.

**Contents:** [Start From the Request Id](#start-from-the-request-id) · [Error Taxonomy](#error-taxonomy) · [Decline Codes That Change What You Do](#decline-codes-that-change-what-you-do) · [The Money Moved but Nothing Happened](#the-money-moved-but-nothing-happened) · [Duplicate Charge Investigation](#duplicate-charge-investigation) · [Worked in Test, Fails in Live](#worked-in-test-fails-in-live) · [State Mismatch Between Stripe and Your Database](#state-mismatch-between-stripe-and-your-database) · [When to Escalate to Stripe Support](#when-to-escalate-to-stripe-support)

## Start From the Request Id

Every Stripe response carries a request id (`req_…`) in its headers and in the error body. That id opens the exact request in the Dashboard's developer logs: parameters as received, the response, the API version used, the key that signed it, and whether it was idempotent-replayed.

Ask for the request id before asking for anything else. It settles in one lookup what a screenshot of an error message argues about for an hour: which key, which mode, which version, which parameters actually arrived. When the user has no request id, the next best identifiers are the object id and the exact minute — the logs are searchable by both.

The idempotency column in the logs is the one people forget: a request marked as a replay did not run again, and the "duplicate" the user is chasing is somewhere else.

## Error Taxonomy

Stripe errors sort into five types, and the type decides who fixes it.

| Type | HTTP | Means | Retry? |
|---|---|---|---|
| `card_error` | 402 | The issuer or the card said no; the request was fine | Only per the `decline_code` below |
| `invalid_request_error` | 400 | Your parameters: missing, malformed, wrong mode, wrong id, not permitted for this account | Never — retrying an invalid request is a loop |
| `authentication_error` | 401 | Key missing, revoked, or the wrong mode | Never; fix the key resolution |
| `rate_limit_error` | 429 | Too many requests for the account | Yes, exponential backoff with jitter |
| `api_error` / `idempotency_error` | 500-ish / 400 | Stripe's side, or a key reused with a different body | `api_error` yes with the *same* idempotency key; idempotency mismatch never |

Two error codes look like bugs and are almost always something else. `resource_missing` on an id you can see in the Dashboard means the wrong mode or a Connect object requested without the `Stripe-Account` header. `parameter_unknown` usually means an API version older or newer than the code was written against — check the pinned version before rewriting the call.

The distinction that matters most on a 402: the request succeeded as a request. Nothing about your integration is broken; a human's card was refused, and the retry policy belongs to the decline code, not to your HTTP client.

## Decline Codes That Change What You Do

`card_declined` is the outcome; `decline_code` is the instruction. Issuers deliberately keep fraud-related codes vague, so treat the vague ones as "not now" rather than "not ever".

| `decline_code` | What it means | Action |
|---|---|---|
| `insufficient_funds` | Exactly that | Retry later — this is the code that recovers best in dunning (`dunning.md`) |
| `generic_decline`, `do_not_honor` | Issuer refuses and will not say why, often risk-based | One retry after a day at most; then ask for another card |
| `expired_card`, `incorrect_cvc`, `incorrect_number` | Input problem | Ask the customer to correct it; retries are pointless |
| `authentication_required` | Issuer wants 3DS | Never retry off-session; recover on-session (`sca-3ds.md`) |
| `card_not_supported`, `currency_not_supported` | The card cannot do this transaction type or currency | Offer another method or currency (`payment-methods.md`) |
| `lost_card`, `stolen_card`, `pickup_card` | Reported card | Stop. Do not retry, do not tell the customer why — the issuer decides what they hear |
| `try_again_later`, `processing_error` | Transient on the issuer or network side | Retry once after a short delay |
| Anything else | Read it literally, then classify as retryable or not | Default to one retry, then request a new payment method |

Rule of thumb worth internalizing: fewer than half of first declines are permanent. Treating every decline as final throws away recoverable revenue, and treating every decline as retryable gets the account flagged for excessive retries.

## The Money Moved but Nothing Happened

The charge is in the Dashboard, the customer has an email from their bank, and your system knows nothing. Walk this in order.

1. **Was an event generated?** Dashboard → Events, filtered by the object id. If there is no event, the flow you think fired did not fire.
2. **Was it delivered?** The endpoint's delivery log shows attempts and response codes. A 2xx that arrived after Stripe's timeout still counts as a failure and triggers a retry.
3. **Did the handler reject it?** A 400 here is almost always signature verification against a parsed body, or the wrong endpoint secret.
4. **Did the handler run and do nothing?** The event type is not in the switch, or the payload shape differs because the endpoint is pinned to another API version.
5. **Did it run twice?** No deduplication by `event.id` — Stripe delivers at least once by design.
6. **Was it the wrong event?** For bank-based methods `checkout.session.completed` arrives with `payment_status: unpaid`; fulfillment belongs on `checkout.session.async_payment_succeeded` (`webhooks.md`).

The corollary: an integration where step 1 has no answer is not a webhook bug, it is a flow that never reached the state you assumed.

## Duplicate Charge Investigation

- Find both charges by `metadata[order_id]`, never by amount and timestamp — two customers buying the same plan in the same minute look identical.
- Compare the request ids. Same idempotency key on both means Stripe did not consider them the same request: the key differed, expired past ~24h, or was absent.
- A retry queue that drains after a day is a duplicate-charge machine. Keys are honored for about 24 hours; anything slower needs a dedup check against your own records before it charges.
- Client-side double submit shows as two charges seconds apart with different keys — disable the button *and* send the key; only the second one is a real fix.
- Refund the later charge, not the earlier one: the earlier one is the one referenced by everything else you already wrote.
- Close the loop by writing the row in `incidents/<year>.md` with the money impact.

## Worked in Test, Fails in Live

| Difference | What breaks |
|---|---|
| Radar rules run for real | Payments blocked in live that always passed in test |
| Payment methods are per-account and per-country | A method available in the docs is not enabled on this account |
| Real 3DS | Issuers challenge for real; test cards only simulate the flow you selected |
| Live webhook secret differs per endpoint | Verification fails on the first live event |
| Tax registrations exist or do not | Stripe Tax returns zero tax when there is no registration for that jurisdiction |
| Payout timing and reserves | Money is in the balance, not in the bank, and a new account has a longer first payout window |
| Rate limits bite | Live traffic is bursty in ways your test script was not |

`go-live.md` has the full pre-launch list; `testing.md` covers what can be rehearsed in test mode and what cannot.

## State Mismatch Between Stripe and Your Database

When your record and Stripe disagree, **Stripe is right** — it is the system that talked to the bank. Repair in one direction only.

- Re-fetch the object rather than trusting the webhook payload for anything you will act on twice; payloads are snapshots at the moment of the event and can arrive out of order.
- Order is not guaranteed. A handler that assumes `customer.subscription.updated` arrives after `invoice.paid` will occasionally be wrong; make each handler compute the state from the object it fetched, not from the sequence.
- For a full repair, list the objects from Stripe with a cursor and reconcile against your table — never the reverse, because your table cannot tell you about objects it never learned.
- A mismatch found twice for the same reason is an incident, not an accident: write it down.

## When to Escalate to Stripe Support

Escalate — with the request id — when the answer is on Stripe's side of the line: a payout that did not arrive after its stated schedule, an account restriction or verification hold, a Radar block you cannot explain from the rules you own, a webhook the Dashboard says was delivered and your logs never received, a dispute the Dashboard shows in an inconsistent state, or PAN migration from another processor (`go-live.md`). Everything above this line is faster to solve from the logs than from a support thread.

---

**After a diagnosis that cost real time**, write the symptom, the root cause and the money impact into `~/Clawic/data/stripe-api-integration/incidents/<year>.md`, and if the fix produced a procedure, save it as `artifacts/runbook-<symptom>.md` and add its `## Boxes` line to `memory.md` in the same turn. The second occurrence of a symptom should cost minutes, not the same afternoon again.
