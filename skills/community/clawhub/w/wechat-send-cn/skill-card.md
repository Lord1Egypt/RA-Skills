## Description:

Send a message to a contact or group via the macOS WeChat desktop client, using an automated locate-and-verify flow with Agent-assisted fallback when verification fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuntong007](https://clawhub.ai/user/chuntong007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send WeChat messages to contacts or groups from a logged-in macOS WeChat desktop client. It is intended for sending messages only, not reading messages or sending files and images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send real WeChat messages after weak recipient verification.

Mitigation: Use it only after intentionally granting Accessibility control, and add or require an explicit final confirmation of recipient and content before sending.

Risk: Private message text and screenshots may remain in predictable temporary files.

Mitigation: Avoid sensitive messages until secure temporary files and cleanup are added; review and remove temporary files after use.

Risk: The skill automates the live WeChat desktop client through macOS Accessibility control.

Mitigation: Install and run it only in environments where that level of local UI control is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chuntong007/skills/wechat-send-cn)
- [Publisher profile](https://clawhub.ai/user/chuntong007)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and operational status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce instructions to inspect a screenshot and rerun the script with screen coordinates when automated verification falls back.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
