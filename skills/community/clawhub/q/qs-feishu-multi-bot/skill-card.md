## Description: <br>
OpenClaw 多飞书机器人 + 多 Agent 配置指南：一个 Gateway 实例运行多个飞书机器人，每个机器人绑定不同 Agent，实现独立工作空间、独立会话、独立人格。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qushengswaych](https://clawhub.ai/user/qushengswaych) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure one Gateway instance with multiple Feishu bot accounts routed to separate agents, workspaces, sessions, identities, and optional model settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Open direct-message access can allow unknown users to contact a BotLand or OpenClaw agent when open policies are enabled. <br>
Mitigation: Restrict allowFrom or require pairing approval unless open access is intentional for the deployment. <br>
Risk: Feishu app secrets and BotLand or OpenClaw credentials are stored in local configuration. <br>
Mitigation: Replace example paths and secrets with environment-specific values, protect configuration file permissions, and review plugin or package source before force-installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qushengswaych/qs-feishu-multi-bot) <br>
- [Feishu Open Platform apps](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON5 and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw Gateway configuration examples, routing guidance, verification commands, and pairing steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
