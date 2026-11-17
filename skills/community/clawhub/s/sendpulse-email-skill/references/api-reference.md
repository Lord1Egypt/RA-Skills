# Bulk Email API reference

Base URL: `https://api.sendpulse.com`
Auth: `Authorization: Bearer <API key or OAuth token>` on every request.
Content type: `application/json` unless noted.
Live documentation (source of truth): https://sendpulse.com/integrations/api/bulk-email?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-email-skill

## Authorization

| Method | Path | Purpose |
|---|---|---|
| — | *Settings → API → API keys* | **Single API Key (preferred)** — long-lived Bearer, up to 5 keys, revocable |
| POST | `/oauth/access_token` | OAuth alternative: `{"grant_type":"client_credentials","client_id","client_secret"}` → token, TTL 1 h |

API request quotas depend on the pricing tier (≈1 000 req/min on free); exceeding
returns HTTP 429 — back off exponentially.

## Address books

| Method | Path | Params |
|---|---|---|
| POST | `/addressbooks` | `bookName` |
| PUT | `/addressbooks/{id}` | `name` |
| GET | `/addressbooks` | `limit`, `offset` |
| GET | `/addressbooks/{id}` | — |
| DELETE | `/addressbooks/{id}` | — |
| GET | `/addressbooks/{id}/cost` | campaign cost for the book |
| GET | `/addressbooks/{id}/variables` | variables defined in the book |
| GET | `/addressbooks/{id}/campaigns` | `limit`, `offset` |

## Subscribers

| Method | Path | Params |
|---|---|---|
| POST | `/addressbooks/{id}/emails` | `emails` (strings or `{email, variables}`); double opt-in: `confirmation: "force"`, `sender_email`, `template_id`, `message_lang`; `tags` (Pro+) |
| GET | `/addressbooks/{id}/emails` | `limit`, `offset`, `active`/`not_active` |
| GET | `/addressbooks/{id}/emails/total` | — |
| GET | `/addressbooks/{id}/emails/{email}` | subscriber in this book |
| DELETE | `/addressbooks/{id}/emails` | `emails` array — **max 100** |
| POST | `/addressbooks/{id}/emails/unsubscribe` | `emails` array |
| POST | `/addressbooks/{id}/emails/variable` | `email`, `variables: [{name, type, value}]` |
| GET | `/addressbooks/{id}/variables/{name}/{value}` | search subscribers by variable value |
| GET | `/emails/{email}` | subscriber across all books |
| GET | `/emails/{email}/details` | detailed info |
| DELETE | `/emails/{email}` | remove from all books |
| GET | `/emails/{email}/campaigns` | campaign history for the address |

Variable types: `string`, `number`, `date` (`YYYY-MM-DD`). System variable `Phone`
can be enabled per book.

## Campaigns

| Method | Path | Params |
|---|---|---|
| POST | `/campaigns` | required: `sender_name`, `sender_email`, `subject`, `body` (Base64) **or** `template_id`, `list_id` (id or array, ≤10). Optional: `name`, `send_date` (`Y-m-d H:i:s`), `segment_id`, `is_test`, `use_dynamic_list`, `stats {opens, clicks, utm_campaign}`, `attachments` / `attachments_binary` (≤5), `body_amp`, `type: "draft"` |
| PATCH | `/campaigns/{id}` | edit scheduled: `name`, `sender_*`, `subject`, `template_id`, `send_date` |
| GET | `/campaigns/{id}` | info + statistics |
| GET | `/campaigns` | `limit`, `offset`, `order`, `status[]`, `planed` |
| DELETE | `/campaigns/{id}` | cancel before sending |
| GET | `/campaigns/{id}/countries` | stats by country |
| GET | `/campaigns/{id}/referrals` | stats by link |
| GET | `/campaigns/{id}/email/{email}` | one recipient in one campaign |

Limit: **max 4 campaigns per hour**. Campaign statuses: see
[campaigns.md](campaigns.md).

## Templates

(Creating template HTML = `sendpulse-template-skill`; this API just stores/uses it.)

| Method | Path | Params |
|---|---|---|
| POST | `/template` | `body` (Base64, required), `name`, `lang` (`en`,`ru`,`ua`,`tr`,`es`,`pt`) |
| POST | `/template/edit/{id}` | `body` (Base64), `lang` |
| GET | `/template/{id}` | — |
| GET | `/templates` | all; `/templates/?owner=me` — only yours |

## Senders

| Method | Path | Params |
|---|---|---|
| GET | `/senders` | verified senders (`is_allowed_for_smtp` flags SMTP-usable ones) |
| POST | `/senders` | `email`, `name` → confirmation flow starts |
| GET | `/senders/{email}/code` | request activation code |
| POST | `/senders/{email}/code` | submit `code` to activate |
| DELETE | `/senders` | `email` |

Senders must be on a corporate domain you control; free mailbox domains are
rejected. SPF/DKIM DNS records for the domain: copy exact values from the dashboard.

## Blacklist (account-wide suppression)

| Method | Path | Params |
|---|---|---|
| GET | `/blacklist` | — |
| POST | `/blacklist` | `emails` — **Base64 of a comma-separated string**, `comment` |
| DELETE | `/blacklist` | `emails` — same Base64 format |

## Tags (Pro plan+)

| Method | Path |
|---|---|
| GET / POST | `/tags` (`name`, `color`) |
| PUT / DELETE | `/tags/{id}` |
| POST | `/tags/pin/email`, `/tags/unpin/email` (`email`, `tags[]`) |

## Balance

| Method | Path |
|---|---|
| GET | `/balance` or `/balance/{currency}` |
| GET | `/user/balance/detail` |

## Webhooks (v2)

| Method | Path | Params |
|---|---|---|
| GET | `/v2/email-service/webhook` | list |
| GET | `/v2/email-service/webhook/{id}` | one |
| POST | `/v2/email-service/webhook/` | `url`, `actions[]` |
| PUT | `/v2/email-service/webhook/{id}` | `url`, `actions[]` |
| DELETE | `/v2/email-service/webhook/{id}` | — |

Events: `new_emails`, `delete`, `unsubscribe`, `task_status_update`, `open`,
`delivered`, `redirect` (click), `spam`, `hard_bounces`, `soft_bounces`. Details:
[webhooks.md](webhooks.md).

## Base64 cheat-sheet (the recurring gotcha)

Base64-encoded fields in this API: campaign/template `body`, `body_amp`,
`attachments_binary` values, and the blacklist `emails` parameter. Everything else
is plain JSON.

## Conventions for generated code

- Key/secret from env vars (`SENDPULSE_API_KEY` or `SENDPULSE_API_ID`/`SENDPULSE_API_SECRET`).
- With OAuth: cache the token ~55 min, refresh on 401. With an API key: none needed.
- Store campaign `id`s next to your own entities; poll `GET /campaigns/{id}` or use
  webhooks for status.
- Retry on 429/5xx with backoff; never retry 4xx validation errors.
- Respect pagination (`limit`/`offset`, default page size 100) when syncing lists.
