## Description:

Pushbullet API integration with managed OAuth for cross-device notification automation. Send pushes, manage devices, create chats, and handle cross-device messaging. Use this skill when users want to send notifications to devices, share links or notes across devices, manage Pushbullet chats, or register and manage connected devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to connect a Pushbullet account through ClawLink, send cross-device notifications, share links or files, inspect push history, and manage devices or chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external ClawLink plugin and OAuth service that can access Pushbullet account data after authorization.

Mitigation: Install it only when the ClawLink service and plugin source are trusted, prefer a pinned or verified plugin release when available, and review OAuth scopes before authorizing.

Risk: Write and destructive Pushbullet operations can send pushes or delete pushes, chats, and devices.

Mitigation: Review confirmation prompts carefully before approving write or delete actions, especially operations that delete all pushes or remove chats or devices.

## Reference(s):

- [Pushbullet API Docs](https://docs.pushbullet.com)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=pushbullet)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted ClawLink plugin connection and user confirmation for write or destructive actions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
