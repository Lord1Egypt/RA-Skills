# SaaS Billing System

Complete billing solution for SaaS businesses.

## Features

- **Subscriptions** - Monthly/yearly plans
- **Usage-based billing** - Track metered usage
- **Invoicing** - Auto-generate invoices
- **Payments** - Stripe integration
- **Dunning** - Failed payment recovery
- **Proration** - Plan changes

## Quick Start

```bash
# Initialize billing
./billing.sh init

# Create plan
./billing.sh create-plan basic --price 29 --interval monthly

# Setup Stripe
./billing.sh stripe --key $STRIPE_KEY

# View dashboard
./billing.sh dashboard
```

## Plans

- Free tier
- Monthly/Annual
- Usage-based
- Enterprise

## Integrations

- Stripe
- PayPal
- Square

## Requirements

- Node.js 18+
- Stripe account

## Author

Sunshine-del-ux
