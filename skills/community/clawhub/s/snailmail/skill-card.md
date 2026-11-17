## Description:

Snail Mail gives agents a slow-channel inbox for storing non-urgent, notable, or decision-requiring operator messages and rendering them when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dvdegenz](https://clawhub.ai/user/dvdegenz)

### License/Terms of Use:


## Use Case:

Agents and operators use this skill to record notable but non-urgent events, decisions, abnormal conditions, and FYIs in a local inbox so the operator can review, mark read, or archive messages later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored inbox messages may contain sensitive operational details.

Mitigation: Keep the workspace private and avoid storing secrets or credentials in inbox messages.

Risk: Rendered messages sent to Slack or Discord may include unescaped formatting or mentions.

Mitigation: Review or sanitize message content before rendering untrusted inbox entries into shared channels.

## Reference(s):

- [Snail Mail ClawHub release](https://clawhub.ai/dvdegenz/skills/snailmail)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, HTML, plain text, and JSON from CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores inbox messages locally in workspace inbox/messages.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
