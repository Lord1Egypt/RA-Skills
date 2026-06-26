# Setup - Shelly

Read this when `~/shelly/` does not exist or is empty.
Keep onboarding short and immediately useful.

## Operating Priorities

- Answer the current user request first.
- Confirm when Shelly support should auto-activate.
- Determine allowed execution mode: read-only, guided writes, or approved apply mode.
- Capture only context needed for reliable control and safe automations.

## First Activation Flow

1. Confirm activation boundaries early:
- Should this activate whenever Shelly, relay, switch, power meter, automation, or scene terms are mentioned?
- Should behavior be proactive or only on explicit request?
- Are there contexts where this must never auto-activate?

2. Confirm environment model:
- local network scope and reachability
- cloud usage requirements and token availability
- MQTT broker usage, if any
- primary objective (single-device control, fleet orchestration, diagnostics)

3. Confirm risk and write boundaries:
- inspection only vs command execution allowed
- single-device canary first vs batch rollout allowed
- mandatory verification checkpoints after each write

4. If context is approved, initialize local workspace:
```bash
mkdir -p ~/shelly
touch ~/shelly/{memory.md,environments.md,devices.md,automations.md,incidents.md}
chmod 700 ~/shelly
chmod 600 ~/shelly/{memory.md,environments.md,devices.md,automations.md,incidents.md}
```

5. If `memory.md` is empty, initialize it from `memory-template.md`.

## Integration Defaults

- Default to read-only inspection until user approves writes.
- Prefer local control for immediate device-state workflows when reachable.
- Use one environment and one device cohort at a time during initial rollout.
- Require post-command verification before continuing to next step.

## What to Save

- activation preferences and do-not-activate boundaries
- control-plane choices and transport priorities
- stable method and component mappings by device model
- automation constraints, rollback rules, and recurring failures
- approved security and privacy constraints

## Guardrails

- Never request pasting raw cloud tokens into chat text.
- Never imply write success without explicit state verification evidence.
- Never recommend bypassing device authentication or platform policy controls.
