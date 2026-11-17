## Description:

Apply Gmail labels to matching messages and archive them to keep your inbox clean.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Users who manage Gmail inboxes use this recipe to find matching messages, apply an existing Gmail label, and archive those messages after checking the selected results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages can be labeled or archived incorrectly if the Gmail query, message ID, or label ID is wrong.

Mitigation: Review search results, message IDs, and label IDs before running modify commands; archiving removes messages from the inbox but does not delete them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-label-and-archive-emails)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gws and gws-gmail; the commands modify Gmail messages by adding labels and removing the INBOX label.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
