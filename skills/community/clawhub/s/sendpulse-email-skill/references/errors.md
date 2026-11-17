# Errors & troubleshooting

"Campaign not sending" is almost always answered by **reading the campaign status**
— start there, not with the code.

## 1. HTTP-level errors

| HTTP | Meaning | Fix |
|---|---|---|
| 401 Unauthorized | Missing/invalid/expired token | API key: check it exists and wasn't revoked (*Settings → API*). OAuth: token TTL is 1 h — refresh. Verify the `Authorization: Bearer` header. |
| 403 Forbidden | Account/feature not allowed | Feature above your plan (tags = Pro+, dynamic lists = paid), or account restricted — check the dashboard for banners. |
| 404 | Wrong path or unknown id | Check endpoint spelling, book/campaign id. |
| 400 / 422 | Validation failed | Read the JSON body — it names the field. Common: `body` not Base64, missing required campaign field, bad `send_date` format (`Y-m-d H:i:s`), invalid `list_id`. |
| 429 | API request quota exceeded | Exponential backoff; batch reads. |
| 5xx | Service-side | Retry with backoff; persistent → support. |

## 2. Campaign creation rejected (POST /campaigns fails)

| Symptom / message | Cause | Fix |
|---|---|---|
| Sender invalid / not found | `sender_email` not in `GET /senders` or not activated | Add & verify the sender first; corporate domain only. |
| Not enough funds / credits | Plan/balance can't cover the recipients (attachments add cost) | Check `GET /addressbooks/{id}/cost` and `/balance`; shrink the segment, drop attachments, or top up. |
| Book not found / empty / no active addresses | Wrong `list_id`, or everyone in the book is unsubscribed/invalid | Verify the id; check `GET /addressbooks/{id}` counts and subscriber statuses. |
| Too many campaigns | **4 campaigns/hour** limit hit | Wait, or consolidate sends. |
| Multiple books rejected | >10 books, or segment/test used with several books | ≤10 books; `segment_id`/`is_test` → exactly one book. |
| Scheduling refused / campaign sent immediately | Sender domain has a strict DMARC policy | Known behavior — use another verified sender/domain if scheduling matters. |
| Body/template error | `body` not Base64, or `template_id` doesn't exist | Encode the HTML; check `GET /templates/?owner=me`. |

## 3. Campaign created but "stuck" — status decoder

`GET /campaigns/{id}` → status:

| Status | Reality | Action |
|---|---|---|
| New / queued | Normal processing | Wait minutes. |
| **Pending review** | Anti-abuse check; routine for a new account's first campaigns | **Wait — this is not an error.** Usually resolves within hours. Don't recreate the campaign repeatedly — it doesn't help. |
| Awaiting clarification | The service has questions (usually list origin) | Answer via dashboard/support: where the list came from, what you send. Sending resumes after. |
| Blocked | Rejected by review | Read the reason in the dashboard/email. Fix the cause (content honesty, list consent, unsubscribe link) and contact support. Do not resubmit cosmetic variants. |
| No credits | Balance ran out mid-flight | Top up; campaign may be resumed/partially sent. |
| No active addresses | Everything in the target was unsendable | Check subscriber statuses; import hygiene ([address-books.md](address-books.md)). |
| Sent partially | Some recipients skipped (limits/errors) | Check stats + error breakdown. |
| Cancelled | You cancelled it | Recreate when ready. |
| Draft | Never launched | Launch from the dashboard or recreate without `type: draft`. |

## 4. Subscribers not getting added

| Symptom | Cause | Fix |
|---|---|---|
| Address accepted but inactive | Double opt-in pending (`confirmation: force`) | The subscriber must click the confirmation link; check their spam folder. |
| Address rejected / stays excluded | Unsubscribed earlier, bounced, or on the account blacklist | Respect it. Check `GET /emails/{email}` and `GET /blacklist`. Genuine re-opt-in → remove from blacklist / let them re-subscribe via a form. |
| DELETE fails on big batch | >100 addresses per call | Chunk to 100. |
| Variables not saved | Wrong structure (`variables` must be an object on add; typed array on the variable endpoint), bad date format | Dates: `YYYY-MM-DD`; check the exact schema in [api-reference.md](api-reference.md). |

## 5. "Sent successfully but results are bad"

That's not an error — that's analytics. Go to [analytics.md](analytics.md) for the
metric-by-metric playbook (opens, clicks, unsubscribes, complaints, bounces).

## 6. Account-level blocks

If the dashboard shows the account or a book blocked/limited: it is usually about
list quality (bounces/complaints) or unclear list origin. Path back: explain the
list source to support, clean the list (Email Verifier, drop inactive), switch to
double opt-in. Prevention beats cure: [list-building.md](list-building.md).

## When stuck

Live API docs: https://sendpulse.com/integrations/api/bulk-email?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-email-skill ·
Knowledge base: https://sendpulse.com/knowledge-base?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-email-skill ·
Support via the dashboard chat — include campaign id, timestamps, and the full JSON
response.
