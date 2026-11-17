# SoundClaw Onboarding

Purpose: Run the first-use SoundClaw readiness check inside OpenClaw and give the next safe step when the backend is missing or degraded.

Runtime dependency:

- narrow local presence check for documented backend markers: `soundclawctl` on
  `PATH`, then `/opt/soundclaw/runtime/current/bin/soundclawctl`
- once a backend marker is present, runtime status through that executable

## Operator Job

This skill handles first-use requests such as "is SoundClaw installed here?",
"help me get started with SoundClaw in OpenClaw", or "rerun the readiness
check after backend install."

It should keep OpenClaw as the discovery surface while making the next owned
step explicit. If the backend marker is missing, the skill should say that
SoundClaw does not appear to be installed locally, point the operator to the
public release surface
`https://github.com/catholicbeer/soundclaw-release/releases`,
and tell them to download and extract one
`soundclaw-pi-release-<release-id>.tar.gz` bundle on the Raspberry Pi. The
next install step should use the bundled wrapper from the extracted bundle
root (`sudo ./install.sh --help` for options), which delegates to bundled
pi-kit scripts under `repos/soundclaw-pi-kit/scripts/`. Then tell the operator
to return to the same OpenClaw workspace and rerun the readiness check after
the backend install completes.

If the backend marker is present, the skill should confirm readiness through
the promoted runtime CLI boundary rather than inventing a second local
contract. Prefer `soundclawctl runtime status [--json]` when `soundclawctl` is
visible on `PATH`; otherwise use the documented stable runtime path:
`/opt/soundclaw/runtime/current/bin/soundclawctl runtime status --json`. When
the runtime looks healthy enough, the skill should say that the SoundClaw
skills in this OpenClaw workspace are ready for normal operator flows such as
playback, asset lookup, output inspection, runtime health, and config
validation.

## Guardrails

- Keep the skill inside the `soundclaw-skills` boundary.
- Treat the active OpenClaw workspace as the supported default install target.
  Mention a shared skills path only when the host under test explicitly
  documents that exception.
- Do not perform host-changing actions.
- Do not fetch installers, packages, or backend artifacts from the skill.
- Do not invent runtime behavior that has not been promoted.
- Do not claim installation success from the marker check alone when
  `soundclawctl runtime status [--json]` still reports a problem.
- Make failure wording explicit about what the operator can do next.
