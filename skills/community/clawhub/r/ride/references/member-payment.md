# Explicit member payments — DHL-30194

This flow is for an authenticated TADA/Throo **member**, not a crypto wallet.
Use the user's selected payment method: `CREDITCARD` or `ABA_AOF`. ABA_AOF is
an already-authorized ABA account-on-file, not a card or manual QR transfer.
Do not create/link/top up accounts on the user's behalf. TADA Wallet and N/A
rides remain out of scope.

## Choose a source and search

Check `amb whoami` first. KH supports both methods, subject to server eligibility.
HK (Hong Kong), like NY and SG, supports `CREDITCARD` only: the CLI rejects
`ABA_AOF` outside KH before any payment call, so never offer an ABA account
there. Ask which method the user wants; do not change a previously selected method.
Account discovery is `amb aba-accounts --json`; never choose an expired account.
An upstream `PAYMENT_API_ERROR` means lookup failed, not that the account list is empty.

Use the previously confirmed pickup/destination coordinates and explicit region:

```bash
amb ride-search <oLat> <oLng> <dLat> <dLng> --region KH --payment-method ABA_AOF --json
```

Without a source UUID, this returns masked eligible sources for selection, not a
quote. Ask the user to select one and rerun with its exact ID:

```bash
amb ride-search <oLat> <oLng> <dLat> <dLng> <payment_item_uuid> --region KH --payment-method ABA_AOF --json
```

For a card, substitute `CREDITCARD`. In HK, use the same command with
`--region HK --payment-method CREDITCARD`, and pass `"region":"HK"` in the
JSON commands below. HK routes through the same gateway as SG; the CLI keeps
`HK` as the ride's region. Explicit-method searches always use v2,
including credit cards. Unflagged commands remain v1 card-only compatibility.
Never switch API versions within a search-to-create flow.

The result carries `api_version: 2`, `search_id`, `payment_method`,
`payment_item_uuid` and product options. Offer only `na: false` products with a
price. Show the returned price/currency verbatim; do not reconstruct discounts.
The CLI stores a short-lived, source/owner-bound quote locally without JWTs.

## Coupons

For the selected product, use its original v2 search context:

```bash
amb coupon-available '{"region":"KH","search_id":"<v2 search>","product_id":100700,"payment_method":"ABA_AOF","payment_item_uuid":"<account>"}' --json
```

Use only `available: true` coupons supporting the selected payment method.
Follow the bounded three-candidate comparison policy in the main skill, but
perform every re-quote with the same `--region`, `--payment-method`, source ID
and `--coupon-code <exact code>`. A coupon change requires a new search. Never
substitute a campaign promotion code for a coupon code.

## Create once

Confirm the selected product, exact quoted total and payment method with the
user. Keep the latest search ID and the same source, route and coupon together:

```bash
amb ride-request '{"region":"KH","search_id":"<v2 search>","payment_method":"ABA_AOF","payment_item_uuid":"<account>","product_id":100700,"confirmed_price":"7200","locations":[{"latitude":11.5639796,"longitude":104.9304278,"name":"Royal Palace","address":"Samdach Sothearos Blvd (3), Phnom Penh"},{"latitude":11.56963,"longitude":104.92102,"name":"Central Market","address":"Street 51, Phnom Penh"}]}' --json
```

These coordinates/price are illustrative: use the user's confirmed locations
and actual latest quote. With a coupon, include the same `coupon_code`.
`confirmed_price` is required for **every v2 booking**, not just coupons.

The CLI checks current ongoing/unpaid slots before creation, echoes server
quote fields, and consumes the quote before submitting once. Do not retry an
ambiguous create. Use `amb ride-current KH --json` to inspect existing rides.
`RIDE_CREATE_OUTCOME_UNKNOWN` means the create was sent but no definite answer
came back (5xx, 408/429, `ride_creation_in_progress`, network failure or
timeout), so a ride may exist. Run
its `inspect_command` first and track any ride it shows; search again only
after it shows no new ride. `NETWORK_ERROR` (with `cause` and `host`) before
submission means the gateway was unreachable and nothing was created; it is
not an expired session, so do not ask the user to log in again. Lookups may be
retried once the network recovers, but a `NETWORK_ERROR` from `ride-pay` or
`tip` (always when `cause` is `TIMEOUT`) may follow a request the server already
processed: re-check `amb ride-current KH --json` / `amb ride-status <request_id>`
before any retry, never blind-retry.
An expired quote or `PRICE_NOT_MATCHED` requires a fresh search and confirmation.
Never reuse a card quote for an ABA account.

On a returned `request_id`, track that ride even if follow-up verification
fails; do not create another. Require `payment_method_verified: true` before
claiming the create/current-ride method check passed. Start the normal
`ride-relay.js` flow immediately. Status, cancellation and receipts retain their
existing commands; there are no crypto `ride-pay-prepare/confirm` steps.

## Unpaid ride and optional tip

Only with the user's approval to settle the specific unpaid ride:

```bash
amb ride-pay '{"region":"KH","request_id":"<current unpaid ride>","payment_method":"ABA_AOF","payment_item_uuid":"<account>"}' --json
```

Do not consider cleanup complete until `cleanup_verified: true`. Ongoing and
unpaid slots are independent. Errors must not trigger automatic card fallback.

For an explicitly approved tip, first inspect `amb tip-config KH --json`.
Do not offer or submit when disabled; respect currency and amount constraints:

```bash
amb tip <ride_id> <amount> --payment-method ABA_AOF --currency KHR
```

Omitting `--payment-item` reuses the ride's source only when the method matches.
Changing the method requires `--payment-item <matching source UUID>`. Tip status
may be asynchronous. The CLI blocks repeat submissions after an attempt; never
work around that guard. Inspect ride status for settlement, or report unresolved
status for operator review. A transport error does not prove no charge occurred.

## Route selection safety

The CLI derives the route group from `car_type` using the server's shared
`CarGroup.fromCarType` mapping and echoes the matching route distance in km.
Multiple route groups are supported. If routing data is present but the matching
group is missing, creation fails closed. Do not substitute another route manually.
When routes are empty, the optional distance is omitted; the base-ride server
computes its distance from its own route.
