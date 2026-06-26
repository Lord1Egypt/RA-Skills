---
name: supabase-vault
description: "Replace OpenClaw's local file vault with Supabase Vault for AES-256 encrypted-at-rest secret storage. All API keys and auth tokens stored encrypted in Postgres via pgsodium/libsodium. Bootstrap credentials protected by OS keychain or machine-derived AES-256-GCM (zero external deps). Includes dashboard Integrations tab with connect/migrate/manage UI. Use when: (1) setting up Supabase Vault as the OpenClaw secrets backend, (2) migrating existing secrets from ~/.openclaw/secrets.json to Supabase, (3) managing or adding secrets from the dashboard."
license: MIT
metadata: {"openclaw":{"emoji":"🔐","requires":{"openclaw":">=2026.1.0"},"category":"integrations"}}
---

# Supabase Vault — Enhanced Secret Storage

Replaces the local `secrets.json` vault with Supabase Vault. All OpenClaw API keys, tokens, and auth credentials are stored AES-256 encrypted in your Supabase Postgres database. Bootstrap credentials (the Supabase URL + service_role key needed to reach the vault) are encrypted locally using OS keychain or machine-derived AES-256-GCM.

See `references/architecture.md` for the full threat model and design rationale.

## Prerequisites

- A Supabase project (free tier works). Get one at [supabase.com](https://supabase.com).
- Project URL + service_role key (from Supabase Dashboard → Settings → API).
- Node.js 18+ (already available in OpenClaw's environment).

## Installation

### Step 1 — Install @supabase/supabase-js

```bash
npm install --prefix ~/.openclaw/skills/supabase-vault @supabase/supabase-js
```

### Step 2 — Run setup.sql in Supabase

Open your Supabase project → SQL Editor → paste and run `assets/setup.sql`.

This creates four wrapper functions (`insert_secret`, `read_secret`, `delete_secret`, `list_secret_names`) restricted to `service_role` only.

Verify with:
```sql
SELECT proname FROM pg_proc
WHERE proname IN ('insert_secret','read_secret','delete_secret','list_secret_names');
-- Should return 4 rows
```

### Step 3 — Install the gateway RPC handler

Copy `assets/rpc-handler.ts` to `src/gateway/server-methods/supabase-vault.ts` in the OpenClaw source, then register it in the server-methods index:

```typescript
// In src/gateway/server-methods.ts (or equivalent)
import { createSupabaseVaultHandlers } from "./supabase-vault.js";
// ...
Object.assign(handlers, createSupabaseVaultHandlers());
```

### Step 4 — Install the dashboard UI

Copy the UI files to their destinations:
```
assets/controller.ts → ui/src/ui/controllers/supabase-vault.ts
assets/views.ts      → ui/src/ui/views/supabase-vault.ts
```

Register as an Integrations tab using the plugin architecture (same pattern as `pipedream-connect` or `discord-connect`):
```typescript
// In the plugin registration or plugins-ui.ts:
{
  id: "supabase-vault",
  label: "Supabase Vault",
  icon: "🔐",
  section: "integrations",
  controller: "supabase-vault",
  view: "supabase-vault",
}
```

### Step 5 — Rebuild & restart

```bash
cd ~/openclaw && npm run build
(sleep 3 && systemctl --user restart openclaw-gateway) &
```

### Step 6 — Connect via dashboard

Open the Control UI → Integrations → Supabase Vault. Enter your Project URL and service_role key, then click **Connect & Test**.

## Exec Provider Config

After connecting, the skill automatically adds this to `~/.openclaw/openclaw.json`:

```json
{
  "secrets": {
    "providers": {
      "supabase": {
        "source": "exec",
        "command": "node",
        "args": ["~/.openclaw/skills/supabase-vault/scripts/fetch-secrets.js"],
        "jsonOnly": true,
        "trustedDirs": ["~/.openclaw/skills/supabase-vault"],
        "timeoutMs": 8000
      }
    }
  }
}
```

After migrating secrets, SecretRefs in config will point to this provider:
```json
{ "source": "exec", "provider": "supabase", "id": "/OPENAI_API_KEY" }
```

## How It Works

```
Gateway starts
  → exec provider triggers fetch-secrets.js
      → keychain.js retrieves SUPABASE_URL + SERVICE_ROLE_KEY
          (macOS: Keychain Access / Linux: GNOME Keyring / fallback: AES-256-GCM file)
      → @supabase/supabase-js createClient(url, key)
      → supabase.rpc('read_secret', { secret_name }) for each requested key
      → outputs: { protocolVersion: 1, values: { "/KEY": "value" }, errors: {} }
  → OpenClaw runtime snapshot populated — secrets in memory only
```

## Bootstrap Credential Storage by Platform

| Platform | Method | Storage |
|----------|--------|---------|
| macOS | `security` CLI | Keychain Access (hardware-backed on Apple Silicon) |
| Linux (desktop) | `secret-tool` | GNOME Keyring / KWallet |
| WSL2 / headless | AES-256-GCM | `~/.openclaw/supabase-vault-config.enc` (machine-derived key) |
| Any | AES-256-GCM | Fallback always available |

The AES-256-GCM fallback uses PBKDF2-HMAC-SHA512 (600,000 iterations) with a key derived from `/etc/machine-id + $USER + app-salt`. The encrypted file is unreadable on any other machine or as any other user.

## Migration

From the dashboard: **Integrations → Supabase Vault → Migrate from Local Vault**.

Or from the CLI:
```bash
node ~/.openclaw/skills/supabase-vault/scripts/migrate.js
node ~/.openclaw/skills/supabase-vault/scripts/migrate.js --yes      # non-interactive
node ~/.openclaw/skills/supabase-vault/scripts/migrate.js --dry-run  # preview only
```

Migration moves all keys from `secrets.json` to Supabase Vault and updates all SecretRefs in `openclaw.json` from `file` → `exec/supabase`. The local `secrets.json` is left in place as a safety backup.

## Security Notes

- **Vault secrets**: AES-256 encrypted at rest via libsodium. Encryption key never in DB — database dumps are useless without it.
- **Bootstrap creds**: Encrypted via OS keychain or AES-256-GCM with machine-derived key. Not readable on another machine.
- **Service_role key**: Bypasses Supabase RLS — keep this project dedicated to OpenClaw secrets only.
- **Memory only at runtime**: No decrypted values on disk. Secrets in RAM during gateway session only.
- **exec provider security**: OpenClaw validates `trustedDirs` and file permissions on `fetch-secrets.js` before execution.
