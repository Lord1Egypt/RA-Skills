## Description:

Install, configure, validate, or troubleshoot the TeamClaw OpenClaw plugin for virtual software-team workflows. Use when users want TeamClaw setup help, controller or worker config snippets, on-demand process/docker/kubernetes workers, external worker registration, or safe first-run validation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topcheer](https://clawhub.ai/user/topcheer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using OpenClaw use this skill to install and configure TeamClaw, choose a suitable worker setup, and validate a first run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation uses an unpinned npm package and bypasses installation safety checks, creating supply-chain risk.

Mitigation: Review the installer and its source before running it; use a pinned package version when available and understand the safety-check override. Take particular care with shared-main mode.

## Reference(s):

- [Install modes](artifact/references/install-modes.md)
- [Validation checklist](artifact/references/validation-checklist.md)
- [TeamClaw repository](https://github.com/topcheer/teamclaw)
- [TeamClaw installation documentation](https://github.com/topcheer/teamclaw/blob/main/INSTALL.md)
- [TeamClaw releases](https://github.com/topcheer/teamclaw/releases)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Topology-specific setup and validation guidance]

## Skill Version(s):

1.0.2 (source: target release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
