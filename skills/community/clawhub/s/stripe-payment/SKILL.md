# SKILL.md — Stripe Payment Integration

## Metadata

**Name:** stripe-payment
**Description:** Enables AI assistants to interact with the Stripe payment platform — manage customers, payments, subscriptions, invoices, refunds, and balance queries via the Stripe REST API.
**Language:** English
**Version:** 1.0.0
**Author:** OpenClaw / CCD
**Platform:** OpenClaw (ClawHub compatible)

---

## Trigger Phrases

Users activate this skill with natural English sentences such as:

1. "Create a Stripe customer for me"
2. "Set up a new customer in Stripe"
3. "I need to charge someone $50 via Stripe"
4. "Create a payment intent for $100"
5. "Start a monthly subscription for a customer"
6. "Look up my Stripe balance"
7. "Show me recent failed payments"
8. "Get the invoice history for customer@example.com"
9. "Issue a refund for payment pi_123456"
10. "Update a customer's email in Stripe"
11. "Find a payment by its ID"
12. "Check my available Stripe balance"
13. "List all recent Stripe transactions"
14. "Cancel a subscription in Stripe"
15. "How much do I have in my Stripe account?"

---

## Capabilities

This skill covers the following Stripe operations:

1. **Customer Management** — Create, retrieve, update, list, and delete customers
2. **Payment Intents** — Create, confirm, capture, cancel, and retrieve one-time payment intents
3. **Subscriptions** — Create, update, pause, resume, and cancel recurring subscriptions
4. **Invoices** — List and retrieve invoices for customers
5. **Refunds** — Issue full or partial refunds by charge/payment intent ID
6. **Balance & Transactions** — Retrieve Stripe balance and list balance transactions
7. **Payment Lookup** — Retrieve a charge or payment intent by ID; list recent payments
8. **Webhook Signature Verification** — Verify incoming webhook payloads (advanced)
9. **Test Mode Awareness** — Use `sk_test_` keys safely without live data impact

---

## Prerequisites

### Required Configuration

Before using this skill, the user must provide:

| Item | Description | Format |
|------|-------------|--------|
| `STRIPE_SECRET_KEY` | Stripe Secret API key (server-side only) | `sk_test_...` or `sk_live_...` |
| `STRIPE_WEBHOOK_SECRET` | Webhook signing secret (`whsec_...`) | Only for webhook verification |
| `CURRENCY` | Default currency for charges (optional, defaults to `usd`) | ISO 4217 e.g., `usd`, `eur` |

### Recommended: Restricted Key

For production, prefer a **Restricted Key** (`rk_live_...`) with minimum required permissions:

- `customers`: Read/Write
- `payment_intents`: Read/Write
- `subscriptions`: Read/Write
- `invoices`: Read
- `refunds`: Write
- `balance`: Read

> ⚠️ **Never expose Secret Keys client-side.** This skill operates server-side via `exec` calls to `curl` or Stripe SDK commands.

### Environment Setup

The skill expects environment variables or a `.env` file:

```bash
export STRIPE_SECRET_KEY="***"
export STRIPE_WEBHOOK_SECRET="***"
export STRIPE_CURRENCY="usd"
```

---

## Detailed Steps

### 1. Create a Customer

**Purpose:** Register a new customer in Stripe before charging them.

**API:** `POST /v1/customers`
**Auth:** `Authorization: Bearer {STRIPE_SECRET_KEY}`

**curl:**
```bash
curl https://api.stripe.com/v1/customers \
  -u "${STRIPE_SECRET_KEY}:" \
  -d email="alice@example.com" \
  -d name="Alice Smith" \
  -d metadata[user_id]="12345"
```

**Stripe SDK (Node.js):**
```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const customer = await stripe.customers.create({
  email: 'alice@example.com',
  name: 'Alice Smith',
  metadata: { user_id: '12345' }
});

console.log(customer.id); // cus_xxx
```

**Stripe SDK (Python):**
```python
import stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

customer = stripe.Customer.create(
    email='alice@example.com',
    name='Alice Smith',
    metadata={'user_id': '12345'}
)
print(customer.id)  # cus_xxx
```

**Response fields to extract:**
- `id` — Customer ID (e.g., `cus_NqM7xK9vL2`)
- `email`, `name`, `metadata`
- `created` — Unix timestamp

---

### 2. Create a Payment Intent (One-Time Charge)

**Purpose:** Initiate a one-time payment. Returns a `client_secret` for frontend collection.

**API:** `POST /v1/payment_intents`
**Auth:** `Authorization: Bearer {STRIPE_SECRET_KEY}`

**curl:**
```bash
curl https://api.stripe.com/v1/payment_intents \
  -u "${STRIPE_SECRET_KEY}:" \
  -d amount=5000 \
  -d currency="usd" \
  -d customer="cus_NqM7xK9vL2" \
  -d metadata[order_id]="order_789"
```

> Note: `amount` is in **smallest currency unit** (cents for USD). $50.00 = `5000`.

**Stripe SDK (Node.js):**
```javascript
const paymentIntent = await stripe.paymentIntents.create({
  amount: 5000,
  currency: 'usd',
  customer: 'cus_NqM7xK9vL2',
  metadata: { order_id: 'order_789' }
});

console.log(paymentIntent.client_secret);
// Send client_secret to frontend to complete payment with Stripe.js
```

**Key statuses:** `requires_payment_method`, `requires_confirmation`, `requires_action`, `processing`, `succeeded`, `canceled`

---

### 3. Confirm a Payment Intent

**Purpose:** Confirm that a payment has been authorized.

**API:** `POST /v1/payment_intents/{id}/confirm`

**curl:**
```bash
curl https://api.stripe.com/v1/payment_intents/pi_3Qx9vL2eZvKYlo2C/confirm \
  -u "${STRIPE_SECRET_KEY}:" \
  -d payment_method="pm_card_visa"
```

---

### 4. Capture a Payment Intent

**Purpose:** Capture funds that were previously authorized (for manual capture workflows).

**API:** `POST /v1/payment_intents/{id}/capture`

**curl:**
```bash
curl https://api.stripe.com/v1/payment_intents/pi_3Qx9vL2eZvKYlo2C/capture \
  -u "${STRIPE_SECRET_KEY}:"
```

> Note: uncaptured PaymentIntents expire after 7 days.

---

### 5. Create a Subscription

**Purpose:** Set up recurring billing for a customer.

**API:** `POST /v1/subscriptions`
**Auth:** `Authorization: Bearer {STRIPE_SECRET_KEY}`

**Prerequisites:**
- A Price/Product must exist in Stripe (create via Dashboard or API)
- A customer ID

**curl:**
```bash
curl https://api.stripe.com/v1/subscriptions \
  -u "${STRIPE_SECRET_KEY}:" \
  -d customer="cus_NqM7xK9vL2" \
  -d items[0][price]="price_1Qx9vL2eZvKYlo2C1234"
```

**Stripe SDK (Node.js):**
```javascript
const subscription = await stripe.subscriptions.create({
  customer: 'cus_NqM7xK9vL2',
  items: [{ price: 'price_1Qx9vL2eZvKYlo2C1234' }],
  payment_behavior: 'default_incomplete',
  expand: ['latest_invoice.payment_intent']
});

console.log(subscription.id); // sub_xxx
const clientSecret = subscription.latest_invoice.payment_intent.client_secret;
```

**Key subscription statuses:** `trialing`, `active`, `past_due`, `canceled`, `paused`

**Common subscription parameters:**
- `billing_cycle_anchor` — manually set billing date
- `trial_period_days` — start with a free trial
- `cancel_at_period_end` — don't renew, cancel at period end

---

### 6. Cancel a Subscription

**API:** `DELETE /v1/subscriptions/{id}`

**curl:**
```bash
curl https://api.stripe.com/v1/subscriptions/sub_3Qx9vL2eZvKYlo2C \
  -u "${STRIPE_SECRET_KEY}:" \
  -X DELETE
```

**To cancel at period end (not immediately):**
```bash
curl https://api.stripe.com/v1/subscriptions/sub_3Qx9vL2eZvKYlo2C \
  -u "${STRIPE_SECRET_KEY}:" \
  -d cancel_at_period_end=true
```

---

### 7. Get Invoice History

**API:** `GET /v1/invoices` (with optional `customer` filter)
**Auth:** `Authorization: Bearer {STRIPE_SECRET_KEY}`

**curl:**
```bash
# All invoices
curl "https://api.stripe.com/v1/invoices?limit=10" \
  -u "${STRIPE_SECRET_KEY}:"

# Invoices for a specific customer
curl "https://api.stripe.com/v1/invoices?customer=cus_NqM7xK9vL2&limit=10" \
  -u "${STRIPE_SECRET_KEY}:"
```

**Stripe SDK (Node.js):**
```javascript
const invoices = await stripe.invoices.list({
  customer: 'cus_NqM7xK9vL2',
  limit: 10
});

for (const invoice of invoices.data) {
  console.log(`${invoice.id} — ${invoice.amount_paid / 100} ${invoice.currency} — ${invoice.status}`);
}
```

**Key invoice fields:** `id`, `customer`, `amount_due`, `amount_paid`, `status`, `due_date`, `period_start`, `period_end`, `invoice_pdf`

---

### 8. Issue a Refund

**API:** `POST /v1/refunds`
**Auth:** `Authorization: Bearer {STRIPE_SECRET_KEY}`

**Full refund by charge ID:**
```bash
curl https://api.stripe.com/v1/refunds \
  -u "${STRIPE_SECRET_KEY}:" \
  -d charge="ch_3Qx9vL2eZvKYlo2C1234"
```

**Partial refund by payment intent ID:**
```bash
curl https://api.stripe.com/v1/refunds \
  -u "${STRIPE_SECRET_KEY}:" \
  -d payment_intent="pi_3Qx9vL2eZvKYlo2C" \
  -d amount=2500  # partial amount in cents
```

**Refund statuses:** `pending`, `succeeded`, `failed`, `canceled`

---

### 9. Check Balance

**API:** `GET /v1/balance`
**Auth:** `Authorization: Bearer {STRIPE_SECRET_KEY}`

**curl:**
```bash
curl https://api.stripe.com/v1/balance \
  -u "${STRIPE_SECRET_KEY}:"
```

**Stripe SDK (Node.js):**
```javascript
const balance = await stripe.balance.retrieve();
console.log(`Available: ${balance.available[0].amount / 100} ${balance.available[0].currency}`);
console.log(`Pending:   ${balance.pending[0].amount / 100} ${balance.pending[0].currency}`);
```

**Response includes:**
- `available` — funds ready to pay out
- `pending` — funds not yet available
- Each with `amount`, `currency`, `source` breakdown

---

### 10. List Recent Payments

**API:** `GET /v1/charges`
**Auth:** `Authorization: Bearer {STRIPE_SECRET_KEY}`

**curl:**
```bash
curl "https://api.stripe.com/v1/charges?limit=20&expand[]=data.payment_intent" \
  -u "${STRIPE_SECRET_KEY}:"
```

**Stripe SDK (Node.js):**
```javascript
const charges = await stripe.charges.list({ limit: 20 });

for (const charge of charges.data) {
  const emoji = charge.paid ? '✅' : '❌';
  console.log(`${emoji} ${charge.id} — ${charge.amount / 100} ${charge.currency} — ${charge.description || 'no description'}`);
}
```

---

### 11. Get Payment by ID

**API:** `GET /v1/payment_intents/{id}`
**Auth:** `Authorization: Bearer {STRIPE_SECRET_KEY}`

**curl:**
```bash
curl "https://api.stripe.com/v1/payment_intents/pi_3Qx9vL2eZvKYlo2C" \
  -u "${STRIPE_SECRET_KEY}:"
```

**Stripe SDK (Node.js):**
```javascript
const pi = await stripe.paymentIntents.retrieve('pi_3Qx9vL2eZvKYlo2C');
console.log(`Status: ${pi.status}`);
console.log(`Amount: ${pi.amount / 100} ${pi.currency}`);
console.log(`Customer: ${pi.customer}`);
```

---

### 12. Webhook Signature Verification (Advanced)

**Purpose:** Verify that incoming webhook requests are genuinely from Stripe.

**Concept:** Stripe signs every webhook with `Stripe-Signature` header using HMAC-SHA256 and your `STRIPE_WEBHOOK_SECRET` (`whsec_...`).

**Node.js verification example:**
```javascript
const express = require('express');
const app = express();
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

app.post('/webhook/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    console.error(`Webhook signature verification failed: ${err.message}`);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Handle event
  switch (event.type) {
    case 'payment_intent.succeeded':
      const pi = event.data.object;
      console.log(`PaymentIntent succeeded: ${pi.id}`);
      break;
    case 'customer.subscription.created':
      console.log('New subscription created');
      break;
  }

  res.json({ received: true });
});
```

**Important:** Use `express.raw()` for the webhook route — not `express.json()` — because Stripe sends raw body for signature verification.

---

## Output Format

### Success — Customer Created

```
✅ Customer created in Stripe
🆔 Customer ID: cus_NqM7xK9vL2
📧 Email: alice@example.com
👤 Name: Alice Smith
🏷️ Metadata: { user_id: "12345" }
🕐 Created: 2026-07-04 12:58:00 UTC
```

### Success — Payment Intent Created

```
✅ Payment Intent created
🆔 ID: pi_3Qx9vL2eZvKYlo2C
💵 Amount: $50.00 USD
📊 Status: requires_confirmation
🔑 Client Secret: pi_3Qx9vL2eZvKYlo2C_secret_xxxxx
👤 Customer: cus_NqM7xK9vL2
ℹ️ Next step: Confirm this Payment Intent with Stripe.js on your frontend
```

### Success — Subscription Created

```
✅ Subscription created
🆔 Subscription ID: sub_3Qx9vL2eZvKYlo2C
👤 Customer: cus_NqM7xK9vL2
💰 Price: $29.00/month
📊 Status: active
🗓️ Current period: 2026-07-04 → 2026-08-04
```

### Success — Refund Issued

```
✅ Refund issued
🆔 Refund ID: re_3Qx9vL2eZvKYlo2C
💵 Amount refunded: $25.00 USD
🔗 Charge ID: ch_3Qx9vL2eZvKYlo2C1234
📊 Status: succeeded
```

### Success — Balance Check

```
✅ Stripe Balance
💰 Available: $1,234.56 USD
⏳ Pending: $567.89 USD
📅 Updated: 2026-07-04 12:58:00 UTC
```

### Error — No Such Customer

```
❌ Failed to retrieve customer
Reason: No such customer: cus_nonexistent
Fix: Verify the customer ID is correct and belongs to your Stripe account
```

### Error — Insufficient Funds (in test mode)

```
❌ Payment failed
Reason: Your card was declined. (In test mode, use card 4000000000000002 to trigger insufficient_funds)
Fix: Use Stripe test card 4000000000000002 to simulate this scenario
```

---

## Example Conversations

### Example 1: Create Customer and Start Subscription

**User:** "I need to set up a new customer and start them on the $29/month plan"

**AI:** "Sure, creating the customer and subscription now..."

**Execute:**
1. Create customer with email/name from user's request
2. Create subscription using price ID `price_1Qx9vL2eZvKYlo2C1234`
3. Return subscription details

**AI:** "✅ All set!
👤 Customer: Alice Smith (cus_NqM7xK9vL2)
💰 Subscription: $29.00/month
📊 Status: active
🗓️ Next billing: 2026-08-04"

---

### Example 2: Check Balance and List Recent Failed Payments

**User:** "Show me my Stripe balance and any failed payments in the last 7 days"

**AI:** "Checking your balance and payment status..."

**Execute:**
1. GET `/v1/balance`
2. GET `/v1/charges?limit=100` and filter for `paid: false`

**AI:** "✅ Stripe Account Status
💰 Available: $1,234.56 USD
⏳ Pending: $567.89 USD

❌ Failed Payments (3 found):
- pi_3Qx9vL2eZvKYlo2C — $89.00 — insufficient_funds — 2026-07-03
- ch_3Qx9vL2eZvKYlo2C1234 — $45.00 — card_declined — 2026-07-01
- pi_3Qx9vL2eZvKYlo2C5678 — $120.00 — expired_card — 2026-06-29"

---

### Example 3: Issue a Partial Refund

**User:** "Issue a $15 refund for order pi_3Qx9vL2eZvKYlo2C — the customer only received part of their order"

**AI:** "Processing a $15.00 partial refund for that payment intent..."

**Execute:**
1. POST `/v1/refunds` with `payment_intent=pi_...` and `amount=1500`

**AI:** "✅ Partial refund issued
💵 Amount refunded: $15.00 USD
🔗 Payment Intent: pi_3Qx9vL2eZvKYlo2C
📊 Refund status: succeeded
🕐 Processed: 2026-07-04 12:59:00 UTC
ℹ️ Note: Original payment was $50.00 — $15.00 remaining"

---

## Installation Guide

### Step 1: Create a Stripe Account

1. Go to https://dashboard.stripe.com/register
2. Complete account setup (email + password)
3. Verify your email address
4. Activate your account (Stripe may require business info depending on region)

### Step 2: Get Your API Keys

1. Go to https://dashboard.stripe.com/apikeys
2. You'll see two key pairs:
   - **Test mode** keys (prefix `sk_test_`) — for development, no real money moves
   - **Live mode** keys (prefix `sk_live_`) — real transactions
3. Copy the **Secret Key** (starts with `sk_test_` or `sk_live_`)
4. Never share these keys publicly

> ⚠️ Keep Test Mode ON while developing. Toggle to Live Mode only when ready for real payments.

### Step 3: Configure OpenClaw

Add to `~/.openclaw/.env`:

```bash
STRIPE_SECRET_KEY="sk_test_51Nx..."
STRIPE_WEBHOOK_SECRET="whsec_..."   # Optional, only for webhook verification
STRIPE_CURRENCY="usd"                # Optional, defaults to usd
```

Restart OpenClaw to load environment variables.

### Step 4: (Optional) Create a Product and Price

Before creating subscriptions, you need at least one Price in Stripe:

**Via Dashboard:**
1. Go to https://dashboard.stripe.com/products
2. Click **Add product**
3. Set name, pricing (e.g., $29/month recurring)
4. Copy the `price_id` (starts with `price_`)

**Via API:**
```bash
# Create product
curl https://api.stripe.com/v1/products \
  -u "${STRIPE_SECRET_KEY}:" \
  -d name="Pro Plan"

# Create recurring price
curl https://api.stripe.com/v1/prices \
  -u "${STRIPE_SECRET_KEY}:" \
  -d product="prod_xxx" \
  -d unit_amount=2900 \
  -d currency="usd" \
  -d recurring[interval]="month"
```

### Step 5: Enable Test Webhooks (Optional)

To test webhooks locally:

1. Install Stripe CLI: https://stripe.com/docs/stripe-cli
2. Login: `stripe login`
3. Forward webhooks to localhost:
   ```bash
   stripe listen --forward-to localhost:3000/webhook/stripe
   ```
4. Copy the `whsec_...` secret from output into `STRIPE_WEBHOOK_SECRET`

### Step 6: Test Your Setup

Try these commands to verify everything works:

1. "Check my Stripe balance" — should return balance info
2. "Create a customer for john@example.com" — should return customer object
3. "Look up payment pi_3Qx9vL2eZvKYlo2C" — should return payment details (or "no such payment" if test mode)

---

## Caveats

### Test Mode vs Live Mode

- **Test mode** (`sk_test_`) keys: simulate all operations without real money
- **Live mode** (`sk_live_`) keys: real charges, real refunds, real settlements
- Always test with `sk_test_` before going live
- Stripe test card numbers: https://stripe.com/docs/testing#cards

### Common Test Card Numbers

| Scenario | Card Number |
|---|---|
| Successful payment | 4242 4242 4242 4242 |
| Insufficient funds | 4000 0000 0000 0002 |
| Card declined | 4000 0000 0000 0002 |
| Expired card | 4000 0000 0000 0069 |
| Incorrect CVC | 4000 0000 0000 0127 |

### Amount Units

- All Stripe amounts are in **smallest currency unit** (cents for USD/EUR, pence for GBP, yen for JPY with no decimals)
- $50.00 USD → `5000`
- ¥1,000 JPY → `1000` (no decimal)
- Always divide by 100 for USD/EUR display

### Rate Limits

- API requests: **1,000/second** on most endpoints (burst allowed)
- `POST /v1/balance` (retrieve): **25/second**
- Exceeding limits returns `429 Too Many Requests` with `Retry-After` header

### PCI Compliance

- Never log full card numbers (Stripe handles this — you only see last 4 digits like `4242`)
- Never store raw card data — use Stripe tokens (`payment_method`) instead
- For high compliance needs, use Stripe's official client-side libraries (Stripe.js)

### PaymentIntent Flow (Standard)

1. Create PaymentIntent → get `client_secret`
2. Frontend uses `client_secret` + Stripe.js to collect card
3. Stripe confirms payment on frontend
4. Webhook `payment_intent.succeeded` fires to your server
5. Backend fulfills the order

> This skill supports steps 1, 3, and 5 server-side. Frontend Stripe.js integration requires separate HTML/JS (outside scope of this skill).

### Refund Rules

- Refunds can only be issued within **90 days** of the original charge
- Partial refunds allowed (minimum 1 cent)
- Refunds to debit cards take 5-10 business days
- Refunds to credit cards: immediate to 30 days (depends on issuer)

### Customer Deletion

- Stripe does not allow deleting customers via API — only archiving
- Archived customers are hidden from lists but data retained for compliance
- `stripe.customers.delete()` actually archives, not deletes

### Idempotency

- Stripe supports idempotency keys to prevent duplicate operations on retry
- Pass `Idempotency-Key: <unique-string>` header when retrying `POST` requests
- Key must be ≤ 255 characters and unique per operation

### Currency Support

- Stripe supports 135+ currencies
- Always specify `currency` explicitly — defaults vary by API call
- All amounts must be positive integers; no negative values
