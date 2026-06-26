---
name: trigger-evaluator
description: Evaluate real OpenClaw trigger rules against the current database state. Use for heartbeat-style trigger checks, especially stale mission detection backed by public.openclaw_trigger_rules, public.openclaw_missions, and public.openclaw_proposals.
metadata: {"clawdbot":{"notes":["Wraps the real stale_missions_engine.sh script in the workspace","Uses only public.openclaw_* tables","Current supported trigger: stale_missions_alert"]}}
---

# Trigger Evaluator

Evaluate real trigger rules already implemented in this workspace.

## Commands

- Run the real trigger evaluator
  `{baseDir}/scripts/trigger-evaluator.sh evaluate stale_missions_alert`

- Inspect the current trigger row
  `{baseDir}/scripts/trigger-evaluator.sh inspect stale_missions_alert`

## Notes

- This skill does not invent new trigger logic.
- It wraps the current production script:
  `/home/cmart/.openclaw/workspace/scripts/stale_missions_engine.sh`
- Current supported trigger:
  `stale_missions_alert`
