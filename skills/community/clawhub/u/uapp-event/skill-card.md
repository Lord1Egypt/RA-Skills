## Description:

友盟 U-App 自定义事件查询技能，支持通过 umeng-cli call 调用友盟 OpenAPI 的 7 个只读事件查询接口，涵盖事件列表、事件触发次数趋势、独立用户数、事件参数列表、参数值分布、指定参数值趋势、参数值时长分布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analytics engineers, and product operators use this skill to query Umeng U-App custom event data, validate event or display-name existence, and inspect trigger counts, unique users, parameters, value distributions, trends, and duration distributions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports mandatory telemetry, including possible appkey telemetry.

Mitigation: Install only where telemetry is acceptable or can be disabled, and require explicit approval before sending appkeys or other identifiers through telemetry.

Risk: The security review flags unsafe install commands such as unpinned CLI installation and curl-piped shell installation.

Mitigation: Prefer a pinned, verified umeng-cli installation and avoid executing remote install scripts directly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squall0925/skills/uapp-event)
- [umeng-cli homepage](https://github.com/umeng/umeng-cli)
- [Umeng OpenAPI gateway](https://gateway.open.umeng.com/openapi)
- [Umeng website](https://www.umeng.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command examples and API response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analytics queries depend on umeng-cli, authenticated Umeng access, appkey, event identifiers, date ranges, and client-side sorting or aggregation for some results.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
