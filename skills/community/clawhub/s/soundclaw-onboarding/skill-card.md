## Description:

Run the OpenClaw-first SoundClaw readiness check and route operators to the next owned step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catholicbeer](https://clawhub.ai/user/catholicbeer)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and developers use this skill to check whether a SoundClaw backend is available in an OpenClaw workspace, understand readiness status, and get the next documented step when the backend is missing or degraded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users toward running a downloaded installer with sudo.

Mitigation: Verify that the SoundClaw release source is trusted and confirm the exact archive with a checksum or signature from a trusted channel before running the installer as root.

Risk: A backend marker alone may not prove the SoundClaw runtime is ready.

Mitigation: Use the documented runtime status command and report degraded or unavailable runtime status without claiming the host was repaired.

## Reference(s):

- [SoundClaw Onboarding README](references/README.md)
- [SoundClaw Onboarding Compatibility](references/compatibility.md)
- [SoundClaw Onboarding Examples](references/examples.md)
- [SoundClaw Onboarding Source](https://github.com/catholicbeer/soundclaw-skills/tree/main/skills/soundclaw-onboarding)
- [SoundClaw Releases](https://github.com/catholicbeer/soundclaw-release/releases)
- [ClawHub Skill Page](https://clawhub.ai/catholicbeer/skills/soundclaw-onboarding)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the agent to run narrow local readiness checks and report whether the backend marker is missing, ready, or degraded.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
