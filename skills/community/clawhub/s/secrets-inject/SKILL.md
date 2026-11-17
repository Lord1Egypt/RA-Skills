---
name: secrets-inject
description: >-
  HIGH-PRIVILEGE companion to secrets-manager. Substitutes encrypted secrets
  into command strings and materializes them as executable shell scripts
  (written to chmod 0600 temp files) or prints them to stdout. This is a
  secret-exfiltration-capable capability by design — it intentionally expands
  a secret store into command material. Use ONLY when you must hand secrets to
  a shell command. The core secrets-manager store deliberately does NOT do
  this; this lives in its own skill so the dangerous capability is opt-in and
  clearly labeled. Requires the secrets-manager store (memory/secrets).
permissions:
  - filesystem.read
  - environment.read
  - crypto.aes-256-gcm
  - command-generation
---

# Secrets Inject ⚠️ (HIGH PRIVILEGE)

**This skill deliberately takes encrypted secrets and turns them into
executable shell commands containing plaintext secrets.** It exists as a
*separate, clearly-labeled* skill so the core `secrets-manager` can stay a
pure, clean store. Only install/use this if you actually need to inject
secrets into a command.

## ⚠️ Why this is dangerous (read before use)

- It **decrypts secrets** and writes them into a **plaintext temp shell
  script** (`/tmp/secrets-inject-*.sh`, mode 0600).
- Anyone who can read that temp file (same user, backups, forensic images,
  exfiltration) gets the plaintext secrets.
- Printing to stdout (`--inject-stdout`) puts plaintext secrets into shell
  history, logs, journald, CI output, and terminal scrollback.
- This is the canonical "secret exfiltration path" — treat it with the same
  care you'd give `cat .master-key`.

## When you might need it

You have a secret in `secrets-manager` and must pass it to a command that
needs it inline (e.g. `curl -H "Authorization: Bearer {{api_key}}"`).

## Quick Start

```bash
# 1) Store the secret first (separate skill)
node skills/secrets-manager/secrets-manager.js --store api_key sk-abc123

# 2) Inject into a command → writes a temp script, prints its path
node skills/secrets-inject/secrets-inject.js --inject "curl -H 'Authorization: Bearer {{api_key}}' https://api.example.com/v1"
# Output: [secrets-inject] ✅ Injected 1 secret(s) into: /tmp/secrets-inject-12345-1.sh
#         [secrets-inject]    Run with:  sh /tmp/secrets-inject-12345-1.sh

# 3) Run it, then CLEAN UP
sh /tmp/secrets-inject-12345-1.sh
node skills/secrets-inject/secrets-inject.js --cleanup-tmp
```

### Print to stdout (DANGEROUS — requires explicit confirmation)

```bash
node skills/secrets-inject/secrets-inject.js --inject-stdout --confirm-expose "echo {{api_key}}"
# Will print the resolved command with the plaintext secret.
```

The skill **refuses** to print to stdout without `--confirm-expose`.

## Cleanup

Temp injection files are tracked in `memory/secrets/.tmp-injections.json`
and removed by `--cleanup-tmp`. They are NOT auto-removed — **delete them
after use.** An undeleted temp file is plaintext-on-disk exposure.

## Security Notes

- Temp scripts are chmod 0600 but are still **plaintext on disk** — the only
  protection is file permissions and your diligence in deleting them.
- Prefer `secrets-manager --get --raw > /tmp/k && chmod 600 /tmp/k` and pass
  the file path to a command instead of inline injection when possible.
- Never run this on a shared host, container, or CI runner you don't fully
  trust.
- This skill does NOT store secrets — it only reads the secrets-manager store.

## What this skill does NOT do

- Does NOT store secrets (that's `secrets-manager`).
- Does NOT transmit secrets anywhere (it only substitutes them locally).
- Does NOT auto-clean temp files (you must run `--cleanup-tmp`).
