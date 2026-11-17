## Description:

Find Gmail messages with a specific label and forward them to another address.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or workspace operators use this recipe to locate Gmail messages under a chosen label and forward their full contents to a destination address for review or follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe forwards full Gmail message bodies to another address, which can expose sensitive personal, legal, financial, customer, or internal data.

Mitigation: Confirm the label query, destination address, matched message count, and exact message content before forwarding; use narrow labels and only forward where policy permits it.

Risk: The documented flow does not include a built-in preview or confirmation step before sending forwarded content.

Mitigation: Add a manual review checkpoint after retrieving each message and before running the send command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/skills/recipe-forward-labeled-emails)
- [Publisher Profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-gmail skill.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
