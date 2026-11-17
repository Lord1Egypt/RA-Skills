# Collector Crypt checkout

Use this flow when the user supplies a Collector Crypt card link or asks to find and buy a tokenized card. SP3ND fetches the live listing, accepts the customer's USDC payment, and then manually purchases and transfers the NFT. The agent handles checkout and status tracking; SP3ND staff handle acquisition, transfer, review, and refunds.

## Contents

- [Requirements](#requirements)
- [Optional card discovery](#optional-card-discovery)
- [Quote the exact card](#quote-the-exact-card)
- [Create the wallet-delivery order](#create-the-wallet-delivery-order)
- [Prepare, sign, and submit payment](#prepare-sign-and-submit-payment)
- [Payment retries and expiry](#payment-retries-and-expiry)
- [Track manual wallet delivery](#track-manual-wallet-delivery)

## Requirements

Base URL: `https://us-central1-sp3nddotshop-prod.cloudfunctions.net`.

Send `X-API-Key` and `X-API-Secret` on every request below, and `Content-Type: application/json` on POST requests. Normal approved Partner/agent credentials work without a separate Collector Crypt opt-in. Keep credentials server-side. `getAgentStatus.agent.collector_crypt_enabled` is a discovery capability, not a flag the caller must enable.

- Accept only canonical card links shaped as `https://collectorcrypt.com/assets/solana/<asset-address>`. The server validates the Solana address and current listing.
- The eligible asset must be a native-Solana Collector Crypt V2 buy-now listing priced in USDC. Supported standards are `Pnft`, `Cnft`, `StandardNft`, and `CoreNft`; not every Collector Crypt page or card is purchasable.
- One card per cart and order, quantity `1`; no mixed carts or shipping address.
- `user_wallet`, `asset_recipient_wallet`, and payment `payer_address` must all be the same valid, on-curve Solana wallet. If an agent pays from its own funded wallet, that wallet receives the NFT. If delivery is intended for another person's wallet, that wallet must authorize the payment. Do not promise gifting or silently substitute the agent's wallet.
- Only `partnerPayment` prepare/submit supports payment for real cards. Neither `payAgentOrder` nor `createPartnerTransaction` is a fallback; both return `COLLECTOR_CRYPT_PAYMENT_METHOD_UNSUPPORTED`.

## Optional card discovery

Skip search when the user already supplied the exact card URL.

```http
GET /searchCollectorCryptCards?q=charizard%20psa%2010&limit=20
```

Read `items` and the opaque `next_cursor` from the response. To fetch another page, URL-encode the cursor unchanged in the `cursor` query parameter. Each card includes `product_url`, `nft_address`, `price`, `currency`, and listing metadata. Search does not reserve a listing. Insured value, catalog counts, and search prices are informational; the cart request refetches the exact card and establishes pricing.

## Quote the exact card

```http
POST /createPartnerCart

{
  "items": [{
    "product_url": "https://collectorcrypt.com/assets/solana/<asset-address>",
    "quantity": 1
  }],
  "user_wallet": "<buyer-wallet>"
}
```

Read `cart.cart_id`, the server-resolved item, totals, and expiry. Do not submit a caller-selected price, seller, receipt, or listing metadata as payment authority. Alternatively, the item may contain `provider: "collectorcrypt"` and `nft_address` instead of `product_url`.

The card quote expires after five minutes. SP3ND may prevent competing SP3ND checkouts, but this does not reserve the listing on Collector Crypt. A changed or sold listing must be repriced or handled by SP3ND; never select a substitute card without a new user-authorized purchase.

## Create the wallet-delivery order

Persist one stable idempotency key for this intended purchase before sending the request. Preserve it on retries.

```http
POST /createPartnerOrder
Idempotency-Key: <stable-checkout-key>

{
  "cart_id": "<cart.cart_id>",
  "customer_email": "buyer@example.com",
  "user_wallet": "<buyer-wallet>",
  "asset_recipient_wallet": "<same-buyer-wallet>"
}
```

Omit `shipping_address`. The recipient is frozen into the order. A different buyer/recipient returns `ASSET_RECIPIENT_WALLET_MISMATCH`; stop and correct the intended checkout before payment rather than changing a paid order.

The returned `order` identifies the `order_id`, `order_number`, exact total, `quote_expires_at`, and `payment_ready`. Card metadata includes:

```json
{
  "order_type": "collector_crypt_card",
  "fulfillment_type": "wallet_delivery",
  "fulfillment_provider": "collectorcrypt",
  "fulfillment_mode": "manual",
  "requires_manual_fulfillment": true,
  "fulfillment_status": "awaiting_payment"
}
```

Confirm the exact card, total, and delivery wallet with the user's purchase intent or existing spending authorization. Read the order again immediately before payment; require `payment_ready === true` and an unexpired quote. If the quote expired before any payment submission, obtain a fresh quote/order. For this new quoted checkout, persist a new idempotency key; retrying the old key returns the original order, not a repriced replacement. Preserve the old key for retries of the old request. First verify that the old order has no confirmed or unresolved payment and stop using any prior signed authorization. If a payment was already prepared, the server may keep the listing claim until its blockhash expires; respect `COLLECTOR_CRYPT_LISTING_RESERVED` and wait or request support rather than bypassing it. Reconfirm a changed total against the user's authorization. Never start a replacement checkout while an earlier payment has an unknown outcome.

## Prepare, sign, and submit payment

Prepare a payment for the canonical order ID:

```http
POST /partnerPayment

{
  "action": "prepare",
  "order_id": "<order_id>",
  "payer_address": "<buyer-wallet>"
}
```

A new prepare returns HTTP `201` with `status: "payment_prepared"`. An unchanged still-valid replay returns HTTP `200` with `idempotent_replay: true` and the same transaction. `already_paid` means read the order and track fulfillment; do not sign another payment.

The prepare response supplies `order_id`, `order_number`, `amount`, `currency`, `network`, `payer_address`, `recipient_address`, `token_mint`, `token_decimals`, string `amount_atomic`, `memo`, `unsigned_transaction_base64`, `recent_blockhash`, and `last_valid_block_height`.

Before signing:

1. Match the returned order and payer to the approved order, total, and buyer wallet. Require `currency: "USDC"`, `network: "solana-mainnet"`, six token decimals, and USDC mint `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`. Validate the exact atomic amount without floating-point rounding.
2. Verify the payment recipient is SP3ND's treasury wallet `2nkTRv3qxk7n2eYYjFAndReVXaV7sTF3Z9pNimvp5jcp`. This receives the USDC; it is distinct from the buyer's NFT delivery wallet.
3. Decode the server-issued legacy Solana transaction and verify its message against those fields: the buyer is the fee payer and sole required signer; the exact USDC `TransferChecked` moves the approved amount from the buyer's canonical USDC token account to the treasury's canonical USDC token account; the memo and recent blockhash match. Reject additional or changed instructions. The current transaction contains the transfer and memo only.
4. Confirm the authorization is still valid against `last_valid_block_height`. The buyer needs USDC and enough SOL for network fees. Have the authorized buyer signer sign the exact returned transaction, preserving every message byte. Do not rebuild it, replace the blockhash, add instructions, or use the x402 script.

Persist the exact signed base64 serialization with the order ID before submission. Keep wallet private keys in the signer; send only the signed transaction to SP3ND:

```http
POST /partnerPayment

{
  "action": "submit",
  "order_id": "<order_id>",
  "signed_transaction_base64": "<exact-signed-serialization>"
}
```

SP3ND validates and broadcasts the transaction. Do not broadcast it separately to an RPC endpoint or wrap it in a `PAYMENT-SIGNATURE` header.

A new submission normally returns HTTP `202`, `status: "verifying_payment"`, order identifiers, and `transaction_signature`. Replays and `already_paid` may return HTTP `200`. A signature or `verifying_payment` response is not confirmed payment; poll the order. This payment charges the customer for the SP3ND order; it does not buy the card from Collector Crypt automatically.

## Payment retries and expiry

These rules apply to `partnerPayment`, not to the separate x402 reference:

- After a submit timeout or unreadable response, preserve the original signed bytes and read the order first. If it has reached `Paid`, `Ordered`, or `Delivered`, track fulfillment instead of resubmitting. If the result remains unresolved, retry only the identical `signed_transaction_base64` for the same order; that call lets SP3ND reconcile the exact payment.
- `PAYMENT_BROADCAST_UNKNOWN`, `PAYMENT_STATUS_UNAVAILABLE`, and `PAYMENT_RECONCILIATION_PENDING` with `retryable: true` permit the same exact-byte retry after reading the order. Back off between retries. An explicit `retryable: false`, a terminal unsuccessful order, or `review_required` means stop automatic retries and report the server state to SP3ND for review. Limit automatic retries to a short bounded window (for example, 60 seconds), then retain the order/signature and report that payment remains unresolved.
- Never rebuild, re-sign, switch payment endpoints, or prepare another authorization while the earlier result is unknown. Blockhash expiry or elapsed time alone does not prove that the payment failed.
- Only an explicit `partnerPayment` submit response with `payment_released: true` (for example, `PAYMENT_TRANSACTION_EXPIRED` or `PAYMENT_TRANSACTION_FAILED`) establishes that an ambiguous prior authorization was reconciled and released. Then refresh the order and its quote before preparing again; an expired card quote may require a fresh checkout using the key lifecycle above.
- If prepare returns `PAYMENT_TRANSACTION_NEAR_EXPIRY` before signing/submitting, do not sign it. Wait until the returned `last_valid_block_height` passes, then refresh and prepare again if the order remains payable. This rule does not authorize replacing an uncertain submitted payment.
- `COLLECTOR_CRYPT_LISTING_CHANGED`, `COLLECTOR_CRYPT_LISTING_RESERVED`, or quote expiry mean refresh/requote when there is no unresolved payment. Do not bypass the error by changing the amount, asset, or wallet.
- Once payment is confirmed, continue tracking that order. Never charge again because manual fulfillment is still pending.

## Track manual wallet delivery

```http
GET /getPartnerOrder?order_id=<url-encoded-order-id>
```

| Order / fulfillment state | Meaning and next step |
|---|---|
| `Paid` / `pending_acquisition` | SP3ND received payment; staff still need to purchase the exact card. Continue polling. |
| `Ordered` / `pending_delivery` | Staff recorded acquisition; transfer to the buyer is still pending. Continue polling. |
| `Delivered` / `delivered`, with `asset_transfer_signature` | SP3ND recorded wallet delivery. Report completion and the transfer reference. |
| `review_required` or an unsuccessful terminal order state | Report the state; SP3ND handles review, reconciliation, or refund. Do not purchase a replacement or retry payment. |

Do not equate `Paid`, a queued job, or `provider_purchase_signature` with NFT delivery. SP3ND records confirmed transaction references and operator attestations, and verifies current asset ownership before recording delivery. If the listing sells or changes before acquisition, fulfillment may require review and a refund.
