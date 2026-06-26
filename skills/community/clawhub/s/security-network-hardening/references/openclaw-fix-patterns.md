# OpenClaw Fix Patterns

## Common findings and fixes

### Elevated wildcard access

Look for both global and agent-level settings in `~/.openclaw/openclaw.json`.

Bad:

```json
"allowFrom": {
  "<channel>": ["*"]
}
```

Safer:

```json
"allowFrom": {
  "<channel>": []
}
```

### Credentials directory too permissive

Restrict the credentials directory so only the owner can access it.

Recommended fix pattern:

```bash
chmod 700 <openclaw-credentials-dir>
```

### Missing gateway auth rate limiting

Recommended baseline:

```json
"auth": {
  "mode": "token",
  "token": "...",
  "rateLimit": {
    "maxAttempts": 10,
    "windowMs": 60000,
    "lockoutMs": 300000
  }
}
```

### Ineffective `gateway.nodes.denyCommands`

Do not invent command IDs. If audit flags custom deny entries as ineffective and they are not needed, remove the custom denylist instead of replacing it with guesses.

### Workspace skill symlink escape

If a workspace skill resolves outside the workspace root, replace the symlink with a real in-workspace copy.

## Verification commands

```bash
openclaw security audit --deep
openclaw gateway status
python3 -m json.tool ~/.openclaw/openclaw.json >/dev/null
openclaw status --deep
```

## Baseline pattern

A good baseline usually includes:
- remove elevated wildcard access from interactive channels
- set the OpenClaw credentials directory to `700`
- add `gateway.auth.rateLimit`
- remove ineffective custom `gateway.nodes.denyCommands`
- replace workspace skill symlinks that escape the workspace root
