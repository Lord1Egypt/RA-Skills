## Description: <br>
WX-Send helps an agent send WeChat messages to a specified contact on macOS, with an optional OCR workflow for reading the current chat window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[libero1980](https://clawhub.ai/user/libero1980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate the local macOS WeChat client through UI automation for reviewed message sending, and to inspect a chat window with OCR when preparing a reply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send WeChat messages through local UI automation without strong scoping controls. <br>
Mitigation: Use it only for explicit, reviewed messages and confirm the recipient and content before execution. <br>
Risk: The OCR workflow can capture the full screen and may include unrelated visible content. <br>
Mitigation: Avoid auto-reply workflows unless confirmation and recipient checks are added, and close unrelated sensitive windows before using OCR. <br>
Risk: UI automation can act on the wrong window or contact if WeChat focus, search results, or account state differs from expectations. <br>
Mitigation: Keep WeChat unlocked and visible, verify the selected chat before sending, and do not run the workflow unattended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/libero1980/wx-send) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/scripts/wx_send.py](artifact/scripts/wx_send.py) <br>
- [artifact/scripts/wx_ocr_reply.py](artifact/scripts/wx_ocr_reply.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger local WeChat UI automation when the referenced scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
