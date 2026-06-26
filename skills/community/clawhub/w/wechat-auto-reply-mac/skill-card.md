## Description: <br>
Automates WeChat message sending and semi-automatic reply suggestions on macOS by searching contacts, using OCR for chat context, and pasting or sending messages through the desktop client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenjunlei1989-glitch](https://clawhub.ai/user/chenjunlei1989-glitch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send messages or prepare OCR-based reply suggestions in a logged-in macOS WeChat desktop environment. It is intended for local chat automation where the user can grant accessibility permissions, verify the target contact, and test behavior before relying on automated sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send messages from a logged-in WeChat account after receiving local UI-control permissions. <br>
Mitigation: Grant accessibility permissions only after reviewing the installed scripts, confirm the target contact before use, and test with a safe recipient such as 文件传输助手 before normal operation. <br>
Risk: OCR and UI automation can misread the chat state or select the wrong search result, especially across WeChat versions, window layouts, or group-chat search results. <br>
Mitigation: Run initial single-chat and group-chat tests, keep automatic sending disabled or manually confirmed until behavior is verified, and recalibrate click paths if the interface layout differs. <br>
Risk: The reviewed artifact references a Homebrew-installed AppleScript runtime file that is not included in the artifact evidence. <br>
Mitigation: Inspect the installed AppleScript from the Homebrew package before executing the wrapper and avoid relying on the skill if the runtime file cannot be verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenjunlei1989-glitch/wechat-auto-reply-mac) <br>
- [Publisher profile](https://clawhub.ai/user/chenjunlei1989-glitch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, WeChat Desktop, local accessibility permissions, and local OCR dependencies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
