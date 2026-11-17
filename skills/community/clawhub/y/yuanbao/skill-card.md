## Description:

Yuanbao groups: @mention users, query group information and members, and send direct messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maliot100x](https://clawhub.ai/user/maliot100x)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents in Yuanbao group chats use this skill to look up group context, identify members for exact @mentions, and send private messages or supported media files when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the agent authority to send visible group replies, notify users with @mentions, and send private messages or files through Yuanbao.

Mitigation: Require clear user intent and confirmation before sending private messages, mentions, or attachments, especially when recipients or content are ambiguous.

Risk: The server security assessment marked the release suspicious because messaging authority is under-disclosed while permission warnings are discouraged.

Mitigation: Deploy only with guardrails that preserve consent checks, constrain outbound messaging, and allow review of sent messages and attachments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maliot100x/skills/yuanbao)
- [Publisher Profile](https://clawhub.ai/user/maliot100x)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Natural-language chat replies with JSON-style tool call arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include @mentions, private-message content, or media attachment paths.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
