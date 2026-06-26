# skill-stripe-monitor

**Your Stripe revenue dashboard, right inside your agent.**

MRR, active subscribers, churn, failed payments, and top products — on demand or on a daily schedule. No dashboard tab required.

---

## What it does

`skill-stripe-monitor` connects to your Stripe account via a read-only API key and surfaces the metrics that matter most for subscription businesses:

- **MRR** — calculated from all active subscriptions, normalised across billing intervals
- **New subscribers** — count for the current month
- **Churn** — cancellations this month and churn rate
- **Failed payments** — last 7 days, with amounts and descriptions
- **Top products** — top 5 by revenue over the last 30 days
- **Balance** — available and pending, with live vs. test mode indicator

Entirely read-only. It never modifies charges, refunds, subscriptions, or any Stripe data.

---

## Installation

```bash
clawhub install skill-stripe-monitor
```

Requires a Stripe API key (see Setup below).

---

## Setup

Get a **Restricted Key** from [dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys) with read-only access to: `customers`, `subscriptions`, `invoices`, `charges`, `products`, `prices`.

Then set it as an environment variable:

```bash
export STRIPE_SECRET_KEY="sk_live_..."
```

Or add it to your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "skills": {
    "entries": {
      "stripe-monitor": {
        "apiKey": "sk_live_..."
      }
    }
  }
}
```

Verify with: *"Check my Stripe connection"* or `/stripe status`.

---

## Commands

| Command | What it does |
|---------|-------------|
| `/stripe status` | Quick health check — live mode, currency, recent activity |
| `/stripe mrr` | Current MRR and 30-day trend |
| `/stripe subscribers` | Active count, new this month, churn this month |
| `/stripe failures` | Failed payments in the last 7 days |
| `/stripe top` | Top 5 products by revenue (last 30 days) |
| `/stripe summary` | Full daily summary — all of the above |

---

## How to use it

**Check MRR:**
> "What's my MRR this month?"

**Check for failed payments:**
> "Any failed payments today?"

**Full revenue snapshot:**
> "Give me a Stripe summary."

**Subscriber activity:**
> "How many new subscribers did we get this month? Any cancellations?"

---

## Scheduled daily summary

Add to `HEARTBEAT.md` to receive a daily Stripe briefing:

```markdown
## Daily Stripe Summary
- Time: 08:00 CET
- Action: Run /stripe summary and send to Telegram
```

---

## Alerts

The skill reacts immediately (without being asked) when it detects:

| Event | Alert |
|-------|-------|
| Failed payment | ⚠️ Failed payment: $XX from [description] |
| New subscription | 🎉 New subscriber! Plan: [name], $XX/mo |
| Cancellation | 📉 Cancellation: [customer], was on [plan] |

---

## Requirements

- `STRIPE_SECRET_KEY` environment variable (or OpenClaw config entry)
- `curl` and `jq` installed on the host
- Read-only Stripe API key recommended (Restricted Key)

---

## Support

- ClawHub: [clawhub.com/@ordo-tech](https://clawhub.com/@ordo-tech)
- Gumroad: [theagentgordo.gumroad.com](https://theagentgordo.gumroad.com/)
