---
name: op-secrets
description: Read and write secrets from 1Password (SDK mode, fully headless). Use when user says "get the API key", "read secret", "store this password", "check 1Password", "what's the token for", or when any operation requires retrieving or storing credentials.
metadata:
  {
    "openclaw":
      {
        "emoji": "\U0001F510",
        "requires": { "plugins": ["1password"] },
      },
  }
---

# 1Password Secrets (SDK)

Use the `op_read_secret`, `op_list_items`, and `op_write_secret` tools to access 1Password secrets directly. Fully headless via service account — no desktop app or biometrics needed.

## Tools

### op_read_secret
Read a specific secret value from 1Password.

Parameters:
- `item` (required): Item title (e.g. "OpenAI API", "Anthropic Auth Token")
- `vault` (optional): Vault name (default: from plugin config)
- `field` (optional): Field name (default: "api key")

### op_list_items
List all items in a 1Password vault.

Parameters:
- `vault` (optional): Vault name (default: from plugin config)

### op_write_secret
Create or update a secret in 1Password. Requires write access on the service account.

Parameters:
- `item` (required): Item title (e.g. "New API Key")
- `value` (required): The secret value to store
- `vault` (optional): Vault name (default: from plugin config)
- `field` (optional): Field name (default: "api key")

## Guardrails

- NEVER log, echo, or paste secret values into chat, logs, or code
- Store returned values in variables only
- If a secret is accidentally exposed, alert the user immediately and recommend rotation
- Prefer `op_read_secret` over reading secrets from config files or environment variables
