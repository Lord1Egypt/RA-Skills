## Description: <br>
Automates WeChat desktop messaging with PyAutoGUI, including contact search, configurable hotkeys, optional no-send preview, and a file-path mode that types the local path into chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anananangela](https://clawhub.ai/user/anananangela) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users can automate WeChat desktop message entry and sending by selecting a contact, composing text, and optionally requiring manual confirmation before the message is sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send WeChat messages immediately through desktop automation. <br>
Mitigation: Use --no-send for sensitive content and verify the selected contact before manually sending. <br>
Risk: The file mode types the local file path as chat text instead of attaching the file. <br>
Mitigation: Avoid --file unless sending the path as text is intended. <br>
Risk: Contacts, message text, and file paths may appear in terminal output. <br>
Mitigation: Avoid sensitive content in environments where terminal output is logged. <br>


## Reference(s): <br>
- [Wechat Sender ClawHub Page](https://clawhub.ai/anananangela/wechat-sender-pyautogui) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run desktop automation commands that interact with an active WeChat session.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
