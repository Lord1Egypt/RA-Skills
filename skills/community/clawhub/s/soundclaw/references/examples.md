# SoundClaw Examples

## First Use

Operator: "Is SoundClaw ready?"

- Check `soundclawctl` on `PATH`, then the stable runtime path.
- If present, run `soundclawctl runtime status --json` through the located
  executable and summarize the runtime-owned result.
- If absent, point to
  `https://github.com/catholicbeer/soundclaw-release/releases`, name the
  public bundle and its `install.sh` wrapper, and stop before installation.

## Find And Play

Operator: "Play the rain asset in the office."

- Use `library list` or `library show` to resolve the asset only if needed.
- Use `outputs list`, `outputs show`, or `config defaults` to resolve the
  logical output only if needed.
- Clarify any remaining ambiguity.
- Run `soundclawctl playback play --asset <id> --output <id> --json` and report
  only the runtime-owned result.

## Stop

Operator: "Stop the office."

- Resolve the named logical output.
- Run `soundclawctl playback stop --output <id> --json`.

## Health And Identity

Operator: "What is installed and is it healthy?"

- Report backend identity from `soundclawctl deployment status --json`.
- Report health from `soundclawctl runtime status --json`.
- Do not infer the installed ClawHub version from either response; use native
  OpenClaw/ClawHub origin and lock evidence for product provenance.

## Safe Deferral

Operator: "Repair the service and reinstall everything."

- Explain that backend repair and installation are outside the skill boundary.
- Do not run service, package-manager, copy, rsync, or Git-sync commands.
- Point to the verified public release bundle workflow when installation is
  genuinely required.
