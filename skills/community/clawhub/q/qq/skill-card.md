## Description: <br>
Qq helps developers work with QQ bots, channel development, mini-programs, and Open Platform APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to plan and implement QQ bot, QQ channel, mini-program, and OAuth integrations with example authentication, messaging, WebSocket event handling, and channel-management patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AppSecret values, access tokens, or OAuth credentials may be exposed if copied into prompts, logs, frontend code, or shared examples. <br>
Mitigation: Keep secrets on the server, avoid logging raw credentials, and redact tokens before sharing code or diagnostic output. <br>
Risk: Messaging, moderation, or OAuth examples can affect real QQ users, groups, channels, or user data if tested directly in production. <br>
Mitigation: Test posting and moderation flows in a sandbox, request only needed intents and scopes, and review rate limits before enabling production workflows. <br>
Risk: Private, group, or OAuth user data may be retained by application logs or downstream code created from the examples. <br>
Mitigation: Minimize collected user data, avoid logging raw private or group messages, and apply retention controls appropriate to the deployment. <br>


## Reference(s): <br>
- [QQ Open Platform](https://q.qq.com) <br>
- [QQ Bot Access Token Endpoint](https://bots.qq.com/app/getAppAccessToken) <br>
- [QQ Bot API Base](https://api.sgroup.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with Python and JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples may require user-supplied QQ application credentials and sandbox validation before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
