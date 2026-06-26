## Description: <br>
Automates sending text messages and image or file attachments through the macOS WeChat desktop app by controlling the visible logged-in GUI with AppleScript and JXA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeholdon](https://clawhub.ai/user/yeholdon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send explicit WeChat text notifications or attachable local files to individual contacts from a logged-in macOS WeChat desktop session. It is not intended for reading messages, managing group chats, or acting as an OpenClaw chat channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send WeChat messages or local files from the user's logged-in account without a final confirmation step. <br>
Mitigation: Use it only for explicit send requests, review the contact, content, and file path before execution, and prefer adding or requiring manual confirmation before the final send action. <br>
Risk: Ambiguous or incorrect contact names can cause WeChat search to select the wrong recipient. <br>
Mitigation: Use exact, specific contact names and confirm the visible chat target before sending. <br>
Risk: Untrusted message text or unusual file paths may be unsafe to pass into UI automation. <br>
Mitigation: Avoid untrusted inputs, keep the WeChat window visible, and use normal local file paths for attachments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yeholdon/wechat-message-sender) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, text] <br>
**Output Format:** [Markdown with inline bash commands and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, WeChat for Mac, a visible logged-in WeChat window, and macOS Accessibility permission for node.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
