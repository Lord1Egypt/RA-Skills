## Description:

Workspace Backup GitHub backs up AI agent workspace files to a private GitHub repository through manual setup or scheduled OpenClaw Cron backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziqi-jin](https://clawhub.ai/user/ziqi-jin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent users use this skill to configure, run, schedule, check, and restore backups of selected workspace files in a private GitHub repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A GitHub token may be exposed through chat, command history, or the Git remote URL.

Mitigation: Use a fine-grained token or credential helper, avoid pasting broad tokens into chat, and revoke or rotate any token that may have been exposed.

Risk: Backups may include sensitive agent memory, identity, user, tool, and skill files.

Mitigation: Use a private repository, review every staged file and ignore rules before pushing, and limit repository access.

Risk: Restoring directly from a backup repository can overwrite local workspace files.

Mitigation: Restore only from a verified commit into a staging directory first, then review and merge selected files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziqi-jin/skills/workspace-backup-github)
- [GitHub token settings](https://github.com/settings/tokens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Git/OpenClaw configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute Git and OpenClaw Cron commands that push selected workspace files to a private GitHub repository.]

## Skill Version(s):

1.3.0 (source: server release evidence, released 2026-03-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
