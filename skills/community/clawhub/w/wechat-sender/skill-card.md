## Description:

Automates WeChat message sending by guiding an agent through contact selection, message entry, sending, and screenshot-based confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noir-hedgehog](https://clawhub.ai/user/noir-hedgehog)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to have an agent operate WeChat locally, find a recipient, send a provided message, and verify that the message appears in the chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can send WeChat messages on the user's behalf.

Mitigation: Require manual confirmation of the exact recipient and message before executing the send command.

Risk: Screenshots of chat windows may expose sensitive conversations or personal data.

Mitigation: Capture only the needed WeChat region, avoid whole-screen capture, and do not retain screenshots longer than needed for confirmation.

Risk: The artifact describes bypassing app screen-capture restrictions.

Mitigation: Do not use workflows that bypass screen-capture protections; review local policy and app terms before enabling screenshot-based automation.

Risk: UI automation can select the wrong contact or send unintended content.

Mitigation: Use screenshot-based verification to confirm the selected contact and visible message content before sending.

## Reference(s):

- [Agent-Eye repository](https://github.com/noir-hedgehog/Agent-eye)
- [ClawHub skill page](https://clawhub.ai/noir-hedgehog/skills/wechat-sender)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with inline shell commands and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local UI automation steps, screenshot review, clipboard paste actions, and message-send confirmation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
