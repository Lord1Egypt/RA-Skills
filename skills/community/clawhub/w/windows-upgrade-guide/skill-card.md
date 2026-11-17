## Description:

Provides Windows-focused OpenClaw installation, upgrade, and troubleshooting guidance for crashes, lost configuration, version compatibility, WeChat integration, and WSL versus native Windows setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Windows OpenClaw users use this skill to diagnose upgrade failures, compare WSL2 with native Windows installation, back up or migrate configuration, and recover from problematic OpenClaw versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reset commands can delete local OpenClaw configuration and data.

Mitigation: Back up ~/.openclaw and specific configuration files before running reset or reinstall steps; prefer migration or recovery steps first.

Risk: Remote installer pipelines and unpinned package execution can run code with elevated permissions.

Mitigation: Verify the source, package name, version, and requested permissions before execution; pin versions or use trusted installers where practical.

Risk: Global installs and administrator shell steps can change system-wide OpenClaw or Node.js state.

Mitigation: Review each command, use the least privileged environment practical, and test recovery steps in WSL2 or a non-production environment first.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai)
- [Microsoft WSL install guide](https://docs.microsoft.com/windows/wsl/install)
- [Node.js downloads](https://nodejs.org/)
- [OpenClaw issue tracker](https://github.com/openclaw/openclaw/issues)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline Bash and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that can modify or delete OpenClaw configuration; users should review and back up data before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
