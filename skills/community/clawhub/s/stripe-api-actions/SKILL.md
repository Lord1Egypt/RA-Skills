---
name: stripe-api-actions
description: Use Stripe's live REST API for authenticated write actions. Use when you need to create or update Stripe customers, products, prices, payment links, refunds, subscriptions, or metadata with a secret key supplied via STRIPE_SECRET_KEY. Keep this separate from read-only inspection when the task changes live billing or payment state.
---

# Stripe API Actions

Use this skill for live Stripe write operations.

## Quick start

1. Set `STRIPE_SECRET_KEY` in the current shell environment.
2. Read `references/actions-and-safety.md` for the supported write actions and example commands.
3. Require `--confirm` on every write command.

## Core workflow

### 1. Confirm scope

Before running a write action, identify exactly which Stripe object should change and what the expected result is.

### 2. Use explicit commands

Examples:

```bash
python skills/stripe-api-actions/scripts/stripe_actions.py create_customer --name "Alice" --email "alice@example.com" --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py create_product --name "Monthly Plan" --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py create_price --product prod_123 --unit-amount 900 --currency eur --interval month --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py create_payment_link --price price_123 --quantity 1 --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py create_refund --payment-intent pi_123 --amount 500 --reason requested_by_customer --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py cancel_subscription sub_123 --invoice-now --prorate --confirm
python skills/stripe-api-actions/scripts/stripe_actions.py update_metadata /customers/cus_123 --metadata external_id=42 --confirm
```

### 3. Prefer narrow changes

Prefer creating or updating the minimum necessary object rather than bundling several unrelated changes into one step.

## Safety rules

- Do not store live Stripe secrets in skill files.
- Require `--confirm` for every write action.
- Be cautious with refunds and subscription cancellation.
- If a task affects live money flow or billing state, double-check the target object IDs first.

## Resources

- `scripts/stripe_actions.py` — minimal authenticated Stripe write helper using Python standard library
- `references/actions-and-safety.md` — supported actions, caveats, and example commands
