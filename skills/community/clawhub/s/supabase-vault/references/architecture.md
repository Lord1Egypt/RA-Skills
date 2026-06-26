# Supabase Vault — Architecture & Threat Model

## System Design

```
┌─────────────────────────────────────────────────────────────┐
│  OpenClaw Gateway                                           │
│                                                             │
│  secrets.providers.supabase                                 │
│    source: "exec"                                           │
│    command: "node fetch-secrets.js"         ─────────────┐  │
│                                                           │  │
│  Runtime snapshot (in-memory only)                        │  │
│    OPENAI_API_KEY = "sk-proj-..."   ◄─────────────────┐  │  │
└───────────────────────────────────────────────────────│──│──┘
                                                        │  │
                                           ┌────────────┘  │
                                           │               ▼
                                    Supabase Vault    fetch-secrets.js
                                    (Postgres/AES)         │
                                    ┌──────────┐           │ keychain.js
                                    │ OPENAI   │  ◄────────┤
                                    │ (encr.)  │           │ ┌────────────────┐
                                    └──────────┘           └►│ macOS Keychain │
                                                             │ GNOME Keyring  │
                                                             │ AES-256-GCM    │
                                                             │ (machine key)  │
                                                             └────────────────┘
                                                             SUPABASE_URL +
                                                             SERVICE_ROLE_KEY
```

## Threat Model

| Threat | Protected? | How |
|--------|-----------|-----|
| secrets.json read by attacker | ✅ Eliminated | No plaintext on disk after migration |
| DB dump / backup leaked | ✅ Protected | Vault stores ciphertext; decryption key never in DB |
| supabase-vault-config.enc stolen | ✅ Protected | AES-256-GCM with machine+user derived key; unreadable on another machine |
| Network eavesdropping | ✅ Protected | All Supabase traffic uses TLS 1.3 |
| openclaw.json read | ✅ Protected | Contains SecretRefs only (no values) |
| Supabase breach (DB stolen) | ✅ Protected | libsodium AEAD; encryption key stored out-of-band by Supabase |
| Runtime memory scraping | ⚠️ Same as any | Secrets in RAM during gateway session |
| Full OS compromise (root/same user) | ⚠️ Same ceiling | Same for all local secret managers |
| Supabase service unavailable | ⚠️ Gateway fails to start | Mitigate with local fallback cache |

## Encryption Layers

### Layer 1 — Supabase Vault (all other secrets)
- **Algorithm**: libsodium `secretbox` (XSalsa20-Poly1305) via pgsodium / Transparent Column Encryption
- **Key location**: Managed by Supabase, stored outside the database (cannot be extracted via SQL)
- **At rest**: `vault.secrets` table stores ciphertext. Decryption only via `vault.decrypted_secrets` VIEW, in-memory at query time
- **Backup safe**: Database dumps contain only ciphertext

### Layer 2 — Bootstrap credentials (SUPABASE_URL + SERVICE_ROLE_KEY)
**macOS Keychain:**
- Encryption managed by macOS Security framework
- On Apple Silicon: hardware-backed via Secure Enclave
- Access gated to the current user session

**Linux GNOME Keyring:**
- AES-256 encrypted by the keyring daemon
- Locked when user session ends

**AES-256-GCM fallback (WSL2 / headless):**
```
key_material = /etc/machine-id + $USER + "openclaw-supabase-v1"
PBKDF2-HMAC-SHA512(key_material, random_salt, iterations=600000) → 32-byte key
AES-256-GCM(key, random_iv, plaintext=JSON({url, serviceRoleKey}))
File: ~/.openclaw/supabase-vault-config.enc (mode 0600)
```
- 600,000 PBKDF2 iterations follows OWASP 2023 recommendation for PBKDF2-SHA512
- File bound to this machine (machine-id) and this user (username)
- Copying file to another machine renders it undecryptable

## exec Provider Security

OpenClaw's built-in exec provider validates the bridge script before execution:
- File must be owned by current user (`uid` check)
- File must not be world-writable or world-readable
- File must be inside `trustedDirs` (configured as the skill directory)
- No symlinks allowed

This means even if an attacker can create files, they cannot redirect the exec provider to a malicious script.

## Service Role Key Risk

The `service_role` key bypasses all Row Level Security in your Supabase project. Mitigations:
1. **Dedicated project**: Use a Supabase project exclusively for OpenClaw secrets (no user data, no other tables)
2. **Rotate periodically**: New secret key can be generated in Supabase Dashboard → Settings → API
3. **Monitor access**: Supabase logs all RPC calls with timestamps

## Supabase Vault pgsodium Deprecation Note

pgsodium is being deprecated as a standalone extension. However, Supabase has committed to keeping the Vault API (`vault.create_secret`, `vault.decrypted_secrets`, etc.) stable through the transition. The `setup.sql` wrapper functions do not depend on pgsodium directly — they call Vault's stable public API.
