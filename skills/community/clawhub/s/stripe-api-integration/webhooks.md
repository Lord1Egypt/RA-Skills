# Webhooks — Events, Verification, Delivery

**Read `## Webhook Endpoints` in `~/Clawic/data/stripe-api-integration/memory.md`** (or `webhook-endpoints.md` when `## Boxes` points there) before adding, re-pointing or debugging an endpoint: which endpoints exist, which events each subscribes to, and which API version each is pinned to. An endpoint nobody recorded is an endpoint nobody audits.

**Contents:** [The Five Properties of a Correct Handler](#the-five-properties-of-a-correct-handler) · [Webhook Fundamentals](#webhook-fundamentals) · [Create Webhook Endpoint](#create-webhook-endpoint) · [Essential Events](#essential-events) · [Signature Verification](#signature-verification) · [Event Handling Pattern](#event-handling-pattern) · [Idempotency](#idempotency) · [Webhook Best Practices](#webhook-best-practices) · [List and Manage Endpoints](#list-and-manage-endpoints) · [Debugging](#debugging)

## The Five Properties of a Correct Handler

Everything else in this file is detail; these five are the contract.

1. **Verifies against the raw body.** Any framework that parses JSON before your handler sees it breaks the signature. Configure the raw-body route explicitly, and use the secret of *that* endpoint.
2. **Acks fast, works later.** Respond 2xx as soon as the event is persisted or queued. A handler that does the work inline gets retried mid-work and produces the duplicate it was meant to prevent.
3. **Idempotent by `event.id`.** Store processed ids and return early on a repeat. At-least-once delivery is a design guarantee, not a rare failure.
4. **Order-independent.** Events can arrive out of order. Compute state from the object you fetch, never from the sequence of arrivals (`debug.md`).
5. **Fetches what it needs.** Payloads cannot be expanded and are snapshots at event time; if the handler acts on related data, it re-fetches it (`api-mechanics.md`).

Practical consequences: one endpoint per concern with an explicit event list, its own secret, and a pinned API version; alerting on delivery failures, because Stripe retries for days and then disables the endpoint after its warnings; and a signature tolerance of five minutes, which means a server with a drifting clock rejects perfectly good events.

## Webhook Fundamentals

Webhooks are essential for:
- Async payment confirmation (3D Secure, bank transfers)
- Subscription lifecycle events
- Dispute notifications
- Payout confirmations

**Never rely solely on API responses.** Always confirm with webhooks.

## Create Webhook Endpoint

### Via API
```bash
curl https://api.stripe.com/v1/webhook_endpoints \
  -u "$STRIPE_SECRET_KEY:" \
  -d "url=https://example.com/webhooks/stripe" \
  -d "enabled_events[]=payment_intent.succeeded" \
  -d "enabled_events[]=payment_intent.payment_failed" \
  -d "enabled_events[]=customer.subscription.created" \
  -d "enabled_events[]=customer.subscription.updated" \
  -d "enabled_events[]=customer.subscription.deleted" \
  -d "enabled_events[]=invoice.paid" \
  -d "enabled_events[]=invoice.payment_failed"
```

### Via Dashboard
1. Go to Developers > Webhooks
2. Add endpoint
3. Select events
4. Copy signing secret

## Essential Events

### Payments
| Event | When | Critical |
|-------|------|----------|
| `payment_intent.succeeded` | Payment completed | Yes |
| `payment_intent.payment_failed` | Payment failed | Yes |
| `payment_intent.requires_action` | 3DS needed | Yes |
| `charge.refunded` | Refund processed | Yes |
| `charge.dispute.created` | Chargeback filed | Yes |

### Subscriptions
| Event | When | Critical |
|-------|------|----------|
| `customer.subscription.created` | New subscription | Yes |
| `customer.subscription.updated` | Plan changed | Yes |
| `customer.subscription.deleted` | Canceled | Yes |
| `customer.subscription.trial_will_end` | 3 days before trial ends | Important |
| `customer.subscription.paused` | Paused | Important |

### Invoices
| Event | When | Critical |
|-------|------|----------|
| `invoice.paid` | Payment succeeded | Yes |
| `invoice.payment_failed` | Payment failed | Yes |
| `invoice.upcoming` | Invoice will be created | Informational |
| `invoice.finalized` | Invoice ready to pay | Informational |

### Checkout
| Event | When | Critical |
|-------|------|----------|
| `checkout.session.completed` | Payment successful | Yes |
| `checkout.session.expired` | Session expired | Important |
| `checkout.session.async_payment_succeeded` | Async payment done | Yes |
| `checkout.session.async_payment_failed` | Async payment failed | Yes |

## Signature Verification

### Python
```python
import stripe
import os

stripe.api_key = os.environ['STRIPE_SECRET_KEY']
endpoint_secret = os.environ['STRIPE_WEBHOOK_SECRET']

def handle_webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return 400, 'Invalid payload'
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 400, 'Invalid signature'
    
    # Handle event
    return 200, 'OK'
```

### Node.js
```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

app.post('/webhooks/stripe', express.raw({type: 'application/json'}), (req, res) => {
  const sig = req.headers['stripe-signature'];
  
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }
  
  // Handle event
  res.json({received: true});
});
```

### Go
```go
import (
    "github.com/stripe/stripe-go/v76/webhook"
)

func handleWebhook(w http.ResponseWriter, req *http.Request) {
    payload, _ := io.ReadAll(req.Body)
    sigHeader := req.Header.Get("Stripe-Signature")
    
    event, err := webhook.ConstructEvent(payload, sigHeader, endpointSecret)
    if err != nil {
        w.WriteHeader(http.StatusBadRequest)
        return
    }
    
    // Handle event
    w.WriteHeader(http.StatusOK)
}
```

## Event Handling Pattern

```python
def handle_event(event):
    event_type = event['type']
    data = event['data']['object']
    
    handlers = {
        'payment_intent.succeeded': handle_payment_success,
        'payment_intent.payment_failed': handle_payment_failure,
        'customer.subscription.created': handle_subscription_created,
        'customer.subscription.updated': handle_subscription_updated,
        'customer.subscription.deleted': handle_subscription_deleted,
        'invoice.paid': handle_invoice_paid,
        'invoice.payment_failed': handle_invoice_failed,
        'charge.dispute.created': handle_dispute,
    }
    
    handler = handlers.get(event_type)
    if handler:
        handler(data)
    else:
        print(f'Unhandled event type: {event_type}')
```

## Idempotency

Webhooks may be sent multiple times. Always handle idempotently:

```python
def handle_payment_success(payment_intent):
    payment_id = payment_intent['id']
    
    # Check if already processed
    if Order.query.filter_by(stripe_payment_id=payment_id).first():
        return  # Already handled
    
    # Process payment
    order = Order(
        stripe_payment_id=payment_id,
        amount=payment_intent['amount'],
        customer_id=payment_intent['customer']
    )
    db.session.add(order)
    db.session.commit()
```

## Webhook Best Practices

### 1. Return 200 Quickly
```python
def webhook_endpoint(request):
    event = verify_signature(request)
    
    # Queue for async processing
    queue.enqueue(process_event, event)
    
    # Return immediately
    return 200
```

### 2. Handle Retries
Stripe retries for up to 3 days with exponential backoff:
- 1 hour, 2 hours, 4 hours, 8 hours...

### 3. Log Everything
```python
def process_event(event):
    logger.info(f"Processing {event['type']}: {event['id']}")
    try:
        handle_event(event)
        logger.info(f"Success: {event['id']}")
    except Exception as e:
        logger.error(f"Failed: {event['id']}: {e}")
        raise
```

### 4. Test with CLI (Optional)

The Stripe CLI is optional and only for local development testing.

```bash
# If Stripe CLI is installed, use for local testing:
stripe listen --forward-to localhost:3000/webhooks/stripe

# Trigger test events
stripe trigger payment_intent.succeeded
stripe trigger customer.subscription.created
```

Note: Stripe CLI installation is not required. Use the Dashboard for webhook testing in production.

## List and Manage Endpoints

### List Endpoints
```bash
curl https://api.stripe.com/v1/webhook_endpoints \
  -u "$STRIPE_SECRET_KEY:"
```

### Update Endpoint
```bash
curl https://api.stripe.com/v1/webhook_endpoints/we_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "enabled_events[]=charge.dispute.created" \
  -d "enabled_events[]=charge.dispute.closed"
```

### Disable Endpoint
```bash
curl https://api.stripe.com/v1/webhook_endpoints/we_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "disabled=true"
```

### Delete Endpoint
```bash
curl -X DELETE https://api.stripe.com/v1/webhook_endpoints/we_XXX \
  -u "$STRIPE_SECRET_KEY:"
```

## Debugging

### View Recent Events
```bash
curl "https://api.stripe.com/v1/events?limit=10" \
  -u "$STRIPE_SECRET_KEY:"
```

### Get Specific Event
```bash
curl https://api.stripe.com/v1/events/evt_XXX \
  -u "$STRIPE_SECRET_KEY:"
```

### Resend Event (via Dashboard)
Dashboard > Developers > Events > Select event > Resend

## The Minimum Event Set by Business Model

Subscribe to what you act on and nothing else — unhandled volume hides the events that matter.

| `billing_model` | Events you cannot skip |
|---|---|
| one-time | `payment_intent.succeeded`, `payment_intent.payment_failed`, `charge.refunded`, `charge.dispute.created` |
| subscription | the above, plus `checkout.session.completed`, `invoice.paid`, `invoice.payment_failed`, `customer.subscription.updated`, `customer.subscription.deleted`, `customer.subscription.trial_will_end` |
| marketplace | plus `account.updated`, `payout.paid`, `payout.failed`, and the dispute events on whichever side holds liability (`connect.md`) |
| invoicing | plus `invoice.finalized`, `invoice.sent`, `invoice.marked_uncollectible`, `credit_note.created` |
| any model with bank-based methods | plus `checkout.session.async_payment_succeeded` and `checkout.session.async_payment_failed` (`payment-methods.md`) |
| anything else | Subscribe to what a handler exists for; an event with no handler is noise that hides a failure |

## When Delivery Is Not the Problem

An endpoint that is healthy and an integration that is broken look the same from the outside. Two safety nets are worth building once:

- **A reconciliation sweep**: periodically list objects changed since the last run and repair anything your database missed. It catches the events lost while an endpoint was down and the ones a bug swallowed with a 200.
- **Polling as a fallback for one critical flow** — usually fulfillment. Not a replacement for webhooks; a floor under them.

---

**Write in the same turn**: every endpoint created, re-pointed, disabled or re-scoped goes to `## Webhook Endpoints` in `~/Clawic/data/stripe-api-integration/memory.md` — environment, URL, event count, API version, a **pointer** for its secret (`env:…`, `ssm:/…`, never the value), and status. Which events have handlers and what each one does belongs in the same section, and moves with it into `webhook-endpoints.md` at the split (`memory-template.md`). A delivery outage that lost events is a row in `incidents/<year>.md`; schedule the endpoint audit in `## Due`.
