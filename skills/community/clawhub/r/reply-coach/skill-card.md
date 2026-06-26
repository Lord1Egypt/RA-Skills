## Description: <br>
从剪贴板读取聊天内容，生成尊重边界、自然不油腻的高情商回复建议，适用于微信、QQ等聊天场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using OpenClaw can use this skill to read copied chat text from the macOS clipboard and receive respectful, natural reply suggestions. It is aimed at social chat scenarios such as WeChat, QQ, daily conversation, icebreakers, and maintaining a conversation without sending messages automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the current macOS clipboard when invoked, which may include passwords, private notes, or unrelated copied content. <br>
Mitigation: Before using it, confirm the clipboard contains only the chat text intended for analysis. <br>
Risk: Reply suggestions could be inappropriate for the relationship context or recipient boundaries. <br>
Mitigation: Review and edit the generated suggestions before sending any message manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/reply-coach) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with copied chat text delimited for agent analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and macOS pbpaste; does not automatically send messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
