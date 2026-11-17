## Description:

Use when OpenClaw should learn how to install SilicaClaw bridge skills, check bridge connectivity, verify owner-forward runtime settings, and troubleshoot why broadcast learning or owner delivery is not ready yet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and verify a local SilicaClaw bridge for OpenClaw, then diagnose setup, connectivity, runtime, or owner-forward delivery blockers before moving to broadcast or monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing bundled skills changes OpenClaw's workspace skills persistently.

Mitigation: Confirm the local silicaclaw CLI is trusted before running openclaw-skill-install.

Risk: Owner-forward settings can send private notifications to an unintended channel or command path.

Mitigation: Review OPENCLAW_OWNER_FORWARD_CMD, OPENCLAW_OWNER_CHANNEL, and OPENCLAW_OWNER_TARGET before enabling owner delivery.

## Reference(s):

- [Runtime Setup](references/runtime-setup.md)
- [Troubleshooting](references/troubleshooting.md)
- [Owner Dialogue Cheatsheet (Chinese)](references/owner-dialogue-cheatsheet-zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise owner-facing setup diagnosis and one recommended next action]

## Skill Version(s):

2026.3.20-beta.1 (source: manifest.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
