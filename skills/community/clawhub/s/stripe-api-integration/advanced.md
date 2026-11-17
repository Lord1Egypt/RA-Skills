# Advanced Products — Issuing, Terminal, Treasury, Identity, Radar

Issuing (virtual/physical cards), Terminal (POS), Treasury (banking), Identity (verification), Radar (fraud), Financial Connections, Climate, Sigma.

**Read `## Account Context` in `~/Clawic/data/stripe-api-integration/memory.md`** (or its box) first: every product here needs separate activation, most carry their own pricing, and several impose regulatory obligations that are not undoable. None of them is a feature flag.

## Before Enabling Any of These

| Product | What it really commits you to |
|---|---|
| Issuing | You are handing out spending power. Authorization decisions, cardholder disputes, funding the card balance, and program-level obligations |
| Terminal | Physical hardware in physical places: readers, locations, network, staff, and the loss of the "it works on my machine" defence |
| Treasury | Financial accounts on top of a bank partner: KYC, money movement rules, and a compliance surface far beyond payments |
| Identity | Collecting government identity documents — the most sensitive data in this whole skill, with retention rules to match |
| Radar for Fraud Teams | Priced per screened payment; rules you write can block real customers silently |
| Financial Connections | Access to the customer's bank data, with consent and scope obligations |
| Sigma | SQL over your account data; an analysis tool, never part of a request path |

Two rules cut across all of them: **the fee line belongs in `~/Clawic/data/finances/subscriptions.md`** alongside other paid add-ons, so unit economics stay honest; and **the sensitive artifacts these products produce — cardholder data, identity documents, bank credentials — are never written under `~/Clawic/data/`**, only their ids and pointers (`memory-template.md`).

## Radar, Practically

Radar runs on every payment whether or not you pay for the rules engine. The judgment that matters is not which rules exist but how you tune them:

- **Block narrow shapes, not broad categories.** Blocking a country blocks its legitimate customers too; blocking "this BIN range plus this email pattern plus mismatched country" blocks the attack.
- **Review the review queue.** A rule that flags for manual review with nobody reviewing is a rule that silently delays revenue.
- **Measure both errors.** False positives are lost sales that never complain; false negatives are disputes. Only the second is visible by default, which is why teams over-tighten.
- **Allow lists are for known-good customers you keep declining**, and they are a liability if they outlive their reason — date them.
- **A rule set that finally worked belongs in `~/Clawic/data/stripe-api-integration/artifacts/radar-rules.md`** with what it was blocking and what it cost, plus its `## Boxes` line — otherwise the next person re-derives it from disputes.

## Issuing, Practically

Real-time authorization decisions are a webhook with a deadline: the handler approves or declines within a very short window, and a slow handler produces a declined card in someone's hand. Design it as the fastest path in your system, with a safe default when your own systems are unavailable — and decide deliberately whether that default is approve or decline, because both are expensive in different ways.

## Terminal, Practically

Readers are physical assets with locations, network dependencies and firmware. The failure modes are logistical rather than logical: a reader on the wrong location object, a network that blocks the reader's traffic, a firmware update mid-shift. Connection tokens are single-use credentials and never get stored.

---

## Issuing (Create Cards)

### Create Cardholder
```bash
curl https://api.stripe.com/v1/issuing/cardholders \
  -u "$STRIPE_SECRET_KEY:" \
  -d "name=Jenny Rosen" \
  -d "email=jenny@example.com" \
  -d "type=individual" \
  -d "billing[address][line1]=123 Main St" \
  -d "billing[address][city]=San Francisco" \
  -d "billing[address][state]=CA" \
  -d "billing[address][postal_code]=94111" \
  -d "billing[address][country]=US"
```

### Create Virtual Card
```bash
curl https://api.stripe.com/v1/issuing/cards \
  -u "$STRIPE_SECRET_KEY:" \
  -d "cardholder=ich_XXX" \
  -d "currency=usd" \
  -d "type=virtual" \
  -d "spending_controls[spending_limits][0][amount]=50000" \
  -d "spending_controls[spending_limits][0][interval]=monthly"
```

### Create Physical Card
```bash
curl https://api.stripe.com/v1/issuing/cards \
  -u "$STRIPE_SECRET_KEY:" \
  -d "cardholder=ich_XXX" \
  -d "currency=usd" \
  -d "type=physical" \
  -d "shipping[name]=Jenny Rosen" \
  -d "shipping[address][line1]=123 Main St" \
  -d "shipping[address][city]=San Francisco" \
  -d "shipping[address][state]=CA" \
  -d "shipping[address][postal_code]=94111" \
  -d "shipping[address][country]=US"
```

### List Transactions
```bash
curl "https://api.stripe.com/v1/issuing/transactions?card=ic_XXX&limit=10" \
  -u "$STRIPE_SECRET_KEY:"
```

### Approve/Decline Authorization (Real-time)
```python
# Webhook handler for issuing_authorization.request
def handle_authorization(event):
    auth = event['data']['object']
    
    # Your logic here
    if auth['amount'] > 100000:  # Over $1000
        return {"approved": False}
    
    return {"approved": True}
```

---

## Terminal (Point of Sale)

### Create Connection Token
```bash
curl https://api.stripe.com/v1/terminal/connection_tokens \
  -u "$STRIPE_SECRET_KEY:"
```

### Register Reader
```bash
curl https://api.stripe.com/v1/terminal/readers \
  -u "$STRIPE_SECRET_KEY:" \
  -d "registration_code=puppies-plug-could" \
  -d "label=Front Counter" \
  -d "location=tml_XXX"
```

### Create Location
```bash
curl https://api.stripe.com/v1/terminal/locations \
  -u "$STRIPE_SECRET_KEY:" \
  -d "display_name=HQ" \
  -d "address[line1]=123 Main St" \
  -d "address[city]=San Francisco" \
  -d "address[state]=CA" \
  -d "address[postal_code]=94111" \
  -d "address[country]=US"
```

### Process Payment
```bash
# Create PaymentIntent
curl https://api.stripe.com/v1/payment_intents \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=1000" \
  -d "currency=usd" \
  -d "payment_method_types[]=card_present" \
  -d "capture_method=manual"

# Process on reader
curl https://api.stripe.com/v1/terminal/readers/tmr_XXX/process_payment_intent \
  -u "$STRIPE_SECRET_KEY:" \
  -d "payment_intent=pi_XXX"
```

### Simulate Reader (Test Mode)
```bash
curl https://api.stripe.com/v1/test_helpers/terminal/readers/tmr_XXX/present_payment_method \
  -u "$STRIPE_SECRET_KEY:"
```

---

## Treasury (Banking-as-a-Service)

### Create Financial Account
```bash
curl https://api.stripe.com/v1/treasury/financial_accounts \
  -u "$STRIPE_SECRET_KEY:" \
  -d "supported_currencies[]=usd" \
  -d "features[card_issuing][requested]=true" \
  -d "features[deposit_insurance][requested]=true" \
  -d "features[financial_addresses][aba][requested]=true"
```

### Get Balance
```bash
curl https://api.stripe.com/v1/treasury/financial_accounts/fa_XXX \
  -u "$STRIPE_SECRET_KEY:"
```

### Create Outbound Transfer (ACH)
```bash
curl https://api.stripe.com/v1/treasury/outbound_transfers \
  -u "$STRIPE_SECRET_KEY:" \
  -d "financial_account=fa_XXX" \
  -d "amount=10000" \
  -d "currency=usd" \
  -d "destination_payment_method=pm_XXX" \
  -d "description=Vendor payment"
```

### Create Outbound Payment
```bash
curl https://api.stripe.com/v1/treasury/outbound_payments \
  -u "$STRIPE_SECRET_KEY:" \
  -d "financial_account=fa_XXX" \
  -d "amount=5000" \
  -d "currency=usd" \
  -d "customer=cus_XXX" \
  -d "description=Refund"
```

### List Transactions
```bash
curl "https://api.stripe.com/v1/treasury/transactions?financial_account=fa_XXX" \
  -u "$STRIPE_SECRET_KEY:"
```

---

## Identity (Verification)

### Create Verification Session
```bash
curl https://api.stripe.com/v1/identity/verification_sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "type=document" \
  -d "options[document][require_matching_selfie]=true"
```

### Get Verification Result
```bash
curl https://api.stripe.com/v1/identity/verification_sessions/vs_XXX \
  -u "$STRIPE_SECRET_KEY:"
```

### Verification Types
- `document` — ID document verification
- `id_number` — ID number check (SSN, etc.)
- `address` — Address verification

---

## Radar (Fraud Prevention)

### Create Radar Rule
```bash
# Via Dashboard: stripe.com/dashboard/radar/rules
# Rules use Stripe's rule language
```

### Review Payments
```bash
curl "https://api.stripe.com/v1/reviews?limit=10" \
  -u "$STRIPE_SECRET_KEY:"
```

### Approve Review
```bash
curl https://api.stripe.com/v1/reviews/prv_XXX/approve \
  -u "$STRIPE_SECRET_KEY:"
```

### Value Lists (Block/Allow)
```bash
# Create blocklist
curl https://api.stripe.com/v1/radar/value_lists \
  -u "$STRIPE_SECRET_KEY:" \
  -d "alias=blocked_emails" \
  -d "name=Blocked Emails" \
  -d "item_type=email"

# Add item
curl https://api.stripe.com/v1/radar/value_list_items \
  -u "$STRIPE_SECRET_KEY:" \
  -d "value_list=rsl_XXX" \
  -d "value=fraud@example.com"
```

### Early Fraud Warnings
```bash
curl "https://api.stripe.com/v1/radar/early_fraud_warnings?limit=10" \
  -u "$STRIPE_SECRET_KEY:"
```

---

## Financial Connections (Plaid Alternative)

### Create Session
```bash
curl https://api.stripe.com/v1/financial_connections/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "account_holder[type]=customer" \
  -d "account_holder[customer]=cus_XXX" \
  -d "permissions[]=balances" \
  -d "permissions[]=transactions"
```

### List Connected Accounts
```bash
curl "https://api.stripe.com/v1/financial_connections/accounts?account_holder[customer]=cus_XXX" \
  -u "$STRIPE_SECRET_KEY:"
```

### Refresh Balance
```bash
curl https://api.stripe.com/v1/financial_connections/accounts/fca_XXX/refresh \
  -u "$STRIPE_SECRET_KEY:" \
  -d "features[]=balance"
```

---

## Climate (Carbon Removal)

### Create Order
```bash
curl https://api.stripe.com/v1/climate/orders \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=climsku_frontier_offtake_portfolio_2027" \
  -d "metric_tons=1"
```

### List Products
```bash
curl https://api.stripe.com/v1/climate/products \
  -u "$STRIPE_SECRET_KEY:"
```

---

## Sigma (SQL Queries)

### Create Scheduled Query
```bash
curl https://api.stripe.com/v1/sigma/scheduled_query_runs \
  -u "$STRIPE_SECRET_KEY:" \
  -d "query=SELECT * FROM charges WHERE created > date_sub(now(), interval 7 day)"
```

### Get Query Results
```bash
curl https://api.stripe.com/v1/sigma/scheduled_query_runs/sqr_XXX \
  -u "$STRIPE_SECRET_KEY:"
```

---

## ID Prefixes

| Prefix | Resource |
|--------|----------|
| `ich_` | Issuing Cardholder |
| `ic_` | Issuing Card |
| `iauth_` | Issuing Authorization |
| `tml_` | Terminal Location |
| `tmr_` | Terminal Reader |
| `fa_` | Financial Account |
| `vs_` | Verification Session |
| `rsl_` | Radar Value List |
| `fca_` | Financial Connections Account |

---

**Write in the same turn**: enabling any product here goes to `## Account Context` in `~/Clawic/data/stripe-api-integration/memory.md` with the date, and its recurring cost to `~/Clawic/data/finances/subscriptions.md` with the currency. Physical Terminal readers are devices: one row each in `~/Clawic/data/devices/devices.md` (name, model, location, network, `tmr_` reference) — read the file first and update in place if the reader is already there. A Radar rule set that worked, or an Issuing authorization policy, is `artifacts/<name>.md` with its `## Boxes` line; a card or identity incident is a row in `incidents/<year>.md`.
