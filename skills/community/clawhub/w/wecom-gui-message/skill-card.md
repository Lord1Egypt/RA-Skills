## Description:

Automates sending messages to WeCom contacts or group chats on macOS through desktop GUI control, window screenshots, OCR, and click/paste actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacky-wzj](https://clawhub.ai/user/jacky-wzj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and automation users can use this skill to send WeCom desktop messages to contacts or groups for workflows such as daily reports and notifications. It is intended for macOS environments where the user has authorized desktop automation and screen capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send live WeCom messages through desktop automation.

Mitigation: Require explicit confirmation of the recipient and message content before sending.

Risk: Desktop control and screen-capture permissions can expose sensitive chats or work data.

Mitigation: Grant permissions only in a controlled macOS environment, prefer window-scoped capture, and clean up temporary screenshots.

Risk: The security evidence flags unsafe shell command construction.

Mitigation: Review or fix command construction before installation, especially when handling untrusted contact names or message text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacky-wzj/skills/wecom-gui-message)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, json]

**Output Format:** [Markdown guidance with command examples and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, the WeCom desktop client, peekaboo, cliclick, swift, and Screen Recording plus Accessibility permissions.]

## Skill Version(s):

3.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
