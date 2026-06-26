---
name: ravi-passwords
description: Store and retrieve website credentials — password manager for domain/username/password entries. Do NOT use for API keys/secrets (use ravi-secrets) or reading messages (use ravi-inbox).
---

# Ravi Passwords

Store and retrieve passwords for services you sign up for. All credential fields (username, password, notes) are server-side encrypted — you send and receive plaintext.

## Commands

```bash
# Create entry (auto-generates password if password not given)
ravi passwords create example.com

# Create with username and password
ravi passwords create example.com --username "me@example.com" --password "S3cret!"

# List all entries
ravi passwords list

# Retrieve a specific entry by UUID
ravi passwords get <uuid>

# Update an entry
ravi passwords update <uuid> --password "NewPass!"

# Delete an entry
ravi passwords delete <uuid>

# Generate a password without storing it
ravi passwords generate
```

**Create fields:** `domain` (required), `--username`, `--password`, `--notes`

If `--password` is omitted, the server auto-generates a strong password.

## JSON Shapes

**`ravi passwords list`:**
```json
[
  {
    "uuid": "uuid",
    "identity": 1,
    "domain": "example.com",
    "username": "me@example.com",
    "password": "S3cret!",
    "notes": "",
    "created_dt": "2026-02-25T10:30:00Z",
    "updated_dt": "2026-02-25T10:30:00Z"
  }
]
```

**`ravi passwords get <uuid>`:**
```json
{
  "uuid": "uuid",
  "identity": 1,
  "domain": "example.com",
  "username": "me@example.com",
  "password": "S3cret!",
  "notes": "",
  "created_dt": "2026-02-25T10:30:00Z",
  "updated_dt": "2026-02-25T10:30:00Z"
}
```

## Common Patterns

### Sign up for a service — store credentials immediately

```bash
# Generate and store credentials during signup
CREDS=$(ravi passwords create example.com --username "me@example.com")
PASSWORD=$(echo "$CREDS" | jq -r '.password')
# Use $PASSWORD in the signup form
```

### Log into a service — retrieve stored credentials

```bash
# Find entry by domain
ENTRY=$(ravi passwords list | jq -r '.[] | select(.domain == "example.com")')
UUID=$(echo "$ENTRY" | jq -r '.uuid')

# Get full credentials including password
CREDS=$(ravi passwords get "$UUID")
USERNAME=$(echo "$CREDS" | jq -r '.username')
PASSWORD=$(echo "$CREDS" | jq -r '.password')
```

## Important Notes

- **Server-side encryption is transparent** — you always see plaintext values.
- **Domain cleaning** — pass the bare domain (e.g., `example.com`), not a full URL. The server normalizes it.
- **Auto-generate password** — if `--password` is omitted when creating an entry, the server auto-generates a strong password. The generated password is returned in the response.
- **Domain normalization** — the server strips subdomains (e.g. `app.example.com` becomes `example.com`). Pass the bare domain or a full URL — both work.

## Full API Reference

For complete endpoint details, request/response schemas, and parameters: [Passwords](https://ravi.id/docs/schema/passwords.json)

## Related Skills

- **ravi-secrets** — Store API keys and env vars (key-value secrets, not website credentials)
- **ravi-login** — End-to-end signup/login workflows that store credentials here
- **ravi-identity** — Get your email address for the username field
- **ravi-feedback** — Report password manager issues or suggest improvements
