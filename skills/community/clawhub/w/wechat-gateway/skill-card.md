## Description: <br>
在 OpenClaw 中提供 WeChat 回调接入、群私聊会话路由、消息发送与图片识别入口能力。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wechat-ipad-api](https://clawhub.ai/user/wechat-ipad-api) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect WeChat private chats and group chats to OpenClaw agents through a runnable gateway with callback handling, session routing, message replies, and image-recognition entry points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote chat users may gain too much control over the connected OpenClaw agent through the gateway defaults. <br>
Mitigation: Restrict slash commands to a small allowlist, run OpenClaw with least-privilege tools, and deploy only in a controlled environment until hardened. <br>
Risk: Chat data, saved images, logs, and tokens may be exposed without stronger transport and storage safeguards. <br>
Mitigation: Use HTTPS for the API endpoint and PUBLIC_URL, protect config.ini and logs, and add authentication, expiry, and deletion controls for saved images. <br>
Risk: Phrase-based private-chat self-whitelisting can allow unintended users to enroll themselves. <br>
Mitigation: Remove phrase-based self-whitelisting and manage private-chat access through an explicit allowlist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wechat-ipad-api/wechat-gateway) <br>
- [wechatapi.net](https://wechatapi.net) <br>
- [WeChat API endpoint](http://api.wechatapi.net/finder/v2/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python code, shell commands, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for configuring and running a single-file WeChat-to-OpenClaw gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
