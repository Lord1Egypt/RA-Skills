## Description:

Controls a local Windows WeChat desktop session to send text or image messages to specified contacts or groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niansen3-svg](https://clawhub.ai/user/niansen3-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to send user-approved WeChat text or image updates from a logged-in Windows desktop client, either through the synchronous CLI or the local HTTP queue service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real WeChat messages from a logged-in desktop session.

Mitigation: Install only where that authority is acceptable and require explicit human confirmation of recipient and content before each send.

Risk: Weak, committed, or exposed tokens could allow unintended access to message-sending capability.

Mitigation: Rotate or remove committed tokens, use a strong per-install secret, and keep the HTTP API bound to loopback.

Risk: Bulk-send and queue behavior can amplify accidental, unwanted, or unsolicited messaging.

Mitigation: Avoid unsolicited messaging, limit recipient lists, and review queued content before dispatch.

Risk: Remote image URL fetching and WPush monitoring can trigger outbound network requests.

Mitigation: Disable or constrain remote image fetching and WPush monitoring unless they have been reviewed and are required.

Risk: Recipient names must match WeChat contact or group names exactly, which can cause failed or misdirected sends.

Mitigation: Confirm the target WeChat display name and use a safe test recipient before operational use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/niansen3-svg/skills/wechat-automation-api)
- [Skill invocation guide](artifact/SKILL.md)
- [Project README](artifact/README.md)
- [Usage documentation](artifact/使用说明.md)
- [Changelog](artifact/docs/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain-text command output with command-line and JSON API usage documented in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows, a logged-in WeChat desktop client, exact recipient names, and reviewed message content or image URLs.]

## Skill Version(s):

1.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
