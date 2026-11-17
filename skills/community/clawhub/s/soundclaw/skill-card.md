## Description:

Onboard and operate SoundClaw through one thin OpenClaw-facing product and the promoted runtime CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catholicbeer](https://clawhub.ai/user/catholicbeer)

### License/Terms of Use:

MIT-0

## Use Case:

External SoundClaw operators use this skill to check backend readiness and route supported audio runtime requests through the promoted SoundClaw CLI boundary. It helps resolve assets and outputs, start or stop playback, inspect health, adjust volume, manage low-risk topology changes, and guide source-preserving ingest while leaving backend installation and repair outside scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide mutating SoundClaw runtime operations, including volume changes, output or zone administration, runtime reload, scene or layer control, and library ingest.

Mitigation: Review mutating requests before approval, clarify the target and proposed change, and rely on runtime-owned JSON results rather than intent alone.

Risk: A missing or unhealthy backend could tempt an agent to install, repair, copy, or sync backend content outside the supported boundary.

Mitigation: Keep backend installation, repair, update, rollback, service manipulation, copying, syncing, and Git-based reconciliation out of scope; use the public release workflow only as a handoff.

Risk: Backend deployment identity, ClawHub product provenance, and current runtime health can be confused with each other.

Mitigation: Report ClawHub product evidence, backend deployment identity, and runtime health as separate facts, using only server-resolved provenance for provenance claims.

## Reference(s):

- [SoundClaw Operator Reference](references/README.md)
- [Compatibility](references/compatibility.md)
- [SoundClaw Examples](references/examples.md)
- [SoundClaw ClawHub Page](https://clawhub.ai/catholicbeer/skills/soundclaw)
- [SoundClaw Skill Homepage](https://github.com/catholicbeer/soundclaw-skills/tree/main/skills/soundclaw)
- [SoundClaw Backend Release Bundles](https://github.com/catholicbeer/soundclaw-release/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and runtime JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses runtime-owned command results as authoritative and asks for missing asset, output, Scene, Layer, volume, or topology facts before proposing mutating commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
