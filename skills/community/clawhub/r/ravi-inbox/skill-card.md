## Description:

Read incoming Ravi SMS and email messages, including OTPs, verification codes, verification links, and incoming mail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunaksingwi](https://clawhub.ai/user/raunaksingwi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to read incoming Ravi SMS or email messages after triggering verification, 2FA, confirmation, or other expected inbox workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive inbox contents, including authentication codes and verification links.

Mitigation: Treat outputs as sensitive and avoid sharing logs or transcripts that contain codes, links, or message content.

Risk: Broad inbox access may retrieve messages beyond the expected verification or thread.

Mitigation: Direct the agent to access only the specific expected message, conversation, or email thread.

## Reference(s):

- [Ravi Inbox API schema](https://ravi.id/docs/schema/inbox.json)
- [Ravi Messages API schema](https://ravi.id/docs/schema/messages.json)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive OTPs, verification codes, verification links, and message content; treat outputs as sensitive.]

## Skill Version(s):

2.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
