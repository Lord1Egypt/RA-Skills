## Description:

Reads chat content from the clipboard and helps draft respectful, natural reply suggestions for WeChat, QQ, and similar conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to analyze copied social chat messages and prepare three bounded reply options, including safer phrasing and guidance on when to reduce frequency or end the exchange.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the current clipboard, which may contain sensitive content unrelated to the intended chat.

Mitigation: Copy only the chat text intended for analysis, avoid copying passwords or confidential material first, and invoke the skill explicitly for reply suggestions.

Risk: Reply suggestions for personal conversations can become inappropriate if used to pressure, manipulate, or harass someone.

Mitigation: Use the skill's bounded guidance for respectful replies and avoid automatic sending or coercive messaging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/reply-coach)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command output for clipboard text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill reads the current macOS clipboard with pbpaste and does not automatically send messages.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
