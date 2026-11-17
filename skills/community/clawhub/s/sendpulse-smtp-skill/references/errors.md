# Errors & troubleshooting

Diagnose in this order — each step rules out a whole class of failures.

## 0. Read the response

Failures come as an HTTP status + JSON body with a message and often a numeric
`error_code`. Always show the raw response body when debugging — the message
usually names the problem.

## 1. HTTP-level errors

| HTTP | Meaning | Fix |
|---|---|---|
| 401 Unauthorized | Token missing/expired/invalid, or wrong `client_id`/`client_secret` | Refresh the token (TTL 1 h). Verify credentials from *Account Settings → API*. Check the `Authorization: Bearer` header is actually sent. |
| 403 Forbidden | Account not allowed to do this (not activated, blocked, IP not in whitelist) | See section 2. |
| 404 Not Found | Wrong path or unknown message id | Check the endpoint spelling and the id. |
| 415 / 400 with parse error | Body is not valid JSON or `Content-Type: application/json` missing | Fix headers/body. |
| 429 Too Many Requests | API rate limit exceeded | Exponential backoff; batch status checks via `POST /smtp/emails/info` (500 ids/call) instead of per-id GETs. |
| 5xx | SendPulse-side issue | Retry with backoff; if persistent, check https://status.sendpulse.com or support. |

## 2. Account-state errors (send rejected for every request)

| Symptom / message | Cause | Fix |
|---|---|---|
| "not activated", sending forbidden while auth works | SMTP moderation not passed | Fill the sender profile in *SMTP → Settings*, wait ≤24 h for moderation. |
| Account blocked banner in dashboard | Bounce/spam-complaint rate exceeded thresholds | Clean the list (drop bounces, honor unsubscribes), contact support via the unblock form. |
| Works from server A, fails from server B with authorization-type error | API IP whitelist enabled | Add B's IP to the whitelist or disable it. |
| "Not supported with your account type" | Feature not available on the free plan | Upgrade the plan. |

## 3. Request-validation errors

| Symptom / message | Cause | Fix |
|---|---|---|
| Sender is invalid / not allowed | `from.email` not verified, or on a free mail domain | Use a verified sender on your own domain (`GET /smtp/senders` shows valid ones). |
| "Please do not use free email services" | Sender on gmail.com/mail.ru/etc. | Sender must be on a corporate domain. |
| "E-mail already exists" when adding sender | Address already added / pending confirmation | Check spam folder for the confirmation email; re-request verification. |
| "Maximum number of domains" | Plan's sender-domain limit reached | Remove unused domains or upgrade. |
| Empty/garbled email body received | `html` was not Base64-encoded | Encode `html`; keep `text` plain. |
| Recipient rejected / silently not delivered | Address on the unsubscribe blocklist or bounced earlier | `GET /smtp/unsubscribe/search?email=...`; if legitimately re-opted-in, `POST /smtp/resubscribe` (max 5/24 h) or `DELETE /smtp/unsubscribe`. |
| "Missed 'to'/'from'/'subject'..." | Malformed body — e.g. `to` not an array of objects | Match the schema in [api-reference.md](api-reference.md) exactly. |
| Attachment ignored/corrupted | Binary file put into `attachments` instead of `attachments_binary` | Base64 the file and use `attachments_binary`. |
| Balance / limit exceeded | Monthly email volume of the plan is spent | Check plan usage in dashboard; upgrade or buy extra volume. |

## 4. "Sent successfully but not received"

`{"result": true}` means SendPulse **accepted** the message, not that it was
delivered. Then:

1. `GET /smtp/emails/{id}` — check the real delivery status.
2. Status *bounced* → read the bounce reason (mailbox full, address doesn't exist,
   rejected by policy).
3. Status *delivered* but user doesn't see it → **spam folder**. That's a
   deliverability problem, not an API problem → [deliverability.md](deliverability.md):
   verify SPF/DKIM pass (send to yourself, read the headers), review content.
4. Nothing arrives to one specific provider (e.g. only Gmail) → usually reputation
   or missing DMARC alignment for that provider.

## 5. SMTP relay errors (when not using the REST API)

| SMTP reply | Meaning | Fix |
|---|---|---|
| 535 Authentication failed | Wrong login/password | Copy exact values from *SMTP → Settings → General*. Password is the SMTP password, not necessarily the dashboard one. |
| Connection timeout on port 25 | ISP/host blocks port 25 | Use 465 (SSL) or 2525/587. |
| 550 sender rejected | From-address not verified | Verify the sender first. |
| Relay works but mail in spam | DNS not configured | SPF/DKIM → [setup.md](setup.md). |

## When stuck

Live API docs: https://sendpulse.com/integrations/api/smtp?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-smtp-skill ·
Knowledge base: https://sendpulse.com/knowledge-base/smtp?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-smtp-skill ·
Support: via the dashboard chat. Include the message `id`, timestamp, and full
JSON response when contacting support.
