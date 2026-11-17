## Description:

Configure Linux swap -- create a swap file, set swappiness, persist via fstab, and resize swap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjxylc](https://clawhub.ai/user/zjxylc)

### License/Terms of Use:

MIT

## Use Case:

Developers and system administrators use this skill to inspect, create, resize, and tune Linux swap configuration. It is intended for Linux hosts where an agent may propose shell commands for swap files, fstab persistence, and swappiness settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to run sudo commands that change swap state and persistent system configuration.

Mitigation: Require explicit user confirmation before executing privileged commands and verify current swap, fstab, and swappiness state before changing them.

Risk: Appending directly to /etc/fstab or /etc/sysctl.conf can create duplicate or incorrect persistent configuration.

Mitigation: Check for existing entries, back up configuration files, validate edits, and keep rollback commands available before persistence changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Linux-only guidance that may include sudo commands for swap, /etc/fstab, and /etc/sysctl.conf changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
