# Claw Host Environment Reference

The skill needs `ROLLINGGO_API_KEY` visible to its process. If the host drops it between runs, use host-managed injection instead of shell exports.

**This skill's key:** `rollinggo-searchflight`

## OpenClaw-family config

Inject at whichever level fits your setup — per-skill is preferred.

### Per-skill (recommended)

```json
{
  "skills": {
    "entries": {
      "rollinggo-searchflight": {
        "env": { "ROLLINGGO_API_KEY": "YOUR_KEY" }
      }
    }
  }
}
```

### Host-wide (when multiple skills share the key)

```json
{ "env": { "ROLLINGGO_API_KEY": "YOUR_KEY" } }
```

Or add to the host's `.env` file: `~/.openclaw/.env` (macOS/Linux) · `%USERPROFILE%\.openclaw\.env` (Windows).  
Override paths: `OPENCLAW_HOME`, `OPENCLAW_STATE_DIR`, or `OPENCLAW_CONFIG_PATH`.

### Shell import fallback

```json
{ "env": { "shellEnv": { "enabled": true, "timeoutMs": 15000 } } }
```

Use only when the key exists in the login shell but child processes cannot see it.

## Sandbox

Host-side env does **not** reach sandboxed processes automatically. Inject `ROLLINGGO_API_KEY` directly into the sandbox: `agents.defaults.sandbox.docker.env` or equivalent.
