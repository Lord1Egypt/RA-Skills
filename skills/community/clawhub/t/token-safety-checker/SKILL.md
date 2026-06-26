---
name: token-safety-checker
description: Scan openclaw.json for plaintext secrets (tokens, API keys, passwords) and migrate them to environment variables using SecretRef. Use when the user asks to "check token safety", "privatize secrets", "move tokens to env vars", "audit openclaw config for secrets", or after any openclaw.json edit that may have introduced plaintext credentials. Also use when setting up a new OpenClaw instance for the first time.
homepage: https://github.com/maoisdamao/token-safety-checker
author: maoisdamao
---

# Token Safety Checker

Scan `openclaw.json` for plaintext secrets and migrate them to environment variables via SecretRef.
All operations run locally. Secret values are never passed as CLI arguments, never logged, and never appear in agent context.

## Script

Single entry point: `scripts/safeclaw.py`

```
python3 safeclaw.py scan    [--config PATH]
python3 safeclaw.py migrate [--findings JSON] [--config PATH] [--profile PATH] [--dry-run] [--restore]
```

## How secrets are protected

| Risk | Mitigation |
|------|-----------|
| Secret values in `scan` output | `scan` returns **paths + lengths only** — never values |
| Secret values in CLI args | `migrate` reads values from disk internally — never via `--values` arg |
| Secret values in dry-run output | Masked as `export VAR="***"` |
| Secret values in agent context | `findings` JSON only contains `path`, `env_var`, `length` — safe to pass through SKILL |
| Secret values in logs | No logging of values at any point |

## Workflow

### 1. Scan

```bash
python3 <skill_dir>/scripts/safeclaw.py scan [--config ~/.openclaw/openclaw.json]
```

Output (safe to use in agent context — no secret values):
```json
{
  "findings": [
    { "path": "channels.discord.token", "env_var": "OPENCLAW_DISCORD_TOKEN", "length": 72 }
  ],
  "shell": { "name": "zsh", "profile": "~/.zshrc", "source_cmd": "source ~/.zshrc" }
}
```

Exit 0 = clean → report and stop. Exit 1 = findings → continue. Exit 2 = config not found.

### 2. Show findings to user and confirm

Present the findings table (`path | env_var | length`). Allow renaming env vars. **Do not proceed without explicit confirmation.**

### 3. Dry-run

```bash
python3 <skill_dir>/scripts/safeclaw.py migrate \
  --findings '<findings JSON from step 1>' \
  --dry-run
```

Show output to user. The script re-reads config from disk to verify findings are still current. Confirm before proceeding.

### 4. Migrate

```bash
python3 <skill_dir>/scripts/safeclaw.py migrate \
  --findings '<findings JSON from step 1>'
```

The script:
1. **Re-scans** config from disk to confirm findings are still plaintext
2. **Backs up** `openclaw.json` → `openclaw.json.bak`
3. **Reads** secret values internally from disk (not from CLI args)
4. **Appends** env exports to shell profile (skips duplicates, masks values in output)
5. **Replaces** plaintext values with SecretRef in `openclaw.json`

### 5. Source profile + restart gateway

⚠️ Check how the gateway is managed:

**Shell-launched (most local setups):**
```bash
source <profile>
openclaw gateway restart
```

**systemd:** Add vars to `EnvironmentFile=` in the unit — sourcing a shell profile won't work.

**Docker:** Pass via `-e` or `environment:` in compose.

### 6. Verify

```bash
python3 <skill_dir>/scripts/safeclaw.py scan   # exit 0 = clean
openclaw gateway status
```

### 7. Rollback

```bash
python3 <skill_dir>/scripts/safeclaw.py migrate --restore
```

## SecretRef format

```json
{ "source": "env",  "provider": "default", "id": "MY_ENV_VAR" }
{ "source": "file", "provider": "default", "id": "/path/to/secret.txt" }
{ "source": "exec", "provider": "default", "id": "command --prints --secret" }
```

`env` is recommended for most setups. For higher-security environments, prefer `file` or `exec`.
