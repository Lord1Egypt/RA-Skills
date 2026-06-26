---
name: skill-stripe-monitor
version: 1.0.2
description: Stripe revenue dashboard in your agent — MRR, churn, new subscriptions, failed payments, and alerts. Use when the operator asks about revenue, subscriptions, churn, failed payments, or Stripe activity.
author: ordo-tech
tags: [stripe, revenue, subscriptions, mrr, payments, dashboard, monitoring]
requires:
  env:
    - STRIPE_SECRET_KEY
  tools: []
---

# skill-stripe-monitor

Live Stripe revenue metrics in your agent. MRR, new subscriptions, cancellations, failed payments, and top products — on demand or on a schedule.

## When to Use

✅ **USE this skill when:**

- "What's my MRR?"
- "Any failed payments today?"
- "How many new subscribers this month?"
- "Show me my Stripe status"
- `/stripe mrr`, `/stripe failures`, `/stripe subscribers`, `/stripe status`
- Scheduled daily revenue briefing

❌ **DON'T use this skill when:**

- Modifying Stripe data (charges, refunds, plan changes) — this skill is read-only
- Detailed invoice reconciliation — use Stripe dashboard directly
- Tax reporting — use Stripe Tax or an accountant

---

## Setup

### 1. Get your Stripe API key

Go to [dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys).

Use a **Restricted Key** (recommended) with read-only access to:
- `customers` — read
- `subscriptions` — read
- `invoices` — read
- `charges` — read
- `products` / `prices` — read

Or use your **Secret Key** (`sk_live_...`) for full access — fine for personal use.

### 2. Store the key

Set the `STRIPE_SECRET_KEY` environment variable:

```bash
export STRIPE_SECRET_KEY="sk_live_..."
```

Use a **Restricted Key** scoped to read-only access for safety.

### 3. Verify connection

Ask your agent: "Check my Stripe connection" or run `/stripe status`.

---

## Commands

| Command | What it does |
|---------|-------------|
| `/stripe status` | Quick health check — live mode, currency, recent activity |
| `/stripe mrr` | Current MRR and 30-day trend |
| `/stripe subscribers` | Active subscriber count, new this month, churn this month |
| `/stripe failures` | Failed payments in the last 7 days |
| `/stripe top` | Top 5 products/plans by revenue |
| `/stripe summary` | Full daily summary (all of the above) |

---

## How to Resolve the API Key

Before making any Stripe API call, read the key from the environment variable:

```bash
STRIPE_KEY="${STRIPE_SECRET_KEY:-}"

if [ -z "$STRIPE_KEY" ]; then
  echo "ERROR: STRIPE_SECRET_KEY not set. See Setup section in SKILL.md."
  exit 1
fi
```

All examples below assume `$STRIPE_KEY` is set via this resolution step.

---

## API Patterns

All Stripe API calls use HTTP Basic auth — key as username, empty password:

```bash
curl -s -u "$STRIPE_KEY:" "https://api.stripe.com/v1/..."
```

### Get MRR

Stripe doesn't expose MRR directly. Calculate it from active subscriptions:

```bash
# Fetch active subscriptions (paginate if needed)
curl -s -u "$STRIPE_KEY:" \
  "https://api.stripe.com/v1/subscriptions?status=active&limit=100&expand[]=data.items.data.price" \
  | jq '
    [.data[].items.data[] | 
      .price.unit_amount / 100 * 
      (if .price.recurring.interval == "year" then 1/12 
       elif .price.recurring.interval == "week" then 4.33
       else 1 end)
    ] | add // 0 | . * 100 | round / 100
  '
```

For more than 100 subscriptions, paginate using `starting_after`:

```bash
# Get all active subscriptions (handles pagination)
ALL_SUBS="[]"
LAST_ID=""

while true; do
  PARAMS="status=active&limit=100&expand[]=data.items.data.price"
  if [ -n "$LAST_ID" ]; then
    PARAMS="${PARAMS}&starting_after=${LAST_ID}"
  fi
  
  RESP=$(curl -s -u "$STRIPE_KEY:" "https://api.stripe.com/v1/subscriptions?${PARAMS}")
  PAGE=$(echo "$RESP" | jq '.data')
  ALL_SUBS=$(echo "$ALL_SUBS $PAGE" | jq -s 'add')
  
  HAS_MORE=$(echo "$RESP" | jq -r '.has_more')
  [ "$HAS_MORE" = "false" ] && break
  LAST_ID=$(echo "$RESP" | jq -r '.data[-1].id')
done

echo "$ALL_SUBS" | jq '
  [.[].items.data[] | 
    .price.unit_amount / 100 *
    (if .price.recurring.interval == "year" then 1/12
     elif .price.recurring.interval == "week" then 4.33
     else 1 end)
  ] | add // 0
'
```

### New Subscriptions This Month

```bash
# Start of current month (Unix timestamp)
MONTH_START=$(date -u +%s -d "$(date +%Y-%m-01)" 2>/dev/null || \
              date -u -j -f "%Y-%m-%d" "$(date +%Y-%m-01)" +%s)

curl -s -u "$STRIPE_KEY:" \
  "https://api.stripe.com/v1/subscriptions?status=active&limit=100&created[gte]=${MONTH_START}" \
  | jq '.data | length'
```

### Cancellations This Month

```bash
MONTH_START=$(date -u +%s -d "$(date +%Y-%m-01)" 2>/dev/null || \
              date -u -j -f "%Y-%m-%d" "$(date +%Y-%m-01)" +%s)

curl -s -u "$STRIPE_KEY:" \
  "https://api.stripe.com/v1/subscriptions?status=canceled&limit=100&canceled_at[gte]=${MONTH_START}" \
  | jq '.data | length'
```

### Failed Payments (Last 7 Days)

```bash
SEVEN_DAYS_AGO=$(( $(date -u +%s) - 604800 ))

curl -s -u "$STRIPE_KEY:" \
  "https://api.stripe.com/v1/charges?limit=100&created[gte]=${SEVEN_DAYS_AGO}" \
  | jq '[.data[] | select(.status == "failed")] | 
    {
      count: length,
      total_failed: ([.[].amount] | add // 0) / 100,
      failures: [.[] | {id, amount: (.amount/100), currency, description, created}]
    }'
```

### Top Products by Revenue (Last 30 Days)

```bash
THIRTY_DAYS_AGO=$(( $(date -u +%s) - 2592000 ))

curl -s -u "$STRIPE_KEY:" \
  "https://api.stripe.com/v1/invoices?limit=100&status=paid&created[gte]=${THIRTY_DAYS_AGO}" \
  | jq '
    [.data[].lines.data[] | {product: .description, amount: .amount}]
    | group_by(.product)
    | map({product: .[0].product, revenue: ([.[].amount] | add) / 100})
    | sort_by(-.revenue)
    | .[:5]
  '
```

### Account Status Check

```bash
curl -s -u "$STRIPE_KEY:" "https://api.stripe.com/v1/balance" \
  | jq '{
      available: [.available[] | {currency, amount: (.amount/100)}],
      pending: [.pending[] | {currency, amount: (.amount/100)}],
      livemode: .livemode
    }'
```

---

## Full `/stripe summary` Response

When the operator asks for a full summary or `/stripe summary`, assemble and report all of the following:

```
💳 Stripe Summary — [Date]

MRR: $X,XXX
Active subscribers: XXX
New this month: XX (+X.X%)
Cancellations this month: XX (churn: X.X%)

Failed payments (7d): X ($XXX total)
  ↳ Most recent: [customer/description] — $XX — [time ago]

Top products (30d):
  1. [Product name] — $X,XXX
  2. [Product name] — $X,XXX
  3. [Product name] — $X,XXX

Balance: $X,XXX available / $X,XXX pending
Mode: live ✅  (or test ⚠️)
```

If any metric fails to fetch, report it as "unavailable" and continue.

---

## Scheduled Daily Summary

To receive a daily Stripe summary via Telegram, set up a cron-style heartbeat task or use OpenClaw's scheduler.

Example HEARTBEAT.md entry:
```markdown
## Daily Stripe Summary
- Time: 08:00 CET
- Action: Run /stripe summary and send to Telegram
```

Or ask: "Set up a daily Stripe summary at 8am."

---

## Alerts

Alert the operator when you detect:

| Event | Trigger | Message |
|-------|---------|---------|
| Failed payment | Any charge with `status: failed` created in the last hour | ⚠️ Failed payment: $XX from [description] |
| New subscription | Subscription created in the last hour | 🎉 New subscriber! Plan: [name], $XX/mo |
| Cancellation | Subscription cancelled in the last hour | 📉 Cancellation: [customer], was on [plan] |

To check for recent events (last 60 minutes):
```bash
ONE_HOUR_AGO=$(( $(date -u +%s) - 3600 ))

# Recent events
curl -s -u "$STRIPE_KEY:" \
  "https://api.stripe.com/v1/events?limit=50&created[gte]=${ONE_HOUR_AGO}&types[]=customer.subscription.created&types[]=customer.subscription.deleted&types[]=charge.failed" \
  | jq '.data[] | {type, created, data: .data.object}'
```

For real-time alerts without polling, configure a **Stripe Webhook** (optional):

1. Go to [dashboard.stripe.com/webhooks](https://dashboard.stripe.com/webhooks)
2. Add endpoint: your OpenClaw webhook URL
3. Select events: `charge.failed`, `customer.subscription.created`, `customer.subscription.deleted`
4. Store the webhook signing secret as `STRIPE_WEBHOOK_SECRET` (used to verify payloads)

Webhook support requires a publicly reachable OpenClaw instance. Polling (above) works without any webhook setup.

---

## Error Handling

| HTTP status | Meaning | Action |
|-------------|---------|--------|
| 401 | Invalid API key | Ask operator to verify `STRIPE_SECRET_KEY` |
| 403 | Restricted key missing permission | Check key permissions in Stripe dashboard |
| 429 | Rate limited | Wait and retry with exponential backoff |
| 5xx | Stripe outage | Check [status.stripe.com](https://status.stripe.com), retry later |

On 429, use this pattern:
```bash
RETRY_AFTER=$(curl -sI -u "$STRIPE_KEY:" "https://api.stripe.com/v1/balance" \
  | grep -i "retry-after" | awk '{print $2}' | tr -d '\r')
sleep "${RETRY_AFTER:-5}"
```

---

## Notes

- All amounts from Stripe are in **smallest currency unit** (cents for USD/EUR). Always divide by 100 before displaying.
- MRR calculation normalizes annual and weekly plans to monthly. This is an approximation.
- The Stripe API paginates at 100 items. For businesses with >100 active subscriptions, always paginate (see MRR pattern above).
- Test mode keys (`sk_test_...`) work identically — the status check will flag `livemode: false` so you don't accidentally report test data as real.
