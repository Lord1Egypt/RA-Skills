# Compatibility

Operator job: First-use onboarding and readiness checking for SoundClaw inside OpenClaw.

Runtime dependency:

- Status: Pending current runtime release-line declaration for the runtime-side readiness command.
- Contract reference: `soundclaw/docs/runtime-spec.md`
- Command(s): `soundclawctl runtime status [--json]`
- Command(s): `/opt/soundclaw/runtime/current/bin/soundclawctl runtime status --json`
- Local preflight note: this skill may do a narrow presence check for
  documented backend markers before it attempts the runtime CLI. The supported
  markers are `soundclawctl` on `PATH` and the stable runtime-owned executable
  path `/opt/soundclaw/runtime/current/bin/soundclawctl`.
- Install-flow handoff: if the backend marker is missing, direct the operator
  to the public release surface
  `https://github.com/catholicbeer/soundclaw-release/releases`, then to the
  extracted-bundle install wrapper `install.sh`, which delegates to the bundled
  pi-kit setup path under `repos/soundclaw-pi-kit/scripts/setup.sh`. The
  supported default return path is the same active OpenClaw workspace unless
  the host explicitly wires a shared skills path into discovery.

Minimum compatible runtime release line: Pending definition in `soundclaw-runtime`.

Tested runtime release line: Not yet validated against a promoted runtime release line.

Packaging target: Plain skill

ClawHub publication status: Ready for first publish as `soundclaw-onboarding` version `1.0.0`.
