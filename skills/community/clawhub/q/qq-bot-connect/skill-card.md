## Description: <br>
QQBot 消息主动推送技能。当需要向 QQ 用户或群发送消息时使用此技能。支持：(1) 主动发送消息到 QQ 对话框 (2) 发送图片/语音/文件等富媒体 (3) 群发消息。触发词：发送 QQ、推送 QQ、QQ 消息、发送到 QQ、QQ 发送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcduann](https://clawhub.ai/user/jcduann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent send QQ private or group messages, including text and media/file attachments, through the qqbot message channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill allows an agent to send real QQ messages and files when invoked. <br>
Mitigation: Configure the openid carefully, test with your own account first, and require explicit confirmation before sending messages. <br>
Risk: Group messages, bulk messages, or media/file attachments can reach unintended recipients or expose unintended content. <br>
Mitigation: Require explicit user confirmation for group messages, bulk sends, and any media or file attachment before using the qqbot message channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcduann/qq-bot-connect) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jcduann) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, Guidance] <br>
**Output Format:** [JSON message-tool payloads and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include qqbot target strings and qqmedia attachment references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
