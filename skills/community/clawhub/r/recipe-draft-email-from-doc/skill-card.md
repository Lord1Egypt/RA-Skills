## Description:

Read content from a Google Doc and use it as the body of a Gmail message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and other Google Workspace users use this recipe to turn content from a selected Google Doc into the body of a Gmail message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe can immediately send selected Google Doc contents through the user's Gmail account even though it is framed as drafting.

Mitigation: Manually verify the document, recipients, subject, and body before use; prefer changing the final step to create a draft or require explicit confirmation before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-draft-email-from-doc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-docs and gws-gmail skills.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
