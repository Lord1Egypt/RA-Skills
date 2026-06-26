## Description: <br>
快速配置 OpenClaw 多 QQBot 账号绑定到不同 Agent。用于首次安装 QQBot、新增 QQBot 账号、创建 agent 绑定关系、重启 gateway 使配置生效。当用户需要安装 QQBot 插件、添加新的 QQBot 机器人或配置多账号路由时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KasonLee-marker](https://clawhub.ai/user/KasonLee-marker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw QQBot accounts, bind each account to the intended agent, and restart or verify the gateway after configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad QQBot access examples can route messages from untrusted users or groups to an agent. <br>
Mitigation: Restrict allowFrom to trusted QQ users or groups before applying the configuration. <br>
Risk: AppSecret and clientSecret values may be exposed through shell history or permissive local config file access. <br>
Mitigation: Protect secrets, avoid placing real secrets in shell history, and set restrictive permissions on ~/.openclaw/openclaw.json. <br>
Risk: Enabling sessions.visibility "all" can share session context across agents. <br>
Mitigation: Enable cross-agent session visibility only when shared context is intentional. <br>


## Reference(s): <br>
- [QQ Open Platform](https://bot.q.qq.com/) <br>
- [Tencent Connect OpenClaw QQBot plugin](https://github.com/tencent-connect/openclaw-qqbot.git) <br>
- [ClawHub skill page](https://clawhub.ai/KasonLee-marker/qqbot-multi-bind) <br>
- [Publisher profile](https://clawhub.ai/user/KasonLee-marker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; the skill itself does not execute commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
