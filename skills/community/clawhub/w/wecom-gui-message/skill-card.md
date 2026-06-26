## Description: <br>
Automates sending messages to WeCom contacts or groups on macOS using GUI automation, screenshot capture, OCR, and click/paste tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacky-wzj](https://clawhub.ai/user/jacky-wzj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users can use this skill to send trusted WeCom notifications, daily reports, or other business messages through the macOS desktop client. It is intended for environments where the user controls the recipient and message text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real business messages to WeCom contacts or groups. <br>
Mitigation: Use only with explicit trusted recipients and reviewed message text, and test first in a harmless chat. <br>
Risk: Security evidence reports an unsafe command execution path. <br>
Mitigation: Do not pass untrusted or generated content until shell command construction is fixed. <br>
Risk: The automation stores screenshots under /tmp/wecom-gui during OCR and login checks. <br>
Mitigation: Clear /tmp/wecom-gui after use or add automatic screenshot cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jacky-wzj/wecom-gui-message) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Message sending script](artifact/scripts/send_message.py) <br>
- [OCR helper script](artifact/scripts/ocr_screen.swift) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown instructions with bash examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, the WeCom desktop client, Screen Recording and Accessibility permissions, and local GUI automation tools.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
