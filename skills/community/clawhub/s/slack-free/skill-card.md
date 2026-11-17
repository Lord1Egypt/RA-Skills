## Description:

Slack helps agents manage Slack messages, reactions, pins, custom emoji, and member information from SkillHub-style instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to carry out Slack workspace actions such as sending or editing messages, adding reactions, managing pins, listing emoji, and retrieving member information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises Slack write and management actions while declaring only read access.

Mitigation: Review the skill before installing if a read-only Slack helper is expected, and deploy it only where Slack write actions are intended.

Risk: Slack actions could send, edit, delete, pin, unpin, or react to messages in a workspace.

Mitigation: Require explicit user confirmation before performing message, pin, unpin, or reaction actions.

Risk: Member information retrieved from Slack may be workplace-sensitive data.

Mitigation: Limit member information requests to the minimum needed and avoid exposing retrieved data outside the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/slack-free)

## Skill Output:

**Output Type(s):** [Guidance, Text, API Calls]

**Output Format:** [Markdown guidance with JSON action examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
