# Compatibility

Operator job: first-run onboarding and normal SoundClaw operation through one
OpenClaw-facing product.

Production identity: `@catholicbeer/soundclaw`

Runtime dependency:

- Status: pending an exact promoted runtime release-line declaration and fresh
  WDR/RTW proof.
- Contract reference: `soundclaw/docs/skills-spec.md` and the promoted command
  shapes owned by `soundclaw/docs/runtime-spec.md`.
- First-run markers: `soundclawctl` on `PATH`, then
  `/opt/soundclaw/runtime/current/bin/soundclawctl`.
- Missing-backend handoff: public GitHub release bundle from
  `https://github.com/catholicbeer/soundclaw-release/releases`; the skill does
  not fetch or install it.
- Normal operations: the `soundclawctl` commands declared in `skill.toml`.

Minimum compatible runtime release line: Pending. Do not infer compatibility
from the package version alone.

Tested runtime release line: Pending fresh WDR and RTW evidence for the
corrected ClawHub-product plus public-backend path.

Packaging target: Plain AgentSkills-compatible skill published as one ClawHub
product.

ClawHub publication status: Ready for first publish as
`@catholicbeer/soundclaw` version `1.0.0`.

Source leaf modules: authoring and test inputs only. They are not separate
supported production identities and are not runtime installation dependencies.
