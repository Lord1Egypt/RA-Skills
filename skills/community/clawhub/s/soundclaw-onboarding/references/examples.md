# SoundClaw Onboarding Examples

## Example Requests

- "Is SoundClaw installed here yet?"
- "Help me get started with SoundClaw in OpenClaw."
- "I just finished the Pi-kit install. Can you recheck SoundClaw readiness?"
- "Why does SoundClaw still not look ready?"

## Expected Skill Behavior

- Check for a documented backend marker before attempting the runtime CLI:
  `soundclawctl` on `PATH`, then
  `/opt/soundclaw/runtime/current/bin/soundclawctl`.
- If the marker is missing, point to the public
  `https://github.com/catholicbeer/soundclaw-release/releases` surface and tell the
  operator to download one `soundclaw-pi-release-<release-id>.tar.gz` bundle,
  run `sudo ./install.sh --help` from the extracted bundle root, then return to
  the same OpenClaw workspace after install.
- If the marker is present, use that executable's `runtime status --json`
  command to decide whether the backend looks ready for normal use.
- Keep the missing-backend path explicit, honest, and non-mutating.
- Treat a shared skills path as an exception only when the host docs explicitly
  name it.
