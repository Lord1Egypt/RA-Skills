## Description:

日用品保质期管理基于飞书多维表格，帮助用户快速录入、查询、删除商品保质期信息，并在首次使用时初始化表格和每日过期提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoxingyao](https://clawhub.ai/user/haoxingyao)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage household item shelf-life records in Feishu Bitable, including adding items, checking expiring or expired goods, marking items used up, and deleting records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a persistent daily agent task for expiration reminders.

Mitigation: Ask for explicit user confirmation before creating the scheduled task and provide a clear way to disable or remove it.

Risk: Broad Chinese-language trigger phrases may start initialization or data-changing actions unexpectedly.

Mitigation: Require confirmation before initialization, deletion, or other destructive changes when the trigger is ambiguous.

Risk: The skill can create, modify, and delete Feishu Bitable records while storing table identifiers locally.

Mitigation: Tell users what data will be persisted, confirm destructive record changes, and limit access to the local configuration file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haoxingyao/skills/shelflife)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration, Guidance]

**Output Format:** [Natural-language responses with Feishu Bitable record operations and JSON configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a local config file, stores Feishu Bitable identifiers, and may create a daily reminder task.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
