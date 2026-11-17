## Description:

Provides automation scripts for routine tasks such as bulk file renaming, backups, scheduled execution, screenshots, and data scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to produce routine automation commands for file renaming, backups, scheduled tasks, screenshots, and data collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation commands can change files through rename and backup workflows.

Mitigation: Use explicit source and destination paths, review proposed commands before execution, and keep backups for reversible changes.

Risk: Scheduled tasks can create recurring execution that persists beyond a single session.

Mitigation: Confirm how scheduled jobs are created, listed, and removed before enabling schedules; avoid elevated privileges.

Risk: Screenshot and scraping workflows may access external websites.

Mitigation: Use only URLs you are authorized to access and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/skills/xiaoming-automation-scripts)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
