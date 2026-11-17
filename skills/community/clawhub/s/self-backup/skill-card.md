## Description:

Backs up OpenClaw workspace files such as AGENTS.md, SOUL.md, scripts, memory logs, skill metadata, and sanitized configuration to a user-configured GitHub repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayueanyou](https://clawhub.ai/user/mayueanyou)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to configure and run backups of workspace configuration, scripts, memory files, and skill metadata to a private GitHub repository they control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace files, memory logs, scripts, skill metadata, and incompletely sanitized configuration may be uploaded to GitHub.

Mitigation: Use a private repository you control and review backup contents before the first real push.

Risk: The sanitizer may not remove every possible secret from OpenClaw configuration or copied files.

Mitigation: Do not rely on sanitization alone; inspect the backup and remove credentials before publishing it.

Risk: Using --force can overwrite remote repository history.

Mitigation: Avoid --force unless intentionally replacing remote history after confirming no important changes will be lost.

## Reference(s):

- [self-backup on ClawHub](https://clawhub.ai/mayueanyou/skills/self-backup)
- [GitHub CLI](https://cli.github.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create backup files and push them to a user-configured GitHub repository when the included scripts are run.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
