---
name: ranking-of-claws
description: "Reports per-model token deltas from JSONL sessions to Ranking of Claws"
metadata:
  openclaw:
    emoji: "👑"
    events: ["gateway:startup", "command:new", "command:reset", "command:compact"]
---

# Ranking of Claws Hook

This hook reads JSONL session logs, computes token deltas per model, and reports them to ROC.

## Registration source

- `~/.openclaw/workspace/skills/ranking-of-claws/config.json`

The config is created by install script (`scripts/install.sh`) and includes:

- `agent_name`
- `country`
- `gateway_id`
- `registered_at`

No writes to `openclaw.json`.

## Session source

- `~/.openclaw/agents/*/sessions/*.jsonl`

Each report includes both token counts and model id.

## Activation

```bash
openclaw hooks install ./skills/ranking-of-claws/hooks
openclaw gateway restart
openclaw hooks list
```
