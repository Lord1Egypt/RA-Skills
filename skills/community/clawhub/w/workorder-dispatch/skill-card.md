## Description:

工单分派与SLA监控技能。基于真实Excel台账（美兰中心C+服务.xlsx）自动分派报修工单，跟踪处理进度，超时自动升级。

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Facilities-management teams use this skill to create and dispatch repair work orders from a business Excel ledger, monitor pending items against SLA thresholds, and escalate overdue work through WeCom notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and update a real facilities-management workbook containing repair and requester details.

Mitigation: Use it only in an authorized facilities-management environment, validate the workbook schema before writes, and review proposed workbook updates before execution.

Risk: Broad WeCom escalation messages could expose repair details or notify more recipients than necessary.

Mitigation: Replace @all escalation with scoped recipient groups and require confirmation or policy checks before sending broad notifications.

Risk: The artifact contains a hardcoded local workbook path and an example WeCom webhook URL.

Mitigation: Configure workbook paths and webhook endpoints per deployment, and manage real webhook secrets outside the skill text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/workorder-dispatch)
- [Reference Documentation for Workorder Dispatch](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces work-order records, SLA status summaries, escalation message templates, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
