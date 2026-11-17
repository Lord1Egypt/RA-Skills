---
name: soundclaw-onboarding
description: Run the OpenClaw-first SoundClaw readiness check and route operators to the next owned step.
version: 1.0.0
homepage: https://github.com/catholicbeer/soundclaw-skills/tree/main/skills/soundclaw-onboarding
metadata:
  openclaw:
    os: ["linux"]
---

# SoundClaw Onboarding

Use this skill when the operator wants to get started with SoundClaw in
OpenClaw, needs a first-use readiness check, or wants to rerun that check after
the backend install flow.

## Behavior

- Start with a narrow local preflight for documented backend markers. Check for
  `soundclawctl` on `PATH`, and if it is not visible there, check the stable
  runtime-owned path `/opt/soundclaw/runtime/current/bin/soundclawctl`.
- If neither marker exists, explain that the SoundClaw backend does not appear
  to be installed locally.
- For the missing-backend path, point the operator to the public SoundClaw
  releases surface at
  `https://github.com/catholicbeer/soundclaw-release/releases`.
  Tell them to download one release bundle named
  `soundclaw-pi-release-<release-id>.tar.gz` on the Raspberry Pi, extract it,
  and run the bundled installer wrapper from the extracted bundle root
  (`sudo ./install.sh --help` for options). The bundle already includes the
  needed pi-kit setup scripts under `repos/soundclaw-pi-kit/scripts/`.
  Tell them to return to the same OpenClaw workspace after install, and stop
  there.
- If a backend marker is present, run runtime status through the executable
  that was found, such as `soundclawctl runtime status [--json]` or
  `/opt/soundclaw/runtime/current/bin/soundclawctl runtime status --json`.
- Summarize the result in operator language as one of:
  - backend marker missing
  - backend present and runtime ready enough for normal use
  - backend present but runtime still degraded or unavailable
- If runtime status looks healthy, say that the SoundClaw skill set in this
  OpenClaw workspace is ready for normal flows such as playback, asset lookup,
  output inspection, runtime health, and config validation.
- If runtime status is degraded or unavailable, explain that the backend marker
  is present but the runtime still needs attention. Point to the `Runtime
  Health` skill or the documented runtime diagnostic path rather than claiming
  the host was repaired.
- Keep success messages short and concrete.
- Keep failures explicit about whether the problem appears to be in the skill
  layer, the runtime layer, or the missing-backend onboarding path.

## Out Of Scope

- Installing the backend
- Downloading release bundles or packages
- Host repair
- Editing OpenClaw discovery paths
- Service manipulation
- Runtime-internal IPC
- Hidden retries for mutating commands

## Local References

- Read `{baseDir}/references/README.md` for the operator job, guardrails, and intent boundary.
- Read `{baseDir}/references/examples.md` for example requests and expected behavior.
- Read `{baseDir}/references/compatibility.md` for runtime dependency and packaging notes.
