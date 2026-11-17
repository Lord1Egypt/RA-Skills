## Description:

Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to troubleshoot OpenClaw gateway routes, QR or setup-code failures, pairing approvals, expired bootstrap tokens, and related Tailscale or public URL configuration issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QR or setup-code JSON may expose sensitive OpenClaw pairing setup details.

Mitigation: Treat setup payloads as sensitive and avoid sharing raw command output.

Risk: Approving the latest pending device may authorize an unintended device.

Mitigation: Require explicit verification of the pending device before approving any pairing request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1yihui/skills/yihui-node-connect)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
