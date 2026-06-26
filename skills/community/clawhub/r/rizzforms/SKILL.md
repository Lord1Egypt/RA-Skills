---
name: rizzforms
description: |
  Create forms, configure webhook delivery, manage submissions, and generate
  embed HTML using the RizzForms API and bundled CLI. Use this skill whenever
  the user asks to add a contact form, feedback form, signup form, lead capture
  form, waitlist form, or any form that collects submissions and delivers them
  via webhook. Also use when the user mentions RizzForms, wants to check form
  submissions, manage webhooks, or integrate a form backend into their site —
  even if they don't say "form backend" explicitly.
---

# RizzForms — Form Backend Skill

Create forms that collect submissions and deliver them via webhook — no server
code required. RizzForms handles storage, spam filtering, and delivery.

## Bundled CLI

This skill includes a CLI at `scripts/rizzforms`. Use it instead of writing raw
curl commands — it handles authentication, pretty-prints JSON, and has commands
for every API operation.

```bash
# Make sure it's executable
chmod +x <skill-path>/scripts/rizzforms

# Set the API key (or run `rizzforms config` interactively)
export RIZZFORMS_API_KEY="frk_..."

# Now use it
<skill-path>/scripts/rizzforms forms
<skill-path>/scripts/rizzforms forms:create "Contact Form"
```

Run `<skill-path>/scripts/rizzforms help` for the full command list.

## Prerequisites

You need a RizzForms API key with the **admin** role (prefix `frk_`).

**Check for an API key:** Look for `RIZZFORMS_API_KEY` in the environment or
`~/.config/rizzforms/config`.

**If no API key exists:**
1. Sign up at https://forms.rizzness.com/signup
2. Go to Account Settings > API Keys > Create API Key (select Admin role)
3. Set it: `export RIZZFORMS_API_KEY="frk_..."`

## Important: Two Subdomains

RizzForms uses two subdomains — using the wrong one is a common mistake:

| Subdomain | Purpose |
|---|---|
| `forms.rizzness.com` | Form submissions only (`/f/` and `/json/` routes) |
| `www.rizzness.com` | API, dashboard, docs (`/api/` routes) |

HTML form `action` and JSON submission URLs use `forms.rizzness.com`.
API management calls use `www.rizzness.com`.
The CLI handles this automatically.

## Workflow

### Step 1: Create a form

```bash
<skill-path>/scripts/rizzforms forms:create "Contact Form"
```

The response includes `endpoint_token`, `submission_url`, `json_url`,
`embed_html`, and `examples` with ready-to-use curl commands.

Save the `endpoint_token` — you need it for every subsequent step.

### Step 2: Configure a webhook (optional)

If the user wants submissions delivered to an external URL:

```bash
<skill-path>/scripts/rizzforms plugins:create <endpoint_token> "https://their-server.com/webhook"
```

Requirements:
- URL must use HTTPS
- URL must not resolve to a private/reserved IP
- **Save the `signing_secret`** from the response — it's shown only once

The webhook receives a JSON POST on each submission:
```json
{
  "id": 12345,
  "created_at": "2026-03-22T12:00:00Z",
  "form_id": "abc123",
  "form_name": "Contact Form",
  "ip": "203.0.113.42",
  "user_agent": "Mozilla/5.0...",
  "referrer": "https://yoursite.com/contact",
  "data": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "message": "Hello!"
  }
}
```

Each webhook includes an `X-RizzForms-Signature` header (HMAC-SHA256 of the
body using the signing secret). See `references/api.md` for verification
examples in Ruby, Node.js, and Python.

### Step 3: Test the pipeline

```bash
<skill-path>/scripts/rizzforms test <endpoint_token>
```

This sends a test submission with `?test=true` for synchronous delivery results.
You can also pass custom JSON:

```bash
<skill-path>/scripts/rizzforms test <endpoint_token> '{"name": "Test", "email": "test@example.com"}'
```

If the webhook returns non-2xx or times out, the delivery status will be
`"failed"` with an error message.

### Step 4: Generate HTML

Use the `embed_html` from the form creation response, or build a custom form.
Always include the hidden honeypot field `_hp` for spam protection.

```html
<form action="https://forms.rizzness.com/f/{endpoint_token}" method="POST">
  <label for="name">Name</label>
  <input type="text" id="name" name="name" required>

  <label for="email">Email</label>
  <input type="email" id="email" name="email" required>

  <label for="message">Message</label>
  <textarea id="message" name="message" required></textarea>

  <!-- Honeypot — keep hidden, critical for spam protection -->
  <input type="text" name="_hp" style="display:none" tabindex="-1" autocomplete="off">

  <button type="submit">Send</button>
</form>
```

RizzForms captures ALL form fields — there is no fixed schema. Add phone,
company, budget, file upload, radio buttons, checkboxes — whatever is needed.

**Match the user's CSS framework:**
- **Tailwind CSS:** utility classes (`class="block w-full rounded-md border..."`)
- **Bootstrap 5:** Bootstrap classes (`class="form-control"`, `class="mb-3"`)
- **Plain CSS:** semantic HTML, no framework classes

### Step 5: Install in the user's project

Place the HTML form in the appropriate location in the codebase. The form
`action` URL points to RizzForms — no server-side code is needed.

For server-side/AJAX submissions, POST JSON to
`https://forms.rizzness.com/json/{endpoint_token}` instead.

## Managing Existing Forms

```bash
# List all forms
<skill-path>/scripts/rizzforms forms

# Show form details (includes submission count, spam rate, plugin status)
<skill-path>/scripts/rizzforms forms:show <token>

# Update a form
<skill-path>/scripts/rizzforms forms:update <token> --name "New Name"
<skill-path>/scripts/rizzforms forms:update <token> --redirect "https://site.com/thanks"
<skill-path>/scripts/rizzforms forms:update <token> --active false

# List/manage plugins
<skill-path>/scripts/rizzforms plugins <token>
<skill-path>/scripts/rizzforms plugins:delete <token> <plugin_id>
<skill-path>/scripts/rizzforms plugins:rotate <token> <plugin_id>
```

## Viewing Submissions

```bash
# Recent submissions (default: last 24h)
<skill-path>/scripts/rizzforms submissions

# Filter by form and time range
<skill-path>/scripts/rizzforms submissions --form <token> --range 7d

# Search submissions
<skill-path>/scripts/rizzforms submissions --search "jane@example.com"

# View a specific submission
<skill-path>/scripts/rizzforms submissions:show <id>

# View spam
<skill-path>/scripts/rizzforms spam --form <token>
```

## Spam Prevention

RizzForms has three layers of spam protection:

1. **Honeypot fields** — Hidden `_hp` (or `_gotcha`) field. Bots fill it, submission gets marked as spam. Always include this in your HTML.
2. **Turnstile CAPTCHA** — Cloudflare Turnstile invisible challenge, enabled in the dashboard.
3. **Rate limiting** — 60 submissions per minute per IP per form. Returns HTTP 429 when exceeded.

## Special Fields

These field names get automatic normalization (stored in `special_normalized`):

| Field | Normalization |
|---|---|
| `email` | Whitespace trimmed |
| `firstName`, `lastName` | Whitespace trimmed |
| `name` | Auto-computed from firstName + lastName if both present |
| `tags` | CSV string converted to array |
| `priority` | Lowercased, validated: low/medium/high/urgent |
| `urgent` | Coerced to boolean |
| `_optin` | Coerced to boolean (marketing opt-in) |

All fields are always stored as-is in `payload_json` regardless of normalization.

## Error Handling

All errors return `{"ok": false, "error": "code", "message": "..."}`.

| Status | Error | Meaning |
|--------|-------|---------|
| 401 | `invalid_api_key` | API key missing, invalid, or expired |
| 403 | `forbidden` | Key lacks required permission |
| 404 | `not_found` | Form/plugin not found or wrong account |
| 404 | `not_active` | Form is deactivated — reactivate with `--active true` |
| 422 | `unsupported_plugin` | Only "webhook" type supported via API |
| 422 | `invalid_config` | Webhook URL invalid, not HTTPS, or private IP |
| 503 | `service_unavailable` | Temporary — retry shortly |

## Full API Reference

For complete endpoint details, webhook signing verification code, and framework
quick-starts (Next.js, Astro, Hugo), see `references/api.md`.
