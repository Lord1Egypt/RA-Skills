---
name: uniprofit-mail-assistant
description: Send emails through the UniProfit OpenClaw-compatible API with a user-created `mail_send` API key. Use when Codex or OpenClaw needs to deliver an already-approved email through a verified UniProfit mail account.
metadata:
  openclaw:
    emoji: ✉️
    requires:
      env: ["UNIPROFIT_API_BASE_URL", "UNIPROFIT_MAIL_SEND_KEY"]
      bins: ["python"]
---

# UniProfit Mail Assistant

Use this skill to send emails through UniProfit.

## Quick Start

Required environment variables:

- `UNIPROFIT_API_BASE_URL`
- `UNIPROFIT_MAIL_SEND_KEY`

Credential format:

```http
X-UniProfit-Key: {UNIPROFIT_MAIL_SEND_KEY}
```

Read only what you need:

- Read `references/api.md` for request and response formats.
- Read `references/mail-constraints.md` for sending prerequisites and safety checks.
- Read `references/error-handling.md` when the API returns a send failure.

## Protocol Contract

For runtime execution, follow this protocol exactly.

Use only these runtime endpoints:

- `GET {UNIPROFIT_API_BASE_URL}/openclaw/credential/me`
- `GET {UNIPROFIT_API_BASE_URL}/openclaw/mail/account/list`
- `POST {UNIPROFIT_API_BASE_URL}/openclaw/mail/send`

Execution checklist:

- send authentication with `X-UniProfit-Key`
- send mail requests as `POST`
- send mail requests with a JSON body
- keep `account_id`, `to_email`, `subject`, and `body` in the request body

Do not replace this skill with generic mail-delivery endpoints.

Canonical runtime pattern:

1. validate the credential if needed with `GET /openclaw/credential/me`
2. fetch available sender accounts with `GET /openclaw/mail/account/list`
3. ask the user to choose sender email from that list
4. map selected email to `account_id` and execute send with `POST /openclaw/mail/send`
5. report the confirmed send status

Run `scripts/check_credential.py` if the credential may be missing or invalid.

## Use This Skill When

- the user clearly wants actual delivery
- recipient, subject, and final body content are already known
- the send should go through a bound UniProfit mail account

Do not use this skill for:

- trade lead search
- email generation or rewriting
- sending when key facts are still missing

## Input Requirements

Require all of:

- selected sender email (from account list)
- recipient email
- subject
- final email body

Then map the selected sender email to its `account_id` before calling the send endpoint.
If any send-critical field is missing, stop and ask for it rather than sending.

## Execution Flow

1. Confirm the user wants actual delivery.
2. Fetch available sender accounts via `GET /openclaw/mail/account/list`.
3. Ask the user to select one sender email from the returned list.
4. Ensure send-critical fields are present.
5. Run `scripts/send_mail.py`, or make the same protocol call to `POST /openclaw/mail/send` with `X-UniProfit-Key` and a JSON body.
6. Report send result clearly.

Never imply an email was sent unless the API confirms success.

## Output Style

Return:

- recipient
- send status
- record id or message id if present

Keep the explanation short and practical.
