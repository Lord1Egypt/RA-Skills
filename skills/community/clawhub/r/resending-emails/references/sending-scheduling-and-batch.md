# Sending, scheduling, and batch operations

This file covers the transactional sending surface of the Resend CLI.

## `emails send`

Use this for one logical email.

### Required flags

- `--from`
- `--to`
- `--subject`
- one of:
  - `--text`
  - `--html`
  - `--html-file`

### High-value optional flags

- `--cc`
- `--bcc`
- `--reply-to`
- `--scheduled-at`
- `--attachment`
- `--headers key=value`
- `--tags name=value`
- `--idempotency-key`

### Agent recommendations

- Prefer `--html-file` for long content.
- Use `--idempotency-key` whenever retries are plausible.
- Prefer explicit ISO timestamps for transactional schedules.
- Keep `--from` on an exact verified domain/subdomain.

Sample:

```bash
resend --json -q emails send \
  --from "Acme <alerts@example.com>" \
  --to user@example.com \
  --subject "Password reset" \
  --html-file ./newsletter.html \
  --idempotency-key password-reset-001
```

## Scheduling transactional emails

The CLI surface for `emails send` and `emails update` documents **ISO 8601** style scheduling for
transactional email. Use that in agent-generated commands because it is explicit and reproducible.

Useful follow-ups:

```bash
resend --json -q emails update <email-id> --scheduled-at 2026-03-15T08:00:00Z
resend --json -q emails cancel <email-id>
```

### Scheduling limits

Resend supports scheduling up to 30 days in advance. Keep that underlying product limit in mind when
you generate future-dated plans.

## `emails batch`

Use batch sends for up to **100 distinct transactional emails** in one request.

### File format

`emails batch` expects a JSON file containing an array of email objects.

Bundled sample:

- `assets/batch-emails.json`

### Important batch rules

- hard limit: 100 emails per request
- unsupported per-email fields:
  - `attachments`
  - `scheduled_at`
- optional idempotency key exists for the whole batch
- validation mode can be `strict` or `permissive`

Sample:

```bash
resend --json -q emails batch --file ./batch-emails.json --idempotency-key shipment-batch-001
```

### Chunking rule

If the user needs 250 notifications:

1. split into chunks of 100, 100, and 50
2. send multiple batch requests
3. throttle appropriately

## `emails list` and `emails get`

Use `list` for summary and pagination:

```bash
resend --json -q emails list --limit 10
resend --json -q emails list --after <cursor> --limit 10
```

Use `get` for one specific message record:

```bash
resend --json -q emails get <email-id>
```

## Attachments

Attachments are supported on `emails send`, not on `emails batch`.

Before attaching files:

- ensure the file exists
- consider total size after Base64 expansion
- use `emails send`, not `emails batch`

## Tags and headers

Good uses:

- correlation IDs
- environment markers
- flow names
- customer or tenant grouping

Keep them short and machine-stable.
