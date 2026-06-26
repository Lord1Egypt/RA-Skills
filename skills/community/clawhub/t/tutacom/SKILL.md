---
name: tuta-mail
description: "Send, read, and manage emails via Tuta (formerly Tutanota) encrypted email service. Use when user asks to send emails, check inbox, read mail, or do any email operations through their Tuta account. Triggers on phrases like email, send email, check inbox, Tuta, Tutanota, mail, read email, compose email."
---

# Tuta Mail

Interact with Tuta (Tutanota) encrypted email via the undocumented REST API at `https://app.tuta.com/rest/`.
All content is E2E encrypted — the client handles crypto locally.

## Prerequisites

Python 3 with: `requests`, `pycryptodome`, `bcrypt`, `argon2-cffi`.

Install if missing:
```bash
python3 -m pip install --break-system-packages requests pycryptodome bcrypt argon2-cffi
```

## Credentials

Store in `openclaw.json` under `skills.entries.tuta-mail.env`:
- `TUTA_EMAIL` — Tuta email address
- `TUTA_PASSWORD` — account password

## Usage

All commands via `scripts/tuta_client.py` (resolve path relative to this skill directory).

### Login (always do first)

```bash
python3 scripts/tuta_client.py login \
  --email "$TUTA_EMAIL" --password "$TUTA_PASSWORD" \
  --session-file /tmp/tuta_session.json
```

Saves session (access token + decrypted keys) to the session file. Reuse until it expires.

### List Inbox

```bash
python3 scripts/tuta_client.py inbox \
  --session-file /tmp/tuta_session.json --count 20
```

Returns JSON array with `id`, `subject`, `sender`, `date`, `unread` for each mail.

### Read Email

```bash
python3 scripts/tuta_client.py read \
  --mail-id "listId/elementId" \
  --session-file /tmp/tuta_session.json
```

Use the `id` from inbox listing. Returns decrypted `subject`, `sender`, `date`, `body`.

### Send Email (External Recipients)

```bash
python3 scripts/tuta_client.py send \
  --to "recipient@example.com" \
  --subject "Subject line" \
  --body "Email body text" \
  --sender-name "Display Name" \
  --session-file /tmp/tuta_session.json
```

Sends non-confidential email to external (non-Tuta) recipients. Creates draft then sends.

## Workflow

1. Login once per session → cache `/tmp/tuta_session.json`
2. If any command returns auth error (401/403), re-login
3. For inbox checks: login → inbox → optionally read specific mails
4. For sending: login → send

## Limitations

- **Tuta-to-Tuta emails**: Sending to other Tuta users requires public key exchange (not yet implemented). Reading Tuta-to-Tuta received mail works.
- **Attachments**: Not yet supported for sending.
- **API versioning**: The `v` header is set to `84`; may need updating if Tuta changes their API version.
- **Newer accounts**: Argon2id key derivation is supported but less tested than bcrypt (legacy).
