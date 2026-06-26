---
name: relic-capture
description: "Automatically captures durable user observations from OpenClaw conversations into the configured relic vault."
metadata: {"openclaw":{"events":["agent:stop"]}}
---

# Relic Capture Hook

Relic Capture is the optional bundled OpenClaw hook that adds passive capture to the relic skill package.

## What it does

- fires on `agent:stop`
- reads transcript data from hook context
- forwards transcript data to `hooks/auto_capture.py`
- lets the Python capture script filter obvious tool and permission noise
- lets the Python capture script extract likely durable user signals
- appends observations to the configured relic vault

## Verification

```bash
openclaw hooks info relic-capture
openclaw hooks check
openclaw hooks enable relic-capture
```

If you just installed or moved the package or hook, start a fresh OpenClaw session or restart the gateway before verifying discovery.

## Vault contract

Default vault path:

```text
~/.openclaw/workspace/projects/relic/vault/
```

Override with:

```bash
export RELIC_VAULT_PATH="/absolute/path/to/your/relic-vault"
```

## Runtime assets

- `hooks/auto_capture.py`
- `hooks/openclaw/handler.ts`
- `hooks/openclaw/handler.js`

The handlers and Python capture script use the same vault path contract so installed-package execution does not depend on the source repo layout.
