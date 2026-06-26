## Description: <br>
闲鱼自动回复助手。帮用户配置并运行闲鱼（Goofish）消息自动回复服务。用户只需提供浏览器 Cookie，即可持续监听闲鱼消息并用 AI 智能回复买家。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinabs](https://clawhub.ai/user/sinabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketplace sellers use this skill to configure and run a local Goofish/Xianyu auto-reply service that monitors buyer messages and sends AI-generated seller replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a live Xianyu/Goofish session cookie that can act as the user's marketplace account. <br>
Mitigation: Treat the cookie like a password, store it only locally, and delete or rotate ~/.xianyu-agent/config.json when the service is no longer needed. <br>
Risk: The monitor can send unattended AI-generated replies to buyers. <br>
Mitigation: Supervise the bot before leaving it running and review logs to confirm replies match the seller's expectations. <br>
Risk: Buyer messages, product information, and chat history are passed to the configured local AI CLI. <br>
Mitigation: Verify how the selected Claude or OpenClaw CLI handles prompts, retention, and telemetry before using the skill with sensitive conversations. <br>


## Reference(s): <br>
- [闲鱼 Cookie 获取指南](references/cookie_guide.md) <br>
- [Skill release page](https://clawhub.ai/sinabs/xianyu-reply) <br>
- [Publisher profile](https://clawhub.ai/user/sinabs) <br>
- [Goofish website](https://www.goofish.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps, service-management commands, and local configuration for an unattended auto-reply monitor.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
