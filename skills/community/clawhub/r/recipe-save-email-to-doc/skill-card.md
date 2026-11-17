## Description:

Save a Gmail message body into a Google Doc for archival or reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workspace users use this skill to save selected Gmail message content into a Google Doc for archival or later reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy sensitive email content into a persistent Google Doc.

Mitigation: Confirm the selected Gmail message, redact sensitive content where possible, and check the destination document sharing settings before saving.

Risk: The recipe shows a shell command pattern where email text could be interpolated directly into a command.

Mitigation: Avoid executing commands that directly interpolate untrusted email text; review and safely quote or sanitize content before passing it to shell commands.

## Reference(s):

- [Recipe Save Email To Doc on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/recipe-save-email-to-doc)

## Skill Output:

**Output Type(s):** [shell commands, guidance, text]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gws plus the gws-gmail and gws-docs skills; copies selected email body text into a Google Doc.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
