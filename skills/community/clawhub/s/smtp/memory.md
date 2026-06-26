# SMTP Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Context
- Primary provider: not set yet
- Typical sender domain: not set yet
- Main use case: not set yet
- Safe canary inbox: not set yet

## Safety Defaults
- Live sends require explicit confirmation.
- First live test should stay one-recipient unless the user says otherwise.
- Keep logs minimal and redact credentials or tokens.

## Notes
- Record only the combinations that actually worked.
- Acceptance by the SMTP server is not enough; capture final inbox, spam, or bounce evidence when available.
- Do not store raw passwords, API tokens, or private keys in this file.
