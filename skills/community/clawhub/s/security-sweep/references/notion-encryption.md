# Notion Encryption System

How secrets found during a security sweep are encrypted and stored in Notion.

## Overview

When the security sweep finds hardcoded secrets, you can encrypt them to your Notion workspace using `notion-secrets.js` — a local encryption tool that wraps secrets in AES-256-GCM before uploading to Notion.

**What Notion stores:** encrypted blobs — completely unreadable without the master password.
**What an attacker needs:** the master password + the Notion page ID.

## Architecture

```
Your machine                          Notion (cloud)
┌──────────────────────┐             ┌──────────────────────┐
│  Master Password      │             │                      │
│       ↓               │             │  Encrypted blob       │
│  PBKDF2 (100k iter)  │             │  [salt][iv][tag][ct] │
│       ↓               │             │                      │
│  AES-256-GCM encrypt │  ──push──>  │  Page: scan-results   │
│                      │             │                      │
│  AES-256-GCM decrypt │  ←─pull──  │  (Notion API)        │
│       ↓               │             │                      │
│  Plaintext secret    │             └──────────────────────┘
└──────────────────────┘
```

## Setup

### 1. Get a Notion API Integration

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Create a new integration ("Security Sweep")
3. Copy the internal API token
4. Store it: `node ~/.openclaw/scripts/notion-secrets.js put notion_api_key "<your-token>"`
5. Share the "RhomBot Secrets" database with your integration

### 2. Store the integration token (encrypted)

```bash
# The token is stored encrypted — never in plain text
node ~/.openclaw/scripts/notion-secrets.js put notion_api_key "<your-token>"
```

### 3. Set the master password

The master password is derived into an encryption key — **never stored**.

```bash
# Recommended: use environment variable (never in shell history)
export NOTION_MASTER_PASSWORD="your-strong-master-password"

# For one-off commands:
NOTION_MASTER_PASSWORD="your-password" node ~/.openclaw/scripts/notion-secrets.js <command>
```

> ⚠️ **CRITICAL:** The master password is the only way to decrypt your secrets. **Forget it and the secrets are permanently unrecoverable** — AES-256-GCM with PBKDF2 (100k iterations) is intentionally slow and cannot be brute-forced. Store it in a password manager.

## Usage

```bash
# Store a secret (use env var — avoids interactive prompt stdin issues)
NOTION_MASTER_PASSWORD="your-password" node ~/.openclaw/scripts/notion-secrets.js put my_api_key "sk-123..."

# List stored secrets (shows names only)
node ~/.openclaw/scripts/notion-secrets.js list

# Get a secret's encrypted blob
node ~/.openclaw/scripts/notion-secrets.js get my_api_key

# Decrypt a blob
node ~/.openclaw/scripts/notion-secrets.js decrypt "<blob>"

# Quick local encrypt (for testing)
node ~/.openclaw/scripts/notion-secrets.js encrypt "plaintext"
```

## How Encryption Works

**Algorithm:** AES-256-GCM
**Key derivation:** PBKDF2 with SHA-512, 100,000 iterations
**IV:** Random 16 bytes per encryption
**Tag:** 16 bytes (authentication tag)

```
plaintext → PBKDF2(pw, salt) → AES-256-GCM → [salt (32)][iv (16)][tag (16)][ciphertext] → base64
```

## Security Properties

| Property | Protection |
|----------|------------|
| Encrypted at rest | Notion only sees ciphertext |
| Key derivation | Brute-force resistant (100k PBKDF2 iterations) |
| Authenticated encryption | Tampering is detectable |
| No password storage | Master password never touches disk |
| Per-secret salt | Same secret encrypts differently each time |

## Important Notes

- **Use `NOTION_MASTER_PASSWORD` env var for scripts** — interactive prompts can have stdin mixing issues in non-TTY environments
- **The `put` command requires the env var** for reliable operation
- **`list` and `get` do not need a password** — they only read encrypted blobs (values stay encrypted client-side)
- **Decrypt requires the password** — the blob is useless without it

## Limitations

- The master password must be set via env var in CI/non-interactive environments
- Notion API rate limits apply (~3 requests/second)
- If Notion is down, secrets are unavailable

## For CI/CD

```bash
# In CI, inject the master password as a secret environment variable:
export NOTION_MASTER_PASSWORD="$NOTION_MASTER_PASSWORD"
bash scripts/full-scan.sh --encrypt-found [options]
```

The password never appears in logs — only the "Stored" confirmation is visible.
