# SendPulse SMTP — project rules for Gemini

> Copy this file into your project root as `GEMINI.md` (or merge into an
> existing one). Keep the full skill folder in the repo — paths below assume
> `docs/sendpulse-smtp-skill/`; adjust if cloned elsewhere.

When the task involves SendPulse email sending (SMTP API, transactional email,
smtp-pulse.com relay, bounces, unsubscribes, deliverability, webhooks), read
`docs/sendpulse-smtp-skill/SKILL.md` first and follow it. Detailed references:

- `docs/sendpulse-smtp-skill/references/quickstart.md` — token + first email
- `docs/sendpulse-smtp-skill/references/setup.md` — account activation, sender verification, SPF/DKIM
- `docs/sendpulse-smtp-skill/references/api-reference.md` — all endpoints
- `docs/sendpulse-smtp-skill/references/errors.md` — troubleshooting order
- `docs/sendpulse-smtp-skill/references/deliverability.md` — list hygiene, warm-up
- `docs/sendpulse-smtp-skill/references/webhooks.md` — event handling
- `docs/sendpulse-smtp-skill/references/smtp-relay.md` — smtp-pulse.com:465 (SSL)
- `docs/sendpulse-smtp-skill/references/email-service-api.md` — campaigns vs SMTP
- `docs/sendpulse-smtp-skill/examples/` — curl, PHP, Python, Node.js code

Hard rules (apply even without reading the references):

1. OAuth: `POST https://api.sendpulse.com/oauth/access_token`, cache the Bearer
   token (1 h TTL), refresh on 401, credentials from env vars only.
2. `POST /smtp/emails`: `html` MUST be Base64-encoded; include a `text` part;
   `to` is an array of objects; `from.email` must be a verified sender on a
   corporate domain.
3. Store the returned message `id` for status lookups (`GET /smtp/emails/{id}`).
4. Check `GET /smtp/unsubscribe/search?email=` before sending; sync bounces
   daily; mirror opt-outs via `POST /smtp/unsubscribe`.
5. Newsletters to lists → Email Service API (campaigns), not a loop over
   `/smtp/emails`.
6. Backoff-retry on 429/5xx only.
