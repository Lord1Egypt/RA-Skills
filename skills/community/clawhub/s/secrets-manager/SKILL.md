---
name: secrets-manager
description: >-
  Encrypted local secret store for OpenClaw agents. AES-256-GCM authenticated
  encryption with per-secret random IVs, master key in chmod 0600 .master-key
  file. A PURE STORE: it encrypts, retrieves, lists, rotates, audits, and deletes
  secrets — it never writes plaintext secrets to disk or generates executable
  command scripts. Modes: --store (encrypt+write), --get (masked; --raw prints
  plaintext to stdout), --list (names+metadata only), --delete (irreversible),
  --rotate and --rotate --all (generate new random values, archive old as
  retired), --audit / --audit --expired / --audit --stale (exposure/rotation
  checks), --status. Supports SECRETS_DIR and SECRETS_MASTER_KEY env overrides.
  For injecting secrets into shell commands, use the separate `secrets-inject`
  skill (high-privilege). Master key is recoverable from .master-key file;
  losing it makes stored secrets unrecoverable.
permissions:
  - filesystem.read-write
  - environment.read
  - crypto.aes-256-gcm
---

# Secrets Manager 🔐

**Encrypted local secret store.** AES-256-GCM authenticated encryption. Master key auto-generated on first store and stored in `memory/secrets/.master-key` (chmod 0600).

> **Important**: If you lose `.master-key`, all stored secrets become unrecoverable. Back it up.

## ⚠️ Important Warnings

### Encryption: AES-256-GCM (Authenticated)
- 256-bit master key, per-secret 96-bit random IV, 128-bit GCM auth tag
- Tampered ciphertext returns `null` from decrypt (no partial decryption)
- Master key stored in `memory/secrets/.master-key` with chmod 0600
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
node secrets-manager.js --get --raw api-key > /tmp/api-key.txt && chmod 600 /tmp/api-key.txt
```

### Rotation: Old Values Are Archived
Rotated secrets keep the old encrypted value as `retired`. Rotate again to discard the archive. There is no `--undo` for archival.

### Storage Location
`memory/secrets/secrets.json` (chmod 0600) plus `memory/secrets/.master-key` (chmod 0600). Override via `--dir <path>` or `SECRETS_DIR=<path>`.

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

### Get raw value (when you must pass it to another tool)

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
- Master key in `memory/secrets/.master-key` (chmod 0600)
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

## Configuration

Data stored in: `memory/secrets/`
- `secrets.json` — encrypted secrets (chmod 0600)
- `.master-key` — 256-bit master key as hex (chmod 0600)
- `permissions.json` — per-secret access rules (chmod 0600)

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
3. **Audit regularly** — `--audit` during heartbeats
5. **Rotate proactively** — rotate secrets flagged as expiring
6. **Back up `.master-key`** — without it, stored secrets are unrecoverable

## Security Notes

- **AES-256-GCM authenticated encryption** — secrets are encrypted at rest, not base64-encoded
- **Master key** in `memory/secrets/.master-key` (chmod 0600) — back it up
- For production-grade secrets with HSM-backed keys, use a real vault (HashiCorp, AWS Secrets Manager, OS keychain)
- `SECRETS_MASTER_KEY` env var for ephemeral/CI environments

## What This Skill Does NOT Do

- Does NOT store secrets in plaintext or base64 — all values are AES-256-GCM encrypted
- Does NOT print secret values to stdout unless explicitly requested via `--get --raw`
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
3. **Safe by default** — Masked output, encrypted at rest, no plaintext-on-disk
4. **Transparent** — Audit reports show exactly what's wrong
5. **Recoverable** — Master key + encrypted secrets = full recovery

<!-- clawhub-sync: 2026-07-22 v1.1.9 security audit remediation -->
