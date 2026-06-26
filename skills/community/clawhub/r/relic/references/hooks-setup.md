# Hook Setup

Relic includes a bundled optional OpenClaw hook named `relic-capture`.

The hook is not the primary package surface. Install the skill first, then optionally enable the hook for passive capture.

## What the hook does

- fires on `agent:stop`
- reads the session transcript from hook context
- forwards the transcript to `hooks/auto_capture.py`
- lets the Python capture script filter obvious tool and permission noise
- lets the Python capture script extract likely durable user signals
- appends observations to the configured relic vault

## Verify the bundled hook

```bash
openclaw hooks info relic-capture
openclaw hooks check
```

## Enable the hook

```bash
openclaw hooks enable relic-capture
```

## Vault contract

Default vault path:

```text
~/.openclaw/workspace/projects/relic/vault/
```

Override with:

```bash
export RELIC_VAULT_PATH="/absolute/path/to/your/relic-vault"
```

The TypeScript/JavaScript hook handlers and `hooks/auto_capture.py` all use this same environment contract.

## Manual smoke test

```bash
echo '{"transcript": "I value clarity. I prefer simple workflows. My goal is to ship relic."}' | \
  RELIC_VAULT_PATH="$HOME/.openclaw/workspace/projects/relic/vault" \
  python3 ~/.openclaw/workspace/skills/relic/hooks/auto_capture.py
```

Expected result: JSON output with one or more captured observations.

## End-to-end verification

1. Start a real OpenClaw conversation.
2. Say something with values, preferences, or goals.
3. End the session so `agent:stop` fires.
4. Inspect the vault inbox:

```bash
tail -5 "$HOME/.openclaw/workspace/projects/relic/vault/inbox.ndjson"
```

If you just installed or moved the skill or hook, start a fresh OpenClaw session or restart the gateway before verifying discovery.
