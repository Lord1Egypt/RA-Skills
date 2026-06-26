---
name: ravi-secrets
description: Store and retrieve key-value secrets — encrypted secret store for API keys and env vars. Do NOT use for website passwords (use ravi-passwords) or reading messages (use ravi-inbox).
---

# Ravi Secrets

Store and retrieve key-value secrets (API keys, environment variables, tokens). All values are server-side encrypted — you send and receive plaintext. Keys are stored in plaintext for lookup/filtering.

## Commands

```bash
# Store a secret
ravi secrets set OPENAI_API_KEY "sk-abc123..."

# List all secrets
ravi secrets list

# Retrieve a secret by key name
ravi secrets get OPENAI_API_KEY

# Delete a secret by UUID
ravi secrets delete <uuid>
```

## JSON Shapes

**`ravi secrets list`:**
```json
[
  {
    "uuid": "...",
    "identity": 1,
    "key": "OPENAI_API_KEY",
    "value": "sk-abc123...",
    "notes": "",
    "created_dt": "2026-02-25T10:30:00Z",
    "updated_dt": "2026-02-25T10:30:00Z"
  }
]
```

**`ravi secrets get OPENAI_API_KEY`:**
```json
{
  "uuid": "...",
  "identity": 1,
  "key": "OPENAI_API_KEY",
  "value": "sk-abc123...",
  "notes": "",
  "created_dt": "2026-02-25T10:30:00Z",
  "updated_dt": "2026-02-25T10:30:00Z"
}
```

## Common Patterns

### Store and retrieve API keys at runtime

```bash
# Store a key
ravi secrets set OPENAI_API_KEY "sk-abc123..."

# Retrieve the key value
API_KEY=$(ravi secrets get OPENAI_API_KEY | jq -r '.value')

# List all available key names
ravi secrets list | jq -r '.[].key'
```

### Store multiple service keys

```bash
ravi secrets set ANTHROPIC_API_KEY "sk-ant-..."
ravi secrets set GITHUB_TOKEN "ghp_..."
```

## Important Notes

- **Server-side encryption is transparent** — you always see plaintext values.
- **Keys must be unique per identity** — if you need to update an existing key, use `ravi secrets set` again (it will upsert). Creating a duplicate key name will return a validation error.
- **Keys are auto-uppercased** — keys are automatically uppercased by the server (e.g. `test_key` becomes `TEST_KEY`). Keys must match `^[A-Z][A-Z0-9_]*$` after uppercasing.
- **Keys are plaintext** — only values and notes are encrypted. Use descriptive key names like `OPENAI_API_KEY`, `STRIPE_SECRET_KEY`.

## Full API Reference

For complete endpoint details, request/response schemas, and parameters: [Secrets](https://ravi.id/docs/schema/secrets.json)

## Related Skills

- **ravi-passwords** — Store website credentials (domain + username + password, not key-value secrets)
- **ravi-login** — Signup workflows that may need API keys stored after registration
- **ravi-feedback** — Report secrets issues or suggest improvements
