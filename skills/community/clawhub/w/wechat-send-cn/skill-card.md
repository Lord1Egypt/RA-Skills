## Description: <br>
Wechat Send helps an agent send text messages to a contact or group through the macOS WeChat desktop client, using automatic GUI control with OCR verification and an agent-assisted fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuntong007](https://clawhub.ai/user/chuntong007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, or developers who use WeChat on macOS can invoke this skill when they need an agent to send a specific text message to a named contact or group. It is limited to sending text messages and does not read messages or send files/images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real WeChat messages through a logged-in desktop session automatically. <br>
Mitigation: Require explicit confirmation of the exact recipient and message before running the send command. <br>
Risk: GUI and OCR matching can be fragile, especially when the workflow falls back to screenshot-coordinate selection. <br>
Mitigation: Verify the selected conversation from the title OCR or fallback screenshot before using --send-only, and stop if the match is ambiguous. <br>
Risk: The workflow writes message text and screenshots to temporary files under /tmp. <br>
Mitigation: Avoid sensitive content and delete /tmp/wechat_send_clip.txt and /tmp/wechat_*.png after sending. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chuntong007/wechat-send-cn) <br>
- [Publisher profile](https://clawhub.ai/user/chuntong007) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown instructions with bash command examples and screenshot-coordinate guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, a logged-in WeChat desktop client, Accessibility permission, cliclick, and macOS Vision/Swift OCR; sends text messages only.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
