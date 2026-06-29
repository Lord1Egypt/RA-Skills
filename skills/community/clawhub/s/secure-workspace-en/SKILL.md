---
name: Secure Workspace
description: Encrypt API keys, tokens and passwords with age to protect secrets in your workspace.
emoji: 🔐
homepage: https://github.com/asistentegordito/secure-workspace
metadata:
  clawdbot:
    emoji: 🔐
    requires:
      exec:
        - age
---

# Secure Workspace

Encrypt secrets with age to protect them in repos and backups.

## Usage

```bash
# 1. Generate key pair (if not exists)
bash scripts/secure/setup.sh

# 2. Encrypt a secret
echo 'export API_KEY=*** | bash scripts/secure/encrypt.sh scripts/secure/secrets.env.age

# 3. Decrypt on the fly
source <(bash scripts/secure/decrypt.sh scripts/secure/secrets.env.age)
```

## Files

| File | Purpose |
|------|---------|
| `scripts/secure/encrypt.sh` | Encrypt stdin → `.age` |
| `scripts/secure/decrypt.sh` | Decrypt `.age` → stdout |
| `scripts/secure/setup.sh` | Generate key pair |

## Requirements

- `age` (apt install age / brew install age)

## Note

The private key is at `/root/.age/key.txt`. It is never uploaded to the repo.
