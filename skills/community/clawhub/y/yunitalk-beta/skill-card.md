## Description:

Connects OpenClaw to Talk Robots for conversations and delivery of text or file messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackbeans](https://clawhub.ai/user/blackbeans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to connect an OpenClaw gateway to Talk Robots and send text or files to a robot conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested unpinned npm initializer reads local OpenClaw credentials.

Mitigation: Install only from a trusted publisher and npm source; pin and review the initializer version before running it.

Risk: The generated initialization string and QR code contain an OpenClaw token, even though it is Base64-encoded.

Mitigation: Keep the string and QR code private and enter them only in the intended robot configuration page.

Risk: Message sending prints signed request details and can target a configurable endpoint.

Mitigation: Use only a trusted Talk Robots endpoint and avoid recording shell output in shared logs.

## Reference(s):

- [yunitalk-beta ClawHub release](https://clawhub.ai/blackbeans/skills/yunitalk-beta)
- [Talk Robots integration guide](artifact/README.md)
- [Robot send API guide](artifact/ROBOT_SEND_API.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send signed text or file events to a configured Talk Robots conversation.]

## Skill Version(s):

0.9.5 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
