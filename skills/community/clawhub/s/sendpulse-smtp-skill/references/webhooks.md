# Webhooks — real-time email events

Webhooks push delivery events to your HTTPS endpoint the moment they happen, so
you don't poll `GET /smtp/emails/{id}`. Use them to update order/user records,
trigger retries, and feed your own analytics.

## Available events

| Event | Meaning | Typical reaction |
|---|---|---|
| `delivered` | Accepted by the recipient's mail server | Mark as delivered |
| `undelivered` | Delivery failed (see bounce type in payload) | Log reason; hard failure → suppress the address |
| `hard_bounced` | Permanent failure (mailbox doesn't exist) | **Remove address from your list permanently** |
| `soft_bounced` | Temporary failure (mailbox full, server busy) | Retry later; drop after repeated soft bounces |
| `opened` | Recipient opened the email (tracking pixel) | Engagement analytics |
| `clicked` | Recipient clicked a tracked link | Engagement analytics / conversion funnel |
| `spam` | Recipient hit "Report spam" | **Suppress the address immediately**; if rate grows, stop and review the list |
| `unsubscribed` | Recipient used the unsubscribe link | Mirror the opt-out in your own database |
| `resubscribed` | Recipient re-confirmed subscription | Re-enable in your database |

## Setup

1. Dashboard: **SMTP → Settings → Webhooks** → add your endpoint URL and pick the
   events. (Requires an activated SMTP account.)
2. The endpoint must be **HTTPS**, respond **200 within a few seconds**, and be
   idempotent — events can occasionally be delivered more than once.
3. Do the heavy work asynchronously: enqueue the payload and return 200
   immediately. Non-2xx responses cause retries.

## Handling pattern (pseudocode)

```
POST /webhooks/sendpulse-smtp
  payload = parse_json(request.body)      # may contain one event or an array
  for event in as_array(payload):
      enqueue(event)                       # process out-of-band
  return 200

worker(event):
  match event.event / event.type:
    "hard_bounced", "spam" -> suppress(event.email)   # never email again
    "unsubscribed"         -> opt_out(event.email)
    "delivered"            -> mark_delivered(event.smtp_answer_data or event.id)
    ...
```

Match events back to your entities via the message `id` you stored when calling
`POST /smtp/emails`, or via the recipient address + timestamp.

## Security

- Put a hard-to-guess token in the webhook URL path
  (`/webhooks/sp/9f2c.../`) and reject requests without it.
- Optionally restrict by SendPulse IPs (`GET /smtp/ips` lists your sending IPs;
  webhook source IPs are documented in the knowledge base).
- Never trust payload fields blindly — treat them as external input.

## Webhooks vs polling

| | Webhooks | Polling (`/smtp/emails`, `/smtp/bounces/day`) |
|---|---|---|
| Latency | Seconds | Minutes–hours |
| Rate-limit pressure | None | Counts against API quota |
| Infra needed | Public HTTPS endpoint | Just a cron job |
| Reliability | Must handle retries/dupes | Simple, easy to backfill |

Recommended: webhooks for real-time state + a **daily polling job on
`/smtp/bounces/day` as a safety net** (catches anything a webhook missed).
