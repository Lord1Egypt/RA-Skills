---
name: sp3nd
description: Purchase shipped products and tokenized Collector Crypt cards through SP3ND with USDC on Solana. Use for product links, live pricing, idempotent orders, payment, and fulfillment tracking. Collector Crypt purchases use wallet delivery with manual acquisition and transfer by SP3ND.
metadata:
  version: 1.11.0
  openclaw:
    requires:
      env:
        - SP3ND_API_KEY
        - SP3ND_API_SECRET
    primaryEnv: SP3ND_API_KEY
    config:
      requiredEnv:
        - SP3ND_API_KEY
        - SP3ND_API_SECRET
      optionalEnv:
        - SOLANA_RPC_URL
        - AGENT_WALLET_PATH
      stateDirs:
        - .wallet.json
---

# SP3ND Agent Purchasing

SP3ND accepts stablecoins for shipped products and tokenized Collector Crypt cards. This skill describes the production Agent API contract, including asynchronous pricing and manual fulfillment.

Choose the payment flow by product type before checkout:

| Purchase | Payment flow | Fulfillment |
|---|---|---|
| Collector Crypt card | `partnerPayment`: prepare, sign the exact transaction, submit | SP3ND manually purchases the exact card and transfers it to the paying wallet |
| Shipped products through the existing agentic x402 integration | `payAgentOrder` | Physical shipping |
| Shipped products through the normal Partner API integration | `createPartnerTransaction` | Physical shipping |

For Collector Crypt, read [Collector Crypt checkout](references/collector-crypt.md) before creating the cart or signing a payment. Both `payAgentOrder` and `createPartnerTransaction` reject real card orders with `COLLECTOR_CRYPT_PAYMENT_METHOD_UNSUPPORTED`; do not fall back to either endpoint. Normal approved API credentials work without a separate Collector Crypt opt-in.

## Base URL and authentication

```text
https://us-central1-sp3nddotshop-prod.cloudfunctions.net
```

Authenticated requests use:

```http
X-API-Key: <api_key>
X-API-Secret: <api_secret>
```

Keep both credentials and the agent wallet private. Never log or commit secrets or wallet key material.

## Non-negotiable safety rules

1. **SP3ND is authoritative for product data and money.** Submit product URLs and quantities. Never treat caller-supplied title, price, shipping, tax, fee, total, currency, recipient, or memo as authoritative.
2. **An order is not always immediately payable.** Inspect `payment_ready` and `pricing_status` after creation and every refresh.
3. **Only pay when `payment_ready === true`.** Canonical current orders also report `pricing_status: "ready_for_payment"`. The deprecated `quoted` value may appear on legacy orders, but it is compatibility metadata and never replaces the `payment_ready` gate.
4. **Never pay an expired quote.** Check `quote_expires_at` immediately before payment and refresh the order if it has expired or is about to expire.
5. **Use stable idempotency keys.** Reuse the same order key after a timeout or uncertain response. Never generate a new key for a retry of the same intended purchase.
6. **Use the server's payment requirements for the selected flow.** Collector Crypt uses the exact transaction and payment fields from `partnerPayment` prepare. Non-card x402 uses the HTTP 402 requirements. Do not calculate or override payment authority, and never combine payment flows.
7. **Always attribute end-user orders.** Send the end user's Solana address as `user_wallet`. Without it, an order remains partner-attributed and end-user points or history may not be credited.
8. **Treat order status and pricing status separately.** Fulfillment `status` does not replace `pricing_status`.
9. **Use one card buyer wallet.** For Collector Crypt, `payer_address`, `user_wallet`, and `asset_recipient_wallet` must be the same valid, on-curve Solana wallet. An agent cannot pay from its own wallet and have SP3ND deliver to a different user wallet. Use the intended recipient's authorized signer; do not substitute a wallet.
10. **Card payment is not delivery.** A paid Collector Crypt order queues manual acquisition and transfer. Poll for delivery and transfer evidence; do not buy or transfer the card yourself as part of this skill.

## Lifecycle at a glance

Shipped products:

```text
register
  -> create server-priced cart
  -> create idempotent order
      -> Ready for Payment
          (`payment_ready: true` and payable `pricing_status`)
          -> select shipping if required
          -> pay using server-issued 402 requirements
      -> Awaiting Review
          (`awaiting_team_quote` / `manual_review`)
          -> poll the order
          -> select a valid shipping option if required
          -> Ready for Payment
          -> pay only after the readiness gate passes
  -> track Paid / Ordered / Shipped / Delivered
```

Mixed shipped-product carts and items SP3ND cannot verify automatically remain one order. They are not split by the caller and must not be paid early.
An order in `Awaiting Review` must first reach the conceptual **Ready for Payment** state before it can be paid. This state means `payment_ready === true`, the canonical `pricing_status` is `ready_for_payment`, the quote is current, and any required shipping option is selected. A deprecated `quoted` status may remain on legacy orders, but never use it without `payment_ready === true`. Do not transition directly from `Awaiting Review` to `Paid`.

Collector Crypt:

```text
one canonical card URL (or optional live card search)
  -> server-priced cart, quantity 1, five-minute quote
  -> idempotent order with buyer wallet = recipient wallet, no shipping address
  -> partnerPayment prepare -> verify and sign exact bytes -> submit
  -> Paid / pending_acquisition: SP3ND manually buys the card
  -> Ordered / pending_delivery: SP3ND manually transfers the NFT
  -> Delivered with asset_transfer_signature
```

Only eligible native-Solana Collector Crypt V2 buy-now listings priced in USDC are supported. Never mix a card with shipped products or another card. A quote does not reserve the listing on Collector Crypt; a sold or changed listing may require review and a refund.

## 1. Register an agent

```http
POST /registerAgent
Content-Type: application/json

{
  "agent_name": "MyShoppingBot",
  "solana_public_key": "<agent-wallet-public-key>",
  "contact_email": "operator@example.com",
  "description": "Purchases products for approved users"
}
```

The response returns `api_key` and a one-time `api_secret`. Save the secret immediately.

If the secret is lost, call `POST /regenerateAgentSecret` using the registered wallet's signed, timestamped challenge. Regeneration invalidates the old secret.

## 2. Create a server-priced cart

Use only product URLs and quantities as purchasing inputs:

```http
POST /createPartnerCart
Content-Type: application/json
X-API-Key: <api_key>
X-API-Secret: <api_secret>

{
  "items": [
    {
      "product_url": "https://www.amazon.com/dp/B08XYZ123",
      "quantity": 1
    },
    {
      "product_url": "https://www.ebay.com/itm/123456789",
      "quantity": 1
    }
  ],
  "user_wallet": "<end-user-solana-wallet>"
}
```

Do not send a caller-selected `price` to control the purchase. Any display metadata accepted for compatibility is non-authoritative; SP3ND resolves the listing and computes purchasable values.

For a Collector Crypt card, use exactly one canonical URL such as `https://collectorcrypt.com/assets/solana/<asset-address>` with quantity `1`. Omit shipping/destination fields. SP3ND refetches the listing and obtains its price; no caller-supplied price is accepted as authority. See the [card cart example](references/collector-crypt.md#quote-the-exact-card).

Shipped-product cart totals can still be provisional. In particular, eBay availability and shipping depend on the destination. Always provide the final destination for shipped products when creating the order.

## 3. Create an idempotent order

Create one stable key for the user's intended checkout. Persist it before sending the request.

```http
POST /createPartnerOrder
Content-Type: application/json
X-API-Key: <api_key>
X-API-Secret: <api_secret>
Idempotency-Key: checkout_01JSTABLEKEY

{
  "cart_id": "cart_abc123",
  "idempotency_key": "checkout_01JSTABLEKEY",
  "user_wallet": "<end-user-solana-wallet>",
  "customer_email": "customer@example.com",
  "shipping_address": {
    "name": "John Doe",
    "recipient": "John Doe",
    "address1": "123 Main St",
    "address2": "Apt 4B",
    "city": "San Francisco",
    "state": "CA",
    "postalCode": "94105",
    "country": "United States",
    "countryCode": "US",
    "phone": "+14155551234"
  }
}
```

Send the stable key in either the `Idempotency-Key` header or the `idempotency_key` body field. Supplying both with the same value is recommended for broad client compatibility. If both are omitted by a legacy integration, the server falls back to `cart_id`, but new integrations must supply an explicit key.

For eBay, the complete destination is required for the location-aware offer and shipping check. Do not assume a price from a different country, postal code, or eBay TLD remains valid.

For Collector Crypt, omit `shipping_address` and send identical `user_wallet` and `asset_recipient_wallet` values along with `cart_id`, `customer_email`, and the stable idempotency key. The recipient is frozen into the order. See the [card order example](references/collector-crypt.md#create-the-wallet-delivery-order).

### Schema v2 lifecycle fields

Create and order-read responses include additive `schema_version: 2` lifecycle fields. Existing fields remain available.

A verified-only order can be created in a payable state:

```json
{
  "success": true,
  "schema_version": 2,
  "order": {
    "order_id": "firebase-document-id",
    "order_number": "ORD-1234567890",
    "status": "Created",
    "pricing_status": "ready_for_payment",
    "requires_manual_quote": false,
    "payment_ready": true,
    "quote_revision": 1,
    "quote_expires_at": "2026-07-26T18:30:00.000Z",
    "shipping_options": [],
    "selected_shipping_option": null
  }
}
```

A mixed or unverified order remains intact and enters review:

```json
{
  "success": true,
  "schema_version": 2,
  "order": {
    "order_id": "firebase-document-id",
    "order_number": "ORD-1234567890",
    "status": "Awaiting Review",
    "checkout_role": "manual_review",
    "pricing_status": "awaiting_team_quote",
    "requires_manual_quote": true,
    "payment_ready": false,
    "quote_revision": 0,
    "quote_expires_at": null,
    "shipping_options": [],
    "selected_shipping_option": null
  }
}
```

For an order in review:

- Show the user that SP3ND is reviewing pricing or shipping.
- Do not call a payment endpoint.
- Poll the singular order endpoint at a reasonable interval or refresh on user action.
- Continue only when the server returns a current payable quote.

## 4. Read orders

Read one order when waiting for a quote or tracking a checkout:

```http
GET /getPartnerOrder?order_id=<order_id>
X-API-Key: <api_key>
X-API-Secret: <api_secret>
```

List the authenticated partner's orders:

```http
GET /getPartnerOrders
X-API-Key: <api_key>
X-API-Secret: <api_secret>
```

**To list all orders, omit `status` (recommended).** `status=all` is also supported for compatibility. Otherwise, use `status` only for a real named order status such as `Created`, `Awaiting Review`, `Paid`, `Ordered`, `Shipped`, or `Delivered`.

Order reads expose the same additive schema v2 lifecycle fields as order creation. Preserve unknown fields for forward compatibility.

## 5. Select a quoted shipping option

When `shipping_options` contains choices and no valid selection exists, present the server-returned options to the user. Use the option's opaque ID; do not reconstruct its price or delivery estimate.

```http
POST /selectPartnerOrderShippingOption
Content-Type: application/json
X-API-Key: <api_key>
X-API-Secret: <api_secret>

{
  "order_id": "<order_id>",
  "shipping_option_id": "<opaque-option-id>"
}
```

The server validates the quote revision and expiry. Use the returned order as the new source of truth. If the selection is rejected because the quote changed or expired, refresh the order and ask the user to choose from the new options.

Before payment, confirm:

- `selected_shipping_option` matches the user's current choice when a choice is required.
- `quote_revision` is the latest revision returned by the server.
- `quote_expires_at` has not passed.
- `payment_ready === true`.
- `pricing_status` is canonically `ready_for_payment`; deprecated `quoted` may appear on legacy orders, but `payment_ready` remains authoritative.

## 6. Pay on the correct payment flow

### Collector Crypt

Use only `POST /partnerPayment` with `action: "prepare"`, verify and sign the returned transaction, then call the same endpoint with `action: "submit"` and the exact signed serialization. Read the [card payment and retry contract](references/collector-crypt.md#prepare-sign-and-submit-payment) before signing. Do not use the x402 example script for cards.

### Shipped products through x402

For the existing non-card agentic x402 integration, start payment using the canonical order ID:

```http
POST /payAgentOrder
Content-Type: application/json
X-API-Key: <api_key>
X-API-Secret: <api_secret>

{
  "order_id": "<order_id>"
}
```

`order_number` is optional. If supplied, the server validates that it belongs to `order_id`.

The initial call returns HTTP 402 with payment requirements in the `PAYMENT-REQUIRED` header and response body. Those requirements are authoritative:

```json
{
  "x402Version": 2,
  "accepts": [
    {
      "scheme": "exact",
      "network": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
      "maxAmountRequired": "<server-value>",
      "resource": "<server-value>",
      "payTo": "<server-value>",
      "asset": "<server-value>",
      "extra": {
        "order_id": "<order_id>",
        "order_number": "<order-number>",
        "feePayer": "<server-value>"
      }
    }
  ]
}
```

Build and sign the transfer strictly from the returned requirements. Include the exact memo specified by the response. Never reuse a 402 response from another order or quote revision.

Submit the signed x402 payload back to `POST /payAgentOrder` in the base64-encoded `PAYMENT-SIGNATURE` header. Do not call the facilitator's verify or settle endpoints directly. SP3ND atomically claims, verifies, settles, and records the payment so the same signed transaction cannot be settled twice.

After SP3ND accepts the signed payload, poll `GET /getPartnerOrder?order_id=...` until the order is `Paid`.

- `PAYMENT_SETTLEMENT_IN_PROGRESS`: do not submit another payment; keep reading the order until settlement resolves.
- `PAYMENT_SETTLEMENT_UNKNOWN` with `retryable: false`: do not retry payment. Retain the `order_id` and escalate for manual reconciliation because the transfer may have reached the network.

The reference implementation remains in:

```text
scripts/x402-pay-with-memo.mjs
```

It must be invoked only after the readiness checks above.

### Shipped-product Partner API transaction registration

Normal Partner API integrations use `POST /createPartnerTransaction` for shipped products. This endpoint rejects Collector Crypt orders. Identify the shipped-product purchase with:

```json
{
  "order_id": "<order_id>",
  "sender_address": "<payer-solana-wallet>"
}
```

`order_number` may also be supplied and is validated against `order_id`. Caller-supplied `amount`, `currency`, `memo`, and recipient fields are ignored. Use only the server-returned payment instructions.

## 7. Track fulfillment

Once paid, monitor the order's fulfillment `status` independently of `pricing_status`.

Pricing and payment gate:

```text
Awaiting Review -> Ready for Payment -> Paid
```

`Ready for Payment` is the readiness condition defined above, not a substitute for inspecting the schema v2 fields. Verified-only orders may begin in that state without entering review.

Shipped-product fulfillment after payment:

```text
Paid -> Ordered -> Shipped -> Delivered
```

Do not infer shipment or delivery from payment alone.

Collector Crypt has no physical shipping stage. `Paid` means SP3ND confirmed the USDC payment; `pending_acquisition` means staff still need to purchase the card, and `pending_delivery` means staff still need to transfer it. Complete only when the order reports `status: "Delivered"`, `fulfillment_status: "delivered"`, and `asset_transfer_signature`. If fulfillment needs review or ends unsuccessfully, report that state and let SP3ND handle reconciliation or a refund. See [manual wallet delivery](references/collector-crypt.md#track-manual-wallet-delivery).

## Retry and idempotency behavior

- Persist `cart_id`, `idempotency_key`, `order_id`, and `order_number`.
- Retry order creation with the original `Idempotency-Key`.
- After a timeout, call `GET /getPartnerOrder` or list orders before retrying.
- Never create a second cart/order solely because the response was lost.
- Never pay twice because a settlement response was lost. Read the order first, and stop for manual reconciliation if the API reports `PAYMENT_SETTLEMENT_UNKNOWN`.
- For a Collector Crypt submit timeout or unknown outcome, preserve the original signed bytes and read the order. Retry only the identical `signed_transaction_base64` when allowed; never rebuild, re-sign, or prepare a replacement while the first outcome is unknown.
- Do not cache a quote beyond `quote_expires_at`.

## Marketplace and destination rules

For shipped products, use a marketplace URL suitable for the recipient's destination, then let SP3ND verify the actual listing. Collector Crypt uses its canonical Solana asset URL and wallet delivery instead of a physical destination.

### Amazon storefronts

| Region | Storefront |
|---|---|
| United States | `amazon.com` |
| United Kingdom | `amazon.co.uk` |
| Canada | `amazon.ca` |
| Germany | `amazon.de` |
| France | `amazon.fr` |
| Spain | `amazon.es` |
| Italy | `amazon.it` |
| Netherlands | `amazon.nl` |
| Belgium | `amazon.com.be` |
| Poland | `amazon.pl` |
| Sweden | `amazon.se` |
| Brazil | `amazon.com.br` |
| Mexico | `amazon.com.mx` |
| Australia | `amazon.com.au` |
| India | `amazon.in` |
| Japan | `amazon.co.jp` |
| Singapore | `amazon.sg` |
| United Arab Emirates | `amazon.ae` |
| Saudi Arabia | `amazon.sa` |
| Egypt | `amazon.eg` |
| Turkey | `amazon.com.tr` |
| South Africa | `amazon.co.za` |

### eBay storefronts

| Region | Storefront |
|---|---|
| United States | `ebay.com` |
| Canada | `ebay.ca` |
| United Kingdom | `ebay.co.uk` |
| Germany | `ebay.de` |
| France | `ebay.fr` |
| Italy | `ebay.it` |
| Spain | `ebay.es` |
| Australia | `ebay.com.au` |

eBay seller availability, item price, and shipping can change with destination. The final order address is always authoritative.

## Minimal lifecycle example

```javascript
const BASE_URL = 'https://us-central1-sp3nddotshop-prod.cloudfunctions.net';
const auth = {
  'Content-Type': 'application/json',
  'X-API-Key': process.env.SP3ND_API_KEY,
  'X-API-Secret': process.env.SP3ND_API_SECRET,
};

async function json(response) {
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || `${response.status}`);
  return body;
}

async function getOrder(orderId) {
  const result = await json(await fetch(
    `${BASE_URL}/getPartnerOrder?order_id=${encodeURIComponent(orderId)}`,
    { headers: auth },
  ));
  return result.order ?? result;
}

async function beginCheckout({ productUrl, userWallet, email, shippingAddress, checkoutKey }) {
  // The server validates the canonical URL and whether the listing is eligible.
  const isCard = new URL(productUrl).hostname === 'collectorcrypt.com';
  const cartResult = await json(await fetch(`${BASE_URL}/createPartnerCart`, {
    method: 'POST',
    headers: auth,
    body: JSON.stringify({
      items: [{ product_url: productUrl, quantity: 1 }],
      user_wallet: userWallet,
    }),
  }));

  const orderResult = await json(await fetch(`${BASE_URL}/createPartnerOrder`, {
    method: 'POST',
    headers: { ...auth, 'Idempotency-Key': checkoutKey },
    body: JSON.stringify({
      cart_id: cartResult.cart.cart_id,
      idempotency_key: checkoutKey,
      user_wallet: userWallet,
      customer_email: email,
      ...(isCard
        ? { asset_recipient_wallet: userWallet }
        : { shipping_address: shippingAddress }),
    }),
  }));

  return orderResult.order;
}

function assertPaymentReady(order) {
  const validPricing = ['ready_for_payment', 'quoted'].includes(order.pricing_status);
  const isCard = order.order_type === 'collector_crypt_card';
  const unexpired = order.quote_expires_at
    ? Date.parse(order.quote_expires_at) > Date.now()
    : !isCard;

  if (order.payment_ready !== true || !validPricing || !unexpired) {
    throw new Error('Order is not ready for payment; refresh it instead.');
  }

  if (order.shipping_options?.length && !order.selected_shipping_option) {
    throw new Error('Select a current shipping option before payment.');
  }
}

async function requestPayment(order) {
  assertPaymentReady(order);
  if (order.order_type === 'collector_crypt_card') {
    return fetch(`${BASE_URL}/partnerPayment`, {
      method: 'POST',
      headers: auth,
      body: JSON.stringify({
        action: 'prepare',
        order_id: order.order_id,
        payer_address: order.user_wallet,
      }),
    });
  }
  // Existing agentic x402 integration: shipped products only.
  return fetch(`${BASE_URL}/payAgentOrder`, {
    method: 'POST',
    headers: auth,
    body: JSON.stringify({ order_id: order.order_id }),
  });
}
```

The example stops before signing. For a card, verify the prepared transaction, sign its exact bytes with the fixed buyer wallet, and submit as described in [Collector Crypt checkout](references/collector-crypt.md). Preparing a payment does not charge the wallet.

## Operator controls

- Use a dedicated, least-funded wallet when the agent is the buyer. For Collector Crypt delivery to an end user, use that same end user's authorized payment signer; do not substitute an agent wallet.
- Add an application-level approval limit before order creation or payment.
- Validate the recipient and destination before creating the order.
- Show review, quote expiry, shipping choice, and total changes to the user.
- Never expose a private shipping address to an unrelated purchaser.

## Support

- API documentation: https://sp3nd.shop/partner-api/docs
- Partner dashboard: https://sp3nd.shop/partner-api/dashboard
- Support: support@sp3nd.shop
