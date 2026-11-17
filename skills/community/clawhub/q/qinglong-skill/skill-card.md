## Description:

青龙面板管理助手。当用户需要操作青龙面板（定时任务/环境变量/脚本/订阅/依赖/系统设置）时触发。支持自然语言操作，例如："列出所有任务"、"添加环境变量"、"运行任务"、"查看日志"等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[awsl1110](https://clawhub.ai/user/awsl1110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Qinglong panel administrators use this skill to translate natural-language requests into authenticated Qinglong panel API operations for cron jobs, environment variables, scripts, subscriptions, dependencies, and system settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Qinglong credentials and administrator APIs.

Mitigation: Use it only with a Qinglong panel you control, prefer HTTPS, avoid pasting long-lived administrator credentials, and redact tokens and environment-variable values from logs.

Risk: Qinglong operations can delete, modify, run, import, update, or execute commands.

Mitigation: Require explicit confirmation before destructive, state-changing, or shell-executing actions.

Risk: Security evidence marks the release as suspicious because the skill is a real panel administration helper with weak safety guidance.

Mitigation: Review before installing and scan the skill before deployment.

## Reference(s):

- [Qinglong API reference](api-reference.md)
- [Official Qinglong API documentation](https://qinglong.online/api/)
- [ClawHub skill page](https://clawhub.ai/awsl1110/skills/qinglong-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown with curl commands, tables or lists, and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated HTTP requests that change Qinglong panel state.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
