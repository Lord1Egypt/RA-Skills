## Description:

Install, verify, update, or roll back the bundled Streaming Mode Control UI for OpenClaw 2026.9.6 on Linux, macOS, or Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[svetlyoh](https://clawhub.ai/user/svetlyoh)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and administrators use this skill to install, check, update, troubleshoot, or roll back a wider, larger-text Control UI for streaming on the Gateway machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation replaces the OpenClaw Control UI on the Gateway machine.

Mitigation: Install only when replacement is intended; keep the state and original-UI backup until rollback is no longer needed.

Risk: A version, checksum, or build-identity mismatch may indicate an incompatible payload or installation.

Mitigation: Do not bypass validation errors; use a release matching the installed OpenClaw build.

## Reference(s):

- [ClawHub Streaming Mode release](https://clawhub.ai/svetlyoh/skills/streaming-mode)
- [Skill homepage listed in metadata](https://github.com/svetlyoh/web-wallet/tree/master/openclaw/skills/streaming-mode)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes status, installation, troubleshooting, and rollback guidance.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
