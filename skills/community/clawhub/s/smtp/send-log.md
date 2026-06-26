# Send Log - SMTP

Use this file as the baseline for `~/smtp/send-log.md`.

Keep entries short and evidence-focused.

## Entry Template

- Date:
- Mode: draft | probe | canary | live
- Provider:
- Host and port:
- TLS mode:
- Recipient scope:
- Message ID or queue ID:
- Result: success | auth_failed | tls_failed | relay_denied | accepted_pending | bounced | spam
- Evidence:
- Next move:

## Rules

- Log canary and live sends, not every draft revision.
- Redact recipients when they do not matter for future debugging.
- Never store raw SMTP passwords, tokens, or private keys.
- If the server accepted the message but placement is unknown, record that as `accepted_pending`, not success.
