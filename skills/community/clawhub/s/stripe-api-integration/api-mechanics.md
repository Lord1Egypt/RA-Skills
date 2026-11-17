# API Mechanics — Conventions That Apply to Every Endpoint

**Read `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`** (or its box) for the pinned API version and SDK before writing any call: parameter names and object shapes are version-dependent, and a sample written against the wrong version fails with `parameter_unknown`.

**Contents:** [Amounts and Currency Exponents](#amounts-and-currency-exponents) · [Idempotency](#idempotency) · [Pagination](#pagination) · [Expanding Objects](#expanding-objects) · [Metadata as an Index](#metadata-as-an-index) · [API Versioning](#api-versioning) · [Rate Limits and Bulk Work](#rate-limits-and-bulk-work) · [Searching and Finding Objects](#searching-and-finding-objects) · [Connect Headers](#connect-headers) · [Restricted Keys](#restricted-keys)

## Amounts and Currency Exponents

Every amount is an integer in the currency's smallest unit. The multiplier is `10^exponent`, and the exponent is a property of the currency, not a constant.

| Exponent | Examples | 10 major units becomes | Extra rule |
|---|---|---|---|
| 2 (most currencies) | USD, EUR, GBP, BRL, INR | `1000` | — |
| 0 (zero-decimal) | JPY, KRW, VND, CLP, ISK | `10` | Multiplying by 100 overcharges 100x |
| 3 (three-decimal) | KWD, BHD, JOD, OMR, TND | `10000` | The value must be a multiple of 10 — the last digit is always 0 |

```
amount = round(major_units * 10^exponent)     # integer arithmetic, never float
```

- Compute in integers or a decimal type end to end. `0.1 + 0.2` is not `0.3` in IEEE-754, and rounding a float total after summing floats loses cents that a customer will eventually notice.
- Percentages (tax, application fees, discounts) round per line item, not on the total, or your invoice will not add up to itself.
- Currency is fixed at creation for a PaymentIntent: changing it means a new object.
- There is a minimum charge per currency, around 0.50 USD equivalent. Aggregate micro-transactions before charging; a metered plan that bills 0.03 EUR is a plan that cannot bill.
- Store the currency next to every amount you persist, including in `memory.md` (`45,250 EUR`, never `€45,250`).

## Idempotency

Send `Idempotency-Key` on every POST that moves money or creates an object with side effects.

- **The key is the business action.** `order-8123-charge`, `sub-4417-2026-07-invoice`. A fresh UUID per attempt makes each retry a distinct action, which is exactly the bug the header exists to prevent.
- Stripe stores the result for about 24 hours and replays it — the same response, including the same object id. A retry queue that can lag more than a day must check its own records before re-sending.
- The key binds to the request body. The same key with a different body returns an error rather than quietly doing either thing. Changing the amount means a new action, so it means a new key.
- Keys are ≤255 characters and scoped per account (and per connected account when using `Stripe-Account`).
- GET and DELETE are naturally idempotent; the header is for POST.
- Two layers deserve keys for different reasons: the HTTP client retrying a timeout, and your queue retrying a job. Derive both from the same business identifier so they collapse into one action.

## Pagination

- `limit` maxes out at 100 per page. Default is smaller; ask for what you need.
- Cursor with `starting_after=<last_object_id>` (or `ending_before`), never an offset. Offsets over a live collection skip and repeat rows as new objects arrive.
- `has_more` is the loop condition. Stopping when a page is short is a bug: a filtered page can be short and still have more.
- Every list endpoint accepts `created[gte]`/`created[lte]` — bound the range before paging a year of charges, or the loop is the rate-limit incident.
- SDK auto-pagination helpers are safe for reads; they still generate one request per page against the rate limit.

## Expanding Objects

- `expand[]=customer`, `expand[]=latest_invoice.payment_intent` — up to 4 levels deep.
- Expanding costs latency on every call. Expand what the code path needs, not what might be nice.
- **Webhook payloads cannot be expanded.** The event carries the object as it was; if the handler needs related data, fetch it inside the handler.
- Lists can expand into their items with `expand[]=data.customer`.
- An expanded field that comes back as a string id and not an object means the expand path was wrong, not that the relation is missing.

## Metadata as an Index

- 50 keys per object, keys around 40 characters, values around 500. It is an index, not a document store.
- Put your own primary key on every object at creation: order, tenant, user. Reconciliation, refunds and disputes all start from "which of ours is this".
- Metadata is visible in the Dashboard and in exports — no personal data beyond what belongs there, and never a secret.
- Metadata does not propagate. A Checkout Session's metadata is not the PaymentIntent's; set `payment_intent_data[metadata]` and `subscription_data[metadata]` explicitly, or the object that survives the flow is the one without your key.
- Subscriptions copy metadata onto invoices at creation, not retroactively — a key added later is missing from every invoice already issued.

## API Versioning

- The account has a default version; each API key call can pin one, and each webhook endpoint carries its own. Three places, and they drift apart quietly.
- Pin explicitly (`api_version` in `config.yaml`) so an upgrade is a deploy you chose, not a Tuesday.
- The pattern that bites: code upgraded, webhook endpoint left on the old version, so the payload the handler parses no longer matches the objects the code fetches.
- Upgrade as a project: read the changelog for the versions you skip, update the endpoints and the code together, replay a sample of events in test, then move the account default. Put the review on a `## Due` row.
- Newer Stripe surfaces (v2 APIs, thin events that carry only ids) coexist with v1; a thin event is a signal to fetch, not a payload to parse.

## Rate Limits and Bulk Work

- Live mode is documented around 100 read and 100 write requests per second, lower in test; limits are per account and Stripe may adjust them.
- Backfills and migrations are the usual trigger. Cap concurrency, add exponential backoff with jitter on 429, and run them off-peak — a 429 storm during checkout is a revenue incident caused by a script.
- Writes are the scarcer budget. Batch by reading what already exists before creating anything in a loop.
- Search and Sigma have their own, lower limits: they are for analysis, not for the request path.

## Searching and Finding Objects

- List endpoints filter by exact fields (customer, status, created range) and are the cheap path.
- The Search API takes a query language over indexed fields including metadata (`metadata['order_id']:'8123'`), and it is **eventually consistent** — an object created a second ago may not be findable yet. Never gate a payment flow on search.
- To find "the customer for this email", prefer looking it up in your own database by your own key. Stripe is not your user directory, and duplicate customers with the same email are legal in Stripe and lethal for billing.

## Connect Headers

- Acting on a connected account means the `Stripe-Account: acct_…` header, not a different key. Omit it and you operate on the platform, which is where the `resource_missing` confusion comes from.
- Idempotency keys are scoped per account, so the same key on platform and connected account are two different actions.
- Full charge-type semantics: `connect.md`.

## Restricted Keys

- Restricted keys (`rk_…`) grant a subset of resources and permissions. A background job that only reads charges gets a read-only restricted key, not the account's secret key.
- One key per workload, so revoking the leaked one does not take down everything else.
- Restricted keys are secrets like any other: pointer only in stored notes (`memory-template.md`), rotation on a `## Due` row (`go-live.md`).

---

**When the pinned API version, the idempotency-key convention or the metadata schema is decided or changed**, write it to `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`, and record the convention itself under `conventions` in `config.yaml` — it is a declaration, not an observation. A version upgrade also updates its `## Due` row.
