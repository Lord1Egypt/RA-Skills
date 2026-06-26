# Setup - Sonoff

Read this when `~/sonoff/` does not exist or is empty.
Keep onboarding short and immediately useful.

## Operating Priorities

- Answer the current user request first.
- Confirm when SONOFF support should auto-activate.
- Determine allowed execution mode: read-only, guided writes, or approved apply mode.
- Capture only context needed for reliable control and safe automation.

## First Activation Flow

1. Confirm activation boundaries early:
- Should this activate whenever SONOFF, eWeLink, relay, switch, iHost, or LAN-control terms are mentioned?
- Should behavior be proactive or only on explicit request?
- Are there contexts where this must never auto-activate?

2. Confirm environment model:
- cloud-only, LAN-only, or mixed control
- iHost presence and local API usage
- DIY mode usage for compatible devices
- primary objective (single-device control, fleet orchestration, diagnostics)

3. Confirm risk and write boundaries:
- inspection only vs command execution allowed
- one-device canary first vs batch rollout allowed
- mandatory verification checkpoints after each write

4. If context is approved, initialize local workspace:
```bash
mkdir -p ~/sonoff
touch ~/sonoff/{memory.md,environments.md,devices.md,automations.md,incidents.md}
chmod 700 ~/sonoff
chmod 600 ~/sonoff/{memory.md,environments.md,devices.md,automations.md,incidents.md}
```

5. If `memory.md` is empty, initialize it from `memory-template.md`.

## Integration Defaults

- Default to read-only inspection until user approves writes.
- Confirm control-plane precedence before first command.
- Use one environment and one device cohort at a time during initial rollout.
- Require post-command verification before continuing to next step.

## What to Save

- activation preferences and do-not-activate boundaries
- control-plane choices and mode eligibility assumptions
- model-specific command and capability mappings
- automation constraints, rollback rules, and recurring failures
- approved security and privacy constraints

## Guardrails

- Never request pasting raw eWeLink tokens into chat text.
- Never imply write success without explicit state verification evidence.
- Never recommend bypassing authentication or platform policy controls.
