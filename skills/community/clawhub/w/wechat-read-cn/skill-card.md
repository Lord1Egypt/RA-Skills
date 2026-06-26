## Description: <br>
Reads chat history from a WeChat contact or group on the macOS desktop client using screenshots and agent OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuntong007](https://clawhub.ai/user/chuntong007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to retrieve and summarize authorized WeChat contact or group conversation history from a logged-in macOS WeChat desktop session. It is intended for reading selected conversations, not sending messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture private WeChat conversations through screenshots and OCR. <br>
Mitigation: Use only on conversations the operator is authorized to access, verify the selected contact or group before capture, and keep requested page counts low. <br>
Risk: Captured screenshots and clipboard staging files may remain in local /tmp paths after use. <br>
Mitigation: Delete /tmp/wechat_read_* files and /tmp/wechat_read_clip.txt after each run. <br>
Risk: The skill requires macOS Accessibility and Screen Recording permissions and can overwrite clipboard contents during execution. <br>
Mitigation: Grant permissions only in trusted environments and assume clipboard contents may change while the skill runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chuntong007/wechat-read-cn) <br>
- [Publisher profile](https://clawhub.ai/user/chuntong007) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown conversation summaries and shell command guidance based on screenshot OCR] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local screenshots and clipboard staging files under /tmp/wechat_read_* and /tmp/wechat_read_clip.txt during execution.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
