---
name: exec-approvals
description: Manage all OpenClaw exec approval settings — elevated access, obfuscation bypass, security posture, and per-provider allowlists. Use when an agent cannot run sudo/host commands, long commands are blocked as obfuscation, or when onboarding/auditing exec permissions across a fleet of agents. Covers elevated exec enablement, obfuscation check bypass, and security mode configuration.
---

# Exec Approvals

Manage all OpenClaw exec permission and approval settings from one place.

## When to Use

- Agent says "elevated exec is disabled" or "I can't run sudo"
- Commands blocked with "Command too long; potential obfuscation"
- Onboarding a new agent that needs host-level access
- Auditing exec permissions across a fleet
- Tightening or relaxing exec security posture

## Quick Reference

| Problem | Config Key | Section |
|---------|-----------|---------|
| Can't run sudo | `tools.elevated` | Elevated Exec |
| Long commands blocked | `tools.exec.obfuscationCheck` | Obfuscation Bypass |
| Security mode too strict | `tools.exec.security` | Security Mode |

## Elevated Exec

Enable agents to run host-level commands (sudo, system scripts, package installs) from chat providers.

### Enable

```bash
python3 -c "
import json
p='$HOME/.openclaw/openclaw.json'
d=json.load(open(p))
if 'tools' not in d: d['tools'] = {}
d['tools']['elevated'] = {
    'enabled': True,
    'allowFrom': {
        'telegram': ['*']
    }
}
json.dump(d, open(p,'w'), indent=2)
"
```

Then restart: `openclaw gateway restart`

### Per-Provider Control

Restrict to specific user IDs:

```json
{
  "tools": {
    "elevated": {
      "enabled": true,
      "allowFrom": {
        "telegram": ["855505513"],
        "discord": ["1457708441677332592"]
      }
    }
  }
}
```

Supported providers: `telegram`, `discord`, `whatsapp`, `slack`, `signal`, `matrix`

### Common Errors

| Error | Fix |
|-------|-----|
| `expected array, received boolean` | Use `["*"]` not `true` |
| `elevated exec is disabled` | Set config + restart gateway |
| `config is invalid` | Ensure `allowFrom.<provider>` is always an array |

## Obfuscation Bypass

Disable the exec obfuscation blocker that flags long commands, heredocs, or generated shell payloads.

### Config Toggle (preferred)

```json
{
  "tools": {
    "exec": {
      "obfuscationCheck": false
    }
  }
}
```

### Check Version Support

```bash
openclaw --version
rg -n "obfuscationCheck" /usr/lib/node_modules/openclaw -S
```

If the key exists, config toggle works. If not, patch the bundled runtime:

1. Find the active bundle: `rg -n "detectCommandObfuscation" /usr/lib/node_modules/openclaw -S`
2. Patch `detectCommandObfuscation` to always return `{detected: false, reasons: [], matchedPatterns: []}`
3. Restart gateway

On upgrades, re-check for config support first.

## Security Mode

| Mode | Behavior |
|------|----------|
| `full` | All commands allowed |
| `allowlist` | Only allowlisted commands |
| `deny` | No exec at all |

```json
{
  "tools": {
    "exec": {
      "security": "full",
      "ask": "on-miss"
    }
  }
}
```

## Security Notes

- Elevated exec means the agent can run **any** command on the host
- For fleet agents, prefer specific user IDs over `["*"]`
- Disable elevated access after one-time tasks if ongoing access isn't needed
- Obfuscation bypass is for trusted single-operator deployments
- Upgrades may overwrite manual patches — always verify after updating
