## Description:

Install, configure, validate, or troubleshoot the TeamClaw OpenClaw plugin for virtual software-team workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topcheer](https://clawhub.ai/user/topcheer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install TeamClaw, choose an appropriate OpenClaw controller or worker topology, generate minimal configuration snippets, and validate a first successful run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable installers and latest-tag worker images can change after review.

Mitigation: Pin the TeamClaw package and worker image to reviewed versions or digests before using the skill in sensitive environments.

Risk: Containerized or Kubernetes workers can receive broader workspace or infrastructure access than needed.

Mitigation: Run Docker and Kubernetes workers with least privilege and grant only the workspace access required for the chosen topology.

Risk: Running the installer with elevated privileges can increase the impact of a compromised or unexpected install path.

Mitigation: Avoid administrator privileges for installation unless a reviewed deployment procedure explicitly requires them.

## Reference(s):

- [TeamClaw ClawHub Skill Page](https://clawhub.ai/topcheer/skills/teamclaw-setup)
- [TeamClaw Homepage](https://github.com/topcheer/teamclaw)
- [TeamClaw Repository](https://github.com/topcheer/teamclaw)
- [TeamClaw Installation Documentation](https://github.com/topcheer/teamclaw/blob/main/INSTALL.md)
- [TeamClaw Changelog](https://github.com/topcheer/teamclaw/releases)
- [TeamClaw Install Modes](references/install-modes.md)
- [TeamClaw Validation Checklist](references/validation-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an install command, minimal topology-specific configuration, startup guidance, validation commands, and a smoke-test task.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
