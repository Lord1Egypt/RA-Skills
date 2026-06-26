# Examples

## Manual capture

```bash
python3 ~/.openclaw/workspace/skills/relic/scripts/capture_note.py "I prefer concise but opinionated assistants" --type preference
python3 ~/.openclaw/workspace/skills/relic/scripts/capture_note.py "I value durable local tools" --type value
```

## Distill and inspect

```bash
python3 ~/.openclaw/workspace/skills/relic/scripts/distill_facets.py
cat "${RELIC_VAULT_PATH:-$HOME/.openclaw/workspace/projects/relic/vault}/self-model.md"
cat "${RELIC_VAULT_PATH:-$HOME/.openclaw/workspace/projects/relic/vault}/facets.json"
```

## Drift and proposal workflow

```bash
python3 ~/.openclaw/workspace/skills/relic/scripts/drift_detection.py
python3 ~/.openclaw/workspace/skills/relic/scripts/propose_update.py
ls "${RELIC_VAULT_PATH:-$HOME/.openclaw/workspace/projects/relic/vault}/evolution/proposals"
```

## Export an agent prompt

```bash
python3 ~/.openclaw/workspace/skills/relic/scripts/render_export.py
cat "${RELIC_VAULT_PATH:-$HOME/.openclaw/workspace/projects/relic/vault}/exports/agent-prompt.md"
```

## Passive capture via hook

1. Enable `relic-capture`.
2. Have a normal OpenClaw conversation.
3. End the session.
4. Inspect `${RELIC_VAULT_PATH:-$HOME/.openclaw/workspace/projects/relic/vault}/inbox.ndjson`.

## Alternate vault path

```bash
export RELIC_VAULT_PATH="$HOME/private/relic-vault"
python3 ~/.openclaw/workspace/skills/relic/scripts/init_relic.py
python3 ~/.openclaw/workspace/skills/relic/scripts/distill_facets.py
```
