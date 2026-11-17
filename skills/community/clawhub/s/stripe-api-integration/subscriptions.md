# Subscriptions — Lifecycle, Plan Changes, Proration

**Read `## Catalog` and `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`** (or their boxes) before changing a plan: which price the customer is on, what replaced it, and whether this team prorates by default.

**Contents:** [Preview Before You Commit](#preview-before-you-commit) · [Subscription Lifecycle](#subscription-lifecycle) · [Status Reference](#status-reference) · [Create Subscription Patterns](#create-subscription-patterns) · [Plan Changes (Upgrades/Downgrades)](#plan-changes-upgradesdowngrades) · [Cancellation Patterns](#cancellation-patterns) · [Pause and Resume](#pause-and-resume) · [Multiple Items (Add-ons)](#multiple-items-add-ons) · [Billing Cycle](#billing-cycle) · [Metered Billing](#metered-billing) · [Failed Payment Handling](#failed-payment-handling) · [Webhook Events for Subscriptions](#webhook-events-for-subscriptions)

## Preview Before You Commit

Any change that touches money — price, quantity, interval, billing anchor — gets previewed against the upcoming invoice first, and the previewed number is the one you show the customer. Announcing a change from an estimate is how refunds and disputes happen.

**Proration arithmetic**, so the preview is verifiable rather than magic: switching mid-period credits the unused portion of the old price and charges the used portion of the new one, prorated by time remaining.

```
credit  = old_price × (seconds_remaining / seconds_in_period)
charge  = new_price × (seconds_remaining / seconds_in_period)
delta   = charge − credit
```

On a 30-day period, upgrading from 10 to 30 on day 20 with 10 days left: credit `10 × 10/30 = 3.33`, charge `30 × 10/30 = 10.00`, delta `6.67` — invoiced immediately with `proration_behavior=create_prorations`, or rolled into the next invoice with `always_invoice` versus `none`.

Three behaviors and when each is right: `create_prorations` for upgrades the customer asked for and expects to pay for now; `none` for downgrades that should take effect at the next renewal without a credit; `always_invoice` when the delta must be collected immediately rather than waiting.

Downgrades are almost always better at period end: an immediate downgrade creates a credit balance that confuses the next invoice and, on annual plans, can produce a refundable amount nobody budgeted.

## Subscription Lifecycle

```
created → active → past_due → canceled
                 ↘ unpaid ↗
                 ↘ paused → active
```

## Status Reference

| Status | Meaning | Action |
|--------|---------|--------|
| `incomplete` | Initial payment failed | Retry or cancel |
| `incomplete_expired` | 23h passed without payment | Start over |
| `trialing` | In trial period | No action needed |
| `active` | Payments current | Normal operation |
| `past_due` | Payment failed, in retry | Contact customer |
| `unpaid` | Retries exhausted | Cancel or intervention |
| `canceled` | Subscription ended | Resubscribe if wanted |
| `paused` | Collection paused | Resume when ready |

## Create Subscription Patterns

### Simple Subscription
```bash
curl https://api.stripe.com/v1/subscriptions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "items[0][price]=price_XXX"
```

### With Trial
```bash
curl https://api.stripe.com/v1/subscriptions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "items[0][price]=price_XXX" \
  -d "trial_period_days=14"
```

### With Specific Trial End
```bash
curl https://api.stripe.com/v1/subscriptions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "items[0][price]=price_XXX" \
  -d "trial_end=$(($(date +%s) + 604800))"  # 7 days from now
```

### With Default Payment Method
```bash
curl https://api.stripe.com/v1/subscriptions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "items[0][price]=price_XXX" \
  -d "default_payment_method=pm_XXX"
```

### With Coupon
```bash
curl https://api.stripe.com/v1/subscriptions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "items[0][price]=price_XXX" \
  -d "coupon=WELCOME20"
```

## Plan Changes (Upgrades/Downgrades)

### Immediate Upgrade with Proration
```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "items[0][id]=si_XXX" \
  -d "items[0][price]=price_HIGHER" \
  -d "proration_behavior=create_prorations"
```

### Downgrade at Period End
```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "items[0][id]=si_XXX" \
  -d "items[0][price]=price_LOWER" \
  -d "proration_behavior=none" \
  -d "billing_cycle_anchor=unchanged"
```

### Preview Proration
```bash
curl https://api.stripe.com/v1/invoices/upcoming \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_XXX" \
  -d "subscription=sub_XXX" \
  -d "subscription_items[0][id]=si_XXX" \
  -d "subscription_items[0][price]=price_NEW" \
  -d "subscription_proration_behavior=create_prorations"
```

## Cancellation Patterns

### Cancel Immediately
```bash
curl -X DELETE https://api.stripe.com/v1/subscriptions/sub_XXX \
  -u "$STRIPE_SECRET_KEY:"
```

### Cancel at Period End
```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "cancel_at_period_end=true"
```

### Cancel at Specific Date
```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "cancel_at=$(($(date +%s) + 2592000))"  # 30 days from now
```

### Undo Pending Cancellation
```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "cancel_at_period_end=false"
```

## Pause and Resume

### Pause Collection
```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "pause_collection[behavior]=mark_uncollectible"
```

Behaviors:
- `mark_uncollectible`: Invoices created but marked uncollectible
- `keep_as_draft`: Invoices created as drafts
- `void`: Invoices voided

### Pause Until Date
```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "pause_collection[behavior]=mark_uncollectible" \
  -d "pause_collection[resumes_at]=$(($(date +%s) + 2592000))"
```

### Resume
```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "pause_collection="
```

## Multiple Items (Add-ons)

### Add Item to Subscription
```bash
curl https://api.stripe.com/v1/subscription_items \
  -u "$STRIPE_SECRET_KEY:" \
  -d "subscription=sub_XXX" \
  -d "price=price_ADDON" \
  -d "quantity=1"
```

### Remove Item
```bash
curl -X DELETE https://api.stripe.com/v1/subscription_items/si_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "proration_behavior=create_prorations"
```

### Update Item Quantity
```bash
curl https://api.stripe.com/v1/subscription_items/si_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "quantity=5"
```

## Billing Cycle

### Change Billing Anchor (Next Renewal Date)
```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "billing_cycle_anchor=now" \
  -d "proration_behavior=create_prorations"
```

### Bill Immediately (Mid-cycle)
```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "billing_cycle_anchor=now"
```

## Metered Billing

### Report Usage
```bash
curl https://api.stripe.com/v1/subscription_items/si_XXX/usage_records \
  -u "$STRIPE_SECRET_KEY:" \
  -d "quantity=100" \
  -d "timestamp=$(date +%s)" \
  -d "action=increment"
```

Actions:
- `increment`: Add to existing usage
- `set`: Replace usage for timestamp

### Get Usage Summary
```bash
curl "https://api.stripe.com/v1/subscription_items/si_XXX/usage_record_summaries?limit=10" \
  -u "$STRIPE_SECRET_KEY:"
```

## Failed Payment Handling

### Retry Invoice Payment
```bash
curl https://api.stripe.com/v1/invoices/in_XXX/pay \
  -u "$STRIPE_SECRET_KEY:"
```

### Update Payment Method and Retry
```bash
# Update customer's default payment method
curl https://api.stripe.com/v1/customers/cus_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "invoice_settings[default_payment_method]=pm_NEW"

# Retry the failed invoice
curl https://api.stripe.com/v1/invoices/in_XXX/pay \
  -u "$STRIPE_SECRET_KEY:"
```

## Webhook Events for Subscriptions

| Event | When | Action |
|-------|------|--------|
| `customer.subscription.created` | New subscription | Provision access |
| `customer.subscription.updated` | Plan change, renewal | Update access |
| `customer.subscription.deleted` | Canceled | Revoke access |
| `customer.subscription.trial_will_end` | 3 days before trial ends | Send reminder |
| `customer.subscription.paused` | Subscription paused | Limit access |
| `customer.subscription.resumed` | Subscription resumed | Restore access |
| `invoice.payment_failed` | Payment failed | Send dunning email |
| `invoice.paid` | Subscription renewed | Confirm renewal |

## Subscription Schedules — When the Future Is Known

A schedule expresses a sequence of phases: an introductory price for three months, then the standard one; a committed annual term that renews to a different price; a start date in the future. Use it instead of a reminder to change the subscription later — a phase change that lives in a calendar entry is a change that will be missed.

- Phases carry their own prices, quantities, coupons and durations; the transition happens on Stripe's clock, not yours.
- A schedule can be released back to a plain subscription, which is the escape hatch when the future turns out differently.
- Rehearse every schedule with a test clock before it reaches a customer (`testing.md`).

## Trials Without Losing the First Renewal

- A trial with no payment method collected is a renewal that will fail. Either collect a card up front (`setup_future_usage`, or a SetupIntent during the trial) or set the trial end behavior explicitly so the subscription cancels or pauses instead of failing silently (`checkout.md`).
- `customer.subscription.trial_will_end` fires a few days before the end. That event is the last cheap moment to fix a missing payment method — handle it or lose the conversion.
- Extending a trial is an update to `trial_end`, not a new subscription.

---

**Write in the same turn**: a plan change policy — prorate up, downgrade at period end, who may grant an extension — goes to `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`, or under `conventions` in `config.yaml` when the user states it as a rule. New or retired prices go to `## Catalog` (`customers.md`). A migration across a cohort belongs in `artifacts/migration-<price>.md` with its `## Boxes` line.
