# Relic Hook Verification

Relic's passive capture is provided by the bundled optional `relic-capture` OpenClaw hook.

## Verify discovery

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

## Functional verification

1. Start a real OpenClaw conversation.
2. Say something that contains values, preferences, or goals.
3. End the session so the `agent:stop` hook fires.
4. Check the vault:

```bash
tail -5 "$HOME/.openclaw/workspace/projects/relic/vault/inbox.ndjson"
```

## Manual smoke test

```bash
echo '{"transcript": "I value clarity. I prefer simple systems. My goal is to ship relic."}' | \
  RELIC_VAULT_PATH="$HOME/.openclaw/workspace/projects/relic/vault" \
  python3 ~/.openclaw/workspace/skills/relic/hooks/auto_capture.py
```

Expected result: JSON output with one or more captured observations.
