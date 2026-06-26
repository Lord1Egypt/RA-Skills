---
name: reaction-processor
description: Record real OpenClaw events and reactions for the current closed-loop workflow. Use for logging duplicate-skipped and proposal-created outcomes in public.openclaw_agent_events and public.openclaw_agent_reactions, and for updating trigger fire metadata when appropriate.
metadata: {"clawdbot":{"notes":["Uses only public.openclaw_* tables","Current implementation supports the stale_missions_alert flow","Wraps the real event/reaction pattern already present in stale_missions_engine.sh"]}}
---

# Reaction Processor

Record real events and reactions for the current OpenClaw closed loop.

## Commands

- Record duplicate skipped outcome for stale missions
  `{baseDir}/scripts/reaction-processor.sh record-duplicate-skipped`

- Record proposal created outcome for stale missions
  `{baseDir}/scripts/reaction-processor.sh record-proposal-created`

## Notes

- This skill uses the current real event/reaction pattern already implemented in the workspace.
- It works against `public.openclaw_agent_events`, `public.openclaw_agent_reactions`, and `public.openclaw_trigger_rules`.
- It is currently scoped to the `stale_missions_alert` flow.
