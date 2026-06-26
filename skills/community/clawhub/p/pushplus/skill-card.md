## Description: <br>
PushPlus sends notifications through WeChat, email, SMS, Work WeChat, DingTalk, Feishu, and related channels for alerts, task results, exception notices, reminders, and delivery-result queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lei-mu](https://clawhub.ai/user/lei-mu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation agents use this skill to send PushPlus notifications, query delivery results, and manage notification tokens, groups, channels, ClawBot bindings, friends, settings, and preprocessing rules when the relevant credentials are provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PushPlus credentials authorize notification sending and optional account-management operations. <br>
Mitigation: Use a message token for ordinary sending and only provide PUSHPLUS_USER_TOKEN plus PUSHPLUS_SECRET_KEY when OpenAPI administration is needed. <br>
Risk: OpenAPI features can delete or change messages, tokens, groups, friends, webhooks, settings, preprocessing rules, and ClawBot bindings. <br>
Mitigation: Require explicit user confirmation before destructive or account-changing operations. <br>
Risk: Verbose execution can expose real tokens or request data in logs. <br>
Mitigation: Avoid verbose mode with production credentials and redact tokens from any shared logs. <br>
Risk: SMS and voice channels may consume paid PushPlus credits. <br>
Mitigation: Do not use paid delivery channels unless the user explicitly selects them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lei-mu/pushplus) <br>
- [PushPlus API reference](artifact/references/api.md) <br>
- [PushPlus documentation](https://www.pushplus.plus/doc/) <br>
- [PushPlus Apifox API documentation](https://pushplus.apifox.cn/) <br>
- [PushPlus website](https://www.pushplus.plus) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration guidance, Text] <br>
**Output Format:** [Markdown or text guidance with Python and shell commands; PushPlus API calls return JSON, except message-detail retrieval can return HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PUSHPLUS_TOKEN for message sending; optional PUSHPLUS_USER_TOKEN and PUSHPLUS_SECRET_KEY enable OpenAPI account-management actions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
