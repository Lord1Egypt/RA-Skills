# SoundClaw

Purpose: provide the one supported OpenClaw-facing SoundClaw product, with
first-run onboarding and later normal capability routing in the same package.

Production identity: `@catholicbeer/soundclaw`

Runtime dependency: documented backend markers followed by promoted
`soundclawctl` commands. This skill does not install or repair the backend.

## Operator Job

On first use, determine whether the SoundClaw backend is present and healthy.
When it is missing, point the operator only to the public GitHub release bundle
and stop before host mutation. When it is ready, translate ordinary SoundClaw
requests into the supported runtime CLI boundary.

The same installed product covers asset discovery, output discovery, playback,
stop, global volume, runtime health, configuration validation, deployment
identity, low-risk output and zone administration, policy, Layer and Scene
requests, and source-preserving ingest guidance. The source repo keeps leaf
skill directories as authoring and test modules; production does not require
those modules to be installed or published separately.

## Command Boundary

Use only command shapes declared in `skill.toml`. Important families are:

- `soundclawctl runtime status|doctor|reload`
- `soundclawctl deployment status`
- `soundclawctl config defaults|validate`
- `soundclawctl library list|show|ingest`
- `soundclawctl outputs ...` and `soundclawctl zones ...`
- `soundclawctl playback play|stop`
- `soundclawctl volume show|set-global`
- `soundclawctl policy status|hold|clear|resume`
- `soundclawctl familiar run-layer|stop-layer`
- `soundclawctl scene apply|show|explain|stop`

Capability-specific flags and safety rules are in `prompt.md` and the exported
references. If the installed runtime does not support a declared capability,
report it as unavailable; do not emulate it.

## Identity Boundary

Keep three facts separate:

1. ClawHub product provenance: exact `@catholicbeer/soundclaw` version plus
   OpenClaw/ClawHub origin and lock evidence.
2. Backend deployment identity: `soundclawctl deployment status --json`.
3. Current runtime health: `soundclawctl runtime status --json`.

Backend installation must not change the first fact.

## Guardrails

- Stay inside the `soundclaw-skills` boundary.
- Do not download, install, repair, update, or restart backend components.
- Do not copy, sync, reconcile, shadow, or remove installed skills.
- Do not call private runtime or Web UI interfaces.
- Clarify the target before a mutating command and surface runtime failures.
- Keep private feedback optional and outside this public package.
