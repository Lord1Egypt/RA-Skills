# Payments — Intents, Saved Cards, Refunds, Payouts

Calls below are raw HTTP; if `stack` in `config.yaml` names a language, translate them to that SDK. Amounts are integers in the currency's minor unit and every money-moving POST carries an idempotency key derived from a business identifier (`api-mechanics.md`).

**Contents:** [The PaymentIntent Lifecycle](#the-paymentintent-lifecycle) · [Payment Intents](#payment-intents) · [Payment Methods](#payment-methods) · [Setup Intents (Save Cards)](#setup-intents-save-cards) · [Refunds](#refunds) · [Disputes (Chargebacks)](#disputes-chargebacks) · [Balance](#balance) · [ID Prefixes Reference](#id-prefixes-reference)

## The PaymentIntent Lifecycle

One object tracks the whole attempt, which is why you resume it instead of creating another.

```
requires_payment_method → requires_confirmation → requires_action → processing → succeeded
                    ↘ (any failure returns here) ↙                        ↘ canceled
```

| State | Means | Correct move |
|---|---|---|
| `requires_payment_method` | No method, or the last one failed | Collect another; the intent is still usable |
| `requires_action` | 3DS or a redirect is pending | Show it on-session; never retry off-session (`sca-3ds.md`) |
| `requires_capture` | Authorized, not captured (manual capture) | Capture within the authorization window or it expires |
| `processing` | Asynchronous method settling | Wait for the event; days for bank debits (`payment-methods.md`) |
| `succeeded` | Money captured | Fulfill from the event, not from this response |
| `canceled` | Ended deliberately or expired | Terminal — a new attempt is a new intent |

Rules that follow: currency and the customer cannot change after creation; the amount can be updated only while the intent has not been confirmed; and `client_secret` is a credential for that one intent — it belongs in the customer's browser, never in your logs or notes.

**Manual capture** (authorize now, charge later) fits order flows where you confirm stock or complete a service first. The authorization holds funds and expires after a period set by the card network — commonly around a week, shorter for some methods. An expired authorization is not a charge, and capturing a smaller amount than authorized is allowed while capturing more is not.

## Payment Intents

### Create Payment Intent
```bash
curl https://api.stripe.com/v1/payment_intents \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=2000" \
  -d "currency=usd" \
  -d "customer=cus_XXX" \
  -d "payment_method_types[]=card" \
  -d "metadata[order_id]=6735"
```

### Confirm Payment Intent
```bash
curl https://api.stripe.com/v1/payment_intents/pi_XXX/confirm \
  -u "$STRIPE_SECRET_KEY:" \
  -d "payment_method=pm_XXX"
```

### Capture Payment Intent (manual capture)
```bash
curl https://api.stripe.com/v1/payment_intents/pi_XXX/capture \
  -u "$STRIPE_SECRET_KEY:"
```

### Cancel Payment Intent
```bash
curl https://api.stripe.com/v1/payment_intents/pi_XXX/cancel \
  -u "$STRIPE_SECRET_KEY:"
```

### List Payment Intents
```bash
curl "https://api.stripe.com/v1/payment_intents?customer=cus_XXX&limit=10" \
  -u "$STRIPE_SECRET_KEY:"
```

---

## Payment Methods

### List Payment Methods
```bash
curl "https://api.stripe.com/v1/payment_methods?customer=cus_XXX&type=card" \
  -u "$STRIPE_SECRET_KEY:"
```

### Get Payment Method
```bash
curl https://api.stripe.com/v1/payment_methods/pm_XXX \
  -u "$STRIPE_SECRET_KEY:"
```

### Attach to Customer
```bash
curl https://api.stripe.com/v1/payment_methods/pm_XXX/attach \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX"
```

### Detach from Customer
```bash
curl https://api.stripe.com/v1/payment_methods/pm_XXX/detach \
  -u "$STRIPE_SECRET_KEY:"
```

---

## Setup Intents (Save Cards)

### Create Setup Intent
```bash
curl https://api.stripe.com/v1/setup_intents \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "payment_method_types[]=card"
```

### Confirm Setup Intent
```bash
curl https://api.stripe.com/v1/setup_intents/seti_XXX/confirm \
  -u "$STRIPE_SECRET_KEY:" \
  -d "payment_method=pm_XXX"
```

---

## Refunds

### Full Refund
```bash
curl https://api.stripe.com/v1/refunds \
  -u "$STRIPE_SECRET_KEY:" \
  -d "payment_intent=pi_XXX"
```

### Partial Refund
```bash
curl https://api.stripe.com/v1/refunds \
  -u "$STRIPE_SECRET_KEY:" \
  -d "payment_intent=pi_XXX" \
  -d "amount=500"
```

### Refund with Reason
```bash
curl https://api.stripe.com/v1/refunds \
  -u "$STRIPE_SECRET_KEY:" \
  -d "payment_intent=pi_XXX" \
  -d "reason=requested_by_customer"
```

Reasons: `duplicate`, `fraudulent`, `requested_by_customer`

### Refund Rules Worth Knowing Before You Promise One

- The original processing fee is generally not returned, so a refunded sale still cost money — a "free" goodwill refund is not free (`reconciliation.md`).
- Refunds go back to the original payment method only. If the card is closed, the issuer routes it to the replacement account; there is no path to a different card.
- Partial refunds can repeat until the full amount is reached; each is its own object with its own balance transaction.
- Refund timing to the customer's statement is days, not instant, and telling them "immediately" produces the support ticket.
- **Never refund a charge that is already disputed** — you can pay twice and the dispute continues.
- Bank-debit and voucher refunds follow their rail's rules and can be slower or constrained (`payment-methods.md`).

---

## Disputes (Chargebacks)

The deadline, the evidence packet per reason code, the rate that triggers network programs and the prevention order live in `disputes.md`. The calls:

```bash
# List disputes
curl "https://api.stripe.com/v1/disputes?limit=10" \
  -u "$STRIPE_SECRET_KEY:"

# Submit evidence — once only, no revisions after submission
curl https://api.stripe.com/v1/disputes/dp_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "evidence[customer_name]=John Doe" \
  -d "evidence[customer_email]=john@example.com" \
  -d "evidence[product_description]=Premium subscription"

# Accept the dispute and stop working on it
curl https://api.stripe.com/v1/disputes/dp_XXX/close \
  -u "$STRIPE_SECRET_KEY:"
```

---

## Balance

### Get Balance
```bash
curl https://api.stripe.com/v1/balance \
  -u "$STRIPE_SECRET_KEY:"
```

### List Balance Transactions
```bash
curl "https://api.stripe.com/v1/balance_transactions?limit=10" \
  -u "$STRIPE_SECRET_KEY:"
```

### Create Payout
```bash
curl https://api.stripe.com/v1/payouts \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=10000" \
  -d "currency=usd"
```

---

## ID Prefixes Reference

| Prefix | Resource |
|--------|----------|
| `pi_` | Payment Intent |
| `pm_` | Payment Method |
| `seti_` | Setup Intent |
| `ch_` | Charge |
| `re_` | Refund |
| `dp_` | Dispute |
| `po_` | Payout |

---

**Write after this file produced something durable**: a duplicate charge, a failed payout or any incident that reached a customer goes to `~/Clawic/data/stripe-api-integration/incidents/<year>.md` with its money impact; a refund policy or an approval threshold the user states is a declaration and goes under `safety_posture` in `config.yaml`; a procedure worth reusing — how this team handles a duplicate charge, who approves large refunds — is `artifacts/runbook-<name>.md` with its `## Boxes` line in `memory.md`, written in the same turn.
