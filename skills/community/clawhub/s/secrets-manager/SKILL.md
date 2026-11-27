---
name: secrets-manager
version: 1.1.19
description: Encrypted local secret store for OpenClaw agents. AES-256-GCM authenticated encryption with per-secret random IVs, master key in restricted-permission .master-key file. Store, retrieve, rotate, and audit secrets. Safe command injection (writes to temp file by default; --inject-stdout requires --confirm-expose). Master key is recoverable from .master-key file; losing it makes stored secrets unrecoverable.
permissions: ["fs", "env", "exec", "shell", "elevated"]
---

# Secrets Manager 🔐

**Encrypted local secret store.** AES-256-GCM authenticated encryption. Master key auto-generated on first store and stored in the skill's private storage directory with restricted permissions (owner-only).

> **Important**: If you lose `.master-key`, all stored secrets become unrecoverable. Back it up.

## ⚠️ Important Warnings

### Encryption: AES-256-GCM (Authenticated)
- 256-bit master key, per-secret 96-bit random IV, 128-bit GCM auth tag
- Tampered ciphertext returns `null` from decrypt (no partial decryption)
- Master key stored in the skill's private storage directory with restricted permissions (owner-only)
- Override via `SECRETS_MASTER_KEY=<hex>` env var
- Losing the master key = all secrets unrecoverable

### `--get --raw` Prints Plaintext to stdout
The secret value goes to stdout, which may be captured in:
- Shell history / terminal scrollback
- Process logs / journald / syslog
- CI/CD pipeline output
- Agent transcripts / OpenClaw session history

Use only when piping to a private process:
```bash
node secrets-manager.js --get --raw api-key > /tmp/api-key.txt
# Restrict file permissions after writing
```

### `--inject` Default: Safe (writes to temp file with restricted permissions)
By default, `--inject "command {{secret}}"` substitutes and writes to a private temp file. **The resolved command is NEVER printed to stdout** unless you pass **both** flags:
```bash
--inject-stdout --confirm-expose "command {{secret}}"
```
The skill refuses to print the resolved command without `--confirm-expose`.

### Rotation: Old Values Are Archived
Rotated secrets keep the old encrypted value as `retired`. Rotate again to discard the archive. There is no `--undo` for archival.

### Storage Location
Encrypted secrets and master key stored in the skill's private storage directory with restricted permissions (owner-only). Override via `--dir <path>` or `SECRETS_DIR=<path>`.

## Permissions

This skill requires the following capabilities:

| Permission | Scope | Reason |
|---|---|---|
| `fs.read` | Private storage | Read encrypted secrets and master key |
| `fs.write` | Private storage | Write encrypted secrets, master key, permission rules |
| `run-cli` | CLI invocation | Invoke `secrets-manager.js` for store/get/rotate/audit operations |
| `elevated` | File permissions | Set restricted permissions on secret files to ensure owner-only access |

Elevation is required only for restricted permission enforcement on files outside the user's home directory. Within `$HOME`, the skill uses standard file operations without elevation.

## Quick Start

### Store a secret

```bash
node skills/secrets-manager/secrets-manager.js --store openai-key sk-abc123
# Output: [secrets-manager] Stored: openai-key (masked: sk-****23)
```

### Get a secret (masked by default)

```bash
node skills/secrets-manager/secrets-manager.js --get openai-key
# Output: [secrets-manager] openai-key: sk-****23
```

### Get raw value (when needed for injection)

```bash
node skills/secrets-manager/secrets-manager.js --get --raw openai-key > /tmp/key.txt
# Output: sk-abc123 (captured to file)
```

### List all secrets (names + metadata, NOT values)

```bash
node skills/secrets-manager/secrets-manager.js --list
```

### Delete a secret

```bash
node skills/secrets-manager/secrets-manager.js --delete old-key
```

### Rotate a secret

```bash
node skills/secrets-manager/secrets-manager.js --rotate openai-key
# New random value generated, old encrypted value archived as retired
```

### Rotate all secrets

```bash
node skills/secrets-manager/secrets-manager.js --rotate --all
```

### Audit for security issues

```bash
node skills/secrets-manager/secrets-manager.js --audit
node skills/secrets-manager/secrets-manager.js --audit --expired
node skills/secrets-manager/secrets-manager.js --audit --stale
```

### Inject secrets into a command (safe default)

```bash
node skills/secrets-manager/secrets-manager.js --inject "curl -H 'Authorization: Bearer {{openai-key}}' https://api.openai.com/v1/chat"
# Output: [secrets-manager] ✅ Injected 1 secret(s) into: /tmp/secrets-inject-12345-1234567890.sh
#         [secrets-manager]    Run with: sh /tmp/secrets-inject-12345-1234567890.sh
```

**Then run the command** (the secrets are in the temp file with restricted permissions):
```bash
sh /tmp/secrets-inject-12345-1234567890.sh
```

### Inject to stdout (DANGEROUS — requires explicit confirmation)

```bash
node skills/secrets-manager/secrets-manager.js --inject-stdout --confirm-expose "echo {{openai-key}}"
# Will print: [secrets-manager] ⚠️ Resolved command below contains 1 secret value(s) in plaintext:
#              echo sk-abc123
```

The skill **refuses** to print the resolved command without `--confirm-expose`. This is to prevent accidental secret leaks to logs.

### Status overview

```bash
node skills/secrets-manager/secrets-manager.js --status
```

## Features

### Encryption
- **AES-256-GCM** authenticated encryption
- 256-bit master key (auto-generated on first store)
- 96-bit per-secret random IV
- 128-bit GCM auth tag (tamper detection)
- Master key in the skill's private storage directory with restricted permissions (owner-only)
- `SECRETS_MASTER_KEY` env var override

### Rotation Tracking
- 90-day default rotation cycle per secret
- Automatic expiration warnings (audit --stale at 70% of cycle)
- One-command rotation with new random value generation
- Old values archived as `retired` (encrypted, recoverable until next rotate)

### Audit System
- Detects expired secrets past rotation date
- Flags secrets approaching rotation deadline (70% threshold)
- Identifies weak patterns (common prefixes, short length <8 chars)
- Detects decryption failures (tampered ciphertext or wrong master key)
- Reports rotation age for each secret

### Safe Command Injection
- `{{secret_name}}` placeholders replaced in command strings
- **Default**: writes resolved command to a temp file with restricted permissions, prints path only
- **Opt-in stdout**: requires both `--inject-stdout` AND `--confirm-expose`
- No secret values ever reach stdout by default

## Configuration

Data stored in the skill's private storage directory:
- Encrypted secrets file (restricted permissions)
- Master key file (restricted permissions)
- Per-secret access rules (restricted permissions)

Override storage location:
```bash
--dir /path/to/secrets
# or env var
SECRETS_DIR=/path/to/secrets node secrets-manager.js --status
```

Override master key:
```bash
SECRETS_MASTER_KEY=<64-hex-chars> node secrets-manager.js --get openai-key
```

## Agent Protocol

When handling secrets:

1. **Store with encryption** — `--store <name> <value>` writes AES-256-GCM ciphertext
2. **Default to masked output** — `--get` (not `--get --raw`) for display
3. **Use safe inject by default** — `--inject` writes to temp file, doesn't leak
4. **Audit regularly** — `--audit` during heartbeats
5. **Rotate proactively** — rotate secrets flagged as expiring
6. **Back up the master key** — without it, stored secrets are unrecoverable

## Security

### Encryption & Storage
- **AES-256-GCM authenticated encryption** — secrets are encrypted at rest, not base64-encoded
- **Master key** in the skill's private storage directory with restricted permissions — back it up
- For production-grade secrets with HSM-backed keys, use a real vault (HashiCorp, AWS Secrets Manager, OS keychain)
- `SECRETS_MASTER_KEY` env var for ephemeral/CI environments
- Default `--inject` never prints secrets; `--inject-stdout` requires explicit confirmation

### Elevation & Least-Privilege
Restricted file permissions ensure only the file owner can read secrets. This skill follows a least-privilege approach:

- **Within `$HOME`**: Standard file permission changes are sufficient; no elevated access required.
- **Outside `$HOME`** (e.g., shared or system directories): Elevation may be needed to set restrictive permissions. The skill requests elevation only for the specific permission operation, not for reading or writing secrets.
- **Best-effort enforcement**: If permission changes fail (e.g., access denied), the skill continues and logs a warning rather than aborting. Secrets are still encrypted regardless of file permissions.
- **No persistent privilege**: Elevation is requested per-operation and released immediately after permission changes complete.

### Credential Path Management
All secret storage files are dynamically managed by the skill itself within a private data directory. These are encrypted storage locations with restricted permissions, not hardcoded credentials.

## What This Skill Does NOT Do

- Does NOT store secrets in plaintext or base64 — all values are AES-256-GCM encrypted
- Does NOT print secret values to stdout unless explicitly requested via `--get --raw` or `--inject-stdout --confirm-expose`
- Does NOT install npm packages
- Does NOT phone home or transmit secrets anywhere
- Does NOT log secret values
- Does NOT require a separate key server — master key is a local file

## Comparison

| Approach | Encryption | Setup | Audit | Rotation | Recovery |
|----------|-----------|-------|-------|----------|----------|
| Environment vars | None | Medium | None | Manual | N/A |
| .env files | None | Low | None | Manual | N/A |
| **Secrets Manager** | **AES-256-GCM** | **None** | **Auto** | **Auto** | **With .master-key** |
| Vault service | Various | High | Auto | Auto | Yes |

**Secrets Manager gives you real encryption + rotation + audit with zero external dependencies.**

## Design Principles

1. **Zero setup** — Works immediately, no config needed
2. **No dependencies** — Pure Node.js crypto, no npm packages
3. **Safe by default** — Masked output, safe inject, encrypted at rest
4. **Transparent** — Audit reports show exactly what's wrong
5. **Recoverable** — Master key + encrypted secrets = full recovery

<!-- clawhub-sync: 2026-07-22 v1.1.9 security audit remediation -->
