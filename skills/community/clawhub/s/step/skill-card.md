## Description:

Log daily steps, set fitness goals, and chart walking trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to record walking activity, goals, reminders, streaks, milestones, and trend notes in a local terminal-first step log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores broad free-form health-related text locally with weak scoping.

Mitigation: Use it only for non-sensitive step or fitness notes on a private account and check permissions on ~/.local/share/step before use.

Risk: Exports may not work as documented because the export command is captured by a logging handler.

Mitigation: Verify export behavior and backups before relying on JSON, CSV, or TXT output.

## Reference(s):

- [Step on ClawHub](https://clawhub.ai/bytesagain-lab/skills/step)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text command guidance and terminal output, with optional JSON, CSV, or TXT export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries locally under ~/.local/share/step.]

## Skill Version(s):

2.0.2 (source: server release evidence; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
