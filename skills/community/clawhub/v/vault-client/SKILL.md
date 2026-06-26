---
name: vault-client
description: Hashicorp Vault client for OpenClaw agents. Read and write secrets from a Vault server without raw curl commands or hardcoded tokens. Use when reading API keys, DB credentials, or any secret stored in Hashicorp Vault; checking token expiry; rotating secrets; or configuring Vault access for the first time. NOT for the zuiho-kai local Vault skill (that is a different, local-only tool).
---

# vault-client

Gives OpenClaw agents clean, cached access to Hashicorp Vault. No curl, no hardcoded tokens in transcripts.

## Setup

Run once after installing:

```bash
node ~/.openclaw/workspace/skills/vault-client/scripts/vault.js setup
```

Prompts for address, token, and mount. Saves to `~/.openclaw/vault.json` and appends a startup block to `AGENTS.md`.

## Startup (every session)

```bash
node ~/.openclaw/workspace/skills/vault-client/scripts/vault.js check
```

- Exit 0 = connected, token valid
- Exit 1 = connected but token expires soon — warn user, run `token-renew`
- Exit 2 = unreachable or invalid token — warn user, check config

## Core commands

```bash
# Read all keys at a path
node vault.js get shopwalk/r2

# Read a single key (returns just the value — pipe-friendly)
node vault.js get shopwalk/database uri

# Write / update a secret (merges with existing keys)
node vault.js put shopwalk/r2 secret_access_key=newvalue

# List paths
node vault.js list shopwalk/

# Token management
node vault.js token-info
node vault.js token-renew
```

## Config reference (`~/.openclaw/vault.json`)

```json
{
  "address": "https://vault.example.com:8200",
  "mount": "secret",
  "auth": { "method": "token", "token": "hvs.xxx" },
  "cache_ttl_seconds": 300,
  "tls": { "verify": true }
}
```

Set `tls.verify: false` for internal Vault with self-signed certs.

Secrets are cached in `~/.openclaw/vault-cache.json` for `cache_ttl_seconds` (default 5 min) to avoid repeated API calls.

## Auth methods

Token auth is the default. For AppRole and Kubernetes auth, see `references/auth-methods.md`.

## No dependencies

Uses Node.js stdlib only (`https`, `fs`, `readline`). No npm install required.
