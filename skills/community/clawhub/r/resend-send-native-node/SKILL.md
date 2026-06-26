---
name: resend-send-native-node
description: Send email via Resend.com's HTTPS API - native Node.js, zero dependencies. Use when the user explicitly asks to email, send a message, mail a report, or deliver a notification to an email address. Externally sends email only with --send; defaults to dry-run and requires RESEND_ALLOWED_TO allowlist for real sends. Requires RESEND_API_KEY in the process environment for real sends. No OAuth, no 2FA, no Gmail required.
version: 1.0.12
risk_class: external-email-send-dry-run-default-send-gated
---

# Resend Send Native Node

Send email via the Resend.com HTTPS API.

Native Node.js. Zero dependencies. One POST call for real sends. Small enough to audit directly.

## When to use

Trigger phrases: "email me", "send an email", "mail this to", "send a notification", "email the report".

**Use this when:**
- The user wants to send an email fast, without Gmail OAuth or App Password pain
- Simple "fire and forget" sends (no inbox reading needed)
- The user has a Resend.com account (check Resend's current pricing/limits before relying on a specific quota)
- Weekly/report-style outbound messages where the body is generated from explicitly reviewed text

**Do NOT use this when:**
- The user wants to READ email (this is send-only)
- The user needs to send from a specific personal Gmail address (use a Gmail-specific skill)
- Sensitive business emails where provenance matters (Resend's default `onboarding@resend.dev` sender looks transactional)
- The recipient, sender, or final body has not been explicitly reviewed/approved for a real send

## Safety policy for agents

This skill is send-only, but it is still externally mutating. For agent use:

1. **Draft first.** Generate or inspect the exact body text before sending.
2. **Dry-run first.** The script dry-runs by default; review the printed payload.
3. **Explicit approval.** Use `--send` only after the user explicitly approves the exact `to`, `cc`, `bcc`, `from`, `reply-to`, `subject`, and body. Treat `reply-to` as response-routing control and review display-name text in `from` for spoof-like wording before any real send.
4. **Use an allowlist.** Real sends fail closed unless `RESEND_ALLOWED_TO=addr@example.com,other@example.com` is set in the process environment for approved recipients.
5. **No raw memory dumps.** Email only curated report text, not unfiltered memory, transcripts, logs, or private workspace context.

## How to run

The script is in `scripts/send.mjs`. Requires Node.js 18+ because real sends use native `fetch` and `AbortController`.

For operator workflows, prefer `--json` so dry-runs and real sends produce a stable machine-readable receipt with `mode`, `sent`, recipients, subject, body byte count, full body SHA-256, SHA-256 prefix, allowlist status, and `resendId` on successful real sends.

**Basic:**
```powershell
node "<skill-dir>/scripts/send.mjs" --to "you@example.com" --subject "Hello" --body "Hi there"
```

Without `--send`, this prints a dry-run payload and does **not** send. Dry-run output includes the full reviewed body JSON plus body byte length and SHA-256 prefix; redact dry-run logs before sharing externally.

**With from address override:**
```powershell
node "<skill-dir>/scripts/send.mjs" --from "Example Sender <onboarding@resend.dev>" --to "you@example.com" --subject "Hello" --body "Hi"
```

**HTML body:**
```powershell
node "<skill-dir>/scripts/send.mjs" --html --to "you@example.com" --subject "Styled" --body "<h1>Hi</h1><p>Hello</p>"
```

**Dry run (no send, just print the payload):**
```powershell
node "<skill-dir>/scripts/send.mjs" --dry-run --to "you@example.com" --subject "Test" --body "..."
```

**Real send (only after explicit approval):**
```powershell
node "<skill-dir>/scripts/send.mjs" --send --to "you@example.com" --subject "Weekly report" --body "Approved report text"
```

### All flags

| Flag | Required? | Purpose |
|---|---|---|
| `--to` | yes | Comma-separated recipient addresses |
| `--subject` | yes | Message subject |
| `--body` | yes | Inline message body |
| `--cc` | no | Comma-separated cc |
| `--bcc` | no | Comma-separated bcc |
| `--from` | no | Override sender, e.g. `"Example Sender <onboarding@resend.dev>"` |
| `--reply-to` | no | Reply-to address |
| `--html` | no | Body is HTML instead of plain text |
| `--dry-run` | no | Don't send; print the JSON payload |
| `--send` | no | Actually send. Without this, the script dry-runs by default |
| `--json` | no | Print a stable JSON receipt for dry-run or real send |
| `-h`, `--help` | no | Show help |

Recipients in `--to`, `--cc`, `--bcc`, and `--reply-to` must be bare email addresses. Only `--from` accepts display-name format such as `"Reports <reports@example.com>"`.

`--body-file` is intentionally not supported in the public package. Review file contents yourself and pass approved text with `--body`.

## Credentials

Requires process environment values:

- `RESEND_API_KEY` - starts with `re_...`
- `RESEND_ALLOWED_TO` - comma-separated recipient allowlist for real sends
- Real sends require `RESEND_ALLOWED_TO`; without it the script refuses `--send`

**How to get one:**
1. Sign up at https://resend.com and check the current pricing/limits for the account
2. Go to **API Keys** in the dashboard
3. Click **Create API Key**, name it, and choose the least-privilege sending permission available for your account
4. Copy the key

Export it in the runtime process environment:
```powershell
$env:RESEND_API_KEY="<your-resend-key>"
$env:RESEND_ALLOWED_TO="you@example.com,reports@example.com"
```

## Sender identity

By default, emails are sent from `onboarding@resend.dev` - Resend's default sender. This may support quick testing subject to current Resend account restrictions; use a verified domain/sender for production-style mail.

**For a custom domain (later, optional):**
1. Add your domain to Resend at https://resend.com/domains
2. Configure DNS records they provide
3. Use a verified sender with `--from "Reports <reports@your-verified-domain.example>"`

## What this skill does

- Reads `RESEND_API_KEY` from the process environment only
- POSTs a JSON request to `https://api.resend.com/emails`
- Prints a one-line confirmation with the Resend message ID
- Defaults to dry-run unless `--send` is present
- Validates basic recipient address shape before sending
- Enforces `RESEND_ALLOWED_TO` for real sends; fail-closed if it is missing
- Prints body byte length and SHA-256 prefix in dry-run so reviewed content can be matched to the send
- Supports `--json` receipt output so automation can compare the reviewed body hash to the send receipt and capture `resendId` without scraping human text

## What this skill does NOT do

- Does not read or manage email (this is send-only)
- Does not read local files or support `--body-file`
- Does not write any files
- Does not make network calls other than to `api.resend.com`
- Does not auto-update
- Does not support attachments in this version

## Output

On success:
```
sent to you@example.com (subject: Hello) - resend-id: c8f43f2a-...
```

With `--json`, dry-runs and sends emit parseable JSON. Successful real sends include `sent: true`, `bodySha256`, `bodySha256Prefix`, and `resendId`.

On failure, clear error on stderr with a non-zero exit code.

## Troubleshooting

- **"RESEND_API_KEY not set"** - create one at https://resend.com, check current pricing/limits, and export `RESEND_API_KEY` in the process environment
- **HTTP 401** - API key is invalid or was revoked
- **HTTP 403** - API key doesn't have send permission, or the from address can only send to the account owner until a domain is verified (check dashboard). On Windows, a Node.js cleanup assertion may appear after a 403 exit; this is cosmetic and does not indicate a successful send.
- **HTTP 422** - the from address isn't verified on your Resend account (use `onboarding@resend.dev` or verify your own domain)
- **HTTP 429** - rate limited; check https://resend.com/pricing or the Resend dashboard for current limits
- **Network error or timeout** - transient, but a network/timeout/read error after the request was sent does not prove the email was not delivered. Check the Resend dashboard before retrying to avoid duplicate sends.

## Sample output

Sanitized representative output for eval/review checks:

```text
$ node scripts/send.mjs --to "you@example.com" --subject "Hello" --body "Hi there"
--- DRY RUN: request would be sent ---
note: add --send to perform a real send after explicit approval.
body: 8 bytes, sha256:8328c36d18b7
WARNING: RESEND_ALLOWED_TO is not configured. Real sends will fail closed until an allowlist is set.
POST https://api.resend.com/emails
Authorization: Bearer [redacted]

{
  "from": "onboarding@resend.dev",
  "to": [
    "you@example.com"
  ],
  "subject": "Hello",
  "text": "Hi there"
}

$ node scripts/send.mjs --send --to "you@example.com" --subject "Hello" --body "Hi there"
error: RESEND_ALLOWED_TO must be set for real sends. Refusing --send without a recipient allowlist.

# PowerShell:
$env:RESEND_ALLOWED_TO="you@example.com"; node scripts/send.mjs --send --to "you@example.com" --subject "Hello" --body "Hi there"
# bash/zsh:
# RESEND_ALLOWED_TO="you@example.com" node scripts/send.mjs --send --to "you@example.com" --subject "Hello" --body "Hi there"
error: RESEND_API_KEY not set in process environment. Create one at https://resend.com, check current pricing/limits, and export RESEND_API_KEY.
```

## Account limits

Resend pricing and free-tier limits can change. Check the current Resend dashboard/pricing page before relying on a specific daily/monthly quota or paid-tier price. New accounts commonly support quick testing from `onboarding@resend.dev`; use a verified domain/sender for production-style mail.

## Changelog

- `1.0.12`: ClawHub publication/version refresh after JSON receipt fix and public-readiness review; no additional runtime behavior change.
- `1.0.11`: Add `--json` structured receipts for dry-run and real send output so operators can capture stable subjects, body hashes, allowlist status, and `resendId` without scraping human text.
- `1.0.10`: Clarify explicit approval must cover all delivery/reply headers (`to`, `cc`, `bcc`, `from`, `reply-to`), subject, and body before real sends.
- `1.0.9`: Add explicit Node.js 18+ usage prerequisite and offline gate-regression tests for dry-run, allowlist fail-closed, missing-key fail-closed, HTML/reply-to payloads, unsupported body-file, invalid recipients, and help output.
- `1.0.8`: Soften public Resend account/default-sender wording to avoid stale pricing/free-tier/domain-setup assumptions.
- `1.0.7`: Fix no-allowlist sample output, document bare-recipient requirement and dry-run body visibility, add 30s send timeout, and warn to verify Resend dashboard before retrying ambiguous network/timeout failures.
- `1.0.6`: Add frontmatter version metadata, hedge rate-limit wording, document Windows 403 cleanup assertion behavior, and include sanitized dry-run/fail-closed sample outputs for eval review.
- `1.0.5`: Public package wording and metadata cleanup; send behavior remains dry-run-first with `--send` plus recipient allowlist required for real sends.

