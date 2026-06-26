## Description: <br>
Windows 电脑端微信消息发送 MCP，实现在微信上给指定联系人发送消息 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[529279917](https://clawhub.ai/user/529279917) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users on Windows use this skill to send WeChat messages through a logged-in desktop WeChat session when they explicitly request WeChat as the communication channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send messages through the active logged-in WeChat desktop session without enforced recipient confirmation. <br>
Mitigation: Confirm the active chat, recipient, and message content with the user before sending. <br>
Risk: The skill writes WeChat window screenshots such as verification, input, search, and result images to local files. <br>
Mitigation: Delete generated screenshot files after use, especially when chats may contain sensitive information. <br>
Risk: The skill copies message content through the system clipboard. <br>
Mitigation: Clear or overwrite the clipboard after sending sensitive messages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/529279917/wechat-skill) <br>
- [Referenced wechat-mcp skill](https://clawhub.ai/dragon015/wechat-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [MCP tool responses and concise setup or confirmation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows, Python, and an active logged-in WeChat desktop session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
