# Setup - Tuya Smart

Read this when `~/tuya/` does not exist or is empty.
Keep onboarding short and immediately useful.

## Operating Priorities

- Answer the current user request first.
- Confirm when Tuya Smart support should auto-activate.
- Determine allowed execution mode: read-only, guided writes, or approved apply mode.
- Capture only context needed for reliable control and safe automation.

## First Activation Flow

1. Confirm activation boundaries early:
- Should this activate whenever Tuya, Smart Life, IoT switches, lights, plugs, sensors, or scenes are mentioned?
- Should behavior be proactive or only on explicit request?
- Are there contexts where this must never auto-activate?

2. Confirm environment model:
- Tuya cloud region and project context
- account model (cloud project only, app account linked, or both)
- primary objective (single-device control, fleet orchestration, diagnostics, or migration)

3. Confirm risk and write boundaries:
- inspection only vs command execution allowed
- single-device first vs bulk rollout allowed
- mandatory verification checkpoints after each write

4. If context is approved, initialize local workspace:
```bash
mkdir -p ~/tuya
touch ~/tuya/{memory.md,environments.md,devices.md,automations.md,incidents.md}
chmod 700 ~/tuya
chmod 600 ~/tuya/{memory.md,environments.md,devices.md,automations.md,incidents.md}
```

5. If `memory.md` is empty, initialize it from `memory-template.md`.

## Integration Defaults

- Default to read-only inspection until user approves writes.
- Require capability discovery before command generation.
- Use one environment and one device group at a time during initial rollout.
- Require post-command state verification before proceeding to next step.

## What to Save

- activation preferences and do-not-activate boundaries
- region and endpoint mapping decisions
- stable device command mappings by product category
- automation constraints, rollback plans, and known failure signatures
- approved security and privacy constraints

## Guardrails

- Never request pasting raw Access Secret values into chat text.
- Never imply write success without status verification evidence.
- Never recommend bypassing Tuya platform policies or undocumented endpoints.
