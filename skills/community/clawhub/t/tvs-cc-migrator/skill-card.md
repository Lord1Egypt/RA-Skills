## Description:

Tvs Cc Migrator helps back up and restore Claude Code configuration under ~/.claude, including instructions, rules, skills, commands, agents, plugins, and settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inksnowhailong](https://clawhub.ai/user/inksnowhailong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to migrate local Claude Code configuration between machines. It guides users through scanning, confirming sensitive items, creating backups, and restoring configurations from a manifest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain sensitive Claude Code configuration or credentials.

Mitigation: Use the sensitive-field redaction option, review every backup item before packaging, and keep generated backups private.

Risk: A tampered restore manifest could cause unwanted configuration overwrites or command execution.

Mitigation: Restore only from backups you created or trust, and approve reinstall commands or overwrite restores only after checking the exact paths and commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inksnowhailong/skills/tvs-cc-migrator)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files, JSON]

**Output Format:** [Markdown guidance with shell commands and generated backup artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scan reports, manifest-driven backup contents, and restore guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
