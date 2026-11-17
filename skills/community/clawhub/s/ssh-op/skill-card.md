## Description:

SSH OP helps agents configure and use ssh-op to load a 1Password-managed SSH key into an in-memory ssh-agent before running ssh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moodykong](https://clawhub.ai/user/moodykong)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect to SSH hosts with a 1Password-managed private key, troubleshoot ssh-op setup, and onboard machines by creating local configuration and optional SSH host aliases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles SSH and 1Password access, which can expose sensitive authentication workflows if configured for an untrusted host or publisher.

Mitigation: Review the package contents and publisher profile before installation, configure only trusted 1Password vault and item names, and run connection tests against known host aliases.

Risk: The onboarding flow and SSH config helper can create persistent local configuration, including config.env and a managed block in ~/.ssh/config.

Mitigation: Inspect config.env and hosts.conf before applying changes, keep backups of existing SSH configuration, and remove the managed block if the skill is no longer used.

Risk: Server security evidence reports that the intended main ssh-op executable is missing from the shipped package.

Mitigation: Verify that scripts/ssh-op exists and matches the expected behavior before relying on this skill for SSH connections.

## Reference(s):

- [SSH OP ClawHub Page](https://clawhub.ai/moodykong/skills/ssh-op)
- [ssh-op onboarding runbook](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local config.env values, symlink commands, smoke tests, and SSH host alias configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
