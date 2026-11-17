## Description:

Provides tool discovery guidance and shell one-liner references for sysadmin, DevOps, and security troubleshooting tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdrhyne](https://clawhub.ai/user/jdrhyne)

### License/Terms of Use:


## Use Case:

Developers, sysadmins, DevOps engineers, and security practitioners use this skill to select operational tools and draft shell commands for network, DNS, TLS, process, log, container, and security troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes high-risk copy-paste commands for system administration and security work.

Mitigation: Review each proposed command before execution and avoid commands that modify critical configuration, wipe data, capture credentials, flood networks, or expose shells unless the environment is owned, authorized, and isolated.

Risk: The refresh workflow can pull mutable upstream content into the reference files.

Mitigation: Avoid automatic refresh for production use, or review and scan refreshed content before publishing or installing an updated skill.

Risk: Broad auto-consult behavior can surface powerful operational or security guidance in contexts where it may be inappropriate.

Mitigation: Disable or narrow auto-consult behavior so the skill is invoked only for authorized sysadmin, DevOps, and security tasks.

## Reference(s):

- [Sysadmin Toolbox on ClawHub](https://clawhub.ai/jdrhyne/skills/sysadmin-toolbox)
- [CLI Tools Reference](artifact/references/cli-tools.md)
- [Security Tools Reference](artifact/references/security-tools.md)
- [Shell One-liners Reference](artifact/references/shell-oneliners.md)
- [Shell Tricks Reference](artifact/references/shell-tricks.md)
- [Web Tools Reference](artifact/references/web-tools.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline shell commands and tool recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should be reviewed before execution, especially when they alter system configuration, capture traffic, remove data, or perform security testing.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
