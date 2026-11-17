## Description:

通联 VIP 对账单配置工作流，当有新增门店或终端需要配置 VIP 对账单时，指导代理按固定 6 列模板生成配置表、发送确认并创建飞书任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shouqianba](https://clawhub.ai/user/shouqianba)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and reconciliation staff use this skill to configure VIP reconciliation statements for newly added stores or terminals. It helps collect merchant, store, terminal, and Tonglian identifiers, produce the required spreadsheet, confirm delivery, and assign the follow-up task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles merchant, store, and terminal identifiers that may be sensitive operational data.

Mitigation: Confirm the spreadsheet contents before sending or attaching the file.

Risk: The skill can send the generated spreadsheet to a named internal contact and create a Feishu task.

Mitigation: Confirm the recipient, attachment, and task details before approving delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shouqianba/skills/tonglian-vip-reconciliation)
- [Publisher profile](https://clawhub.ai/user/shouqianba)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with spreadsheet configuration details and delivery steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or attach an Excel configuration file when the host agent has file and messaging tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
