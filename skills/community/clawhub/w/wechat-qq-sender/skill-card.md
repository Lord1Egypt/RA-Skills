## Description:

Windows 平台微信和 QQ 自动发消息工具，支持搜索联系人、发送消息、截图 OCR 分析和需用户确认的智能回复建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallccwc](https://clawhub.ai/user/smallccwc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate WeChat and QQ desktop messaging on Windows, including contact search, message sending, local chat screenshots, OCR-assisted review, and suggested replies with user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUI automation may send a message to the wrong active chat or contact because recipient verification is fragile.

Mitigation: Use only in a trusted Windows desktop session, test with non-sensitive contacts first, and require an explicit recipient and message confirmation before sending.

Risk: Screenshots and OCR can expose sensitive chat content.

Mitigation: Avoid sensitive conversations, keep screenshots local, delete saved screenshots after use, and do not upload captures to external AI or OCR services.

Risk: Clipboard and keyboard/mouse automation can interfere with concurrent desktop activity.

Mitigation: Do not use the keyboard, mouse, or clipboard during execution, and review results before relying on the workflow for important messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallccwc/skills/wechat-qq-sender)
- [Tesseract OCR Windows installer documentation](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may guide Windows GUI automation, local screenshot capture, OCR setup, and user-confirmed message sending workflows.]

## Skill Version(s):

1.1.3 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
