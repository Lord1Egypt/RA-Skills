---
name: stripe-setup
description: Add Stripe payments to any agent-built app. Covers checkout sessions, subscription billing, webhook handling, customer portal, and test-mode validation. Use when you need to accept payments, set up subscriptions, handle billing events, or wire Stripe into a Flask/FastAPI/Express app. No prior Stripe experience needed — follow the steps and you'll have a working payment flow. Assumes Python + Flask on a VPS with a .env file. Adapt patterns for FastAPI, serverless, or other stacks.
---

# Stripe Setup

Wire Stripe payments into any agent-built application. Covers the full stack: checkout → webhook → subscription management → customer portal.

## What You Get

- One-time and recurring (subscription) checkout flows
- Webhook handler for all critical billing events
- Customer portal (manage billing, cancel, update card)
- Test-mode → live-mode migration checklist
- Ready-to-run scripts for Flask and FastAPI

## Prerequisites

1. **Stripe account** — [stripe.com](https://stripe.com) (free, takes 5 min)
2. **API keys** — Dashboard → Developers → API Keys
3. **Python SDK**: `pip install stripe python-dotenv`

## Environment Variables

```bash
STRIPE_SECRET_KEY=sk_test_...        # Secret key (never expose client-side)
STRIPE_PUBLISHABLE_KEY=pk_test_...   # Safe for frontend
STRIPE_WEBHOOK_SECRET=whsec_...      # From webhook endpoint setup (Step 3)
STRIPE_PRICE_ID=price_...            # Your subscription price ID
```

Add these to `.env` and load with `python-dotenv`.

---

## Step 1 — Create a Product + Price

In the Stripe Dashboard:

1. Go to **Products** → **Add product**
2. Name it (e.g., "MyApp Pro")
3. Set pricing: choose **Recurring** (monthly/annual) or **One time**
4. Copy the **Price ID** → save as `STRIPE_PRICE_ID`

Or via API:

```python
import stripe, os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

product = stripe.Product.create(name="MyApp Pro")
price = stripe.Price.create(
    product=product.id,
    unit_amount=1000,         # $10.00 in cents — replace with your price
    currency="usd",
    recurring={"interval": "month"},
)
print(price.id)  # → save as STRIPE_PRICE_ID
```

---

## Step 2 — Checkout Session (Subscription)

```python
import stripe, os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout_session(customer_email: str, success_url: str, cancel_url: str) -> str:
    """Create a Stripe Checkout session. Returns the redirect URL."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{"price": os.getenv("STRIPE_PRICE_ID"), "quantity": 1}],
        customer_email=customer_email,
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
        allow_promotion_codes=True,
    )
    return session.url
```

### Flask route

```python
from flask import Flask, redirect, request
app = Flask(__name__)

@app.route("/subscribe")
def subscribe():
    url = create_checkout_session(
        customer_email=request.args.get("email", ""),
        success_url="https://yourapp.com/success",
        cancel_url="https://yourapp.com/pricing",
    )
    return redirect(url)
```

### One-time payment variant

```python
session = stripe.checkout.Session.create(
    mode="payment",              # ← change from "subscription"
    line_items=[{"price": PRICE_ID, "quantity": 1}],
    ...
)
```

---

## Step 3 — Webhook Handler

Webhooks tell your app when payments succeed, fail, or subscriptions change. **This is required** — don't skip it.

### Register the endpoint

1. Dashboard → **Developers** → **Webhooks** → **Add endpoint**
2. URL: `https://yourapp.com/webhook/stripe`
3. Events to listen for:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_failed`
4. Copy the **Signing secret** → save as `STRIPE_WEBHOOK_SECRET`

### Flask webhook handler

```python
import stripe
from flask import Flask, request, jsonify

app = Flask(__name__)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@app.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid signature"}), 400

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        handle_checkout_complete(data)
    elif event_type == "customer.subscription.deleted":
        handle_subscription_cancelled(data)
    elif event_type == "invoice.payment_failed":
        handle_payment_failed(data)

    return jsonify({"status": "ok"}), 200


# Idempotency: Stripe retries failed webhook deliveries. Without this, one payment
# can trigger duplicate fulfillment. Store processed event IDs to prevent double-firing.
#
# Simple implementation (use Redis or DB in production):
PROCESSED_EVENTS = set()
def is_duplicate_event(event_id: str) -> bool:
    if event_id in PROCESSED_EVENTS:
        return True
    PROCESSED_EVENTS.add(event_id)
    return False
#
# Then in stripe_webhook(), after construct_event():
# if is_duplicate_event(event["id"]):
#     return jsonify({"status": "duplicate"}), 200


def handle_checkout_complete(session):
    customer_email = session.get("customer_email")
    subscription_id = session.get("subscription")
    # REQUIRED: activate user in your DB here. Do not skip this step.
    # The payment is complete — if you do not provision access now, the user
    # paid but got nothing. This is not optional.
    # Example: db.users.update(email=customer_email, fields={active: True, stripe_sub_id: subscription_id})
    print(f"New subscriber: {customer_email}, sub: {subscription_id}")


def handle_subscription_cancelled(subscription):
    customer_id = subscription.get("customer")
    # REQUIRED: revoke user access in your DB here. Do not skip this step.
    # Example: db.users.update(customer_id=customer_id, fields={active: False})
    print(f"Subscription cancelled: customer {customer_id}")


def handle_payment_failed(invoice):
    customer_id = invoice.get("customer")
    # REQUIRED: notify user and pause or revoke access depending on your grace period policy.
    # Example: send_dunning_email(customer_id) and set user status to past_due
    print(f"Payment failed: customer {customer_id}")
```

### Testing webhooks locally

```bash
# Install Stripe CLI (Linux/VPS)
curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg
echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee /etc/apt/sources.list.d/stripe.list
sudo apt update && sudo apt install stripe

# Login
stripe login

# Forward to your local server
stripe listen --forward-to localhost:5000/webhook/stripe
```

---

## Step 4 — Customer Portal (Self-Service Billing)

Let users manage their own subscription (cancel, update card, view invoices).

```python
def create_portal_session(stripe_customer_id: str, return_url: str) -> str:
    """Create a Stripe billing portal session."""
    session = stripe.billing_portal.Session.create(
        customer=stripe_customer_id,
        return_url=return_url,
    )
    return session.url
```

```python
@app.route("/billing")
@login_required
def billing_portal():
    customer_id = current_user.stripe_customer_id
    url = create_portal_session(customer_id, return_url="https://yourapp.com/dashboard")
    return redirect(url)
```

Enable the portal: Dashboard → **Settings** → **Billing** → **Customer portal** → Toggle on.

---

## Step 5 — Verify a Subscription is Active

```python
def get_subscription_access(stripe_customer_id: str) -> dict:
    subs = stripe.Subscription.list(customer=stripe_customer_id, limit=1)
    if not subs.data:
        return {"access": False, "reason": "no_subscription"}
    status = subs.data[0].status
    access_map = {
        "active":    {"access": True,  "reason": "active"},
        "trialing":  {"access": True,  "reason": "in_trial"},
        "past_due":  {"access": True,  "reason": "past_due_grace"},
        "incomplete": {"access": False, "reason": "incomplete_payment"},
        "canceled":  {"access": False, "reason": "canceled"},
        "unpaid":    {"access": False, "reason": "unpaid"},
    }
    return access_map.get(status, {"access": False, "reason": f"unknown_status:{status}"})
```

Use this to gate features behind a paid plan check.

---

## Step 6 — Go Live Checklist

Before switching from test keys (`sk_test_...`) to live keys (`sk_live_...`):

- [ ] All webhook events handled (especially `payment_failed`)
- [ ] Webhook signature verification is enabled (not bypassed)
- [ ] Success/cancel URLs are production URLs (not localhost)
- [ ] Test a full checkout → subscription → cancellation flow in test mode
- [ ] Re-register webhook endpoint with live URL in Stripe Dashboard
- [ ] Update `.env`: replace `sk_test_` → `sk_live_`, `pk_test_` → `pk_live_`
- [ ] New `STRIPE_WEBHOOK_SECRET` from the live endpoint (different from test)
- [ ] Stripe account fully activated (bank account + identity verified)
- [ ] Success page validates session_id via Stripe API — do not trust the URL parameter alone. Example: stripe.checkout.Session.retrieve(session_id) and confirm payment_status == paid

> ⚠️ Live keys and test keys have different webhook secrets. Update both.

---

## Common Errors

| Error | Fix |
|-------|-----|
| `No such price: price_xxx` | Wrong env or created in wrong mode (test vs live) |
| `Webhook signature verification failed` | Using wrong `STRIPE_WEBHOOK_SECRET` (test vs live) |
| `Customer portal not enabled` | Enable it in Dashboard → Settings → Billing |
| `Invalid request: success_url must be absolute` | Use full URL including `https://` |
| `stripe.error.AuthenticationError` | Wrong or missing `STRIPE_SECRET_KEY` |

---

## References

- [Stripe Python SDK docs](https://stripe.com/docs/api?lang=python)
- [Checkout Session API](https://stripe.com/docs/api/checkout/sessions)
- [Webhook events reference](https://stripe.com/docs/api/events/types)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [Customer Portal](https://stripe.com/docs/billing/subscriptions/customer-portal)
