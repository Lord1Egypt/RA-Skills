## Description:

QQ-Bot-connect helps an agent send QQ Bot messages to configured private or group recipients, including text and media files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcduann](https://clawhub.ai/user/jcduann)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent send text or media to QQ private chats or groups through a configured QQ Bot recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user content and files to external QQ recipients.

Mitigation: Require the agent to show the resolved recipient and message content before every send.

Risk: A configured or user-supplied recipient ID can route messages to the wrong QQ private chat or group.

Mitigation: Replace placeholder configuration with validated recipient IDs and confirm the target before sending.

## Reference(s):

- [QQ-Bot-connect ClawHub release](https://clawhub.ai/jcduann/skills/qq-bot-connect)
- [jcduann ClawHub publisher profile](https://clawhub.ai/user/jcduann)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown with JSON-style message payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recipient targeting guidance for QQ private chats and groups; supports media paths wrapped in qqmedia tags.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
