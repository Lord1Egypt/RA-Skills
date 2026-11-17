## Description:

友盟 U-App 渠道/版本分析技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 5 个只读查询接口，涵盖渠道/版本单日快照与渠道/版本的启动次数、活跃用户、新增用户趋势分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to query read-only Umeng U-App channel and version analytics, compare daily rankings, and review launch, active-user, and new-user trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags an unsafe remote installer command.

Mitigation: Prefer the npm install path or a pinned, verified installer before using the skill.

Risk: The security evidence notes telemetry that may report appkeys and skill usage.

Mitigation: Use the skill only when credential handling and appkey reporting are acceptable for the deployment environment.

Risk: The skill depends on stored Umeng login credentials for CLI access.

Mitigation: Review credential storage and login practices before installing or running umeng-cli.

## Reference(s):

- [umeng-cli project homepage](https://github.com/umeng/umeng-cli)
- [Umeng website](https://www.umeng.com/)
- [ClawHub skill page](https://clawhub.ai/squall0925/skills/uapp-channel-version)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides read-only Umeng analytics calls and may summarize returned channel or version metrics in tables or trend narratives.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
