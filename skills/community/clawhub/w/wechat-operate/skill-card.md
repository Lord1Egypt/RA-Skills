## Description: <br>
通过微信查询好友、最近联系人、群聊和群成员，并在确认目标后发送文本、图片或文件消息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aw11100](https://clawhub.ai/user/aw11100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who manage WeChat conversations can use this skill to find friends, recent contacts, group chats, or group members, then send a text, image, or file message after recipient confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real WeChat messages through a cleartext local-network gateway. <br>
Mitigation: Install only if you control and trust the gateway, know which WeChat account it controls, and keep the gateway protected on your network. <br>
Risk: Messages, image URLs, file URLs, or file names could be sent to the wrong recipient if the target is not reviewed carefully. <br>
Mitigation: Review every recipient, message, image, file URL, and file name before approving a send. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [HTTP requests with concise text confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted WeChat gateway and a configured WECHAT_APPID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
