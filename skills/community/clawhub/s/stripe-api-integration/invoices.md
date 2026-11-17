# Invoices, Quotes, and the Billing Portal

**Read `## Account Context` and `tax_handling`** in `~/Clawic/data/stripe-api-integration/memory.md` and `config.yaml` before issuing anything: the entity details and tax registrations are printed on the document, and fixing them afterwards means a credit note.

**Contents:** [Finalization Is the Point of No Return](#finalization-is-the-point-of-no-return) · [Invoices](#invoices) · [Billing Portal](#billing-portal) · [Quotes](#quotes) · [Stripe Tax](#stripe-tax) · [Usage-Based Billing (Meters)](#usage-based-billing-meters) · [Subscription Schedules](#subscription-schedules) · [ID Prefixes Reference](#id-prefixes-reference)

## Finalization Is the Point of No Return

An invoice is a `draft` you can change freely, and then a legal document you cannot.

| State | Editable? | How you leave it |
|---|---|---|
| `draft` | Yes — add, remove, reprice line items | Finalize (automatically ~1 hour after creation for subscription invoices, or explicitly) |
| `open` | No | Paid, voided, or marked uncollectible |
| `paid` | No | Refund the payment and issue a credit note |
| `void` | No | Terminal; the number stays used |
| `uncollectible` | No | An accounting statement, not a deletion |

Consequences: **fix draft invoices, never finalized ones.** After finalization the instrument is a credit note, which is a separate document with its own number, and the tax effect follows the credit note rather than the refund (`tax.md`). Numbering must stay sequential without gaps, which is exactly why voiding is supported and deleting is not.

`collection_method` decides who chases the money: `charge_automatically` charges the saved payment method, `send_invoice` emails a hosted invoice page with `days_until_due` and waits. B2B usually wants the second, and the second means dunning is a human process, not a retry schedule.

## The Billing Portal Replaces Most Support Tickets

A configured portal lets customers update their card, change plan within the options you allow, view invoices and cancel — the four requests that otherwise arrive by email. The configuration is the policy: which plan changes are permitted, whether cancellation is immediate or at period end, whether a cancellation reason is collected. Making cancellation hard here converts churn into disputes, which cost more (`disputes.md`).

## Invoices

### Create Invoice
```bash
curl https://api.stripe.com/v1/invoices \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "auto_advance=false"
```

### Add Invoice Item
```bash
curl https://api.stripe.com/v1/invoiceitems \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "price=price_XXX" \
  -d "invoice=in_XXX"
```

### Finalize Invoice
```bash
curl https://api.stripe.com/v1/invoices/in_XXX/finalize \
  -u "$STRIPE_SECRET_KEY:"
```

### Send Invoice
```bash
curl https://api.stripe.com/v1/invoices/in_XXX/send \
  -u "$STRIPE_SECRET_KEY:"
```

### Pay Invoice
```bash
curl https://api.stripe.com/v1/invoices/in_XXX/pay \
  -u "$STRIPE_SECRET_KEY:"
```

### Void Invoice
```bash
curl https://api.stripe.com/v1/invoices/in_XXX/void \
  -u "$STRIPE_SECRET_KEY:"
```

### Mark Uncollectible
```bash
curl https://api.stripe.com/v1/invoices/in_XXX/mark_uncollectible \
  -u "$STRIPE_SECRET_KEY:"
```

### List Invoices
```bash
curl "https://api.stripe.com/v1/invoices?customer=cus_XXX&status=paid" \
  -u "$STRIPE_SECRET_KEY:"
```

Status: `draft`, `open`, `paid`, `void`, `uncollectible`

---

## Billing Portal

### Create Portal Session
```bash
curl https://api.stripe.com/v1/billing_portal/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "return_url=https://example.com/account"
```

Portal allows customers to:
- Update payment methods
- View invoice history
- Cancel/pause subscriptions
- Download invoices

Configure in Dashboard > Settings > Billing > Customer Portal

---

## Quotes

### Create Quote
```bash
curl https://api.stripe.com/v1/quotes \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "line_items[0][price]=price_XXX" \
  -d "line_items[0][quantity]=1"
```

### Finalize Quote
```bash
curl https://api.stripe.com/v1/quotes/qt_XXX/finalize \
  -u "$STRIPE_SECRET_KEY:"
```

### Accept Quote
```bash
curl https://api.stripe.com/v1/quotes/qt_XXX/accept \
  -u "$STRIPE_SECRET_KEY:"
```

---

## Stripe Tax

### Create Tax Calculation
```bash
curl https://api.stripe.com/v1/tax/calculations \
  -u "$STRIPE_SECRET_KEY:" \
  -d "currency=usd" \
  -d "line_items[0][amount]=1000" \
  -d "line_items[0][reference]=L1" \
  -d "customer_details[address][country]=US" \
  -d "customer_details[address][state]=CA"
```

### Enable Tax on Checkout
```bash
curl https://api.stripe.com/v1/checkout/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "mode=payment" \
  -d "automatic_tax[enabled]=true" \
  -d "line_items[0][price]=price_XXX" \
  -d "line_items[0][quantity]=1" \
  -d "success_url=https://example.com/success" \
  -d "cancel_url=https://example.com/cancel"
```

---

## Usage-Based Billing (Meters)

### Create Meter
```bash
curl https://api.stripe.com/v1/billing/meters \
  -u "$STRIPE_SECRET_KEY:" \
  -d "display_name=API Calls" \
  -d "event_name=api_call" \
  -d "default_aggregation[formula]=sum"
```

### Report Usage Event
```bash
curl https://api.stripe.com/v1/billing/meter_events \
  -u "$STRIPE_SECRET_KEY:" \
  -d "event_name=api_call" \
  -d "payload[stripe_customer_id]=cus_XXX" \
  -d "payload[value]=100"
```

### Create Metered Price
```bash
curl https://api.stripe.com/v1/prices \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=prod_XXX" \
  -d "currency=usd" \
  -d "recurring[interval]=month" \
  -d "recurring[usage_type]=metered" \
  -d "recurring[meter]=mtr_XXX" \
  -d "unit_amount=1"
```

---

## Subscription Schedules

### Create Schedule (Future Start)
```bash
curl https://api.stripe.com/v1/subscription_schedules \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "start_date=$(date -d '+7 days' +%s)" \
  -d "end_behavior=release" \
  -d "phases[0][items][0][price]=price_XXX" \
  -d "phases[0][iterations]=1"
```

### Schedule Upgrade
```bash
curl https://api.stripe.com/v1/subscription_schedules \
  -u "$STRIPE_SECRET_KEY:" \
  -d "from_subscription=sub_XXX" \
  -d "phases[0][items][0][price]=price_BASIC" \
  -d "phases[0][iterations]=3" \
  -d "phases[1][items][0][price]=price_PRO" \
  -d "phases[1][iterations]=12"
```

---

## ID Prefixes Reference

| Prefix | Resource |
|--------|----------|
| `in_` | Invoice |
| `ii_` | Invoice Item |
| `qt_` | Quote |
| `sub_sched_` | Subscription Schedule |
| `mtr_` | Meter |

---

**Write in the same turn**: invoice numbering conventions, `collection_method` per customer type and the portal policy go to `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md` (or under `conventions` in `config.yaml` when the user states them as rules). A client you invoice is a person: their record goes to `~/Clawic/data/contacts/contacts.md` and is referenced here by name only. A quote template or a collections procedure worth reusing is `artifacts/<name>.md` with its `## Boxes` line.
