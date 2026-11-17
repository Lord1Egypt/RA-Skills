# Security Hardening — keys.json Hygiene

Captured from the 2026-07-08 audit: 4 real `tvly-dev-...` keys were sitting in plaintext in `config/keys.json` on老大's NAS. The bundled `.gitignore` is a 34-byte stub that may not actually exclude them. Below is the migration path to environment variables.

## Threat model

| Vector | Risk | Impact |
|---|---|---|
| Backup leak (`/home/cubeSugar` → cloud sync) | High | All 4 keys exposed, attacker drains 4000 quota/month, account may be banned for ToS violation |
| Skill directory shared / published | Critical | Same as above, but adversary knows your account structure |
| `state/quota.json` leaked | Low | Reveals `last_sync_at` + key index map, useful for fingerprinting |
| `.gitignore` gap | High if you `git init` the parent | Sudden key exposure in commit history |

## Verify the .gitignore

```bash
cat /home/cubeSugar/.hermes/skills/openclaw-imports/tavily-quota-router/.gitignore
# Should exclude: config/keys.json  state/quota.json
# Real file is ~34 bytes — check it actually lists both
```

If either file is missing from the gitignore, add it:

```gitignore
config/keys.json
state/quota.json
```

## Migration to environment variables

The router script (`tavily_multi_key.py`) reads keys from JSON only. To swap to env-var-driven config, two options:

### Option A: wrapper script (least invasive)

Create `scripts/tavily_env.sh` that exports keys before calling the Python script:

```bash
#!/bin/bash
# scripts/tavily_env.sh
export TAVILY_KEY_1="${TAVILY_KEY_1}"
export TAVILY_KEY_2="${TAVILY_KEY_2}"
# ... as many as you have
exec python3 "$(dirname "$0")/tavily_multi_key.py" "$@"
```

Then in `config/keys.json` you'd still have a stub, but the **real** keys live in your shell env / secret manager. This is a half-measure — the JSON is still there.

### Option B: patch the script (cleaner)

Modify `load_config()` to read from `os.environ` when `config/keys.json` is absent:

```python
import os
def load_config():
    raw_cfg = load_json(CONFIG, {})
    if not raw_cfg.get('keys'):
        # Fall back to env vars: TAVILY_KEY_1, TAVILY_KEY_2, ...
        env_keys = []
        for i in range(1, 20):  # arbitrary upper bound
            k = os.environ.get(f'TAVILY_KEY_{i}')
            if k:
                env_keys.append({'key': k, 'account': os.environ.get(f'TAVILY_ACCOUNT_{i}'), 'notes': f'from env TAVILY_KEY_{i}'})
        if env_keys:
            return {'format_version': 2, 'cooldown_minutes': 10, 'keys': env_keys}
    # ... rest of original logic
```

Then `config/keys.json` only needs the example structure, real keys stay in `.bashrc` / systemd EnvironmentFile / secret manager.

## Quick wins (do these today)

1. **Check what `state/quota.json` shows** — if you don't recognize all 4 keys, rotate the unrecognized ones at https://app.tavily.com/home
2. **Verify the directory isn't in any git repo**:
   ```bash
   cd /home/cubeSugar/.hermes/skills/openclaw-imports/tavily-quota-router
   git rev-parse --is-inside-work-tree 2>/dev/null && echo "WARNING: in a git repo" || echo "safe"
   ```
3. **Audit your backup targets** — if `/home/cubeSugar` syncs to cloud (OneDrive, iCloud, Synology Cloud Sync, restic, etc.), those keys are syncing with it
4. **Consider per-key scoping** — Tavily allows you to create multiple keys under one account with separate quotas. If you want isolation per usage, create one key per agent

## Rotation policy (suggested)

- Every 90 days: rotate all 4 keys, update `config/keys.json`, run `test-keys` to confirm
- Immediately on: any unauthorized search spike visible in `state/quota.json` `plan_usage`
- On any backup leak suspicion: rotate all, audit Tavily usage dashboard for the last 7 days
