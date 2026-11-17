## Description:

多平台返利聚合管理，统一追踪各平台返利订单状态、到账进度，提供返利数据分析与省钱报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to track rebate orders across shopping platforms, monitor settlement status, and generate concise savings reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A future implemented version may connect to shopping-platform accounts and read order or rebate data.

Mitigation: Confirm connected platforms, accessed order fields, and data handling expectations before deployment.

Risk: Automated sync or rebate reminders could act without clear user approval in a future implementation.

Mitigation: Require explicit approval for account sync, reminders, and any state-changing workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/skills/rebate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown rebate status summaries and savings reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform breakdowns, settlement status, rebate totals, and exception summaries.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
