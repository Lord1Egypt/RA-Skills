# Stripe API Objects and Workflows

## Read-first safety rules

- Treat any `sk_live_...` secret as highly sensitive.
- Never store live keys in `SKILL.md`, scripts, git-tracked files, or chat transcripts.
- Prefer environment variable `STRIPE_SECRET_KEY`.
- Default to read-only inspection first.
- Ask before any write action that could move money, refund, cancel, or modify billing state.

## Common objects

- `account`: Stripe account identity, business profile, capabilities
- `customers`: people or businesses you bill
- `products`: what you sell
- `prices`: billing terms for products
- `payment_intents`: payment lifecycle state machine
- `charges`: resulting charge records
- `subscriptions`: recurring billing contracts
- `invoices`: billing documents and payment attempts
- `refunds`: money returned to customers
- `disputes`: chargebacks and card disputes
- `payouts`: transfers from Stripe balance to bank
- `balance_transactions`: ledger-style balance events
- `webhook_endpoints`: webhook destinations configured on the account

## Suggested inspection flow

1. Retrieve `/account`
2. List recent `payment_intents`, `charges`, and `invoices`
3. List `products` and `prices`
4. List `subscriptions` if recurring billing matters
5. Inspect `payouts`, `balance_transactions`, and `disputes`
6. Inspect `webhook_endpoints`

## Useful customer search examples

Customer search query language examples:

- `email:'alice@example.com'`
- `name:'Alice Example'`
- `metadata['external_id']:'12345'`

## Write actions to add later carefully

Possible future additions:

- create customer
- create product
- create price
- create refund
- cancel subscription
- create checkout session / payment link

Keep those separate from read-only inspection commands and require explicit user confirmation before use.
