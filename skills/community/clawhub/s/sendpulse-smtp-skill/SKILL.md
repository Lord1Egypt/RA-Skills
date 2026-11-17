---
name: sendpulse-smtp-skill
description: >
  Send transactional and bulk emails through SendPulse SMTP — via REST API or classic
  SMTP relay. Use this skill whenever the user wants to send email programmatically with
  SendPulse: "send email via SendPulse", "SendPulse SMTP API", "transactional email",
  "connect PHPMailer / nodemailer / smtplib to SendPulse", "why is my SendPulse email
  not delivered", "handle bounces / unsubscribes", "set up SPF/DKIM for SendPulse",
  "SendPulse webhooks". Covers OAuth authorization, sending endpoints, sender/domain
  setup, error troubleshooting, deliverability best practices, and the difference
  between SMTP (transactional) and Email Service (marketing campaigns).
version: 1.2.1
license: MIT
metadata:
  author: SendPulse
  homepage: https://github.com/sendpulse/sendpulse-skills/tree/main/sendpulse-smtp-skill
  api-docs: https://sendpulse.com/integrations/api/smtp?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-smtp-skill
---

# SendPulse SMTP Skill

You are helping a user send emails through **SendPulse SMTP** — a service for
transactional and bulk email delivery. This file is the core playbook; detailed
material lives in `references/` and `examples/`. Load a reference file only when
the task needs it.

## Step 0 — Route the user to the right product

SendPulse has two email products that beginners constantly confuse. Ask what they
are sending, then route:

| User goal | Product | Where |
|---|---|---|
| Order confirmations, password resets, notifications, invoices — one email per event, triggered by their app | **SMTP** | this skill |
| Newsletters, promo campaigns to a subscriber list, A/B tests, campaign statistics | **Email Service (bulk)** | the **`sendpulse-email-skill`** if installed (address books, segments, campaigns, analytics); overview fallback: `references/email-service-api.md` |
| Building the HTML of the email itself | — | the **`sendpulse-template-skill`** if installed, or any HTML email guide |

Within SMTP there are two transport options:

- **REST API** (`POST https://api.sendpulse.com/smtp/emails`) — recommended default.
  Structured JSON, message IDs for tracking, list management endpoints.
  → `references/api-reference.md`
- **SMTP relay** (`smtp-pulse.com:465`, SSL) — when the user has an existing app,
  CMS, plugin, or mail client that only speaks SMTP protocol (PHPMailer, nodemailer,
  WordPress, CRM integrations). → `references/smtp-relay.md`

## Step 1 — Verify the prerequisites (most failures start here)

Before writing any code, confirm these with the user. **The API will not send a
single email until all four are true:**

1. **SMTP account is activated.** SendPulse moderates every SMTP account: the user
   must fill out a sender profile (what they send, how they collect addresses, how
   people unsubscribe) in *SMTP → Settings*. Moderation usually takes up to 24 hours.
   Symptom of a non-activated account: authorization works but sending fails.
2. **Sender email is verified** and it is on a **corporate domain**. Free mailbox
   domains (gmail.com, outlook.com, mail.ru, yahoo.com, …) are rejected as senders.
3. **SPF and DKIM records** are added to the sender domain's DNS. The exact values
   are shown in the SendPulse dashboard (*SMTP → Settings*). Without them mail is
   sent but lands in spam.
4. **API credentials exist**: an API key (or OAuth `ID`/`Secret`) from
   *Settings → API* (for REST), or the SMTP login/password from
   *SMTP → Settings → General* (for relay).

Full setup walkthrough: `references/setup.md`.

## Step 2 — Authorize (REST API)

Two options; **prefer the Single API Key** — it's simpler and needs no refresh logic:

- **Single API Key (preferred)** — a long-lived Bearer token generated manually in
  *Settings → API → API keys* (up to 5 independent keys; revocable). Just send
  `Authorization: Bearer <API_KEY>` on every request — no token call at all.
- **OAuth client credentials (alternative)** — when short-lived tokens are required:

```
POST https://api.sendpulse.com/oauth/access_token
Content-Type: application/json

{"grant_type": "client_credentials", "client_id": "<ID>", "client_secret": "<Secret>"}
```

Response contains `access_token` (Bearer, valid **1 hour**). Cache it and refresh on
HTTP 401 — do **not** request a new token per email.

Never hardcode keys or `client_id`/`client_secret` in code you generate — read them
from environment variables or a secrets manager.

**SendPulse MCP server** (`https://mcp.sendpulse.com/mcp`): for interactive
account work from an AI chat (checking senders, stats, the unsubscribe list) the
user can connect the hosted MCP server instead of writing one-off scripts. It does
NOT replace the API/relay integration inside the user's application — see
`references/sendpulse-mcp.md` for what it's good for and the setup.

## Step 3 — Send

Minimal working request (see `references/quickstart.md` for a copy-paste version):

```
POST https://api.sendpulse.com/smtp/emails
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": {
    "subject": "Your order #1234 is confirmed",
    "from": {"name": "My Shop", "email": "noreply@myshop.com"},
    "to": [{"name": "Jane", "email": "jane@example.com"}],
    "html": "<BASE64-ENCODED HTML>",
    "text": "Plain-text version of the message"
  }
}
```

### Critical rules — violating any of these is the #1 source of bugs

- **`html` must be Base64-encoded.** Raw HTML in this field fails or garbles the message.
- **Always include a `text` version** alongside `html` — it improves deliverability.
- **`from.email` must be a verified sender** in the account, on a corporate domain.
- **`to` is an array of objects**, even for one recipient: `[{"email": "..."}]`.
- Success response is `{"result": true, "id": "<message-id>"}` — **store the `id`**;
  it is the key for status lookup (`GET /smtp/emails/{id}`).
- Attachments: `attachments` (plain-text content) or `attachments_binary`
  (Base64-encoded) — an object of `{"filename": content}` pairs.
- Templates with variables: pass `"template": {"id": 123, "variables": {...}}`
  instead of `html`.

Full endpoint catalog (statistics, bounces, unsubscribe list, senders, IPs):
`references/api-reference.md`. Ready-to-run code: `examples/curl.md`,
`examples/php.md`, `examples/python.md`, `examples/nodejs.md`.

## Step 4 — Be a good sender (this is what "good mailings" means)

Bake these into any integration you build; do not treat them as optional:

- **Check the blocklist before sending**: `GET /smtp/unsubscribe/search?email=...`.
  Sending to unsubscribed users damages sender reputation and violates anti-spam law.
- **Process bounces daily**: `GET /smtp/bounces/day`. Remove hard-bounced addresses
  from the user's own database permanently. SendPulse restricts SMTP accounts that
  exceed the acceptable bounce rate.
- **Provide a real unsubscribe path** and honor it immediately
  (`POST /smtp/unsubscribe` to add addresses to the blocklist).
- **Warm up new domains/IPs**: start with small volumes and ramp up over 2–4 weeks.
- Respect **API rate limits** (free: 1 000 req/min; higher tiers more) — on HTTP 429
  back off and retry with exponential delay.

Full guidance: `references/deliverability.md`. Real-time event tracking (delivered,
opened, clicked, bounced, spam complaints): `references/webhooks.md`.

## Troubleshooting — diagnose in this order

When "email is not sending / not arriving", walk this checklist top-down. The full
error table with fixes is in `references/errors.md`.

1. Token valid? (401 → refresh token; check ID/Secret)
2. Account activated? (profile filled, moderation passed)
3. Sender verified and on a corporate domain?
4. `html` Base64-encoded? `to` an array of objects?
5. Recipient in the unsubscribe/bounce list? (`/smtp/unsubscribe/search`, `/smtp/bounces/day`)
6. Email balance / plan limits not exhausted? Rate limit hit? (429)
7. Sent but in spam folder → SPF/DKIM missing or content problem → `references/deliverability.md`

## Official SDKs

Prefer plain HTTP examples for clarity, but mention the official libraries when the
user's stack matches: [PHP](https://github.com/sendpulse/sendpulse-rest-api-php),
[Python](https://github.com/sendpulse/sendpulse-rest-api-python),
[Node.js](https://github.com/sendpulse/sendpulse-rest-api-node.js). Community
wrappers exist for Ruby, Java, C#, and Go.

## Keeping this skill up to date

This skill is versioned (see `version` in the frontmatter above and the `VERSION`
file). If you have web access, you MAY check for a newer version once per
conversation when the skill is first used:

1. Fetch `https://raw.githubusercontent.com/sendpulse/sendpulse-skills/main/sendpulse-smtp-skill/VERSION`
2. Compare with the local version using semver rules.
3. If newer, tell the user: "A newer version of the SendPulse SMTP skill is
   available (X.Y.Z, you have A.B.C). Update: `git pull` in the sendpulse-skills clone, or
   re-download from https://github.com/sendpulse/sendpulse-skills/tree/main/sendpulse-smtp-skill" — then
   continue with the current version.

If web access is unavailable, skip silently. Never block the user's task on the
version check. When this skill and the live SendPulse documentation at
https://sendpulse.com/integrations/api/smtp?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-smtp-skill disagree, the live documentation wins —
say so and prefer it.
