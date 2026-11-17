## Description:

友盟 U-App 核心指标查询技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 9 个只读查询接口，涵盖账户维度所有 App 合计、单日快照（DAU/新增/启动/总用户）、活跃/新增/启动趋势、使用时长。

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to answer U-App analytics questions about DAU, new users, launches, total users, active/new/launch trends, and usage duration. It helps an agent form read-only umeng-cli calls, interpret required parameters such as appkey and date ranges, and return concise metric answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs telemetry calls that may include skill usage and appkey values.

Mitigation: Do not allow an agent to auto-run trace commands or send appkeys in telemetry unless that data flow is explicitly approved.

Risk: The skill recommends host-level installation methods for umeng-cli.

Mitigation: Install umeng-cli only from a trusted, pinned, and reviewed source before using this skill.

Risk: Using the skill can require login to an Umeng analytics account, with credentials cached by umeng-cli.

Mitigation: Review who has access to the host environment and understand how umeng-cli stores credentials before login.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squall0925/skills/uapp-core-index)
- [umeng-cli project homepage](https://github.com/umeng/umeng-cli)
- [Umeng OpenAPI gateway](https://gateway.open.umeng.com/openapi)
- [Umeng website](https://www.umeng.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown text with inline shell commands and JSON API parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are oriented around read-only Umeng analytics queries and may require an appkey or authenticated umeng-cli session.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
