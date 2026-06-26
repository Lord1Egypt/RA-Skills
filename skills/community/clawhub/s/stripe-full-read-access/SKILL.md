---
name: stripe-full-read-access
description: Access Stripe directly with a Stripe secret or restricted API key for broad read-only platform queries, especially Connect accounts, application fees, balances, charges, customers, invoices, subscriptions, payouts, transfers, and balance transactions. Use when users want direct Stripe platform analytics or connected-account reporting without an intermediary gateway.
---

# Stripe Full Read Access

Use direct Stripe API access with a locally stored Stripe API key.

## Requirements

- Stripe API key stored locally, outside git
- Prefer a platform-level key when querying Connect accounts or application fees
- Use this skill for read-oriented Stripe analysis and reporting

Local key path used in this workspace:
- `/home/clawd/.config/stripe/api_key`

## Authentication

```text
Authorization: Bearer $STRIPE_API_KEY
```

Example shell setup:

```bash
export STRIPE_API_KEY="$(cat /home/clawd/.config/stripe/api_key)"
```

## Base URL

```text
https://api.stripe.com/v1/
```

## Quick checks

### Get platform account

```bash
curl -sS https://api.stripe.com/v1/account \
  -H "Authorization: Bearer $(cat /home/clawd/.config/stripe/api_key)"
```

### List connected accounts

```bash
curl -sS 'https://api.stripe.com/v1/accounts?limit=10' \
  -H "Authorization: Bearer $(cat /home/clawd/.config/stripe/api_key)"
```

### Get balance

```bash
curl -sS https://api.stripe.com/v1/balance \
  -H "Authorization: Bearer $(cat /home/clawd/.config/stripe/api_key)"
```

## Common endpoints

- Account: `/v1/account`
- Balance: `/v1/balance`
- Connected accounts: `/v1/accounts`
- Charges: `/v1/charges`
- Customers: `/v1/customers`
- Payment intents: `/v1/payment_intents`
- Payouts: `/v1/payouts`
- Invoices: `/v1/invoices`
- Subscriptions: `/v1/subscriptions`
- Balance transactions: `/v1/balance_transactions`
- Application fees: `/v1/application_fees`
- Transfers: `/v1/transfers`

## Useful patterns

### Count connected accounts

Use pagination until `has_more` is false.

```bash
python3 - <<'PY'
import json, urllib.request, urllib.parse
from pathlib import Path
key = Path('/home/clawd/.config/stripe/api_key').read_text().strip()
count = 0
starting_after = None
while True:
    params = {'limit': 100}
    if starting_after:
        params['starting_after'] = starting_after
    req = urllib.request.Request('https://api.stripe.com/v1/accounts?' + urllib.parse.urlencode(params))
    req.add_header('Authorization', f'Bearer {key}')
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    items = data.get('data', [])
    count += len(items)
    if not data.get('has_more') or not items:
        print(count)
        break
    starting_after = items[-1]['id']
PY
```

### List recent application fees

```bash
curl -sS 'https://api.stripe.com/v1/application_fees?limit=10' \
  -H "Authorization: Bearer $(cat /home/clawd/.config/stripe/api_key)"
```

### List recent payouts

```bash
curl -sS 'https://api.stripe.com/v1/payouts?limit=10' \
  -H "Authorization: Bearer $(cat /home/clawd/.config/stripe/api_key)"
```

### List recent charges

```bash
curl -sS 'https://api.stripe.com/v1/charges?limit=10' \
  -H "Authorization: Bearer $(cat /home/clawd/.config/stripe/api_key)"
```

## Connect notes

- Use direct Stripe auth for platform-level Connect reporting.
- This setup can access `/v1/accounts`, which confirms platform visibility.
- For fee-revenue questions, inspect `application_fees`, `balance_transactions`, and `transfers` together.
- Some money fields are integer minor units. For GBP, divide by 100.
- Be explicit about whether figures are gross charges, application fees, net balance movement, pending, or available.

## Safety

- Never commit Stripe API keys.
- Never write Stripe API keys into memory files.
- Prefer read-only analysis unless the user explicitly asks for writes.
- Be careful with endpoints that can create refunds, payouts, transfers, or account changes.
