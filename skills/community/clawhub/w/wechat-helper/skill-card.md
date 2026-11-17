## Description:

Automates WeChat File Helper browser workflows to send text messages and handle login QR code delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidu](https://clawhub.ai/user/qidu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate WeChat File Helper message sending through a browser, including QR-based login handling for a dedicated File Helper account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send messages and screenshots without tight recipient validation or per-action confirmation.

Mitigation: Use only a dedicated WeChat File Helper account and a private, verified QR delivery recipient; require confirmation before sending messages or screenshots.

Risk: Full browser screenshots may expose login QR material or surrounding page content.

Mitigation: Capture only the QR element, delete temporary QR files after use, and avoid storing or forwarding broader browser screenshots.

Risk: The cron wrapper can repeatedly trigger automated checks and sends.

Mitigation: Avoid enabling cron until scripts target a specific WeChat tab, validate recipients, and require confirmation for send actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qidu/skills/wechat-helper)
- [WeChat File Helper](https://filehelper.weixin.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser automation steps, cron setup guidance, QR capture commands, and message-send commands.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
