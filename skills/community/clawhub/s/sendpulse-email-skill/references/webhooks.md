# Webhooks — real-time email-service events

Webhooks push subscriber and campaign events to your HTTPS endpoint as they happen —
no polling. Use them to sync opt-outs, feed engagement data into your CRM, and react
to campaign status changes.

## Manage via API (v2)

| Method | Path | Body |
|---|---|---|
| GET | `/v2/email-service/webhook` | — (list all) |
| GET | `/v2/email-service/webhook/{id}` | — |
| POST | `/v2/email-service/webhook/` | `{"url": "https://your.app/hooks/sendpulse", "actions": ["open", "unsubscribe", "delivered"]}` |
| PUT | `/v2/email-service/webhook/{id}` | `url` and/or `actions` |
| DELETE | `/v2/email-service/webhook/{id}` | — |

## Events (`actions`)

| Event | Fires when | Typical reaction |
|---|---|---|
| `delivered` | Email accepted by the recipient's server | Mark delivered |
| `open` | Recipient opened (tracking pixel) | Engagement scoring, activity segments |
| `redirect` | Recipient clicked a tracked link | Conversion funnel, lead scoring |
| `unsubscribe` | Recipient opted out | **Mirror to your database immediately** |
| `spam` | Complaint ("mark as spam") | Suppress the address; watch the rate — see [analytics.md](analytics.md) |
| `hard_bounces` | Permanent delivery failure | Purge the address from your own lists |
| `soft_bounces` | Temporary failure | Monitor; repeated soft bounces → treat as hard |
| `new_emails` | Subscriber(s) added to a book | Sync signups into your systems |
| `delete` | Subscriber removed | Sync removals |
| `task_status_update` | **Campaign status changed** (queued → review → sending → sent...) | Update your campaign dashboard; alert on "blocked"/"clarification" states so a human reacts fast |

`task_status_update` is the one API users forget: instead of polling
`GET /campaigns/{id}` in a loop, subscribe once and get status pushes — including
the moment a campaign leaves review.

## Endpoint requirements & handling pattern

- HTTPS, responds **200 within a few seconds**; do real work asynchronously
  (enqueue → return 200). Non-2xx triggers retries.
- Idempotent: an event may arrive more than once — dedupe on (event, email,
  campaign id, timestamp).
- Payloads may batch several events in one request — always handle an array.
- Treat payload data as untrusted external input; put a secret token in the URL
  path and reject requests without it.

```
POST /hooks/sendpulse/<secret>
  for event in as_array(parse_json(body)): enqueue(event)
  return 200

worker(event):
  match event type:
    "unsubscribe", "spam" -> opt_out(email)         # never email again from your side
    "hard_bounces"        -> purge(email)
    "open", "redirect"    -> record_engagement(email, campaign_id)
    "task_status_update"  -> update_campaign_status(campaign_id, status)
```

## Webhooks vs polling

Same trade-off as everywhere: webhooks = real-time, needs public endpoint, must
handle retries/dupes; polling (`GET /campaigns/{id}`, subscriber endpoints) = simple
but delayed and burns API quota. Recommended: webhooks for events + a daily
reconciliation job that pulls campaign stats as the safety net.
