# Secrets Manager 🔐

**Encrypted local secret store.** AES-256-GCM authenticated encryption, rotation
tracking, audit, and delete. A **PURE STORE** — it encrypts, retrieves, lists,
rotates, audits, and deletes secrets. It does **not** generate executable command
scripts and does **not** write plaintext secrets to disk.

> **Important**: If you lose `.master-key`, all stored secrets become unrecoverable. Back it up.

## Security model

- **AES-256-GCM** authenticated encryption (tamper → decrypt returns `null`)
- 256-bit master key, auto-generated on first store, stored in
  `memory/secrets/.master-key` (chmod 0600)
- Per-secret random 96-bit IV, 128-bit GCM auth tag
- Encrypted secrets persist in `memory/secrets/secrets.json` (chmod 0600)
- No plaintext secrets are ever written to disk or to logs

## Quick Start

```bash
# Store a secret (encrypted at rest)
node secrets-manager.js --store openai-key sk-abc123
# → Stored: openai-key (masked: sk-****23)

# Get a secret (masked by default)
node secrets-manager.js --get openai-key
# → openai-key: sk-****23

# Get the raw value (prints to stdout — use only when you must pass it onward)
node secrets-manager.js --get --raw openai-key > /tmp/key.txt && chmod 600 /tmp/key.txt

# List secret names + metadata (never values)
node secrets-manager.js --list

# Delete a secret (irreversible)
node secrets-manager.js --delete old-key

# Rotate a secret (generates a new random value; old value archived as retired)
node secrets-manager.js --rotate openai-key

# Rotate all secrets
node secrets-manager.js --rotate --all

# Audit for exposure / rotation issues
node secrets-manager.js --audit
node secrets-manager.js --audit --expired
node secrets-manager.js --audit --stale

# Status overview
node secrets-manager.js --status
```

## Features

- **Encryption** — AES-256-GCM, per-secret IV, authenticated (tamper detection)
- **Rotation tracking** — 90-day default cycle, expiration warnings, one-command rotation
- **Audit system** — flags expired/stale secrets, weak patterns, decryption failures
- **Masked by default** — values never printed unless explicitly requested via `--get --raw`
- **Zero plaintext-on-disk** — secrets are encrypted at rest; no temp scripts are generated

## Configuration

Data stored in `memory/secrets/`:
- `secrets.json` — encrypted secrets (chmod 0600)
- `.master-key` — 256-bit master key as hex (chmod 0600)
- `permissions.json` — per-secret access rules (chmod 0600)

Override storage location:
```bash
SECRETS_DIR=/path/to/secrets node secrets-manager.js --status
```

Override master key (ephemeral/CI only):
```bash
SECRETS_MASTER_KEY=<64-hex-chars> node secrets-manager.js --get openai-key
```
> Never set `SECRETS_MASTER_KEY` in shared, containerized, CI, or logged
> environments — anyone who can read process env or logs can recover the key.
> Prefer the file-based `.master-key` (chmod 0600) on a single-user host.

## Agent Protocol

1. **Store with encryption** — `--store <name> <value>` writes AES-256-GCM ciphertext
2. **Default to masked output** — `--get` (not `--get --raw`) for display
3. **Audit regularly** — `--audit` during heartbeats
4. **Rotate proactively** — rotate secrets flagged as expiring
5. **Back up `.master-key`** — without it, stored secrets are unrecoverable

## Security Notes

- AES-256-GCM authenticated encryption — secrets encrypted at rest, not base64
- Master key in `memory/secrets/.master-key` (chmod 0600) — back it up
- For production-grade secrets with HSM-backed keys, use a real vault
  (HashiCorp, AWS Secrets Manager, OS keychain)
- `SECRETS_MASTER_KEY` env var for ephemeral/CI environments
- **No plaintext is written to disk** — the store only ever holds ciphertext

## What This Skill Does NOT Do

- Does NOT store secrets in plaintext or base64 — all values are AES-256-GCM encrypted
- Does NOT print secret values to stdout unless explicitly requested via `--get --raw`
- Does NOT generate executable command scripts (no `--inject`)
- Does NOT install npm packages
- Does NOT phone home or transmit secrets anywhere
- Does NOT log secret values
- Does NOT require a separate key server — master key is a local file

## Design Principles

1. **Zero setup** — Works immediately, no config needed
2. **No dependencies** — Pure Node.js crypto, no npm packages
3. **Safe by default** — Masked output, encrypted at rest, no plaintext-on-disk
4. **Transparent** — Audit reports show exactly what's wrong
5. **Recoverable** — Master key + encrypted secrets = full recovery

> **Need to inject a secret into a shell command?** Use the separate
> `secrets-inject` skill (high-privilege, clearly labeled). This store
> deliberately does not do that.
