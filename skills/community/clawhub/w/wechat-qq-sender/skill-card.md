## Description: <br>
Windows 平台微信和 QQ 自动发消息工具。支持搜索联系人、发送消息、截图OCR分析、智能回复建议（需用户确认后发送）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallccwc](https://clawhub.ai/user/smallccwc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill on Windows to automate WeChat and QQ desktop messaging, capture chat screenshots, run local OCR, and draft reply suggestions that can be reviewed before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control live WeChat and QQ desktop apps, including keyboard, mouse, clipboard, and logged-in chat sessions. <br>
Mitigation: Install only in a trusted Windows environment, test with low-risk contacts first, and avoid using the machine while automation is running. <br>
Risk: Direct-send commands may send messages immediately or with uneven confirmation behavior. <br>
Mitigation: Review target contacts and message text before running send commands, and prefer confirmation-based reply flows for higher-risk conversations. <br>
Risk: Chat screenshots are saved locally and may contain private or sensitive conversation content. <br>
Mitigation: Review and delete saved screenshots after use, and do not upload chat screenshots to external AI services unless that privacy exposure is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallccwc/wechat-qq-sender) <br>
- [Tesseract OCR Windows installer wiki](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python script usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local desktop automation steps, screenshot/OCR outputs, and reply suggestions; sending behavior depends on the selected script and user confirmation flow.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
