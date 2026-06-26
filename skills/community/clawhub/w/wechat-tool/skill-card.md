## Description: <br>
The skill helps an agent query WeChat friends, recent contacts, chatrooms, and chatroom members, then send confirmed text, image, or file messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aw11100](https://clawhub.ai/user/aw11100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to find WeChat recipients, resolve ambiguous contact or group matches, and send confirmed text, image, or file messages to selected friends or group chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a powerful WeChat account token, contact data, message text, and shared file links through a plain HTTP service endpoint. <br>
Mitigation: Use it only if you trust synodeai.com with that data, prefer a provider-supported HTTPS path for real use, and use a revocable token where available. <br>
Risk: Messages or media could be sent to the wrong friend or group if recipient lookup returns multiple or unexpected matches. <br>
Mitigation: Follow the documented lookup, selection, and second-confirmation flow, and verify the recipient and message content before confirming final delivery. <br>
Risk: Image and file sends may expose externally hosted content links to the service and selected WeChat recipients. <br>
Mitigation: Share only links and files appropriate for those recipients and the service provider, and avoid private or regulated content unless the service has been approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aw11100/wechat-tool) <br>
- [Publisher profile](https://clawhub.ai/user/aw11100) <br>
- [WeChat tool service endpoint](http://www.synodeai.com/ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with WeChat API request and response content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WECHAT_APPID and WECHAT_TOKEN; sending actions require target lookup, user selection when needed, and explicit confirmation before final delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
