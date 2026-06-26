# RizzForms API Reference

Complete API documentation. The SKILL.md covers the common workflow — this file
has the full endpoint details for when you need them.

## Table of Contents

- [Authentication](#authentication)
- [API Discovery](#api-discovery)
- [Forms API](#forms-api)
- [Submissions API](#submissions-api)
- [Plugins API](#plugins-api)
- [Ingest Endpoints](#ingest-endpoints)
- [Webhook Signing Verification](#webhook-signing-verification)
- [Framework Quick Starts](#framework-quick-starts)

---

## Authentication

All API endpoints require:
```
Authorization: Bearer frk_your_api_key
```

**Roles:**
- `admin` — full access: create/update forms, manage plugins, read submissions
- `readonly` — read submissions only

**Permission scopes:**
| Permission | Allows |
|---|---|
| `can_create_forms` | Create/update forms, create/delete/rotate plugins |
| `can_read_submissions` | List and read non-spam submissions |
| `can_read_spam_submissions` | List and read spam submissions |

---

## API Discovery

### GET /api/

HATEOAS root. Returns links to all available resources based on your key's
permissions. Navigate the API by following links, not by guessing URLs.

```json
{
  "ok": true,
  "account_id": 789,
  "links": [
    {"rel": "self", "href": "/api/", "method": "GET"},
    {"rel": "forms", "href": "/api/forms", "method": "GET"},
    {"rel": "create_form", "href": "/api/forms", "method": "POST"},
    {"rel": "submissions", "href": "/api/submissions", "method": "GET"},
    {"rel": "spam_submissions", "href": "/api/submissions/spam", "method": "GET"}
  ]
}
```

---

## Forms API

Base: `https://www.rizzness.com`

### POST /api/forms — Create Form

Requires: `can_create_forms`

```json
{"name": "Contact Form"}
```

Response includes: `endpoint_token`, `submission_url`, `json_url`, `embed_html`,
`examples` (curl commands), `help` (setup guidance).

### GET /api/forms — List Forms

Returns array with: `id`, `name`, `endpoint_token`, `is_active`,
`submission_url`, `json_url`, `embed_html`, `submission_count`,
`submission_spam_count`, `last_submission_at`, `notification_email_addresses`,
`examples`, `help`.

### GET /api/forms/:endpoint_token — Form Detail

Same fields as list, for a single form.

### PATCH /api/forms/:endpoint_token — Update Form

Requires: `can_create_forms`

Updatable fields:
- `name` (string)
- `success_redirect_url` (string — redirect after HTML form submission)
- `is_active` (boolean)
- `notification_email_addresses` (array of email strings)

```json
{"success_redirect_url": "https://yoursite.com/thanks", "is_active": true}
```

---

## Submissions API

Base: `https://www.rizzness.com`

### GET /api/submissions — List Submissions

Requires: `can_read_submissions`

Query params:
- `form_id` — endpoint_token or form ID
- `range` — `24h` (default), `7d`, `30d`
- `q` — search referrer and payload

Max 500 results, ordered by `created_at` descending.

### GET /api/submissions/:id — Submission Detail

Returns: `id`, `form_id`, `form_endpoint_token`, `source_ip`, `user_agent`,
`referrer`, `payload_json` (raw fields), `special_normalized` (normalized
fields), `created_at`.

### GET /api/submissions/spam — Spam Submissions

Requires: `can_read_spam_submissions`. Same filters as regular submissions.

---

## Plugins API

Base: `https://www.rizzness.com`

### GET /api/forms/:endpoint_token/plugins — List Plugins

Returns array with: `id`, `key`, `name`, `enabled`, `config`.

### POST /api/forms/:endpoint_token/plugins — Create Webhook

Requires: `can_create_forms`. Only `webhook` type is supported via API.

```json
{"plugin_type": "webhook", "config": {"url": "https://yoursite.com/webhook"}}
```

Response includes `signing_secret` — shown once. Save it for signature
verification.

URL must be HTTPS. Private/reserved IPs are blocked (SSRF protection).

### DELETE /api/forms/:endpoint_token/plugins/:id — Remove Plugin

Requires: `can_create_forms`.

### POST /api/forms/:endpoint_token/plugins/:id/rotate_secret — Rotate Secret

Requires: `can_create_forms`. Returns new `signing_secret`.

---

## Ingest Endpoints

Base: `https://forms.rizzness.com` (different subdomain!)

These are public — no authentication required.

### POST /f/:endpoint_token — HTML Form Submission

Standard form POST. Redirects to thank-you page on success.
Default redirect: `/f/:endpoint_token/thanks`.
Custom redirect: set `success_redirect_url` via API.

### POST /json/:endpoint_token — JSON Submission

```bash
curl -X POST "https://forms.rizzness.com/json/TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "message": "Hello"}'
```

Response: `{"ok": true, "id": 12345, "links": [...]}`

**Test mode** — append `?test=true`:
```json
{"ok": true, "id": 12345, "test": true, "deliveries": [
  {"plugin": "webhook", "status": "success", "response_code": 200}
]}
```

---

## Webhook Signing Verification

Every webhook POST includes `X-RizzForms-Signature` — HMAC-SHA256 of the
request body using your `signing_secret`.

### Ruby
```ruby
expected = OpenSSL::HMAC.hexdigest("SHA256", signing_secret, request.body.read)
halt 401 unless Rack::Utils.secure_compare(expected, request.env["HTTP_X_RIZZFORMS_SIGNATURE"])
```

### Node.js
```javascript
const crypto = require("crypto");
const expected = crypto.createHmac("sha256", signingSecret)
  .update(rawBody).digest("hex");
if (expected !== req.headers["x-rizzforms-signature"]) {
  return res.status(401).end();
}
```

### Python
```python
import hmac, hashlib
expected = hmac.new(
    signing_secret.encode(), request.data, hashlib.sha256
).hexdigest()
if not hmac.compare_digest(
    expected, request.headers.get("X-RizzForms-Signature", "")
):
    abort(401)
```

---

## Framework Quick Starts

### Next.js
```jsx
// app/contact/page.tsx
export default function Contact() {
  return (
    <form action="https://forms.rizzness.com/f/YOUR_TOKEN" method="POST">
      <input type="email" name="email" required />
      <textarea name="message" required />
      <input type="text" name="_hp" style={{display: "none"}} tabIndex={-1} />
      <button type="submit">Send</button>
    </form>
  );
}
```

For server-side: POST to `/json/YOUR_TOKEN` from an API route or Server Action.

### Astro
```astro
---
// src/pages/contact.astro
---
<form action="https://forms.rizzness.com/f/YOUR_TOKEN" method="POST">
  <input type="email" name="email" required />
  <textarea name="message" required></textarea>
  <input type="text" name="_hp" style="display:none" tabindex="-1" />
  <button type="submit">Send</button>
</form>
```

### Hugo
```html
<!-- layouts/partials/contact-form.html -->
<form action="https://forms.rizzness.com/f/{{ .Site.Params.rizzformsToken }}" method="POST">
  <input type="email" name="email" required>
  <textarea name="message" required></textarea>
  <input type="text" name="_hp" style="display:none" tabindex="-1">
  <button type="submit">Send</button>
</form>
```

Add to `hugo.toml`: `[params]` > `rizzformsToken = "YOUR_TOKEN"`

### Rails ERB
```erb
<%# app/views/contact/new.html.erb %>
<%= form_tag "https://forms.rizzness.com/f/#{ENV['RIZZFORMS_TOKEN']}", method: :post do %>
  <%= email_field_tag :email, nil, required: true %>
  <%= text_area_tag :message, nil, required: true %>
  <%= text_field_tag :_hp, nil, style: "display:none", tabindex: "-1", autocomplete: "off" %>
  <%= submit_tag "Send" %>
<% end %>
```
