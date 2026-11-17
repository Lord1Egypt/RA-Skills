# Transactions and account data

## Edit a cart or checkout

1. Read the resource with `get_cart` or `get_checkout`. Copy only the returned `cart` or `checkout` object, not the response envelope.
2. Find the intended line by its top-level `id`, not its variant `item.id`.
3. Exclude the response-only root `next`; remove fetched `signals` and `attribution`.
4. Change only the requested fields. Do not recalculate totals. Preserve unrelated fields and unknown extensions, including empty objects and arrays such as `payment.instruments`.
5. Call `update_cart` or `update_checkout` with `shop`, `id`, and the edited `cart` or `checkout`.
6. Verify returned items, quantities, prices, messages, and status.

The server removes schema-declared response-only fields. Do not reduce the document to changed fields.

Mutations accept `meta:{"idempotency-key":uuid}`. Reuse the UUID only for the same intended operation.

## Complete a checkout

1. Inspect the latest checkout returned by `create_checkout`, `update_checkout`, or `get_checkout`, including status, items, totals, messages, and `payment.instruments`. If it may be stale, call `get_checkout` first.
2. Treat checkout status as authoritative. Resolve `incomplete` messages. For `requires_escalation`, give the user its `continue_url`. Proceed only from `ready_for_complete`; do not recreate Checkout's eligibility decision from `get_account` spend permissions.
3. Present the offered instruments and have the user confirm one exact instrument with the current merchant, items, quantities, and total. Copy that full object exactly as returned, preserving every field and extension; never choose a default, resolve by id/handler/display, or invent a credential or token.
4. Send `complete_checkout` exactly once; never repeat it, even with the same idempotency key. Add `selected: true` at the top level of the copied instrument, change nothing else, and send it as the single entry in `payment.instruments`:

```text
{shop,id,checkout:{payment:{instruments:[exact_confirmed_instrument_with_selected_true]}}}
```

The merchant remains authoritative for freshness, readiness, and whether the instrument is still offered. A spend permission shown by `get_account` explains what the user has granted the agent; checkout status is the completion decision. No separate spend request is needed for `create_checkout` or `complete_checkout`, even when buyer review opens in a browser. API failure or escalation is not permission to switch to a spend request. Report every returned message and disclosure. Only a `completed` checkout with an order confirms purchase.

## Pay through a website's card form

Choose the purchase path before requesting approval. Shop search results provide `seller.domain`; use Shop's structured checkout directly.

For a purchase URL, inspect its HTTP headers and HTML. A `powered-by` header naming Shopify, or `rel="buy"` with `dev.shopify.shop_pay` among its payment handlers, identifies a Shop checkout path: use Shop tools with that store. If neither appears on the page, inspect the checkout page before requesting approval.

Use a spend request only when the chosen path requires entering a card into the website's checkout form. A failed Shop checkout or `requires_escalation` is not permission to switch paths. The buyer reviews the payee, purchase terms, saved card and spending limit before approving the spend request.

1. Read the site's checkout terms. Use its stated currency and total; never convert prices or invent missing details. Include the business country only when the site states it.
2. Create one spend request with those terms, a spending limit and a description of the purchase the buyer will recognize. Keep URLs and personal/payment details out of the approval text. Shop uses the preferred saved card unless the buyer chose another; use a returned saved-card id for that choice.
3. Share `continue_url` so the buyer can review and approve the spend request.
4. After the buyer approves the request, call `get_spend_request` with `include:"card"` to obtain the issued card.
5. Enter the issued `card` only into the approved merchant's checkout form, exactly as returned. Keep credentials confined to payment entry or a private handoff file, never chat, logs or other output.
6. Report the observed merchant result with `complete_spend_request`. Report `success` only when the merchant confirms it, with order details when known. Otherwise report `error` with the observed failure information; keep an unknown charge outcome unknown.

Updates are partial: send only changed fields to `update_spend_request`. Omitted fields stay unchanged, lists replace their previous values, and supplied address fields merge with the saved address.

`cancel_spend_request` cancels only the request; it does not cancel or refund the merchant's purchase or revoke an issued card. The request's `expires_at` is its approval/retrieval deadline, not card expiry. `consumed` alone proves neither card delivery nor merchant payment.

Use `display.funding_instrument` to name the saved card funding the purchase; the issued card's `display.last_digits` identifies the payment to the merchant. Present returned description labels as is, otherwise brand and last digits.

If an error is returned, follow its retry guidance. If the operation cannot complete, report the error. An error recording the purchase result does not mean the purchase failed.

## Recover a write

Trust returned state when it resolves the outcome. Spend-request failures follow the rule above instead. For a timeout or ambiguous cart or checkout write, read the resource first. Except for checkout completion, repeat only the exact original request with the same idempotency key; never start a new purchase or spend request to recover an uncertain one. If a create returned no ID and had no key, report the outcome unknown and stop. Preserve successful results from other merchants.

`complete_checkout` is excluded from repetition, even with the same key. After an uncertain completion, read `get_checkout`; only `completed` with an `order` confirms the purchase. Report any other state, or a failed read, as not confirmed; give the user a returned `continue_url` and stop. Never complete again or buy a replacement to recover it.

## Use the user's Shop account

`get_account` reads the connected Shop identity and wallet: saved addresses, the spend permissions the buyer has granted the agent, and saved payment methods with the account's preferred card. `search_orders` and `get_order` read the orders and packages Shop tracks for the account. Use these operations to understand the user and complete their task; a successful `get_account` also confirms that Shop is connected.

On `auth_required`, follow the binding's sign-in path, then retry. An operation-local `insufficient_scope` means the agent lacks the access named in `required_scope`: that call was not executed, and other Shop tools are unaffected. Explain the limit; do not retry automatically or switch tools to work around it. A missing field means no result was returned; use messages to distinguish a skipped read from an unavailable one. An empty list means the field was checked and nothing was available. Use only returned information. Do not copy `buyer.email` into checkout. Copy a selected `addresses[]` entry unchanged when checkout needs a saved delivery address.

## Search orders

Use `search_orders` for personal orders. Sign-in is required. Do not ask for a merchant order ID first. Use query text for merchant, item, or order number. Shop tracks every order from any store. By default only in-progress orders are returned; set `filters.status: all` to search the full order history, including when the default returns nothing. Refine the query and the date filters before reporting an order as not found. `shipments` are packages Shop is tracking without their order, usually found in email.

| Optional field | Values |
|---|---|
| `filters.status` | `in_progress` (default), `all` searches the full order history. |
| `filters.date` | `{from?,to?}`, inclusive placement dates, `YYYY-MM-DD`. |
| `pagination` | `{limit?,cursor?}`; copy returned cursors unchanged. |

Order prices and totals are integer minor units in the order's `currency`. `XXX` means no known currency; Shop order history uses hundredths, so `1250` represents `12.50` without a currency symbol. Distinguish line totals from a missing order total; never combine amounts with unknown or different currencies into one spending total.

Read returned events, expectations, tracking, `permalink_url` and each record's `messages` when present. Missing data is unknown, not zero, unpaid or undelivered: a record can omit `line_items`, and a line can omit its price, totals or quantity. Each `fulfillment.events[]` entry is one shipment's latest known snapshot. “Fulfilled” or “label created” does not prove shipment or delivery.

## Read one order

Use `get_order` to reread an order or package from `search_orders`. Copy its `id` from `orders[]` or `shipments[]` unchanged. Sign-in is required; call it directly without checking the account first.
