# Stripe API Actions and Safety

## Purpose

Use this skill for authenticated write actions against Stripe.

## Secret handling

- Read `STRIPE_SECRET_KEY` from the environment.
- Never hardcode live keys in skill files.
- Treat keys shared in chat as compromised and rotate them.

## Supported write actions

- create customer
- update customer
- create product
- create price
- create payment link
- create refund
- cancel subscription
- update metadata on supported objects

## Safety pattern

- Require `--confirm` for every write action.
- Preview the exact command before running it when possible.
- Be extra careful with refunds and subscription cancellation.
- Prefer metadata updates over destructive changes when that solves the need.

## Important notes

- `unit_amount` values are in the smallest currency unit, e.g. cents for EUR/USD.
- `create_price` becomes recurring only when `--interval` is supplied.
- `create_refund` can accept either a payment intent or a charge.
- `cancel_subscription` is immediate cancellation via Stripe API delete semantics.

## Example commands

```bash
python skills/stripe-api-actions/scripts/stripe_actions.py create_customer --name "Alice" --email "alice@example.com" --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py create_product --name "Monthly Plan" --description "Recurring support plan" --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py create_price --product prod_123 --unit-amount 900 --currency eur --interval month --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py create_payment_link --price price_123 --quantity 1 --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py update_metadata /customers/cus_123 --metadata external_id=42 --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py create_refund --payment-intent pi_123 --amount 500 --reason requested_by_customer --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py cancel_subscription sub_123 --invoice-now --prorate --confirm
```
