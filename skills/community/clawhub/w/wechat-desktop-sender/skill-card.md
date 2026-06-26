## Description: <br>
Windows WeChat desktop automation for opening chats and sending messages, including single sends, serial batch sends, personalized campaigns, and template-based recipient lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinhuadeng](https://clawhub.ai/user/jinhuadeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and agent users use this skill to route conversational requests into Windows WeChat Desktop message-sending workflows. It supports testing with WeChat File Transfer Assistant, sending one message to one chat, serial batch sending, personalized recipient lists, and template-variable campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real WeChat messages, including serial batch and personalized campaign messages, through a logged-in desktop session. <br>
Mitigation: Only run it after reviewing the exact recipients and message text, test with WeChat File Transfer Assistant first, and avoid unsolicited or large campaigns. <br>
Risk: Logs and run artifacts may contain contact names, message bodies, screenshots, and WeChat UI text. <br>
Mitigation: Treat wechat_automation_logs/ and any custom log directory as sensitive, restrict access to those files, and remove or archive them according to local data-handling policy. <br>
Risk: Desktop UI automation and optional OCR verification provide practical confirmation but not a guaranteed delivery proof. <br>
Mitigation: Review success, verification, retry recommendations, and failure details before relying on a send or retrying failed recipients. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jinhuadeng/wechat-desktop-sender) <br>
- [Single Send](artifact/references/single-send.md) <br>
- [Batch Send](artifact/references/batch-send.md) <br>
- [Personalized Send](artifact/references/personalized-send.md) <br>
- [Template Variable Send](artifact/references/template-send.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands plus log and JSON summary file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs may create logs, screenshots, control-tree dumps, and batch summary JSON files under wechat_automation_logs/ or a configured log directory.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
