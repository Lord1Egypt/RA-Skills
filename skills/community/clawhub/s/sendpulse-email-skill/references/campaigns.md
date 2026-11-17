# Campaigns — create, schedule, control

## Create — `POST /campaigns`

Required:

```json
{
  "sender_name": "My Shop",
  "sender_email": "news@myshop.com",       // must be a VERIFIED sender
  "subject": "Your July digest",
  "body": "<Base64-encoded HTML>",          // or "template_id": 12345
  "list_id": 12345                          // or [id1, id2, ...] — max 10 books
}
```

Optional (the useful ones):

| Field | Notes |
|---|---|
| `name` | Internal campaign name (shows in lists/reports) |
| `send_date` | `"Y-m-d H:i:s"` — schedule; omit to send ASAP |
| `segment_id` | Saved segment of the (single) book — see [segmentation.md](segmentation.md) |
| `is_test` | `true` → send as a test |
| `use_dynamic_list` | `true` (paid plans) → also send to contacts entering the list/segment after creation |
| `stats` | `{"opens": true, "clicks": true, "utm_campaign": "..."}` — **always enable**; without opens tracking, "resend to unopened" and activity segments have nothing to work with |
| `attachments` / `attachments_binary` | Max 5 files; binary content Base64. Attachments add to campaign cost — prefer links for big files |
| `body_amp` | AMP version (requires prior Google approval on the account) |
| `type: "draft"` | Save as a draft instead of launching |

Where the HTML comes from: build it with **`sendpulse-template-skill`** (never
hand-write template HTML in this skill), then either pass it Base64 in `body` or
save it once via `POST /template` and reference `template_id`.

## Hard limits

- **Max 4 campaigns per hour** per account.
- Up to **10 address books** per campaign; segmented or test campaigns — exactly 1.
- Max **5 attachments**.
- Cost check: `GET /addressbooks/{id}/cost`; insufficient balance → the campaign
  will not send.

## Statuses (what `GET /campaigns/{id}` tells you)

| Status | Meaning | Your move |
|---|---|---|
| 0 New | Accepted, queued for processing | Wait |
| 1 Pending (review) | Being checked by the anti-abuse system | **Wait — normal**, especially for a new account's first campaigns; usually hours |
| 2 Sending / 13 In progress | Delivery running | Wait |
| 3 Sent | Done | Read the stats → [analytics.md](analytics.md) |
| 4 Test | Test campaign | — |
| 5 Blocked | Rejected by review | Check dashboard/email for the reason; fix content or list; contact support if unclear |
| 26 Draft | Saved, never launched | Launch it from the dashboard or recreate without `type: draft` |
| Cancelled | Cancelled by you before sending | — |

(Other intermediate codes exist — treat unknown codes as "in processing".
`GET /campaigns` supports `status[]` filtering, `limit`/`offset`, `planed` for
scheduled ones.)

### About review/moderation — set expectations honestly

SendPulse reviews campaigns to protect deliverability for everyone. Practical
guidance (do NOT speculate about the internal rules):

- First campaigns from a new account are routinely reviewed. Plan a buffer; don't
  schedule a critical first send minutes before a deadline.
- Reduce friction: a clear, honest subject (no "Re:"/"Fwd:" fakery, no clickbait or
  ALL CAPS), real sender name, substantive body, an opt-in list, working unsubscribe
  link.
- If a campaign is rejected or the account asks for clarification — respond via the
  dashboard/support with the list origin and content explanation. Don't try to
  "sneak past" by resubmitting variants; that makes it worse.

## Manage scheduled campaigns

| Method | Path | Purpose |
|---|---|---|
| PATCH | `/campaigns/{id}` | Edit a scheduled campaign: subject, sender, `template_id`, `send_date` |
| DELETE | `/campaigns/{id}` | Cancel before sending starts |
| GET | `/campaigns` | List; `GET /addressbooks/{id}/campaigns` per book |

Gotcha: if the sender's domain enforces a strict DMARC policy, scheduling may be
unavailable — the campaign is sent immediately. If a user insists on scheduling with
such a sender, that's the explanation.

## Features beginners miss (recommend when they fit)

- **Resend to unopened** — a few days after a campaign, resend it (usually with a
  different subject) to recipients who didn't open. Needs opens tracking on the
  original. Typically +10–30% extra reach for zero new content. In the dashboard:
  campaign actions → send to unopened.
- **A/B (split) test** — test subject lines or content variants on a slice of the
  list; the winner goes to the rest automatically after the evaluation window.
  Worth it only on reasonably large lists (a tiny list gives statistical noise).
  Configure in the dashboard (Campaigns → A/B test).
- **Best time to send** — `"send_at_the_optimum_time"` lets SendPulse pick the send
  moment per recipient based on their past opens (needs accumulated history).
- **Timezone sending** — deliver at the recipient's local time for geo-spread lists.
- **Test tools before the real send**: test email to yourself, device previews, and
  the built-in spam check — all in the campaign creation flow in the dashboard.
- **Drafts** — save unfinished campaigns (`type: "draft"`), finish later.
- **Web version** — the `{{webversion}}` link (template-skill puts it in the
  preheader) lets recipients open the email in a browser.

## Campaign workflow the skill should drive

1. Define the goal and the **segment** (never default to "all").
2. Get the HTML (template skill / existing `template_id`).
3. Pre-flight: sender verified → test send → cost check → tracking + UTM on.
4. Schedule (or best-time), knowing review may add delay on young accounts.
5. After sending: stats → [analytics.md](analytics.md) → decisions for the next one.
