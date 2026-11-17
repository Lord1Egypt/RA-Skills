## Description:

在 OpenClaw 中提供 WeChat 回调接入、群私聊会话路由、消息发送与图片识别入口能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wechat-ipad-api](https://clawhub.ai/user/wechat-ipad-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect WeChat private chats and group chats to OpenClaw agents through a runnable gateway with callback handling, session routing, message sending, and image-recognition handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public WeChat callbacks can reach OpenClaw command and chat execution paths with weak authentication.

Mitigation: Deploy only in a controlled environment until webhook verification, HTTPS, and narrowly scoped OpenClaw credentials are added.

Risk: Private-chat enrollment uses a fixed phrase to add users to the whitelist.

Mitigation: Replace fixed-phrase enrollment with an administrator-managed allowlist or a stronger approval flow before production use.

Risk: Slash commands may expose high-impact OpenClaw actions through chat messages.

Mitigation: Disable slash command forwarding by default or restrict it to an explicit allowlist of low-risk commands.

Risk: Retained image files can be served through the configured public URL.

Mitigation: Avoid publicly serving retained user images; add retention limits, access controls, and log redaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wechat-ipad-api/skills/wechat-gateway)
- [wechatapi.net](https://wechatapi.net)
- [WeChat API default endpoint](http://api.wechatapi.net/finder/v2/api)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code, shell commands, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a runnable single-file gateway and setup guidance requiring WX_API_TOKEN and PUBLIC_URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
