## Description:

Update Plus provides full backup, update, and restore for OpenClaw config, workspace, and skills with auto-rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hopyky](https://clawhub.ai/user/hopyky)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and administrators use this skill to back up configured directories, check and apply updates, restore selected backup contents, and optionally schedule recurring updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically update OpenClaw and installed skills.

Mitigation: Use it only with trusted configured repositories and review update plans before enabling automatic updates.

Risk: Restore operations can overwrite configured directories.

Mitigation: Verify the backup contents and keep a separate known-good backup before running restore or update --force.

Risk: Backups may contain sensitive configuration or workspace data.

Mitigation: Keep remote storage and notifications disabled unless needed, and enable encryption before cloud sync.

Risk: Cron auto-updates can apply changes without interactive review.

Mitigation: Avoid scheduled updates unless the environment and all configured update sources are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hopyky/skills/update-plus)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may also guide file backup, restore, update, notification, and cron configuration workflows.]

## Skill Version(s):

4.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
