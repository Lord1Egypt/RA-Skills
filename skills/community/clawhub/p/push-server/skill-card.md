## Description:

Helps agents send task updates and structured data to user-selected notification or webhook channels, review sent messages, and manage personal channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teakong](https://clawhub.ai/user/teakong)

### License/Terms of Use:

MIT

## Use Case:

Developers and other agent users can send task results, alerts, and structured updates to their own notification or webhook channels, review message history, and set up or manage channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notifications and webhook messages can disclose task results to configured recipients.

Mitigation: Confirm the intended channel and recipients before sending; exclude secrets and private tokens from message bodies.

Risk: A leaked channel code can permit unwanted use of a notification channel.

Mitigation: Treat the channel code as a credential and keep it out of public instructions and messages.

Risk: Deleting, disabling, or resetting a channel can interrupt delivery or invalidate its code.

Mitigation: Obtain explicit confirmation before channel delete, disable, or reset operations.

## Reference(s):

- [push-server on ClawHub](https://clawhub.ai/teakong/skills/push-server)
- [Push service documentation](https://push.phprm.com/mcp.html)
- [API reference](artifact/references/api.md)
- [Message examples](artifact/references/example.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Plain text, Markdown, or JSON notification content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional notification title and destination link; messages can be sent individually or in batches.]

## Skill Version(s):

1.6.3 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
