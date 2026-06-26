---
name: resend
description: "Send and manage emails via the Resend CLI. Covers sending, domains, contacts, segments, broadcasts, templates, topics, webhooks, and API keys."
homepage: https://github.com/resend/resend-cli
source: https://github.com/resend/resend-cli
license: MIT
metadata:
  emoji: "📧"
  primaryEnv: RESEND_API_KEY
  requires:
    bins: ["resend"]
    env: ["RESEND_API_KEY"]
  configPaths:
    - "~/.config/resend/credentials.json"
  install:
    - id: resend-brew
      kind: brew
      tap: resend/cli
      formula: resend
      bins: ["resend"]
      label: "Install Resend CLI (brew)"
---

# Resend CLI — Email for Developers

Official CLI for [Resend](https://resend.com). Covers sending, domains, contacts, segments, broadcasts, templates, webhooks, and API keys.

## Prerequisites

- Install: `brew install resend/cli/resend` (recommended) or `npm install -g resend-cli`
- Auth: `resend login` or set `RESEND_API_KEY` env var
- Credentials stored at: `~/.config/resend/credentials.json` (0600 permissions)
- For automation, use a domain-scoped `sending_access` key (not full-access) when possible

## Auth

Key priority: `--api-key` flag > `RESEND_API_KEY` env var > `~/.config/resend/credentials.json`.

Always use `--json` or `--quiet` flag for non-interactive (agent) usage — forces JSON output, no spinners.

## Quick Reference

### Emails

```bash
# Send
resend emails send \
  --from "Name <you@yourdomain.com>" \
  --to recipient@example.com \
  --subject "Subject" \
  --text "Body" \
  --json

# Send with HTML file
resend emails send --from you@domain.com --to user@example.com \
  --subject "Newsletter" --html-file ./email.html --json

# Send with attachments
resend emails send --from you@domain.com --to user@example.com \
  --subject "Report" --text "See attached" --attachment ./report.pdf --json

# Schedule for later
resend emails send --from you@domain.com --to user@example.com \
  --subject "Later" --text "Hi" --scheduled-at 2026-08-05T11:00:00Z --json

# With CC, BCC, reply-to, tags, headers
resend emails send --from you@domain.com --to user@example.com \
  --subject "Meeting" --text "Notes" \
  --cc manager@example.com --bcc archive@example.com \
  --reply-to noreply@example.com \
  --tags category=marketing --headers X-Entity-Ref-ID=123 --json

# Batch send (up to 100 emails from JSON file)
resend emails batch --file ./emails.json --json
# File format: [{"from":"...","to":["..."],"subject":"...","text":"..."},...]

# List sent emails
resend emails list --json

# Get email details
resend emails get <email-id> --json

# Cancel scheduled email
resend emails cancel <email-id> --json

# Update scheduled email
resend emails update <email-id> --scheduled-at 2026-08-06T09:00:00Z --json
```

### Inbound (Receiving) Emails

```bash
# List received emails
resend emails receiving list --json

# Get received email
resend emails receiving get <email-id> --json

# List attachments
resend emails receiving attachments <email-id> --json

# Get single attachment
resend emails receiving attachment <email-id> <attachment-id>

# Forward received email
resend emails receiving forward <email-id> \
  --to user@example.com --from you@domain.com --json
```

### Domains

```bash
# List domains
resend domains list --json

# Create domain (returns DNS records to configure)
resend domains create --name example.com --region eu-west-1 --tls enforced --json

# Create with receiving enabled
resend domains create --name example.com --sending --receiving --json

# Verify domain (trigger DNS check)
resend domains verify <domain-id> --json

# Get domain details + DNS records
resend domains get <domain-id> --json

# Update domain settings
resend domains update <domain-id> --tls enforced --open-tracking --json

# Delete domain
resend domains delete <domain-id> --yes --json
```

Domain lifecycle: create → configure DNS → verify → get (poll until "verified").
Regions: `us-east-1`, `eu-west-1`, `sa-east-1`, `ap-northeast-1`.

### Contacts

```bash
# List contacts
resend contacts list --json

# Create contact
resend contacts create --email jane@example.com \
  --first-name Jane --last-name Smith --json

# Create with properties + segments
resend contacts create --email jane@example.com \
  --properties '{"company":"Acme","plan":"pro"}' \
  --segment-id <segment-id> --json

# Get contact (by ID or email)
resend contacts get user@example.com --json

# Update contact
resend contacts update user@example.com --unsubscribed --json

# Delete contact
resend contacts delete <contact-id> --yes --json

# List contact's segments
resend contacts segments user@example.com --json

# Add contact to segment
resend contacts add-segment user@example.com --segment-id <id> --json

# Remove from segment
resend contacts remove-segment user@example.com <segment-id> --json

# List contact's topic subscriptions
resend contacts topics user@example.com --json

# Update topic subscriptions
resend contacts update-topics user@example.com \
  --topics '[{"id":"topic-uuid","subscription":"opt_in"}]' --json
```

### Segments

```bash
# List segments
resend segments list --json

# Create segment
resend segments create --name "Newsletter Subscribers" --json

# Get segment
resend segments get <segment-id> --json

# Delete segment (no update endpoint — delete + recreate to rename)
resend segments delete <segment-id> --yes --json
```

### Broadcasts

```bash
# Create draft
resend broadcasts create \
  --from hello@domain.com \
  --subject "Weekly Update" \
  --segment-id <segment-id> \
  --html "<p>Hello {{{FIRST_NAME|there}}}</p>" --json

# Create from HTML file
resend broadcasts create --from hello@domain.com \
  --subject "Launch" --segment-id <id> --html-file ./email.html --json

# Create + send immediately
resend broadcasts create --from hello@domain.com \
  --subject "Launch" --segment-id <id> --html "<p>Hi</p>" --send --json

# Create + schedule
resend broadcasts create --from hello@domain.com \
  --subject "News" --segment-id <id> --text "Hello!" \
  --send --scheduled-at "tomorrow at 9am ET" --json

# Send existing draft
resend broadcasts send <broadcast-id> --json

# List broadcasts
resend broadcasts list --json

# Get broadcast details
resend broadcasts get <broadcast-id> --json

# Update draft
resend broadcasts update <broadcast-id> --subject "Updated Subject" --json

# Delete broadcast
resend broadcasts delete <broadcast-id> --yes --json
```

Template variables in HTML: `{{{FIRST_NAME|Friend}}}` — triple-brace with optional fallback.

### Templates

```bash
# List templates
resend templates list --json

# Create template with variables
resend templates create --name "Welcome" \
  --subject "Welcome!" \
  --html "<h1>Hello {{{NAME}}}</h1>" \
  --var NAME:string --json

# Create with fallback
resend templates create --name "Invoice" \
  --subject "Invoice" \
  --html "<p>Amount: {{{AMOUNT}}}</p>" \
  --var AMOUNT:number:0 --json

# Get template
resend templates get <template-id> --json

# Update template
resend templates update <template-id> --subject "Updated Subject" --json

# Publish draft → live
resend templates publish <template-id> --json

# Duplicate template
resend templates duplicate <template-id> --json

# Delete template
resend templates delete <template-id> --yes --json
```

Lifecycle: create (draft) → update → publish. Re-publish after updating a published template.

### Topics

```bash
# List topics
resend topics list --json

# Create topic
resend topics create --name "Product Updates" --json

# Create with default opt-out
resend topics create --name "Weekly Digest" --default-subscription opt_out --json

# Get topic
resend topics get <topic-id> --json

# Update topic
resend topics update <topic-id> --name "Security Alerts" --json

# Delete topic
resend topics delete <topic-id> --yes --json
```

### Webhooks

```bash
# List webhooks
resend webhooks list --json

# Create webhook (all events)
resend webhooks create \
  --endpoint https://app.example.com/hooks/resend \
  --events all --json

# Get webhook
resend webhooks get <webhook-id> --json

# Update webhook
resend webhooks update <webhook-id> --status disabled --json

# Delete webhook
resend webhooks delete <webhook-id> --yes --json

# Listen locally (dev)
resend webhooks listen --json
```

Event types (17): email.sent, email.delivered, email.delivery_delayed, email.bounced, email.complained, email.opened, email.clicked, email.failed, email.scheduled, email.suppressed, email.received, contact.created, contact.updated, contact.deleted, domain.created, domain.updated, domain.deleted.

### API Keys

```bash
# List API keys
resend api-keys list --json

# Create full-access key
resend api-keys create --name "Production" --json

# Create domain-scoped sending key
resend api-keys create --name "CI Token" \
  --permission sending_access --domain-id <domain-id> --json

# Delete key (immediate, irreversible)
resend api-keys delete <api-key-id> --yes --json
```

### Utility

```bash
# Doctor — check CLI version, API key, domains, AI agent detection
resend doctor --json

# Who am I
resend whoami --json

# Open dashboard in browser
resend open

# Auth — switch profile
resend auth switch

# Login (non-interactive)
resend login --key re_xxx --json

# Logout
resend logout --json
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--api-key <key>` | Override API key for this command |
| `-p, --profile <name>` | Use specific profile |
| `--json` | Force JSON output |
| `-q, --quiet` | Suppress spinners (implies `--json`) |

## Agent Usage Rules

1. **Always use `--json` flag** — ensures structured output, no TTY prompts.
2. **All required flags must be provided** — no interactive prompts in non-TTY mode.
3. **Destructive actions need `--yes`** — deletes require confirmation bypass.
4. **Exit codes:** 0 = success, 1 = error. Errors include `message` + `code`.
5. **Batch limit:** 100 emails per `emails batch` request.
6. **Attachments not supported in batch sends.**
7. **`--scheduled-at` requires `--send` flag on broadcasts.**

## Error Codes

| Code | Cause |
|------|-------|
| `auth_error` | No API key found |
| `missing_body` | No --text/--html/--html-file |
| `file_read_error` | Can't read file |
| `send_error` | API rejected the send |
| `missing_key` | Login without --key in non-interactive |
| `validation_failed` | API rejected the key |
