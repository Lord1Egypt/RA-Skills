---
name: stripe-api
description: Use Stripe's live REST API for authenticated account inspection and operational lookup. Use when you need to connect to a Stripe account with a secret key, inspect account details, list customers/products/prices/payments/subscriptions/invoices/refunds/disputes/payouts/webhook endpoints, or retrieve a specific Stripe object safely via read-only commands.
---

# Stripe API

Use this skill for real Stripe API access.

## Quick start

1. Set `STRIPE_SECRET_KEY` in the local shell environment.
2. Start with read-only inspection:
   - `python skills/stripe-api/scripts/stripe_api.py account`
   - `python skills/stripe-api/scripts/stripe_api.py payment_intents --limit 10`
   - `python skills/stripe-api/scripts/stripe_api.py customers --limit 10`
3. Read `references/objects-and-workflows.md` when you need object guidance or a sensible inspection order.

## Core workflow

### 1. Verify access

Run:

```bash
python skills/stripe-api/scripts/stripe_api.py account
```

If this fails with authentication errors, fix the environment variable first.

### 2. Inspect the account safely

Use read-only list commands first:

```bash
python skills/stripe-api/scripts/stripe_api.py products --limit 20
python skills/stripe-api/scripts/stripe_api.py prices --limit 20
python skills/stripe-api/scripts/stripe_api.py payment_intents --limit 20
python skills/stripe-api/scripts/stripe_api.py charges --limit 20
python skills/stripe-api/scripts/stripe_api.py invoices --limit 20
python skills/stripe-api/scripts/stripe_api.py subscriptions --limit 20
python skills/stripe-api/scripts/stripe_api.py payouts --limit 20
python skills/stripe-api/scripts/stripe_api.py disputes --limit 20
python skills/stripe-api/scripts/stripe_api.py webhook_endpoints --limit 20
```

### 3. Retrieve a known object directly

```bash
python skills/stripe-api/scripts/stripe_api.py get /customers/cus_123
python skills/stripe-api/scripts/stripe_api.py get /payment_intents/pi_123
```

### 4. Search customers

```bash
python skills/stripe-api/scripts/stripe_api.py search_customers "email:'alice@example.com'"
```

## Safety rules

- Do not put live secrets in the skill files.
- Do not commit or publish secrets.
- Default to read-only operations.
- Before any write action in the future, confirm with the user.
- Treat secrets shared in chat as compromised and recommend rotation.

## Resources

- `scripts/stripe_api.py` — minimal authenticated Stripe API helper using only Python standard library
- `references/objects-and-workflows.md` — common Stripe objects, safe inspection order, and search examples
